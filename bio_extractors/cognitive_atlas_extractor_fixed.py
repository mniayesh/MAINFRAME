"""
Fixed Cognitive Atlas Extractor with Pydantic Validation

Improves on the original Cognitive Atlas extractor by adding:
- Pydantic validation for API responses
- Enhanced error prevention
- Better caching and retry logic
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator
from enhanced_base import EnhancedBaseExtractor, console
from rich.panel import Panel

logger = logging.getLogger(__name__)


# ===== Pydantic Models for Cognitive Atlas API =====

class CognitiveAtlasConcept(BaseModel):
    """Validated Cognitive Atlas concept"""
    id: str
    name: str
    definition: Optional[str] = ""
    alias: Optional[str] = None
    event_stamp: Optional[str] = None

    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        """Ensure ID is a string"""
        if v is None:
            return "unknown"
        return str(v)

    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, v):
        """Ensure name is a string"""
        if v is None or str(v).strip() == "":
            return "Unknown concept"
        return str(v).strip()

    @field_validator('definition', mode='before')
    @classmethod
    def validate_definition(cls, v):
        """Handle definition variations"""
        if v is None:
            return ""
        return str(v).strip()


class CognitiveAtlasTask(BaseModel):
    """Validated Cognitive Atlas task"""
    id: str
    name: str
    definition: Optional[str] = ""

    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        if v is None:
            return "unknown"
        return str(v)

    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, v):
        if v is None or str(v).strip() == "":
            return "Unknown task"
        return str(v).strip()


class CognitiveAtlasExtractorFixed(EnhancedBaseExtractor):
    """
    Fixed Cognitive Atlas extractor with full pydantic validation

    Prevents parser errors by validating all API responses.
    Extracts cognitive concepts, tasks, and disorders.
    """

    def __init__(self):
        super().__init__(
            base_url="https://www.cognitiveatlas.org/api/v-alpha",
            rate_limit=10,
            max_retries=3,
            timeout=30
        )

    def extract_concepts(
        self,
        max_concepts: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Extract cognitive concepts with validation

        Args:
            max_concepts: Maximum number of concepts to extract

        Returns:
            List of validated concept dictionaries
        """
        logger.info("Starting Cognitive Atlas concept extraction...")
        console.print("[cyan]Extracting Cognitive Atlas concepts...[/cyan]")

        concepts = []

        try:
            # Query concepts from Cognitive Atlas API
            url = f"{self.base_url}/concept"

            response = self._make_request(url)
            data = response.json()

            if not isinstance(data, list):
                logger.warning(f"Expected list, got {type(data)}")
                return []

            logger.info(f"Retrieved {len(data)} concepts from API")

            # Validate and transform each concept
            for item in data[:max_concepts]:
                try:
                    # Validate with pydantic
                    concept = CognitiveAtlasConcept(**item)

                    # Transform to standard entity format
                    validated_concept = {
                        'identifier': f"COGAT:{concept.id}",
                        'name': concept.name,
                        'description': concept.definition,
                        'entity_type': 'computation',  # Cognitive processes are computations
                        'source_database': 'Cognitive Atlas',
                        'confidence_score': 0.85,
                        'evidence_strength': 'computational',
                        'metadata': {
                            'alias': concept.alias,
                            'event_stamp': concept.event_stamp,
                            'operation_type': self._infer_operation_type(concept.name)
                        }
                    }

                    concepts.append(validated_concept)

                except Exception as e:
                    logger.warning(f"Skipping invalid concept: {e}")
                    self.stats['validations_failed'] += 1
                    continue

            logger.info(f"Successfully validated {len(concepts)} concepts")

            console.print(Panel(
                f"[bold green]Successfully extracted {len(concepts)} cognitive concepts[/bold green]",
                title="Cognitive Atlas Extraction Complete",
                border_style="green"
            ))

        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            console.print(Panel(
                f"[bold red]Extraction failed: {e}[/bold red]",
                title="Cognitive Atlas Extraction Error",
                border_style="red"
            ))

        return concepts

    def extract_tasks(
        self,
        max_tasks: int = 300
    ) -> List[Dict[str, Any]]:
        """
        Extract cognitive tasks with validation

        Args:
            max_tasks: Maximum number of tasks to extract

        Returns:
            List of validated task dictionaries
        """
        logger.info("Starting Cognitive Atlas task extraction...")

        tasks = []

        try:
            # Query tasks from Cognitive Atlas API
            url = f"{self.base_url}/task"

            response = self._make_request(url)
            data = response.json()

            if not isinstance(data, list):
                logger.warning(f"Expected list, got {type(data)}")
                return []

            logger.info(f"Retrieved {len(data)} tasks from API")

            # Validate and transform each task
            for item in data[:max_tasks]:
                try:
                    # Validate with pydantic
                    task = CognitiveAtlasTask(**item)

                    # Transform to standard entity format
                    validated_task = {
                        'identifier': f"COGAT_TASK:{task.id}",
                        'name': task.name,
                        'description': task.definition,
                        'entity_type': 'process',  # Tasks are processes
                        'source_database': 'Cognitive Atlas',
                        'confidence_score': 0.80,
                        'evidence_strength': 'computational',
                        'metadata': {
                            'process_category': 'cognitive'
                        }
                    }

                    tasks.append(validated_task)

                except Exception as e:
                    logger.warning(f"Skipping invalid task: {e}")
                    self.stats['validations_failed'] += 1
                    continue

            logger.info(f"Successfully validated {len(tasks)} tasks")

            console.print(Panel(
                f"[bold green]Successfully extracted {len(tasks)} cognitive tasks[/bold green]",
                title="Cognitive Atlas Tasks Complete",
                border_style="green"
            ))

        except Exception as e:
            logger.error(f"Error during task extraction: {e}")
            console.print(Panel(
                f"[bold red]Task extraction failed: {e}[/bold red]",
                title="Cognitive Atlas Task Error",
                border_style="red"
            ))

        return tasks

    def _infer_operation_type(self, name: str) -> str:
        """Infer cognitive operation type from name"""
        name_lower = name.lower()

        operation_keywords = {
            'memory': 'memory_operation',
            'attention': 'attention_control',
            'decision': 'decision_making',
            'learning': 'learning',
            'perception': 'perception',
            'motor': 'motor_control',
            'language': 'language_processing',
            'reasoning': 'reasoning',
            'emotion': 'emotion_processing',
            'executive': 'executive_function',
            'working': 'working_memory'
        }

        for keyword, operation in operation_keywords.items():
            if keyword in name_lower:
                return operation

        return 'cognitive_operation'


def test_fixed_extractor():
    """Test the fixed Cognitive Atlas extractor"""
    extractor = CognitiveAtlasExtractorFixed()

    # Test concept extraction
    concepts = extractor.extract_concepts(max_concepts=200)

    print(f"\n✓ Extracted {len(concepts)} concepts")
    print(f"\nSample concepts:")
    for concept in concepts[:5]:
        print(f"  - {concept['name']} [{concept['identifier']}]")
        print(f"    Operation: {concept['metadata']['operation_type']}")

    # Print statistics
    extractor.print_stats()

    return concepts


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_fixed_extractor()
