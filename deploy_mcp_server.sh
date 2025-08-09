#!/bin/bash
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
