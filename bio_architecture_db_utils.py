"""
Biological Architectural Primitives Database Utilities

This module provides a Python interface to the biological architectural primitives database,
including:
- Database initialization and schema creation
- Entity CRUD operations
- Relationship management
- Computational mapping
- Query helpers
- Data import/export

Usage:
    from bio_architecture_db_utils import BioArchDB

    # Initialize database
    db = BioArchDB('bio_architecture.db')

    # Create an entity
    entity_id = db.create_mechanism(
        identifier='MECH_001',
        name='Lateral Inhibition',
        description='Mechanism where active neurons suppress neighbors',
        update_rule='dy_i/dt = -y_i + f(x_i - sum(w_ij * y_j))'
    )

    # Add computational mapping
    db.add_computational_mapping(
        entity_id=entity_id,
        pattern_name='Winner-Take-All Network',
        mapping_type='isomorphic',
        fidelity_score=0.90
    )

    # Query entities
    mechanisms = db.query_entities_by_type('mechanism', validated_only=True)
"""

import sqlite3
import json
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime
from pathlib import Path
import csv


class BioArchDB:
    """Main database interface for biological architectural primitives."""

    def __init__(self, db_path: str = 'bio_architecture.db'):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self.cursor = self.conn.cursor()

        # Enable foreign keys
        self.cursor.execute("PRAGMA foreign_keys = ON")

        # Performance optimizations
        self.cursor.execute("PRAGMA journal_mode = WAL")
        self.cursor.execute("PRAGMA synchronous = NORMAL")
        self.cursor.execute("PRAGMA cache_size = -64000")  # 64MB cache
        self.cursor.execute("PRAGMA temp_store = MEMORY")

    def initialize_schema(self, schema_file: str = 'bio_architecture_schema.sql'):
        """
        Initialize database schema from SQL file.

        Args:
            schema_file: Path to schema SQL file
        """
        with open(schema_file, 'r') as f:
            schema_sql = f.read()

        # Execute schema (split by statement if needed)
        self.cursor.executescript(schema_sql)
        self.conn.commit()
        print(f"Database schema initialized from {schema_file}")

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    # =========================================================================
    # ENTITY CREATION
    # =========================================================================

    def create_entity(
        self,
        entity_type: str,
        identifier: str,
        name: str,
        description: str = None,
        mathematical_formulation: str = None,
        confidence_score: float = 0.8,
        evidence_strength: str = 'inferred',
        source_database: str = None,
        curator: str = None,
        **kwargs
    ) -> int:
        """
        Create a new entity in the database.

        Args:
            entity_type: Type name (e.g., 'mechanism', 'process', 'enzyme')
            identifier: Unique identifier for the entity
            name: Entity name
            description: Optional description
            mathematical_formulation: Optional mathematical equation
            confidence_score: Confidence in data (0-1)
            evidence_strength: 'experimental', 'computational', 'inferred', 'predicted'
            source_database: Source database name
            curator: Curator name
            **kwargs: Additional fields (complexity_level, common_name, etc.)

        Returns:
            entity_id: ID of created entity
        """
        # Get entity_type_id
        self.cursor.execute(
            "SELECT type_id FROM entity_types WHERE type_name = ?",
            (entity_type,)
        )
        result = self.cursor.fetchone()
        if not result:
            raise ValueError(f"Unknown entity type: {entity_type}")
        entity_type_id = result[0]

        # Insert entity
        self.cursor.execute('''
            INSERT INTO entities (
                entity_type_id, identifier, name, description,
                mathematical_formulation, confidence_score, evidence_strength,
                source_database, curator, complexity_level, common_name
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entity_type_id, identifier, name, description,
            mathematical_formulation, confidence_score, evidence_strength,
            source_database, curator,
            kwargs.get('complexity_level'),
            kwargs.get('common_name')
        ))

        entity_id = self.cursor.lastrowid
        self.conn.commit()

        return entity_id

    def create_mechanism(
        self,
        identifier: str,
        name: str,
        description: str = None,
        update_rule: str = None,
        mechanism_class: str = None,
        time_scale_ms: float = None,
        reversibility: bool = None,
        **kwargs
    ) -> int:
        """
        Create a mechanism entity with mechanism-specific fields.

        Args:
            identifier: Unique identifier
            name: Mechanism name
            description: Description
            update_rule: Mathematical update rule
            mechanism_class: Class (e.g., 'feedback', 'feedforward')
            time_scale_ms: Characteristic timescale in milliseconds
            reversibility: Whether mechanism is reversible
            **kwargs: Additional fields for create_entity

        Returns:
            entity_id: ID of created mechanism
        """
        # Create base entity
        entity_id = self.create_entity(
            entity_type='mechanism',
            identifier=identifier,
            name=name,
            description=description,
            mathematical_formulation=update_rule,
            **kwargs
        )

        # Insert mechanism-specific data
        self.cursor.execute('''
            INSERT INTO mechanisms (
                mechanism_id, entity_id, mechanism_class, update_rule,
                time_scale_ms, reversibility
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (entity_id, entity_id, mechanism_class, update_rule, time_scale_ms, reversibility))

        self.conn.commit()
        return entity_id

    def create_process(
        self,
        identifier: str,
        name: str,
        description: str = None,
        process_category: str = None,
        temporal_dynamics: str = None,
        spatial_scale: str = None,
        rate_equation: str = None,
        **kwargs
    ) -> int:
        """Create a process entity."""
        entity_id = self.create_entity(
            entity_type='process',
            identifier=identifier,
            name=name,
            description=description,
            mathematical_formulation=rate_equation,
            **kwargs
        )

        self.cursor.execute('''
            INSERT INTO processes (
                process_id, entity_id, process_category, temporal_dynamics,
                spatial_scale, rate_equation
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (entity_id, entity_id, process_category, temporal_dynamics,
              spatial_scale, rate_equation))

        self.conn.commit()
        return entity_id

    def create_enzyme(
        self,
        identifier: str,
        name: str,
        description: str = None,
        ec_number: str = None,
        km_value: float = None,
        kcat_value: float = None,
        catalytic_mechanism: str = None,
        **kwargs
    ) -> int:
        """Create an enzyme entity."""
        entity_id = self.create_entity(
            entity_type='enzyme',
            identifier=identifier,
            name=name,
            description=description,
            **kwargs
        )

        self.cursor.execute('''
            INSERT INTO enzymes (
                enzyme_id, entity_id, ec_number, catalytic_mechanism,
                km_value, kcat_value
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (entity_id, entity_id, ec_number, catalytic_mechanism,
              km_value, kcat_value))

        self.conn.commit()
        return entity_id

    # =========================================================================
    # RELATIONSHIP MANAGEMENT
    # =========================================================================

    def add_relationship(
        self,
        source_entity_id: int,
        target_entity_id: int,
        relationship_type: str,
        strength: float = None,
        confidence: float = None,
        context: str = None,
        evidence: str = None
    ) -> int:
        """
        Add a relationship between two entities.

        Args:
            source_entity_id: Source entity ID
            target_entity_id: Target entity ID
            relationship_type: Type name (e.g., 'parent_of', 'regulates')
            strength: Relationship strength (0-1)
            confidence: Confidence in relationship (0-1)
            context: Context description
            evidence: Supporting evidence

        Returns:
            relationship_id: ID of created relationship
        """
        # Get relationship_type_id
        self.cursor.execute(
            "SELECT relationship_type_id FROM relationship_types WHERE type_name = ?",
            (relationship_type,)
        )
        result = self.cursor.fetchone()
        if not result:
            raise ValueError(f"Unknown relationship type: {relationship_type}")
        relationship_type_id = result[0]

        # Insert relationship
        self.cursor.execute('''
            INSERT INTO entity_relationships (
                source_entity_id, target_entity_id, relationship_type_id,
                strength, confidence, context, evidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (source_entity_id, target_entity_id, relationship_type_id,
              strength, confidence, context, evidence))

        relationship_id = self.cursor.lastrowid
        self.conn.commit()

        return relationship_id

    def get_relationships(
        self,
        entity_id: int,
        direction: str = 'both',
        relationship_type: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get all relationships for an entity.

        Args:
            entity_id: Entity ID
            direction: 'outgoing', 'incoming', or 'both'
            relationship_type: Filter by relationship type (optional)

        Returns:
            List of relationship dictionaries
        """
        conditions = []
        params = []

        if direction in ['outgoing', 'both']:
            conditions.append("er.source_entity_id = ?")
            params.append(entity_id)

        if direction in ['incoming', 'both']:
            conditions.append("er.target_entity_id = ?")
            params.append(entity_id)

        where_clause = f"WHERE ({' OR '.join(conditions)})"

        if relationship_type:
            where_clause += " AND rt.type_name = ?"
            params.append(relationship_type)

        query = f'''
            SELECT
                er.relationship_id,
                er.source_entity_id,
                e1.name as source_name,
                er.target_entity_id,
                e2.name as target_name,
                rt.type_name as relationship_type,
                er.strength,
                er.confidence,
                er.context
            FROM entity_relationships er
            JOIN relationship_types rt ON er.relationship_type_id = rt.relationship_type_id
            JOIN entities e1 ON er.source_entity_id = e1.entity_id
            JOIN entities e2 ON er.target_entity_id = e2.entity_id
            {where_clause}
        '''

        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]

    # =========================================================================
    # COMPUTATIONAL MAPPING
    # =========================================================================

    def create_architectural_pattern(
        self,
        pattern_name: str,
        pattern_category: str,
        formal_description: str,
        pseudocode: str = None,
        complexity_class: str = None,
        properties: Dict = None
    ) -> int:
        """
        Create an architectural pattern.

        Args:
            pattern_name: Pattern name
            pattern_category: Category (e.g., 'control_flow', 'algorithm')
            formal_description: Formal description
            pseudocode: Pseudocode implementation
            complexity_class: Computational complexity
            properties: Additional properties as dict

        Returns:
            pattern_id: ID of created pattern
        """
        properties_json = json.dumps(properties) if properties else None

        self.cursor.execute('''
            INSERT INTO architectural_patterns (
                pattern_name, pattern_category, formal_description,
                pseudocode, complexity_class, properties_json
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (pattern_name, pattern_category, formal_description,
              pseudocode, complexity_class, properties_json))

        pattern_id = self.cursor.lastrowid
        self.conn.commit()

        return pattern_id

    def add_computational_mapping(
        self,
        entity_id: int,
        pattern_id: int = None,
        pattern_name: str = None,
        mapping_type: str = 'analogous',
        fidelity_score: float = None,
        description: str = None,
        mathematical_correspondence: str = None,
        implementation_notes: str = None,
        validated: bool = False
    ) -> int:
        """
        Map a biological entity to an architectural pattern.

        Args:
            entity_id: Entity ID
            pattern_id: Pattern ID (or provide pattern_name)
            pattern_name: Pattern name (alternative to pattern_id)
            mapping_type: 'isomorphic', 'analogous', 'approximates'
            fidelity_score: How well biology maps to architecture (0-1)
            description: Mapping description
            mathematical_correspondence: Mathematical relationship
            implementation_notes: Implementation notes
            validated: Whether mapping is validated

        Returns:
            mapping_id: ID of created mapping
        """
        # Get pattern_id if pattern_name provided
        if pattern_id is None and pattern_name:
            self.cursor.execute(
                "SELECT pattern_id FROM architectural_patterns WHERE pattern_name = ?",
                (pattern_name,)
            )
            result = self.cursor.fetchone()
            if not result:
                raise ValueError(f"Unknown pattern: {pattern_name}")
            pattern_id = result[0]

        if pattern_id is None:
            raise ValueError("Must provide either pattern_id or pattern_name")

        self.cursor.execute('''
            INSERT INTO computational_mappings (
                entity_id, pattern_id, mapping_type, fidelity_score,
                description, mathematical_correspondence, implementation_notes,
                validated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (entity_id, pattern_id, mapping_type, fidelity_score,
              description, mathematical_correspondence, implementation_notes,
              validated))

        mapping_id = self.cursor.lastrowid
        self.conn.commit()

        return mapping_id

    def get_computational_mappings(
        self,
        entity_id: int = None,
        pattern_id: int = None,
        validated_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get computational mappings.

        Args:
            entity_id: Filter by entity ID
            pattern_id: Filter by pattern ID
            validated_only: Only return validated mappings

        Returns:
            List of mapping dictionaries
        """
        conditions = []
        params = []

        if entity_id:
            conditions.append("cm.entity_id = ?")
            params.append(entity_id)

        if pattern_id:
            conditions.append("cm.pattern_id = ?")
            params.append(pattern_id)

        if validated_only:
            conditions.append("cm.validated = 1")

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

        query = f'''
            SELECT
                cm.mapping_id,
                e.entity_id,
                e.name as entity_name,
                et.type_name as entity_type,
                ap.pattern_id,
                ap.pattern_name,
                ap.pattern_category,
                cm.mapping_type,
                cm.fidelity_score,
                cm.description,
                cm.mathematical_correspondence,
                cm.validated
            FROM computational_mappings cm
            JOIN entities e ON cm.entity_id = e.entity_id
            JOIN entity_types et ON e.entity_type_id = et.type_id
            JOIN architectural_patterns ap ON cm.pattern_id = ap.pattern_id
            {where_clause}
            ORDER BY cm.fidelity_score DESC
        '''

        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]

    # =========================================================================
    # QUERY OPERATIONS
    # =========================================================================

    def query_entities_by_type(
        self,
        entity_type: str,
        validated_only: bool = False,
        min_confidence: float = 0.0,
        limit: int = None
    ) -> List[Dict[str, Any]]:
        """
        Query entities by type.

        Args:
            entity_type: Entity type name
            validated_only: Only return validated entities
            min_confidence: Minimum confidence score
            limit: Maximum number of results

        Returns:
            List of entity dictionaries
        """
        conditions = ["et.type_name = ?"]
        params = [entity_type]

        if validated_only:
            conditions.append("e.validation_status = 'validated'")

        if min_confidence > 0:
            conditions.append("e.confidence_score >= ?")
            params.append(min_confidence)

        where_clause = "WHERE " + " AND ".join(conditions)
        limit_clause = f"LIMIT {limit}" if limit else ""

        query = f'''
            SELECT
                e.entity_id,
                e.identifier,
                e.name,
                e.description,
                e.mathematical_formulation,
                e.confidence_score,
                e.validation_status,
                et.type_name as entity_type
            FROM entities e
            JOIN entity_types et ON e.entity_type_id = et.type_id
            {where_clause}
            ORDER BY e.confidence_score DESC, e.name
            {limit_clause}
        '''

        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_entity_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """Get entity by ID with all details."""
        query = '''
            SELECT
                e.*,
                et.type_name as entity_type,
                et.type_category
            FROM entities e
            JOIN entity_types et ON e.entity_type_id = et.type_id
            WHERE e.entity_id = ?
        '''

        self.cursor.execute(query, (entity_id,))
        result = self.cursor.fetchone()

        return dict(result) if result else None

    def get_entity_by_identifier(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Get entity by identifier."""
        query = '''
            SELECT
                e.*,
                et.type_name as entity_type
            FROM entities e
            JOIN entity_types et ON e.entity_type_id = et.type_id
            WHERE e.identifier = ?
        '''

        self.cursor.execute(query, (identifier,))
        result = self.cursor.fetchone()

        return dict(result) if result else None

    def search_entities(self, search_term: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Full-text search across entities.

        Args:
            search_term: Search query
            limit: Maximum results

        Returns:
            List of matching entities
        """
        query = '''
            SELECT
                e.entity_id,
                e.identifier,
                e.name,
                e.description,
                et.type_name as entity_type,
                bm25(entities_fts) as relevance_score
            FROM entities_fts
            JOIN entities e ON entities_fts.entity_id = e.entity_id
            JOIN entity_types et ON e.entity_type_id = et.type_id
            WHERE entities_fts MATCH ?
            ORDER BY relevance_score
            LIMIT ?
        '''

        self.cursor.execute(query, (search_term, limit))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_entity_hierarchy(self, root_entity_id: int, max_depth: int = 5) -> List[Dict[str, Any]]:
        """
        Get hierarchical descendants of an entity.

        Args:
            root_entity_id: Root entity ID
            max_depth: Maximum depth to traverse

        Returns:
            List of descendants with depth information
        """
        query = '''
            WITH RECURSIVE descendants(entity_id, depth) AS (
                SELECT entity_id, 0 as depth
                FROM entities
                WHERE entity_id = ?

                UNION ALL

                SELECT er.target_entity_id, d.depth + 1
                FROM entity_relationships er
                JOIN descendants d ON er.source_entity_id = d.entity_id
                JOIN relationship_types rt ON er.relationship_type_id = rt.relationship_type_id
                WHERE rt.is_hierarchical = 1 AND d.depth < ?
            )
            SELECT
                e.entity_id,
                e.identifier,
                e.name,
                et.type_name as entity_type,
                d.depth
            FROM descendants d
            JOIN entities e ON d.entity_id = e.entity_id
            JOIN entity_types et ON e.entity_type_id = et.type_id
            ORDER BY d.depth, e.name
        '''

        self.cursor.execute(query, (root_entity_id, max_depth))
        return [dict(row) for row in self.cursor.fetchall()]

    # =========================================================================
    # PARAMETER AND PROPERTY MANAGEMENT
    # =========================================================================

    def add_parameter(
        self,
        entity_id: int,
        parameter_type: str,
        value: float,
        uncertainty: float = None,
        value_min: float = None,
        value_max: float = None,
        organism: str = None,
        confidence: float = None
    ) -> int:
        """Add a quantitative parameter to an entity."""
        # Get parameter_type_id
        self.cursor.execute(
            "SELECT parameter_type_id FROM parameter_types WHERE parameter_name = ?",
            (parameter_type,)
        )
        result = self.cursor.fetchone()
        if not result:
            raise ValueError(f"Unknown parameter type: {parameter_type}")
        parameter_type_id = result[0]

        self.cursor.execute('''
            INSERT INTO parameters (
                entity_id, parameter_type_id, value, uncertainty,
                value_min, value_max, organism, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (entity_id, parameter_type_id, value, uncertainty,
              value_min, value_max, organism, confidence))

        parameter_id = self.cursor.lastrowid
        self.conn.commit()

        return parameter_id

    def add_property(
        self,
        entity_id: int,
        property_name: str,
        value: Any,
        confidence: float = None
    ) -> int:
        """
        Add a property to an entity using the EAV pattern.

        Args:
            entity_id: Entity ID
            property_name: Property name
            value: Property value (type determined automatically)
            confidence: Confidence in property value

        Returns:
            property_instance_id: ID of created property instance
        """
        # Get or create property definition
        self.cursor.execute(
            "SELECT property_id, data_type FROM property_definitions WHERE property_name = ?",
            (property_name,)
        )
        result = self.cursor.fetchone()

        if not result:
            # Auto-create property definition
            data_type = self._infer_data_type(value)
            self.cursor.execute('''
                INSERT INTO property_definitions (property_name, data_type)
                VALUES (?, ?)
            ''', (property_name, data_type))
            property_id = self.cursor.lastrowid
        else:
            property_id, data_type = result

        # Insert property value
        value_field = f"value_{data_type}"
        self.cursor.execute(f'''
            INSERT INTO entity_properties (
                entity_id, property_id, {value_field}, confidence
            ) VALUES (?, ?, ?, ?)
        ''', (entity_id, property_id, value, confidence))

        property_instance_id = self.cursor.lastrowid
        self.conn.commit()

        return property_instance_id

    def _infer_data_type(self, value: Any) -> str:
        """Infer SQL data type from Python value."""
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'real'
        elif isinstance(value, str):
            return 'string' if len(value) < 500 else 'text'
        elif isinstance(value, (dict, list)):
            return 'json'
        else:
            return 'text'

    # =========================================================================
    # CROSS-REFERENCE MANAGEMENT
    # =========================================================================

    def add_cross_reference(
        self,
        entity_id: int,
        database_name: str,
        external_id: str,
        external_url: str = None,
        confidence: float = None
    ) -> int:
        """Add a cross-reference to an external database."""
        # Get database_id
        self.cursor.execute(
            "SELECT database_id FROM external_databases WHERE database_name = ?",
            (database_name,)
        )
        result = self.cursor.fetchone()
        if not result:
            raise ValueError(f"Unknown database: {database_name}")
        database_id = result[0]

        self.cursor.execute('''
            INSERT INTO cross_references (
                entity_id, database_id, external_id, external_url, confidence
            ) VALUES (?, ?, ?, ?, ?)
        ''', (entity_id, database_id, external_id, external_url, confidence))

        xref_id = self.cursor.lastrowid
        self.conn.commit()

        return xref_id

    def get_cross_references(self, entity_id: int) -> List[Dict[str, Any]]:
        """Get all cross-references for an entity."""
        query = '''
            SELECT
                xr.xref_id,
                db.database_name,
                xr.external_id,
                xr.external_url,
                xr.confidence
            FROM cross_references xr
            JOIN external_databases db ON xr.database_id = db.database_id
            WHERE xr.entity_id = ?
        '''

        self.cursor.execute(query, (entity_id,))
        return [dict(row) for row in self.cursor.fetchall()]

    # =========================================================================
    # BULK OPERATIONS
    # =========================================================================

    def bulk_import_entities(
        self,
        entities: List[Dict[str, Any]],
        entity_type: str,
        batch_size: int = 1000
    ) -> List[int]:
        """
        Bulk import entities.

        Args:
            entities: List of entity dictionaries
            entity_type: Entity type name
            batch_size: Commit after this many inserts

        Returns:
            List of created entity IDs
        """
        entity_ids = []

        for i, entity in enumerate(entities):
            entity_id = self.create_entity(entity_type=entity_type, **entity)
            entity_ids.append(entity_id)

            # Commit in batches
            if (i + 1) % batch_size == 0:
                self.conn.commit()
                print(f"Imported {i + 1}/{len(entities)} entities...")

        self.conn.commit()
        print(f"Bulk import complete: {len(entity_ids)} entities created")

        return entity_ids

    def export_to_csv(
        self,
        entity_type: str,
        output_file: str,
        include_type_specific: bool = True
    ):
        """
        Export entities to CSV.

        Args:
            entity_type: Entity type to export
            output_file: Output CSV file path
            include_type_specific: Include type-specific fields
        """
        # Get entities
        entities = self.query_entities_by_type(entity_type)

        if not entities:
            print(f"No entities of type {entity_type} found")
            return

        # Write to CSV
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=entities[0].keys())
            writer.writeheader()
            writer.writerows(entities)

        print(f"Exported {len(entities)} entities to {output_file}")

    # =========================================================================
    # STATISTICS AND REPORTING
    # =========================================================================

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        stats = {}

        # Entity counts by type
        self.cursor.execute('''
            SELECT et.type_name, COUNT(*) as count
            FROM entities e
            JOIN entity_types et ON e.entity_type_id = et.type_id
            GROUP BY et.type_name
            ORDER BY count DESC
        ''')
        stats['entity_counts'] = {row['type_name']: row['count'] for row in self.cursor.fetchall()}

        # Validation status distribution
        self.cursor.execute('''
            SELECT validation_status, COUNT(*) as count
            FROM entities
            GROUP BY validation_status
        ''')
        stats['validation_status'] = {row['validation_status']: row['count']
                                     for row in self.cursor.fetchall()}

        # Computational mappings
        self.cursor.execute('SELECT COUNT(*) as count FROM computational_mappings')
        stats['total_mappings'] = self.cursor.fetchone()['count']

        # Cross-references
        self.cursor.execute('SELECT COUNT(*) as count FROM cross_references')
        stats['total_xrefs'] = self.cursor.fetchone()['count']

        # Relationships
        self.cursor.execute('SELECT COUNT(*) as count FROM entity_relationships')
        stats['total_relationships'] = self.cursor.fetchone()['count']

        return stats

    def print_statistics(self):
        """Print formatted database statistics."""
        stats = self.get_statistics()

        print("\n=== Database Statistics ===\n")

        print("Entity Counts by Type:")
        for entity_type, count in stats['entity_counts'].items():
            print(f"  {entity_type:20s}: {count:6d}")

        print("\nValidation Status:")
        for status, count in stats['validation_status'].items():
            print(f"  {status:20s}: {count:6d}")

        print(f"\nComputational Mappings: {stats['total_mappings']}")
        print(f"Cross-References:       {stats['total_xrefs']}")
        print(f"Relationships:          {stats['total_relationships']}")


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def example_usage():
    """Demonstrate database usage."""

    # Initialize database
    db = BioArchDB('bio_architecture.db')

    # Create schema (only needed once)
    # db.initialize_schema('bio_architecture_schema.sql')

    # Create a mechanism
    mechanism_id = db.create_mechanism(
        identifier='MECH_LI_001',
        name='Lateral Inhibition',
        description='Mechanism where active neurons suppress neighboring neurons',
        update_rule='dy_i/dt = -y_i + f(x_i - sum(w_ij * y_j))',
        mechanism_class='lateral_inhibition',
        time_scale_ms=50.0,
        reversibility=True,
        confidence_score=0.95,
        evidence_strength='experimental'
    )
    print(f"Created mechanism with ID: {mechanism_id}")

    # Add parameter
    param_id = db.add_parameter(
        entity_id=mechanism_id,
        parameter_type='time_constant',
        value=50.0,
        uncertainty=5.0,
        organism='Homo sapiens',
        confidence=0.90
    )

    # Create architectural pattern
    pattern_id = db.create_architectural_pattern(
        pattern_name='Winner-Take-All Network',
        pattern_category='neural_network',
        formal_description='Competitive network where strongest input suppresses others',
        complexity_class='O(n^2)'
    )

    # Add computational mapping
    mapping_id = db.add_computational_mapping(
        entity_id=mechanism_id,
        pattern_id=pattern_id,
        mapping_type='isomorphic',
        fidelity_score=0.90,
        description='Lateral inhibition directly implements WTA competition',
        mathematical_correspondence='Inhibitory weights w_ij implement competitive suppression'
    )

    # Query mechanisms
    mechanisms = db.query_entities_by_type('mechanism', validated_only=False)
    print(f"\nFound {len(mechanisms)} mechanisms")

    # Get computational mappings
    mappings = db.get_computational_mappings(entity_id=mechanism_id)
    for mapping in mappings:
        print(f"\nMapping: {mapping['entity_name']} → {mapping['pattern_name']}")
        print(f"  Fidelity: {mapping['fidelity_score']}")
        print(f"  Description: {mapping['description']}")

    # Search entities
    results = db.search_entities('lateral inhibition')
    print(f"\nSearch results: {len(results)} entities")

    # Print statistics
    db.print_statistics()

    db.close()


if __name__ == '__main__':
    example_usage()
