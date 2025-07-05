# Python MCP Server Development with Cursor Rules

> **A comprehensive development framework for Python MCP servers with enforced incremental development practices**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://docs.astral.sh/uv/)

## 🌟 What This Is

This repository showcases a **production-ready development framework** for building Python MCP (Model Context Protocol) servers using **Cursor Rules**. The system enforces **incremental development practices** and provides comprehensive guidelines for building reliable, secure, and maintainable MCP servers.

## 🚀 Key Features

### 🎯 Enforced Incremental Development
- **NEVER** create multiple untested files at once
- Mandatory TODO.md and TASKS.md management
- Step-by-step development workflow
- Built-in quality gates

### 🔧 Comprehensive Tooling
- **UV** integration for modern Python dependency management
- **Type checking** with mypy
- **Code formatting** with black and isort
- **Testing** with pytest and pytest-asyncio
- **Pre-commit hooks** for quality assurance

### 🛡️ Security First
- File path validation and directory traversal protection
- SQL injection prevention
- Input sanitization and validation
- Comprehensive error handling

### 📋 Smart Rule System
- **Auto-attached rules** based on file location
- **Manual rules** for deployment and troubleshooting
- **Always-active rules** for global standards
- Context-aware development guidelines

## 📁 Repository Structure

```
python-mcp-development-framework/
├── .cursor/
│   └── rules/
│       ├── python_mcp_servers.mdc        # Main development rules
│       ├── global-standards.mdc          # Global standards
│       ├── file-server-rules.mdc         # File server specific rules
│       ├── database-server-rules.mdc     # Database server specific rules
│       ├── deployment-guide.mdc          # Deployment procedures
│       └── troubleshooting.mdc           # Troubleshooting guide
├── examples/
│   ├── file-server/                      # File server examples
│   └── db-server/                        # Database server examples
├── docs/                                 # Additional documentation
└── README.md                             # This file
```

## 🎯 Development Philosophy

### The Incremental Approach

This framework is built around a **strict incremental development methodology**:

1. **📋 Plan First** - Update TODO.md with specific tasks
2. **🔨 Implement One Thing** - Build one component at a time
3. **🧪 Test Immediately** - Write and run tests before proceeding
4. **✅ Verify** - Ensure current step works completely
5. **📝 Document** - Update progress and notes

### Why This Matters

- **Reduces bugs** by catching issues early
- **Improves code quality** through focused development
- **Enhances maintainability** with clear progression
- **Increases reliability** through comprehensive testing
- **Accelerates debugging** with smaller change sets

## 🛠️ How the Rule System Works

### Auto-Attached Rules

Rules automatically apply based on your file location:

```bash
# Working in file server? File server rules auto-apply
servers/file-server/main.py  → file-server-rules.mdc

# Working in database server? Database rules auto-apply
servers/db-server/main.py    → database-server-rules.mdc
```

### Manual Rules

Call specific rules in Cursor chat when needed:

```
@deployment-guide    # Get deployment procedures
@troubleshooting     # Get debugging help
```

### Always-Active Rules

Core development standards apply everywhere:
- Type hints are mandatory
- Error handling is required
- Tests must be written
- Documentation is enforced

## 🚀 Quick Start

### 1. Copy the Rules

```bash
# Copy the .cursor directory to your project
cp -r .cursor /path/to/your/mcp-project/
```

### 2. Initialize Your Project

```bash
# Initialize with UV
uv init your-mcp-project
cd your-mcp-project

# Add dependencies
uv add mcp fastapi uvicorn pydantic aiofiles
uv add --dev pytest pytest-asyncio black isort mypy ruff
```

### 3. Create Task Files

```bash
# Create required task management files
touch TODO.md TASKS.md
```

### 4. Start Development

The rules will automatically guide you through:
- Creating minimal implementations first
- Writing tests immediately
- Following security best practices
- Maintaining proper documentation

## 📊 Examples

### File Server Example

