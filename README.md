# BrandNexus

**An intelligent MCP server that seamlessly connects your strategy documents, brand guidelines, and messaging templates to AI-powered workflows through Claude Desktop, Cursor IDE, and VS Code, enabling instant search, classification, and contextual access to organizational knowledge.**

## MCP Server Architecture

```mermaid
flowchart TB
  subgraph L0["Client Layer"]
    CL1["Cursor IDE"]
    CL2["Claude Desktop"]
    CL3["VS Code"]
    CL4["Roo Code (agents)"]
  end

  subgraph L1["MCP Protocol"]
    P1["stdio"]
    P2["SSE (server-sent events)"]
    P3["HTTP (optional)"]
  end

  subgraph L2["Domain-Specific MCP Server (FastMCP)"]
    S1["Tools (@mcp.tool)"]
    S2["Resources (@mcp.resource)"]
    S3["Access Control (optional JWT)"]
  end

  subgraph L3["Document Processing"]
    DP1["DocumentIndexer"]
    DP2["Classifier (rules/ML)"]
    DP3["Metadata Extractor"]
    DP4["Content Parser (md/txt/pdf/docx/yaml/json)"]
  end

  subgraph L4["Storage"]
    ST1["SQLite DB"]
    ST2["Full-text Index"]
    ST3["Metadata Tables"]
    ST4["(Optional) Embedding Index"]
  end

  subgraph L5["File System (Project)"]
    FS1["/strategy/"]
    FS2["/brand/"]
    FS3["/messaging/"]
    FS4["/templates/"]
    FS5["/guidelines/"]
  end

  CL4 --> P1
  P1 --> S1
  S1 --> DP1
  S1 --> DP2
  S1 --> DP3
  S1 --> DP4
  DP1 --> ST1
  DP2 --> ST3
  DP3 --> ST3
  DP4 --> ST2
  ST1 --> S1
  ST2 --> S1
  ST3 --> S1
  FS1 --> DP4
  FS2 --> DP4
  FS3 --> DP4
  FS4 --> DP4
  FS5 --> DP4


## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Client Integration](#client-integration)
- [API Documentation](#api-documentation)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Overview

BrandNexus is a specialized Model Context Protocol (MCP) server designed to revolutionize how organizations manage and access their strategic content. By creating an intelligent bridge between your documents and AI-powered tools, BrandNexus enables instant search, automatic classification, and contextual access to strategy documents, brand guidelines, and messaging templates.

### What is MCP?

The Model Context Protocol (MCP) is an open standard that enables seamless communication between AI applications and data sources. BrandNexus implements this protocol to make your organizational knowledge instantly accessible to AI assistants like Claude, enhancing their ability to provide contextually relevant and brand-consistent responses.

### Why BrandNexus?

- **🔍 Intelligent Search**: Find documents instantly using natural language queries
- **🏷️ Smart Classification**: Automatically categorizes documents by type and content
- **🔗 Seamless Integration**: Works with Claude Desktop, Cursor IDE, and VS Code
- **📊 Real-time Indexing**: Automatically updates when documents change
- **🛡️ Enterprise Ready**: Built with security, performance, and scalability in mind

## Features

### Core Functionality
- **Document Indexing**: Automatically scans and indexes strategy, brand, and messaging documents
- **Full-Text Search**: Powerful search across all document content with metadata filtering
- **Smart Classification**: Rule-based and ML-powered document type detection
- **Resource URIs**: Structured access patterns for different document types
- **Relationship Analysis**: Discover connections and dependencies between documents

### Supported File Types
- Markdown (`.md`)
- Text files (`.txt`)
- Microsoft Word (`.docx`)
- PDF documents (`.pdf`)
- YAML configuration (`.yaml`, `.yml`)
- JSON data (`.json`)

### AI Client Integration
- **Claude Desktop**: Native MCP integration for document-aware conversations
- **Cursor IDE**: Enhanced coding with brand and strategy context
- **VS Code**: Document access through MCP extensions
- **Custom Clients**: FastMCP SDK support for building custom integrations

### Advanced Capabilities
- **Semantic Search**: Vector-based similarity search (optional)
- **Real-time Monitoring**: File system change detection
- **ML Classification**: Machine learning-enhanced document categorization
- **Performance Optimization**: Caching and background processing
- **Security Features**: Authentication and path validation

## Quick Start

Get BrandNexus running in under 5 minutes:

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/brandnexus.git
cd brandnexus

# 2. Run automated deployment
chmod +x deploy_mcp_server.sh
./deploy_mcp_server.sh

# 3. Configure your AI client (see Client Integration section)

# 4. Start using
# In Claude Desktop: "Index all strategy documents"
# In Cursor IDE: "Search for brand guidelines about logo usage"
```

