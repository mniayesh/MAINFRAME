"""
Base Extractor Infrastructure

Provides abstract base class for all extractors with:
- Rate limiting (respecting API limits like KEGG's 3/sec)
- Retry logic with exponential backoff
- Error handling and logging
- Progress tracking
- 15-minute caching mechanism
"""

import time
import json
import hashlib
import logging
import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from datetime import datetime, timedelta
from functools import wraps
import sqlite3


class ExtractionError(Exception):
    """Base exception for extraction errors."""
    pass


class RateLimitError(ExtractionError):
    """Raised when rate limit is exceeded."""
    pass


class Cache:
    """Simple file-based cache with TTL support."""

    def __init__(self, cache_dir: str = ".cache", ttl_minutes: int = 15):
        """
        Initialize cache.

        Args:
            cache_dir: Directory to store cache files
            ttl_minutes: Time-to-live in minutes (default 15 like WebFetch)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(minutes=ttl_minutes)

    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for a key."""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"

    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value if it exists and hasn't expired.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, 'r') as f:
                cached = json.load(f)

            # Check expiration
            cached_time = datetime.fromisoformat(cached['timestamp'])
            if datetime.now() - cached_time > self.ttl:
                cache_path.unlink()  # Delete expired cache
                return None

            return cached['data']

        except (json.JSONDecodeError, KeyError, ValueError):
            # Corrupted cache file
            cache_path.unlink()
            return None

    def set(self, key: str, value: Any):
        """
        Set cached value.

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
        """
        cache_path = self._get_cache_path(key)

        cached = {
            'timestamp': datetime.now().isoformat(),
            'data': value
        }

        with open(cache_path, 'w') as f:
            json.dump(cached, f)

    def clear(self):
        """Clear all cache files."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()


class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, max_calls: int, period_seconds: float):
        """
        Initialize rate limiter.

        Args:
            max_calls: Maximum number of calls per period
            period_seconds: Period in seconds
        """
        self.max_calls = max_calls
        self.period = period_seconds
        self.calls = []

    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        now = time.time()

        # Remove old calls outside the window
        self.calls = [call_time for call_time in self.calls
                      if now - call_time < self.period]

        if len(self.calls) >= self.max_calls:
            # Need to wait
            sleep_time = self.period - (now - self.calls[0]) + 0.1
            if sleep_time > 0:
                time.sleep(sleep_time)
            # Clear old calls after waiting
            self.calls = []

        # Record this call
        self.calls.append(time.time())


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (requests.RequestException,)
):
    """
    Decorator for retry logic with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    if attempt == max_retries:
                        # Last attempt failed
                        raise ExtractionError(
                            f"Failed after {max_retries} retries: {str(e)}"
                        )

                    # Log and wait
                    if hasattr(args[0], 'logger'):
                        args[0].logger.warning(
                            f"Attempt {attempt + 1} failed: {str(e)}. "
                            f"Retrying in {delay}s..."
                        )

                    time.sleep(delay)
                    delay *= backoff_factor

            return None  # Should never reach here

        return wrapper
    return decorator


