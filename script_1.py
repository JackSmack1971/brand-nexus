# Create a configuration guide and deployment script for the MCP server

config_guide = """
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
"""

# Save the configuration guide
with open("MCP_SERVER_CONFIG_GUIDE.md", "w") as f:
    f.write(config_guide)

# Create a deployment script
deployment_script = """#!/bin/bash
# MCP Server Deployment Script

set -e

echo "🚀 Deploying Domain-Specific MCP Server..."

# Check prerequisites
echo "📋 Checking prerequisites..."
python3 --version || { echo "Python 3 required"; exit 1; }

# Install dependencies
echo "📦 Installing dependencies..."
pip install fastmcp pathlib pyyaml sqlite3

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p {strategy,brand,messaging,templates,guidelines}

# Set up configuration
echo "⚙️  Setting up configuration..."
cat > .env << EOF
DOCUMENT_PATHS=./strategy/,./brand/,./messaging/,./templates/,./guidelines/
DATABASE_PATH=document_index.db
AUTO_REINDEX=true
DEBUG=false
EOF

# Initialize database
echo "🗃️  Initializing database..."
python3 -c "
from domain_specific_mcp_server import DocumentIndexer
indexer = DocumentIndexer(['./strategy/', './brand/', './messaging/'])
print('Database initialized successfully')
"

# Create sample documents
echo "📄 Creating sample documents..."
cat > strategy/sample-strategy.md << EOF
---
title: "Sample Strategy Document"
category: "corporate-strategy"
tags: ["strategy", "planning", "2025"]
---

# Sample Strategy Document

This is a sample strategy document for testing the MCP server.

## Objectives
- Increase market share
- Improve customer satisfaction
- Expand product line
EOF

cat > brand/sample-brand-guide.md << EOF
---
title: "Brand Guidelines"
category: "visual-identity"
tags: ["brand", "guidelines", "logo"]
---

# Brand Guidelines

## Logo Usage
- Use primary logo on white backgrounds
- Maintain clear space equal to logo height
- Never distort or modify the logo

## Color Palette
- Primary: #1F2937
- Secondary: #3B82F6
- Accent: #10B981
EOF

cat > messaging/sample-template.md << EOF
---
title: "Email Template - Product Launch"
category: "email"
tags: ["template", "product-launch", "email"]
---

# Product Launch Email Template

Subject: Introducing [Product Name] - Revolutionary [Category]

Dear [Customer Name],

We're excited to introduce [Product Name], our latest innovation in [category].

Key benefits:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

[CTA Button]

Best regards,
[Team Name]
EOF

echo "🔄 Running initial indexing..."
python3 domain_specific_mcp_server.py --mode index || echo "Manual indexing may be required"

echo "✅ Deployment complete!"
echo ""
echo "📖 Next steps:"
echo "1. Configure your MCP client (Cursor, Claude Desktop, etc.)"
echo "2. Add your actual documents to the created directories"
echo "3. Run manual indexing if needed"
echo ""
echo "🔧 Configuration files created:"
echo "- .env (environment variables)"
echo "- Sample documents in strategy/, brand/, messaging/"
echo ""
echo "📚 Documentation:"
echo "- See MCP_SERVER_CONFIG_GUIDE.md for detailed configuration"
echo "- Check domain_specific_mcp_server.py for customization options"
"""

with open("deploy_mcp_server.sh", "w") as f:
    f.write(deployment_script)

# Make deployment script executable
import os
import stat
os.chmod("deploy_mcp_server.sh", stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

print("✅ Configuration guide and deployment script created!")
print("\n📋 Files created:")
print("- MCP_SERVER_CONFIG_GUIDE.md (detailed configuration guide)")
print("- deploy_mcp_server.sh (automated deployment script)")
print("\n🚀 Quick start:")
print("1. Run: chmod +x deploy_mcp_server.sh && ./deploy_mcp_server.sh")
print("2. Configure your MCP client (Cursor/Claude Desktop)")
print("3. Start using: 'Index all documents' or 'Search for strategy docs'")