## Installation

### Prerequisites

- **Python 3.8+**: Required for running the MCP server
- **pip**: Python package manager (usually included with Python)
- **Git**: For cloning the repository (optional)

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 512MB RAM (2GB+ recommended for large document sets)
- **Storage**: 100MB for installation + space for your documents and index
- **Network**: Internet connection for initial dependency installation

### Manual Installation

1. **Download BrandNexus**:
   ```bash
   git clone https://github.com/yourusername/brandnexus.git
   cd brandnexus
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install fastmcp sqlite3 pathlib pyyaml
   
   # Optional: For enhanced document processing
   pip install python-docx PyPDF2 markdown
   
   # Optional: For advanced features
   pip install scikit-learn sentence-transformers faiss-cpu
   ```

3. **Create Directory Structure**:
   ```bash
   mkdir -p strategy brand messaging templates guidelines
   ```

4. **Initialize Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your specific paths and settings
   ```

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```env
# Document paths (comma-separated)
DOCUMENT_PATHS=./strategy/,./brand/,./messaging/,./templates/,./guidelines/

# Database configuration
DATABASE_PATH=document_index.db

# Server settings
SERVER_NAME=BrandNexus Document Server
LOG_LEVEL=INFO

# Features
AUTO_REINDEX=true
REINDEX_INTERVAL=3600
ENABLE_SEMANTIC_SEARCH=false
ENABLE_ML_CLASSIFICATION=false
```

### Directory Structure

Organize your documents in the following structure:

```
your-project/
├── strategy/                    # Strategic documents
│   ├── company-strategy-2025.md
│   ├── product-roadmap.md
│   └── market-analysis.pdf
├── brand/                       # Brand guidelines
│   ├── brand-guidelines.md
│   ├── logo-usage.md
│   ├── color-palette.yaml
│   └── typography-guide.pdf
├── messaging/                   # Templates and copy
│   ├── email-templates/
│   ├── social-media-templates/
│   └── press-release-formats/
├── templates/                   # Additional templates
└── guidelines/                  # Other guidelines
```

### Advanced Configuration

For advanced setups, create a `config.yaml` file:

```yaml
server:
  name: "BrandNexus Document Server"
  version: "1.0.0"

paths:
  strategy: "./strategy/"
  brand: "./brand/"
  messaging: "./messaging/"

indexing:
  supported_extensions: [".md", ".txt", ".docx", ".pdf", ".yaml"]
  exclude_patterns: ["*.tmp", ".*", "__pycache__"]
  auto_reindex: true

classification:
  rules:
    strategy:
      path_patterns: ["/strategy/", "strategy"]
      keywords: ["roadmap", "objectives", "goals"]
    brand:
      path_patterns: ["/brand/", "brand"]
      keywords: ["guidelines", "identity", "voice"]