```python
# examples/file-server/main.py
from typing import Dict, Any
import aiofiles
import logging

logger = logging.getLogger(__name__)

async def read_file_tool(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle file read requests with security validation"""
    try:
        file_path = request.get("file_path")
        if not file_path:
            raise ValueError("file_path is required")
        
        # Security: Validate file path
        safe_path = validate_file_path(file_path)
        
        # Read file asynchronously
        async with aiofiles.open(safe_path, 'r') as f:
            content = await f.read()
        
        return {
            "status": "success",
            "data": {"content": content, "path": str(safe_path)}
        }
    except Exception as e:
        logger.error(f"File read error: {e}")
        return {"status": "error", "error": str(e)}
```

### Database Server Example

```python
# examples/db-server/main.py
from typing import Dict, Any
import aiosqlite
import logging

logger = logging.getLogger(__name__)

async def query_database_tool(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle database queries with SQL injection prevention"""
    try:
        table = request.get("table")
        if not table:
            raise ValueError("table is required")
        
        # Security: Validate table name
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table):
            raise ValueError("Invalid table name")
        
        # Execute query safely
        async with aiosqlite.connect("database.db") as conn:
            async with conn.execute(f"SELECT * FROM {table} LIMIT 100") as cursor:
                rows = await cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
        
        return {
            "status": "success",
            "data": {"rows": rows, "columns": columns}
        }
    except Exception as e:
        logger.error(f"Database query error: {e}")
        return {"status": "error", "error": str(e)}
```

## 📚 Documentation

### Core Rules

1. **[Main Development Rules](/.cursor/rules/python_mcp_servers.mdc)** - Primary development guidelines
2. **[Global Standards](/.cursor/rules/global-standards.mdc)** - Universal development standards
3. **[File Server Rules](/.cursor/rules/file-server-rules.mdc)** - File operation specific guidelines
4. **[Database Server Rules](/.cursor/rules/database-server-rules.mdc)** - Database operation guidelines

### Operational Guides

1. **[Deployment Guide](/.cursor/rules/deployment-guide.mdc)** - Production deployment procedures
2. **[Troubleshooting](/.cursor/rules/troubleshooting.mdc)** - Debugging and problem resolution

## 🎯 Benefits

### For Developers
- **Faster development** with clear guidelines
- **Fewer bugs** through incremental approach
- **Better code quality** with enforced standards
- **Easier debugging** with comprehensive logging

### For Teams
- **Consistent code style** across projects
- **Reduced onboarding time** for new developers
- **Better collaboration** with clear practices
- **Improved maintainability** of codebases

### For Projects
- **Higher reliability** through comprehensive testing
- **Better security** with built-in protections
- **Easier deployment** with detailed guides
- **Faster troubleshooting** with comprehensive documentation

## 🔄 Development Workflow Example

```markdown
# TODO.md
## Current Sprint: File Server Basic Operations
- [ ] Implement file read functionality
- [ ] Add file write functionality
- [ ] Implement directory listing
- [ ] Add file metadata retrieval

## Next Sprint
- [ ] Add file streaming for large files
- [ ] Implement file caching
```

```markdown
# TASKS.md
## Task: Implement File Read Functionality
**Status**: In Progress
**Priority**: High

### Subtasks:
1. [x] Create basic file read function
2. [x] Add path validation
3. [x] Write unit tests
4. [ ] Add error handling
5. [ ] Add logging

### Acceptance Criteria:
- [ ] Function can read text files
- [ ] Path validation prevents directory traversal
- [ ] All tests pass
- [ ] Proper error handling implemented
- [ ] Logging is comprehensive
```

## 🤝 Contributing

This showcase demonstrates best practices for MCP server development. Feel free to:

1. **Use these rules** in your own projects
2. **Adapt the system** to your specific needs
3. **Share improvements** through issues and discussions
4. **Contribute examples** for different use cases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for the [Cursor AI IDE](https://cursor.sh/)
- Designed for [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)
- Powered by [UV](https://docs.astral.sh/uv/) for Python package management

---

> **Remember**: The key to successful development is not speed, but consistency and quality. This framework helps you achieve both through disciplined, incremental development practices.

**🚀 Ready to transform your MCP server development? Copy the `.cursor` directory to your project and start building better, faster, and more reliably!** 