
# MCP Server Configuration Guide
# Domain-Specific Document Indexing Server

## 1. Installation & Setup

### Prerequisites
```bash
pip install fastmcp sqlite3 pathlib pyyaml
# Optional: For enhanced document processing
pip install python-docx PyPDF2 markdown
```

### Directory Structure
```
/your-project/
├── strategy/
│   ├── company-strategy-2025.md
│   ├── product-roadmap.md
│   └── market-analysis.pdf
├── brand/
│   ├── brand-guidelines.md
│   ├── logo-usage.md
│   └── color-palette.yaml
├── messaging/
│   ├── email-templates/
│   ├── social-media-templates/
│   └── press-release-templates/
└── domain_specific_mcp_server.py
```

## 2. Configuration Options

### Basic Configuration (.env file)
```env
# Document paths (comma-separated)
DOCUMENT_PATHS=/strategy/,/brand/,/messaging/,/templates/,/guidelines/

# Database configuration
DATABASE_PATH=document_index.db

# Server settings
SERVER_NAME=Strategy & Brand Document Server
LOG_LEVEL=INFO

# Indexing settings
AUTO_REINDEX=true
REINDEX_INTERVAL=3600  # seconds

# Search configuration
DEFAULT_SEARCH_LIMIT=10
ENABLE_FULL_TEXT_SEARCH=true
```

### Advanced Configuration (config.yaml)
```yaml
server:
  name: "Strategy & Brand Document Server"
  version: "1.0.0"
  description: "Domain-specific MCP server for strategic documents"

paths:
  strategy: "/strategy/"
  brand: "/brand/"
  messaging: "/messaging/"
  templates: "/templates/"
  guidelines: "/guidelines/"

indexing:
  supported_extensions:
    - .md
    - .txt
    - .docx
    - .pdf
    - .yaml
    - .json
  exclude_patterns:
    - "*.tmp"
    - ".*"
    - "__pycache__"
  auto_reindex: true
  index_metadata: true
  extract_tags: true

classification:
  rules:
    strategy:
      path_patterns: ["/strategy/", "strategy"]
      keywords: ["roadmap", "objectives", "goals"]
    brand:
      path_patterns: ["/brand/", "brand"]
      keywords: ["guidelines", "identity", "voice"]
    messaging:
      path_patterns: ["/messaging/", "template"]
      keywords: ["template", "copy", "message"]

search:
  enable_fuzzy: true
  enable_semantic: false  # Requires embedding model
  default_limit: 10
  highlight_results: true
```

## 3. Client Configuration Files

### Cursor IDE (.cursor/mcp.json)
```json
{
  "mcpServers": {
    "strategy-docs": {
      "command": "python",
      "args": ["/path/to/domain_specific_mcp_server.py"],
      "env": {
        "DOCUMENT_PATHS": "/strategy/,/brand/,/messaging/"
      }
    }
  }
}
```

### Claude Desktop (claude_desktop_config.json)
```json
{
  "mcpServers": {
    "strategy-brand-server": {
      "command": "python3",
      "args": ["/absolute/path/to/domain_specific_mcp_server.py"],
      "env": {
        "DATABASE_PATH": "/path/to/document_index.db"
      }
    }
  }
}
```

### VS Code (.vscode/mcp.json)
```json
{
  "servers": {
    "strategy-docs": {
      "type": "stdio",
      "command": "python",
      "args": ["/workspace/domain_specific_mcp_server.py"]
    }
  }
}
```

## 4. Usage Examples

### Initial Setup
1. Place server file in your document root
2. Configure paths in environment or config file
3. Run initial indexing:
   ```bash
   python domain_specific_mcp_server.py --index
   ```

### Integration Commands
Once configured in your MCP client:

- "Index all strategy documents"
- "Search for messaging templates related to product launch"
- "Show me brand guidelines for logo usage"
- "Find all documents mentioning 'customer acquisition'"
- "Get the latest strategy document"
- "Analyze relationships between brand and messaging docs"

### API Usage
```python
# Direct server usage
from domain_specific_mcp_server import mcp

# Search documents
results = mcp.search_documents("brand voice", document_type="brand_guideline")

# Get specific content
content = mcp.get_document_content("/brand/brand-voice.md")

# Get templates
templates = mcp.get_messaging_templates(category="email")
```

## 5. Customization Options

### Custom Document Types
Add new document types by extending the DocumentType enum:
```python
class DocumentType(Enum):
    STRATEGY = "strategy"
    BRAND_GUIDELINE = "brand_guideline"
    MESSAGING_TEMPLATE = "messaging_template"
    # Add custom types
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    MARKET_RESEARCH = "market_research"
    CREATIVE_BRIEF = "creative_brief"
```

### Custom Classification Rules
Modify the classify_document function:
```python
def classify_document(file_path: str) -> str:
    path_lower = file_path.lower()
    filename = os.path.basename(path_lower)

    # Custom rules
    if 'competitive' in path_lower or 'competitor' in filename:
        return DocumentType.COMPETITIVE_ANALYSIS.value
    elif 'market' in path_lower and 'research' in path_lower:
        return DocumentType.MARKET_RESEARCH.value
    # ... existing rules
```

### Enhanced Metadata Extraction
```python
def extract_metadata(file_path: str) -> Dict[str, Any]:
    metadata = {}

    with open(file_path, 'r') as f:
        content = f.read()

    # Extract frontmatter
    if content.startswith('---'):
        try:
            _, frontmatter, _ = content.split('---', 2)
            metadata.update(yaml.safe_load(frontmatter))
        except:
            pass

    # Extract hashtags
    hashtags = re.findall(r'#(\w+)', content)
    metadata['tags'] = hashtags

    # Extract mentions
    mentions = re.findall(r'@(\w+)', content)
    metadata['mentions'] = mentions

    return metadata
```

## 6. Monitoring & Maintenance

### Health Check Endpoint
```python
@mcp.tool()
def health_check() -> Dict[str, Any]:
    conn = sqlite3.connect(indexer.db_path)
    cursor = conn.execute("SELECT COUNT(*) FROM documents")
    doc_count = cursor.fetchone()[0]

    return {
        "status": "healthy",
        "document_count": doc_count,
        "database_size": os.path.getsize(indexer.db_path),
        "last_index_update": get_last_index_time()
    }
```

### Automated Reindexing
```python
import schedule
import time

def auto_reindex():
    if os.getenv('AUTO_REINDEX', 'false').lower() == 'true':
        schedule.every(1).hour.do(index_documents)

        while True:
            schedule.run_pending()
            time.sleep(60)
```

## 7. Troubleshooting

### Common Issues
- **Permission errors**: Ensure read access to document directories
- **Database locks**: Use connection pooling for concurrent access
- **Large files**: Implement streaming for documents >10MB
- **Encoding issues**: Use UTF-8 encoding detection

### Debug Mode
Set environment variable `DEBUG=true` for verbose logging:
```python
import logging
if os.getenv('DEBUG'):
    logging.basicConfig(level=logging.DEBUG)
```
