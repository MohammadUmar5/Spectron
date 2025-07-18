import psycopg2
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import hashlib

class DatabaseHandler:
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize database connection.
        
        Args:
            db_config: Dictionary with database connection parameters
                      {'user': 'REDACTED_USER', 'host': 'localhost', 'database': 'REDACTED_DB', 
                       'password': 'REDACTED', 'port': '5432'}
        """
        self.db_config = db_config
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection."""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            print("Database connection established")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise
            
    def disconnect(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed")
    
    def verify_database_setup(self) -> Dict[str, Any]:
        """
        Verify that we're connected to the correct database and table exists.
        
        Returns:
            Dict with verification results
        """
        if not self.connection:
            self.connect()
            
        try:
            # Check current database name
            self.cursor.execute("SELECT current_database();")
            current_db = self.cursor.fetchone()[0]
            
            # Check if schema exists
            self.cursor.execute("""
                SELECT schema_name 
                FROM information_schema.schemata 
                WHERE schema_name = 'ndvi_analysis';
            """)
            schema_exists = self.cursor.fetchone() is not None
            
            # Check if table exists
            self.cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'ndvi_analysis' 
                AND table_name = 'image_results';
            """)
            table_exists = self.cursor.fetchone() is not None
            
            # Get table column info if table exists
            columns = []
            if table_exists:
                self.cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_schema = 'ndvi_analysis' 
                    AND table_name = 'image_results'
                    ORDER BY ordinal_position;
                """)
                columns = [{"name": row[0], "type": row[1]} for row in self.cursor.fetchall()]
            
            verification_result = {
                "database_name": current_db,
                "expected_database": "satellite_analysis_db",
                "database_correct": current_db == "satellite_analysis_db",
                "schema_exists": schema_exists,
                "table_exists": table_exists,
                "table_columns": columns,
                "setup_valid": (
                    current_db == "satellite_analysis_db" and 
                    schema_exists and 
                    table_exists
                )
            }
            
            print(f"Database Verification Results:")
            print(f"  Connected to database: {current_db}")
            print(f"  Expected database: satellite_analysis_db")
            print(f"  Database correct: {verification_result['database_correct']}")
            print(f"  Schema 'ndvi_analysis' exists: {schema_exists}")
            print(f"  Table 'image_results' exists: {table_exists}")
            print(f"  Setup valid: {verification_result['setup_valid']}")
            
            if table_exists:
                print(f"  Table has {len(columns)} columns")
            
            return verification_result
            
        except Exception as e:
            print(f"Error during database verification: {e}")
            raise
    
    def generate_analysis_id(self, bbox: list, start_date: str, end_date: str, 
                           selection_mode: str) -> str:
        """
        Generate a unique analysis ID based on parameters.
        
        Args:
            bbox: Bounding box coordinates
            start_date: Start date string
            end_date: End date string
            selection_mode: Selection mode used
            
        Returns:
            str: Unique analysis ID
        """
        # Create a hash from the parameters
        params_str = f"{bbox}_{start_date}_{end_date}_{selection_mode}"
        hash_obj = hashlib.md5(params_str.encode())
        return f"ndvi_{hash_obj.hexdigest()[:12]}"
    
    def save_analysis_results(self, 
                            bbox: list,
                            start_date: str,
                            end_date: str,
                            selection_mode: str,
                            early_image_data: Dict[str, Any],
                            late_image_data: Dict[str, Any],
                            analysis_results: Dict[str, Any],
                            early_ndvi_image: bytes,
                            late_ndvi_image: bytes,
                            difference_image: bytes) -> str:
        """
        Save complete analysis results to database.
        
        Args:
            bbox: Bounding box coordinates
            start_date: Start date string
            end_date: End date string
            selection_mode: Selection mode used
            early_image_data: Early image metadata
            late_image_data: Late image metadata
            analysis_results: Analysis results dictionary
            early_ndvi_image: Early NDVI image as bytes
            late_ndvi_image: Late NDVI image as bytes
            difference_image: Difference image as bytes
            
        Returns:
            str: Analysis ID of saved record
        """
        if not self.connection:
            self.connect()
            
        try:
            # Generate analysis ID
            analysis_id = self.generate_analysis_id(bbox, start_date, end_date, selection_mode)
            
            # Parse dates from image data
            early_date = datetime.fromisoformat(early_image_data['datetime'][:10])
            late_date = datetime.fromisoformat(late_image_data['datetime'][:10])
            
            # Prepare SQL query
            insert_query = """
                INSERT INTO ndvi_analysis.image_results (
                    analysis_id, bbox, start_date, end_date, 
                    early_image_date, late_image_date, selection_mode,
                    early_ndvi_image, late_ndvi_image, difference_image,
                    early_ndvi_metadata, late_ndvi_metadata, analysis_results
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (analysis_id) 
                DO UPDATE SET
                    early_ndvi_image = EXCLUDED.early_ndvi_image,
                    late_ndvi_image = EXCLUDED.late_ndvi_image,
                    difference_image = EXCLUDED.difference_image,
                    early_ndvi_metadata = EXCLUDED.early_ndvi_metadata,
                    late_ndvi_metadata = EXCLUDED.late_ndvi_metadata,
                    analysis_results = EXCLUDED.analysis_results,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING analysis_id;
            """
            
            # Execute query
            self.cursor.execute(insert_query, (
                analysis_id,
                json.dumps(bbox),
                start_date,
                end_date,
                early_date,
                late_date,
                selection_mode,
                early_ndvi_image,
                late_ndvi_image,
                difference_image,
                json.dumps(early_image_data),
                json.dumps(late_image_data),
                json.dumps(analysis_results)
            ))
            
            # Commit transaction
            self.connection.commit()
            
            # Get the returned analysis_id
            result = self.cursor.fetchone()
            saved_analysis_id = result[0] if result else analysis_id
            
            print(f"Analysis results saved to database with ID: {saved_analysis_id}")
            return saved_analysis_id
            
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            print(f"Error saving to database: {e}")
            raise
    
    def get_analysis_results(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve analysis results from database.
        
        Args:
            analysis_id: Analysis ID to retrieve
            
        Returns:
            Dict containing analysis results or None if not found
        """
        if not self.connection:
            self.connect()
            
        try:
            query = """
                SELECT analysis_id, bbox, start_date, end_date, 
                       early_image_date, late_image_date, selection_mode,
                       early_ndvi_metadata, late_ndvi_metadata, analysis_results,
                       created_at, updated_at
                FROM ndvi_analysis.image_results 
                WHERE analysis_id = %s;
            """
            
            self.cursor.execute(query, (analysis_id,))
            result = self.cursor.fetchone()
            
            if result:
                return {
                    'analysis_id': result[0],
                    'bbox': json.loads(result[1]),
                    'start_date': result[2].isoformat(),
                    'end_date': result[3].isoformat(),
                    'early_image_date': result[4].isoformat(),
                    'late_image_date': result[5].isoformat(),
                    'selection_mode': result[6],
                    'early_ndvi_metadata': json.loads(result[7]),
                    'late_ndvi_metadata': json.loads(result[8]),
                    'analysis_results': json.loads(result[9]),
                    'created_at': result[10].isoformat(),
                    'updated_at': result[11].isoformat()
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error retrieving from database: {e}")
            raise
    
    def get_image_data(self, analysis_id: str, image_type: str) -> Optional[bytes]:
        """
        Retrieve image data from database.
        
        Args:
            analysis_id: Analysis ID
            image_type: Type of image ('early', 'late', 'difference')
            
        Returns:
            bytes: Image data or None if not found
        """
        if not self.connection:
            self.connect()
            
        try:
            column_map = {
                'early': 'early_ndvi_image',
                'late': 'late_ndvi_image',
                'difference': 'difference_image'
            }
            
            if image_type not in column_map:
                raise ValueError(f"Invalid image_type: {image_type}")
                
            query = f"""
                SELECT {column_map[image_type]}
                FROM ndvi_analysis.image_results 
                WHERE analysis_id = %s;
            """
            
            self.cursor.execute(query, (analysis_id,))
            result = self.cursor.fetchone()
            
            if result and result[0]:
                return bytes(result[0])
            else:
                return None
                
        except Exception as e:
            print(f"Error retrieving image data: {e}")
            raise
    
    def list_analyses(self, limit: int = 100) -> list:
        """
        List recent analyses from database.
        
        Args:
            limit: Maximum number of results to return
            
        Returns:
            List of analysis summaries
        """
        if not self.connection:
            self.connect()
            
        try:
            query = """
                SELECT analysis_id, bbox, start_date, end_date, 
                       early_image_date, late_image_date, selection_mode,
                       created_at, updated_at
                FROM ndvi_analysis.image_results 
                ORDER BY created_at DESC
                LIMIT %s;
            """
            
            self.cursor.execute(query, (limit,))
            results = self.cursor.fetchall()
            
            analyses = []
            for result in results:
                analyses.append({
                    'analysis_id': result[0],
                    'bbox': json.loads(result[1]),
                    'start_date': result[2].isoformat(),
                    'end_date': result[3].isoformat(),
                    'early_image_date': result[4].isoformat(),
                    'late_image_date': result[5].isoformat(),
                    'selection_mode': result[6],
                    'created_at': result[7].isoformat(),
                    'updated_at': result[8].isoformat()
                })
            
            return analyses
            
        except Exception as e:
            print(f"Error listing analyses: {e}")
            raise

# Database configuration
DB_CONFIG = {
    'user': 'REDACTED_USER',
    'host': 'localhost',
    'database': 'REDACTED_DB',
    'password': 'REDACTED',
    'port': '5432'
}

# Global database handler instance
db_handler = DatabaseHandler(DB_CONFIG)