# Quick Start Guide

Get up and running with the Python MCP Server Development Framework in minutes.

## Prerequisites

- Python 3.11 or higher
- [UV](https://docs.astral.sh/uv/) package manager
- [Cursor IDE](https://cursor.sh/) (recommended)

## Installation

### 1. Install UV (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Create Your Project

```bash
# Initialize new project
uv init my-mcp-server
cd my-mcp-server

# Add MCP dependencies
uv add mcp fastapi uvicorn pydantic aiofiles aiosqlite

# Add development dependencies
uv add --dev pytest pytest-asyncio black isort mypy ruff pre-commit
```

### 3. Copy Cursor Rules

```bash
# Copy the .cursor directory from this repository
cp -r /path/to/python-mcp-development-framework/.cursor ./
```

### 4. Create Task Management Files

```bash
# Create required files
touch TODO.md TASKS.md

# Create project structure
mkdir -p servers/{file-server,db-server} tests docs
```

### 5. Setup Development Environment

```bash
# Install pre-commit hooks
uv run pre-commit install

# Verify setup
uv run pytest --version
uv run black --version
uv run mypy --version
```

## Your First MCP Server

### 1. Create TODO.md

```markdown
# TODO List

## Current Sprint: Basic Server Setup
- [ ] Implement ping/pong handler
- [ ] Add basic error handling
- [ ] Write unit tests
- [ ] Add logging configuration

## Next Sprint
- [ ] Add file operations
- [ ] Implement database tools

## Completed ✅
- [x] Project initialization
- [x] Dependencies installed
- [x] Cursor rules setup
```

### 2. Create TASKS.md

```markdown
# Detailed Task Breakdown

## Task: Implement Ping/Pong Handler
**Status**: In Progress
**Priority**: High
**Server**: basic

### Subtasks:
1. [ ] Create basic ping function
2. [ ] Add input validation
3. [ ] Write unit tests
4. [ ] Add error handling
5. [ ] Add logging

### Acceptance Criteria:
- [ ] Function responds to ping with pong
- [ ] Input validation works
- [ ] All tests pass
- [ ] Proper error handling
- [ ] Logging is implemented

### Notes:
- Start with minimal implementation
- Add features incrementally
- Test each step before proceeding
```

### 3. Implement Your First Tool

Create `servers/basic/ping.py`:

```python
"""
Basic ping tool - demonstrating incremental development
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def ping_tool(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle ping requests.
    
    Development progression:
    1. ✅ Basic ping response (minimal implementation)
    2. [ ] Add input validation
    3. [ ] Add error handling
    4. [ ] Add logging
    """
    try:
        # Basic implementation first
        logger.info("Processing ping request")
        
        return {
            "status": "success",
            "data": {"message": "pong"}
        }
        
    except Exception as e:
        logger.error(f"Ping error: {e}")
        return {"status": "error", "error": str(e)}
```

### 4. Write Tests

Create `tests/test_ping.py`:

```python
import pytest
from servers.basic.ping import ping_tool

@pytest.mark.asyncio
async def test_ping_tool():
    """Test basic ping functionality"""
    request = {}
    result = await ping_tool(request)
    
    assert result["status"] == "success"
    assert result["data"]["message"] == "pong"
```

### 5. Run Tests

```bash
# Run tests
uv run pytest tests/test_ping.py -v

# Format code
uv run black .
uv run isort .

# Type check
uv run mypy .
```

### 6. Update Progress

Update your TODO.md:

```markdown
## Completed ✅
- [x] Project initialization
- [x] Dependencies installed
- [x] Cursor rules setup
- [x] Basic ping/pong handler implemented
```

## Next Steps

1. **Add More Tools**: Implement file operations or database tools
2. **Follow the Rules**: Let Cursor Rules guide your development
3. **Use Manual Rules**: Reference `@deployment-guide` and `@troubleshooting`
4. **Stay Incremental**: Always implement one feature at a time

## Getting Help

- **Deployment**: Use `@deployment-guide` in Cursor chat
- **Troubleshooting**: Use `@troubleshooting` in Cursor chat
- **File Server**: Work in `servers/file-server/` for auto-attached rules
- **Database Server**: Work in `servers/db-server/` for auto-attached rules

## Common Commands

```bash
# Development workflow
uv run pytest                    # Run tests
uv run black .                   # Format code
uv run isort .                   # Sort imports
uv run mypy .                    # Type checking
uv run ruff check .              # Linting

# Pre-commit (runs all checks)
uv run pre-commit run --all-files
```

Happy coding! 🚀 