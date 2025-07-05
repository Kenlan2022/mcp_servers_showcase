"""
File Server Example - Demonstrating Incremental Development with Cursor Rules

This example shows how to build a file server following the incremental development approach:
1. Start with minimal implementation
2. Add security validation
3. Implement error handling
4. Add comprehensive logging
5. Write tests for each component

The file-server cursor rules automatically apply when working in a servers/file-server/ directory.
"""

import asyncio
import logging
import re
from pathlib import Path
from typing import Dict, Any, List
import aiofiles
import aiofiles.os
from dataclasses import dataclass

# Setup logging (enforced by cursor rules)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
BASE_DIR = Path("./data/files")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".txt", ".json", ".csv", ".md", ".py"}


@dataclass
class FileOperation:
    """Type-safe file operation result (type hints enforced by cursor rules)"""
    success: bool
    data: Dict[str, Any]
    error: str = ""


def validate_file_path(file_path: str, base_dir: Path = BASE_DIR) -> Path:
    """
    Validate file path to prevent directory traversal attacks.
    
    Security validation is enforced by file-server cursor rules.
    """
    try:
        # Resolve path and ensure it's within base directory
        resolved_path = base_dir.resolve() / Path(file_path).name
        
        # Check if path is within base directory
        if not str(resolved_path).startswith(str(base_dir.resolve())):
            raise ValueError("Invalid file path: directory traversal detected")
        
        return resolved_path
    except Exception as e:
        logger.error(f"Path validation error: {e}")
        raise ValueError(f"Invalid file path: {e}")


def validate_file_extension(file_path: Path) -> bool:
    """Validate file extension against allowed types"""
    return file_path.suffix.lower() in ALLOWED_EXTENSIONS


async def check_file_size(file_path: Path) -> None:
    """Check file size before processing"""
    try:
        if file_path.exists():
            file_size = await aiofiles.os.path.getsize(file_path)
            if file_size > MAX_FILE_SIZE:
                raise ValueError(f"File too large: {file_size} bytes (max: {MAX_FILE_SIZE})")
    except Exception as e:
        logger.error(f"File size check error: {e}")
        raise


# MCP Tool Implementation Following Incremental Development

async def read_file_tool(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle file read requests with comprehensive security validation.
    
    Development progression (incremental approach):
    1. ✅ Basic file reading (minimal implementation)
    2. ✅ Path validation (security)
    3. ✅ File type validation (security)
    4. ✅ Size checking (performance)
    5. ✅ Error handling (reliability)
    6. ✅ Logging (debugging)
    
    This follows the incremental development approach enforced by cursor rules.
    """
    try:
        # Input validation
        file_path = request.get("file_path")
        if not file_path:
            raise ValueError("file_path is required")
        
        encoding = request.get("encoding", "utf-8")
        logger.info(f"Processing file read request: {file_path}")
        
        # Security: Validate file path
        safe_path = validate_file_path(file_path)
        
        # Security: Validate file extension
        if not validate_file_extension(safe_path):
            raise ValueError(f"File type not allowed: {safe_path.suffix}")
        
        # Performance: Check file size
        await check_file_size(safe_path)
        
        # Read file asynchronously
        async with aiofiles.open(safe_path, 'r', encoding=encoding) as f:
            content = await f.read()
        
        logger.info(f"Successfully read file: {safe_path}")
        return {
            "status": "success",
            "data": {
                "content": content,
                "path": str(safe_path),
                "size": len(content),
                "encoding": encoding
            }
        }
        
    except FileNotFoundError:
        error_msg = f"File not found: {file_path}"
        logger.error(error_msg)
        return {"status": "error", "error": error_msg}
    except PermissionError:
        error_msg = f"Permission denied: {file_path}"
        logger.error(error_msg)
        return {"status": "error", "error": error_msg}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"status": "error", "error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error reading file: {e}")
        return {"status": "error", "error": "Internal server error"}


async def write_file_tool(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle file write requests with security validation.
    
    Incremental development progression:
    1. ✅ Basic file writing
    2. ✅ Path validation
    3. ✅ Content validation
    4. ✅ Directory creation
    5. ✅ Error handling
    6. ✅ Logging
    """
    try:
        # Input validation
        file_path = request.get("file_path")
        content = request.get("content")
        
        if not file_path:
            raise ValueError("file_path is required")
        if content is None:
            raise ValueError("content is required")
        
        encoding = request.get("encoding", "utf-8")
        logger.info(f"Processing file write request: {file_path}")
        
        # Security: Validate file path
        safe_path = validate_file_path(file_path)
        
        # Security: Validate file extension
        if not validate_file_extension(safe_path):
            raise ValueError(f"File type not allowed: {safe_path.suffix}")
        
        # Performance: Check content size
        content_size = len(content.encode(encoding))
        if content_size > MAX_FILE_SIZE:
            raise ValueError(f"Content too large: {content_size} bytes")
        
        # Create directory if needed
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file asynchronously
        async with aiofiles.open(safe_path, 'w', encoding=encoding) as f:
            await f.write(content)
        
        logger.info(f"Successfully wrote file: {safe_path}")
        return {
            "status": "success",
            "data": {
                "path": str(safe_path),
                "size": content_size,
                "encoding": encoding
            }
        }
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"status": "error", "error": str(e)}
    except PermissionError:
        error_msg = f"Permission denied: {file_path}"
        logger.error(error_msg)
        return {"status": "error", "error": error_msg}
    except Exception as e:
        logger.error(f"Unexpected error writing file: {e}")
        return {"status": "error", "error": "Internal server error"}


# Example usage demonstrating the incremental development approach
async def main():
    """
    Example usage of the file server tools.
    
    This demonstrates how each tool was built incrementally:
    1. Start with basic functionality
    2. Add security measures
    3. Implement error handling
    4. Add comprehensive logging
    """
    
    # Ensure base directory exists
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Example 1: Write a file
    print("=== Example 1: Writing a file ===")
    write_result = await write_file_tool({
        "file_path": "example.txt",
        "content": "Hello, World!\nThis is a test file created by the MCP file server."
    })
    print(f"Write result: {write_result}")
    
    # Example 2: Read the file
    print("\n=== Example 2: Reading a file ===")
    read_result = await read_file_tool({
        "file_path": "example.txt"
    })
    print(f"Read result: {read_result}")
    
    # Example 3: Error handling demonstration
    print("\n=== Example 3: Error handling ===")
    error_result = await read_file_tool({
        "file_path": "nonexistent.txt"
    })
    print(f"Error result: {error_result}")


if __name__ == "__main__":
    asyncio.run(main()) 