```

## Usage

### Starting the Server

Run BrandNexus as an MCP server:

```bash
python domain_specific_mcp_server.py
```

The server will start in stdio mode, ready to accept MCP protocol connections from AI clients.

### Basic Operations

Once connected through an AI client, you can use natural language commands:

#### Document Indexing
- "Index all documents"
- "Refresh the document index"
- "Show indexing status"

#### Searching Documents
- "Find strategy documents about customer acquisition"
- "Search for brand guidelines on logo usage"
- "Show me messaging templates for product launches"
- "Find all documents mentioning 'sustainability'"

#### Document Access
- "Get the content of our brand voice guide"
- "Show me the latest strategy document"
- "Display all email templates"

#### Analysis and Insights
- "Analyze relationships between documents"
- "Show document type distribution"
- "What are the most common tags across all documents?"

### Working with Document Types

BrandNexus automatically classifies documents into these types:

- **Strategy**: Company strategies, roadmaps, objectives
- **Brand Guidelines**: Visual identity, logo usage, brand voice
- **Messaging Templates**: Email templates, social copy, campaigns
- **Positioning**: Market positioning, competitive analysis
- **Campaign Briefs**: Campaign strategies and briefs
- **Brand Voice**: Tone and voice guidelines

## Client Integration

### Claude Desktop

1. **Install Claude Desktop** from Anthropic's website

2. **Configure MCP Server**:
   Create or edit `~/.config/claude-desktop/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "brandnexus": {
         "command": "python3",
         "args": ["/absolute/path/to/domain_specific_mcp_server.py"],
         "env": {
           "DOCUMENT_PATHS": "/path/to/strategy/,/path/to/brand/,/path/to/messaging/"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop** and start using document-aware conversations!

### Cursor IDE

1. **Install Cursor IDE** from cursor.sh

2. **Configure MCP Integration**:
   Create `.cursor/mcp.json` in your workspace:
   ```json
   {
     "mcpServers": {
       "brandnexus": {
         "command": "python",
         "args": ["./domain_specific_mcp_server.py"],
         "env": {
           "DOCUMENT_PATHS": "./strategy/,./brand/,./messaging/"
         }
       }
     }
   }
   ```

3. **Use in Cursor**: Access documents while coding with AI assistance

### VS Code

1. **Install MCP Extension** (when available)

2. **Configure Server**:
   Create `.vscode/mcp.json`:
   ```json
   {
     "servers": {
       "brandnexus": {
         "type": "stdio",
         "command": "python",
         "args": ["./domain_specific_mcp_server.py"]
       }
     }
   }
   ```

## API Documentation

### MCP Tools

BrandNexus provides these tools through the MCP protocol:

#### `index_documents()`
Scans and indexes all documents in configured directories.

**Returns:**
```json
{
  "indexed": 42,
  "updated": 5,
  "errors": [],
  "document_types": {
    "strategy": 12,
    "brand_guideline": 8,
    "messaging_template": 22
  }
}
```

#### `search_documents(query, document_type?, category?, limit?)`
Searches documents by content, title, or metadata.

**Parameters:**
- `query` (string): Search terms
- `document_type` (optional): Filter by document type
- `category` (optional): Filter by category
- `limit` (optional): Maximum results (default: 10)

**Example:**
```python
search_documents("brand voice", document_type="brand_guideline", limit=5)
```

#### `get_document_content(path)`
Retrieves the full content of a specific document.

#### `get_messaging_templates(category?)`
Returns available messaging templates, optionally filtered by category.

#### `get_brand_guidelines(section?)`
Retrieves brand guidelines, optionally filtered by section.

#### `analyze_document_relationships()`
Analyzes relationships and dependencies between documents.

### MCP Resources

Access documents through structured URI patterns:

- `strategy://document/{doc_id}` - Strategy document access
- `brand://guidelines/{section}` - Brand guideline sections  
- `templates://messaging/{template_type}` - Messaging templates

### Direct API Usage

For programmatic access:

```python
from domain_specific_mcp_server import mcp

# Search documents
results = mcp.search_documents("brand voice", document_type="brand_guideline")

# Get specific content
content = mcp.get_document_content("/brand/brand-voice.md")

# Get templates
templates = mcp.get_messaging_templates(category="email")
```

## Advanced Features

### Machine Learning Classification

Enable ML-powered document classification:

```bash
# Install ML dependencies
pip install scikit-learn

# Set environment variable
export ENABLE_ML_CLASSIFICATION=true

# Train classifier (requires at least 10 classified documents)
python -c "
from domain_specific_mcp_server import mcp
result = mcp.train_document_classifier()
print(result)
"
```

### Semantic Search

Enable vector-based semantic search:

```bash
# Install semantic search dependencies
pip install sentence-transformers faiss-cpu

# Enable in configuration
export ENABLE_SEMANTIC_SEARCH=true
```

### Real-time Monitoring

Enable automatic reindexing when files change:

```bash
# Install file monitoring dependencies
pip install watchdog

# Enable in configuration
export AUTO_REINDEX=true
```

### Performance Optimization

For large document sets:

```bash
# Enable caching
export CACHE_TTL=600  # 10 minutes

# Increase search limits
export MAX_SEARCH_RESULTS=50

# Use background processing
export BACKGROUND_INDEXING=true
```

## Troubleshooting

### Common Issues

#### "Permission denied" errors
```bash
# Ensure read access to document directories
chmod -R 755 ./strategy/ ./brand/ ./messaging/
```

#### "Database is locked" errors
```bash
# Close any other connections to the database
# Restart the MCP server
python domain_specific_mcp_server.py
```

#### "Module not found" errors
```bash
# Reinstall dependencies
pip install --upgrade fastmcp sqlite3 pathlib pyyaml
```

#### Large files not processing
```bash
# Check file size limits and encoding
# For files >10MB, enable streaming processing
export ENABLE_STREAMING=true
```

### Debug Mode

Enable detailed logging:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
python domain_specific_mcp_server.py
```

### Health Check

Verify server status:

```python
from domain_specific_mcp_server import mcp
health = mcp.diagnose_server_health()
print(health)
```

### Getting Help

1. **Check the logs**: Look in `mcp_server.log` for error details
2. **Verify configuration**: Ensure paths and permissions are correct
3. **Test with sample documents**: Use the provided sample files
4. **Check client configuration**: Verify MCP client setup

## Contributing

We welcome contributions to BrandNexus! Here's how to get started:

### Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/brandnexus.git
   cd brandnexus
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Run tests**:
   ```bash
   python -m pytest tests/
   ```

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings for all public functions
- Include unit tests for new features

### Pull Request Process

1. Create a feature branch: `git checkout -b feature/amazing-feature`
2. Make your changes and add tests
3. Run the test suite: `pytest`
4. Commit your changes: `git commit -m "Add amazing feature"`
5. Push to your fork: `git push origin feature/amazing-feature`
6. Open a Pull Request

### Areas for Contribution

- **New document types**: Add support for additional file formats
- **Enhanced classification**: Improve ML classification algorithms
- **Performance optimizations**: Optimize indexing and search performance
- **Security features**: Add authentication and authorization
- **Documentation**: Improve guides and examples
- **Testing**: Expand test coverage

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

## Support

### Community Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/yourusername/brandnexus/issues)
- **Discussions**: [Join community discussions](https://github.com/yourusername/brandnexus/discussions)
- **Documentation**: [Comprehensive guides](docs/)

### Professional Support

For enterprise deployments and professional support:

- **Email**: support@brandnexus.dev
- **Enterprise**: enterprise@brandnexus.dev
- **Consulting**: consulting@brandnexus.dev

### Resources

- **FastMCP Documentation**: [FastMCP Docs](https://fastmcp.dev)
- **MCP Protocol**: [Model Context Protocol](https://modelcontextprotocol.io)
- **Anthropic Claude**: [Claude AI](https://claude.ai)

---

## Acknowledgments

- **Anthropic** for the Model Context Protocol specification
- **FastMCP** for the excellent MCP server framework
- **Contributors** who help make BrandNexus better

## Roadmap

### Version 2.0 (Planned)
- **Multi-language support**: International document processing
- **Advanced analytics**: Content performance insights
- **Collaboration features**: Team workflows and permissions
- **Cloud deployment**: Hosted service options

### Version 2.1 (Future)
- **AI-powered summarization**: Automatic document summaries
- **Version control integration**: Git-based document tracking
- **Advanced visualizations**: Interactive document maps
- **API marketplace**: Third-party integrations

---

**Made with ❤️ by the BrandNexus team**

*BrandNexus - Connecting your knowledge to AI-powered workflows*

</readme>

