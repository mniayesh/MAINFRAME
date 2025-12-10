"""
Enhanced Base Extractor with Error Prevention

Uses pydantic for validation, tenacity for retries, requests-cache for caching,
and rich for better error display.
"""

import logging
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
import hashlib
import json
from pathlib import Path
import time

# Error prevention packages
from pydantic import BaseModel, Field, ValidationError, field_validator
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import requests_cache
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Set up console for rich output
console = Console()

# Install requests cache globally (15 min TTL)
requests_cache.install_cache(
    cache_name='bio_extractors_cache',
    backend='filesystem',
    expire_after=900,  # 15 minutes
    allowable_codes=[200],
    allowable_methods=['GET', 'POST']
)

logger = logging.getLogger(__name__)


class ExtractionError(Exception):
    """Base exception for extraction errors"""
    pass


class RateLimitError(ExtractionError):
    """Raised when rate limit is exceeded"""
    pass


class ValidationError(ExtractionError):
    """Raised when data validation fails"""
    pass


class EnhancedBaseExtractor:
    """
    Enhanced base extractor with:
    - Automatic retry with tenacity
    - Request caching with requests-cache
    - Data validation with pydantic
    - Beautiful error output with rich
    """

    def __init__(
        self,
        base_url: str = "",
        rate_limit: float = 0.0,
        max_retries: int = 3,
        timeout: int = 30
    ):
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self.timeout = timeout

        # Session with automatic caching
        self.session = requests_cache.CachedSession(
            cache_name='bio_extractors_cache',
            expire_after=900
        )

        # Statistics
        self.stats = {
            'requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'errors': 0,
            'validations_failed': 0
        }

        # Rate limiting
        self.last_request_time = 0

        logger.info(f"Initialized {self.__class__.__name__}")

    def _rate_limit(self):
        """Enforce rate limiting"""
        if self.rate_limit > 0:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.rate_limit:
                time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.ConnectionError, requests.Timeout)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def _make_request(
        self,
        url: str,
        method: str = 'GET',
        **kwargs
    ) -> requests.Response:
        """
        Make HTTP request with automatic retry and rate limiting

        Uses tenacity for smart retries:
        - Exponential backoff (2s, 4s, 8s, 10s max)
        - Only retries on connection/timeout errors
        - Logs before each retry
        """
        self._rate_limit()
        self.stats['requests'] += 1

        response = self.session.request(method, url, timeout=self.timeout, **kwargs)

        # Track cache hits
        if hasattr(response, 'from_cache') and response.from_cache:
            self.stats['cache_hits'] += 1
        else:
            self.stats['cache_misses'] += 1

        response.raise_for_status()
        return response

    def validate_and_extract(
        self,
        data: Any,
        model: type[BaseModel],
        extract_fn: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Validate data against pydantic model and optionally transform

        Args:
            data: Raw data from API
            model: Pydantic model class for validation
            extract_fn: Optional function to transform validated data

        Returns:
            Validated (and optionally transformed) data

        Raises:
            ValidationError: If data doesn't match model
        """
        try:
            # Validate with pydantic
            validated = model(**data) if isinstance(data, dict) else model.model_validate(data)

            # Optionally transform
            if extract_fn:
                return extract_fn(validated)

            return validated.model_dump()

        except ValidationError as e:
            self.stats['validations_failed'] += 1
            console.print(Panel(
                f"[bold red]Validation Error[/bold red]\n\n"
                f"Model: {model.__name__}\n"
                f"Errors:\n{e}",
                title="Data Validation Failed",
                border_style="red"
            ))
            raise ExtractionError(f"Validation failed: {e}")

    def extract_with_progress(
        self,
        items: List[Any],
        process_fn: callable,
        description: str = "Extracting"
    ) -> List[Any]:
        """
        Process items with rich progress bar

        Args:
            items: Items to process
            process_fn: Function to apply to each item
            description: Progress bar description

        Returns:
            List of processed items
        """
        results = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"[cyan]{description}", total=len(items))

            for item in items:
                try:
                    result = process_fn(item)
                    if result:
                        results.append(result)
                except Exception as e:
                    logger.error(f"Error processing item: {e}")
                    self.stats['errors'] += 1
                finally:
                    progress.update(task, advance=1)

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get extraction statistics"""
        total = self.stats['cache_hits'] + self.stats['cache_misses']
        hit_rate = (self.stats['cache_hits'] / total * 100) if total > 0 else 0

        return {
            **self.stats,
            'cache_hit_rate': f"{hit_rate:.1f}%"
        }

    def print_stats(self):
        """Print statistics with rich formatting"""
        stats = self.get_stats()

        console.print(Panel(
            f"[bold]Total Requests:[/bold] {stats['requests']}\n"
            f"[bold]Cache Hits:[/bold] {stats['cache_hits']}\n"
            f"[bold]Cache Misses:[/bold] {stats['cache_misses']}\n"
            f"[bold]Cache Hit Rate:[/bold] {stats['cache_hit_rate']}\n"
            f"[bold]Errors:[/bold] {stats['errors']}\n"
            f"[bold]Validation Failures:[/bold] {stats['validations_failed']}",
            title=f"[bold cyan]{self.__class__.__name__} Statistics",
            border_style="cyan"
        ))


# Example Pydantic models for common response types
class ReactomePathwayModel(BaseModel):
    """Validated Reactome pathway response"""
    displayName: str
    stId: str
    schemaClass: str = Field(default="Pathway")
    species: Optional[List[Dict[str, Any]]] = None

    @field_validator('species', mode='before')
    @classmethod
    def handle_species(cls, v):
        """Handle species being either dict or list"""
        if v is None:
            return None
        if isinstance(v, dict):
            return [v]
        return v


class GOTermModel(BaseModel):
    """Validated GO term response"""
    id: str
    label: str
    definition: Optional[str] = None
    category: Optional[str] = None
    namespace: Optional[str] = None
    synonyms: Optional[List[str]] = None

    @field_validator('synonyms', mode='before')
    @classmethod
    def ensure_list(cls, v):
        """Ensure synonyms is a list"""
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        return v


class InterProEntryModel(BaseModel):
    """Validated InterPro entry response"""
    metadata: Dict[str, Any]

    @field_validator('metadata', mode='before')
    @classmethod
    def handle_metadata(cls, v):
        """Handle metadata structure variations"""
        if isinstance(v, str):
            # If it's a string, wrap it in a dict
            return {'name': v}
        return v if isinstance(v, dict) else {}


if __name__ == '__main__':
    # Example usage
    extractor = EnhancedBaseExtractor()

    # Example: validate Reactome data
    reactome_data = {
        'displayName': 'Test Pathway',
        'stId': 'R-HSA-12345',
        'schemaClass': 'Pathway',
        'species': {'displayName': 'Homo sapiens'}  # Can be dict or list
    }

    validated = extractor.validate_and_extract(
        reactome_data,
        ReactomePathwayModel
    )

    print(f"Validated: {validated}")
    extractor.print_stats()