class BaseExtractor(ABC):
    """
    Abstract base class for all biological database extractors.

    Provides:
        - Rate limiting
        - Caching
        - Retry logic
        - Error handling
        - Progress tracking
        - Logging
    """

    def __init__(
        self,
        cache_dir: str = ".cache",
        cache_ttl_minutes: int = 15,
        rate_limit_calls: int = 10,
        rate_limit_period: float = 1.0,
        log_level: int = logging.INFO
    ):
        """
        Initialize base extractor.

        Args:
            cache_dir: Directory for cache files
            cache_ttl_minutes: Cache time-to-live in minutes
            rate_limit_calls: Maximum API calls per period
            rate_limit_period: Rate limit period in seconds
            log_level: Logging level
        """
        self.cache = Cache(cache_dir, cache_ttl_minutes)
        self.rate_limiter = RateLimiter(rate_limit_calls, rate_limit_period)

        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BioArchExtractor/1.0 (Research; contact@example.com)'
        })

        # Progress tracking
        self.stats = {
            'total_requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'errors': 0,
            'items_extracted': 0
        }

    @abstractmethod
    def extract(self) -> List[Dict[str, Any]]:
        """
        Extract data from the database.

        Returns:
            List of extracted entities as dictionaries
        """
        pass

    @retry_with_backoff(max_retries=3, initial_delay=1.0, backoff_factor=2.0)
    def make_request(
        self,
        url: str,
        method: str = 'GET',
        params: Dict = None,
        headers: Dict = None,
        json_data: Dict = None,
        use_cache: bool = True
    ) -> requests.Response:
        """
        Make HTTP request with rate limiting, caching, and retry logic.

        Args:
            url: Request URL
            method: HTTP method
            params: Query parameters
            headers: Additional headers
            json_data: JSON data for POST/PUT
            use_cache: Whether to use cache

        Returns:
            Response object

        Raises:
            ExtractionError: If request fails after retries
        """
        # Create cache key
        cache_key = f"{method}:{url}:{json.dumps(params, sort_keys=True)}"

        # Check cache
        if use_cache and method == 'GET':
            cached_response = self.cache.get(cache_key)
            if cached_response is not None:
                self.stats['cache_hits'] += 1
                self.logger.debug(f"Cache hit for {url}")

                # Create mock response object
                response = requests.Response()
                response.status_code = 200
                response._content = json.dumps(cached_response).encode()
                return response

        self.stats['cache_misses'] += 1

        # Rate limiting
        self.rate_limiter.wait_if_needed()

        # Make request
        self.stats['total_requests'] += 1

        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=request_headers,
                json=json_data,
                timeout=30
            )

            response.raise_for_status()

            # Cache successful GET requests
            if use_cache and method == 'GET' and response.status_code == 200:
                try:
                    self.cache.set(cache_key, response.json())
                except json.JSONDecodeError:
                    # Response is not JSON, cache the text
                    self.cache.set(cache_key, response.text)

            return response

        except requests.HTTPError as e:
            if e.response.status_code == 429:
                raise RateLimitError(f"Rate limit exceeded: {url}")
            self.stats['errors'] += 1
            raise

        except requests.RequestException as e:
            self.stats['errors'] += 1
            raise

    def get_json(
        self,
        url: str,
        params: Dict = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Make GET request and return JSON response.

        Args:
            url: Request URL
            params: Query parameters
            use_cache: Whether to use cache

        Returns:
            JSON response as dictionary
        """
        response = self.make_request(url, params=params, use_cache=use_cache)
        return response.json()

    def paginate(
        self,
        url: str,
        params: Dict = None,
        page_param: str = 'page',
        page_size_param: str = 'size',
        page_size: int = 100,
        max_pages: int = None,
        results_key: str = 'results'
    ) -> List[Dict[str, Any]]:
        """
        Handle pagination for API endpoints.

        Args:
            url: Base URL
            params: Base query parameters
            page_param: Parameter name for page number
            page_size_param: Parameter name for page size
            page_size: Items per page
            max_pages: Maximum pages to fetch (None = all)
            results_key: Key in response containing results list

        Returns:
            List of all results from all pages
        """
        all_results = []
        params = params or {}
        page = 0

        while True:
            if max_pages and page >= max_pages:
                break

            page_params = params.copy()
            page_params[page_param] = page
            page_params[page_size_param] = page_size

            self.logger.info(f"Fetching page {page + 1}...")

            try:
                data = self.get_json(url, params=page_params)

                # Extract results
                if results_key:
                    results = data.get(results_key, [])
                elif isinstance(data, list):
                    results = data
                else:
                    results = [data]

                if not results:
                    break

                all_results.extend(results)
                self.logger.info(f"Page {page + 1}: {len(results)} items")

                # Check if there are more pages
                if len(results) < page_size:
                    break

                page += 1

            except Exception as e:
                self.logger.error(f"Error fetching page {page + 1}: {str(e)}")
                break

        self.logger.info(f"Total items fetched: {len(all_results)}")
        return all_results

    def save_to_json(self, data: List[Dict], output_file: str):
        """
        Save extracted data to JSON file.

        Args:
            data: List of dictionaries to save
            output_file: Output file path
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        self.logger.info(f"Saved {len(data)} items to {output_file}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get extraction statistics.

        Returns:
            Dictionary of statistics
        """
        cache_hit_rate = (
            self.stats['cache_hits'] / max(1, self.stats['cache_hits'] + self.stats['cache_misses'])
        ) * 100

        return {
            **self.stats,
            'cache_hit_rate_percent': round(cache_hit_rate, 2)
        }

    def print_stats(self):
        """Print extraction statistics."""
        stats = self.get_stats()

        print("\n=== Extraction Statistics ===")
        print(f"Total API requests:  {stats['total_requests']}")
        print(f"Cache hits:          {stats['cache_hits']}")
        print(f"Cache misses:        {stats['cache_misses']}")
        print(f"Cache hit rate:      {stats['cache_hit_rate_percent']}%")
        print(f"Errors:              {stats['errors']}")
        print(f"Items extracted:     {stats['items_extracted']}")

    def close(self):
        """Clean up resources."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
