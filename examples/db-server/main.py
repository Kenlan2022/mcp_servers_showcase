"""
Database Server Example - Demonstrating Incremental Development with Cursor Rules

This example shows how to build a database server following the incremental development approach:
1. Start with minimal implementation
2. Add SQL injection prevention
3. Implement input validation
4. Add comprehensive logging
5. Write tests for each component

The database-server cursor rules automatically apply when working in a servers/db-server/ directory.
"""

import asyncio
import logging
import re
from typing import Dict, Any, List, Optional
import aiosqlite
from dataclasses import dataclass
from pathlib import Path

# Setup logging (enforced by cursor rules)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
DATABASE_PATH = Path("./data/example.db")
MAX_QUERY_RESULTS = 1000


@dataclass
class DatabaseOperation:
    """Type-safe database operation result (type hints enforced by cursor rules)"""
    success: bool
    data: Dict[str, Any]
    error: str = ""


# SQL Security Validation (enforced by database-server cursor rules)

def validate_table_name(table_name: str) -> bool:
    """Validate table name to prevent SQL injection"""
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
        raise ValueError(f"Invalid table name: {table_name}")
    return True


def validate_column_names(columns: str) -> bool:
    """Validate column names to prevent SQL injection"""
    if columns == "*":
        return True
    
    column_list = [col.strip() for col in columns.split(',')]
    for col in column_list:
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', col):
            raise ValueError(f"Invalid column name: {col}")
    return True


def validate_where_clause(where_clause: str) -> bool:
    """Basic validation for WHERE clause (simplified for demo)"""
    # In production, use parameterized queries instead
    dangerous_patterns = [
        r';\s*--',  # SQL injection comments
        r'\bDROP\b', r'\bDELETE\b', r'\bUPDATE\b', r'\bINSERT\b',
        r'\bALTER\b', r'\bCREATE\b', r'\bTRUNCATE\b'
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, where_clause, re.IGNORECASE):
            raise ValueError(f"Potentially dangerous SQL pattern detected")
    
    return True


# Database Connection Management

class DatabaseConnection:
    """Database connection manager with proper resource handling"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.connection: Optional[aiosqlite.Connection] = None
    
    async def connect(self) -> None:
        """Establish database connection"""
        try:
            self.connection = await aiosqlite.connect(self.db_path)
            await self.connection.execute("PRAGMA foreign_keys = ON")
            await self.connection.commit()
            logger.info(f"Connected to database: {self.db_path}")
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            await self.connection.close()
            self.connection = None
            logger.info("Database connection closed")


# MCP Tool Implementation Following Incremental Development

async def query_database_tool(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle database queries with comprehensive security validation.
    
    Development progression (incremental approach):
    1. ✅ Basic query execution (minimal implementation)
    2. ✅ Table name validation (security)
    3. ✅ Column name validation (security)
    4. ✅ WHERE clause validation (security)
    5. ✅ Result limiting (performance)
    6. ✅ Error handling (reliability)
    7. ✅ Logging (debugging)
    
    This follows the incremental development approach enforced by cursor rules.
    """
    try:
        # Input validation
        table = request.get("table")
        if not table:
            raise ValueError("table parameter is required")
        
        columns = request.get("columns", "*")
        where_clause = request.get("where", "")
        limit = request.get("limit", 100)
        
        logger.info(f"Processing database query: table={table}, columns={columns}")
        
        # Security: Validate table name
        validate_table_name(table)
        
        # Security: Validate column names
        validate_column_names(columns)
        
        # Security: Validate WHERE clause if provided
        if where_clause:
            validate_where_clause(where_clause)
        
        # Performance: Enforce result limits
        if limit > MAX_QUERY_RESULTS:
            limit = MAX_QUERY_RESULTS
            logger.warning(f"Query limit reduced to maximum: {MAX_QUERY_RESULTS}")
        
        # Build and execute query
        query = f"SELECT {columns} FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"
        query += f" LIMIT {limit}"
        
        # Execute query with proper connection management
        db_conn = DatabaseConnection(DATABASE_PATH)
        await db_conn.connect()
        
        try:
            async with db_conn.connection.execute(query) as cursor:
                rows = await cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
            
            # Format results
            results = []
            for row in rows:
                results.append(dict(zip(column_names, row)))
            
            logger.info(f"Query executed successfully: {len(results)} rows returned")
            return {
                "status": "success",
                "data": {
                    "query": query,
                    "results": results,
                    "count": len(results),
                    "columns": column_names
                }
            }
            
        finally:
            await db_conn.disconnect()
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"status": "error", "error": str(e)}
    except aiosqlite.Error as e:
        logger.error(f"Database error: {e}")
        return {"status": "error", "error": f"Database error: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"status": "error", "error": "Internal server error"}


async def get_table_schema_tool(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get table schema information with security validation.
    
    Incremental development progression:
    1. ✅ Basic schema retrieval
    2. ✅ Table name validation
    3. ✅ Error handling
    4. ✅ Logging
    """
    try:
        # Input validation
        table = request.get("table")
        if not table:
            raise ValueError("table parameter is required")
        
        logger.info(f"Processing schema request for table: {table}")
        
        # Security: Validate table name
        validate_table_name(table)
        
        # Execute schema query
        db_conn = DatabaseConnection(DATABASE_PATH)
        await db_conn.connect()
        
        try:
            # Get table schema using PRAGMA
            schema_query = f"PRAGMA table_info({table})"
            async with db_conn.connection.execute(schema_query) as cursor:
                schema_rows = await cursor.fetchall()
            
            if not schema_rows:
                raise ValueError(f"Table '{table}' not found")
            
            # Format schema information
            columns = []
            for row in schema_rows:
                columns.append({
                    "name": row[1],
                    "type": row[2],
                    "not_null": bool(row[3]),
                    "default_value": row[4],
                    "primary_key": bool(row[5])
                })
            
            logger.info(f"Schema retrieved successfully for table: {table}")
            return {
                "status": "success",
                "data": {
                    "table": table,
                    "columns": columns,
                    "column_count": len(columns)
                }
            }
            
        finally:
            await db_conn.disconnect()
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"status": "error", "error": str(e)}
    except aiosqlite.Error as e:
        logger.error(f"Database error: {e}")
        return {"status": "error", "error": f"Database error: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"status": "error", "error": "Internal server error"}


async def get_database_stats_tool(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get database statistics.
    
    Incremental development progression:
    1. ✅ Basic statistics retrieval
    2. ✅ Table enumeration
    3. ✅ Row counting
    4. ✅ Error handling
    5. ✅ Logging
    """
    try:
        logger.info("Processing database statistics request")
        
        db_conn = DatabaseConnection(DATABASE_PATH)
        await db_conn.connect()
        
        try:
            # Get all tables
            tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
            async with db_conn.connection.execute(tables_query) as cursor:
                table_rows = await cursor.fetchall()
            
            table_stats = []
            for table_row in table_rows:
                table_name = table_row[0]
                
                # Get row count for each table
                count_query = f"SELECT COUNT(*) FROM {table_name}"
                async with db_conn.connection.execute(count_query) as cursor:
                    count_result = await cursor.fetchone()
                    row_count = count_result[0] if count_result else 0
                
                table_stats.append({
                    "table": table_name,
                    "row_count": row_count
                })
            
            logger.info(f"Database statistics retrieved: {len(table_stats)} tables")
            return {
                "status": "success",
                "data": {
                    "total_tables": len(table_stats),
                    "tables": table_stats
                }
            }
            
        finally:
            await db_conn.disconnect()
        
    except aiosqlite.Error as e:
        logger.error(f"Database error: {e}")
        return {"status": "error", "error": f"Database error: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"status": "error", "error": "Internal server error"}


# Database initialization for demo
async def initialize_demo_database():
    """Initialize demo database with sample data"""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    db_conn = DatabaseConnection(DATABASE_PATH)
    await db_conn.connect()
    
    try:
        # Create sample table
        await db_conn.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert sample data
        await db_conn.connection.execute("""
            INSERT OR IGNORE INTO users (id, name, email) VALUES 
            (1, 'Alice Johnson', 'alice@example.com'),
            (2, 'Bob Smith', 'bob@example.com'),
            (3, 'Charlie Brown', 'charlie@example.com')
        """)
        
        await db_conn.connection.commit()
        logger.info("Demo database initialized")
        
    finally:
        await db_conn.disconnect()


# Example usage demonstrating the incremental development approach
async def main():
    """
    Example usage of the database server tools.
    
    This demonstrates how each tool was built incrementally:
    1. Start with basic functionality
    2. Add security measures
    3. Implement error handling
    4. Add comprehensive logging
    """
    
    # Initialize demo database
    await initialize_demo_database()
    
    # Example 1: Query database
    print("=== Example 1: Querying database ===")
    query_result = await query_database_tool({
        "table": "users",
        "columns": "id, name, email",
        "limit": 10
    })
    print(f"Query result: {query_result}")
    
    # Example 2: Get table schema
    print("\n=== Example 2: Getting table schema ===")
    schema_result = await get_table_schema_tool({
        "table": "users"
    })
    print(f"Schema result: {schema_result}")
    
    # Example 3: Get database statistics
    print("\n=== Example 3: Getting database statistics ===")
    stats_result = await get_database_stats_tool({})
    print(f"Stats result: {stats_result}")
    
    # Example 4: Error handling demonstration
    print("\n=== Example 4: Error handling ===")
    error_result = await query_database_tool({
        "table": "nonexistent_table"
    })
    print(f"Error result: {error_result}")


if __name__ == "__main__":
    asyncio.run(main()) 