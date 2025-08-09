# Create a comprehensive implementation template for a domain-specific MCP server
# that indexes strategy, brand documents, and messaging templates

implementation_template = """
# Domain-Specific MCP Server Implementation Template
# For indexing /strategy/, brand documents, and messaging templates

from fastmcp import FastMCP
from pathlib import Path
import json
import yaml
import sqlite3
from typing import Dict, List, Optional, Any
import hashlib
import datetime
import os
import re
from dataclasses import dataclass
from enum import Enum

@dataclass
class DocumentMetadata:
    path: str
    title: str
    document_type: str
    category: str
    last_modified: datetime.datetime
    content_hash: str
    tags: List[str]
    summary: str
    word_count: int
    
class DocumentType(Enum):
    STRATEGY = "strategy"
    BRAND_GUIDELINE = "brand_guideline"
    MESSAGING_TEMPLATE = "messaging_template"
    POSITIONING = "positioning"
    CAMPAIGN_BRIEF = "campaign_brief"
    BRAND_VOICE = "brand_voice"

class DocumentIndexer:
    def __init__(self, base_paths: List[str], db_path: str = "document_index.db"):
        self.base_paths = base_paths
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                path TEXT UNIQUE,
                title TEXT,
                document_type TEXT,
                category TEXT,
                last_modified TIMESTAMP,
                content_hash TEXT,
                tags TEXT,
                summary TEXT,
                word_count INTEGER,
                full_text TEXT
            )
        ''')
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_document_type ON documents(document_type)
        ''')
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_category ON documents(category)
        ''')
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_tags ON documents(tags)
        ''')
        conn.commit()
        conn.close()

# Initialize the MCP server
mcp = FastMCP(
    name="Strategy & Brand Document Server",
    instructions=\"\"\"
    This server provides access to organizational strategy documents, brand guidelines,
    and messaging templates. It can search, retrieve, and analyze strategic content
    to help maintain brand consistency and strategic alignment.
    \"\"\"
)

# Configuration
DOCUMENT_PATHS = [
    "/strategy/",
    "/brand/",
    "/messaging/",
    "/templates/",
    "/guidelines/"
]

indexer = DocumentIndexer(DOCUMENT_PATHS)

@mcp.tool()
def index_documents() -> Dict[str, Any]:
    \"\"\"Scan and index all documents in configured directories.\"\"\"
    results = {
        "indexed": 0,
        "updated": 0,
        "errors": [],
        "document_types": {}
    }
    
    for base_path in DOCUMENT_PATHS:
        if not os.path.exists(base_path):
            results["errors"].append(f"Path does not exist: {base_path}")
            continue
            
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith(('.md', '.txt', '.docx', '.pdf', '.yaml', '.json')):
                    file_path = os.path.join(root, file)
                    try:
                        # Process and index the document
                        doc_type = classify_document(file_path)
                        results["indexed"] += 1
                        
                        if doc_type not in results["document_types"]:
                            results["document_types"][doc_type] = 0
                        results["document_types"][doc_type] += 1
                        
                    except Exception as e:
                        results["errors"].append(f"Error indexing {file_path}: {str(e)}")
    
    return results

@mcp.tool()
def search_documents(
    query: str,
    document_type: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    \"\"\"Search documents by content, title, or metadata.\"\"\"
    conn = sqlite3.connect(indexer.db_path)
    
    sql = \"\"\"
        SELECT path, title, document_type, category, summary, tags
        FROM documents 
        WHERE (full_text LIKE ? OR title LIKE ? OR summary LIKE ?)
    \"\"\"
    params = [f'%{query}%', f'%{query}%', f'%{query}%']
    
    if document_type:
        sql += " AND document_type = ?"
        params.append(document_type)
    
    if category:
        sql += " AND category = ?"
        params.append(category)
    
    sql += f" LIMIT {limit}"
    
    cursor = conn.execute(sql, params)
    results = []
    
    for row in cursor.fetchall():
        results.append({
            "path": row[0],
            "title": row[1],
            "document_type": row[2],
            "category": row[3],
            "summary": row[4],
            "tags": row[5].split(',') if row[5] else []
        })
    
    conn.close()
    return results

@mcp.tool()
def get_document_content(path: str) -> Dict[str, Any]:
    \"\"\"Retrieve full content of a specific document.\"\"\"
    if not os.path.exists(path):
        return {"error": f"Document not found: {path}"}
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "path": path,
            "content": content,
            "size": len(content),
            "last_modified": datetime.datetime.fromtimestamp(
                os.path.getmtime(path)
            ).isoformat()
        }
    except Exception as e:
        return {"error": f"Error reading document: {str(e)}"}

@mcp.tool()
def get_messaging_templates(category: Optional[str] = None) -> List[Dict[str, Any]]:
    \"\"\"Retrieve available messaging templates, optionally filtered by category.\"\"\"
    conn = sqlite3.connect(indexer.db_path)
    
    sql = "SELECT path, title, category, summary FROM documents WHERE document_type = 'messaging_template'"
    params = []
    
    if category:
        sql += " AND category = ?"
        params.append(category)
    
    cursor = conn.execute(sql, params)
    templates = []
    
    for row in cursor.fetchall():
        templates.append({
            "path": row[0],
            "title": row[1],
            "category": row[2],
            "summary": row[3]
        })
    
    conn.close()
    return templates

@mcp.tool()
def get_brand_guidelines(section: Optional[str] = None) -> Dict[str, Any]:
    \"\"\"Retrieve brand guidelines, optionally filtered by section.\"\"\"
    conn = sqlite3.connect(indexer.db_path)
    
    sql = \"\"\"
        SELECT path, title, category, full_text 
        FROM documents 
        WHERE document_type = 'brand_guideline'
    \"\"\"
    params = []
    
    if section:
        sql += " AND (category = ? OR full_text LIKE ?)"
        params.extend([section, f'%{section}%'])
    
    cursor = conn.execute(sql, params)
    guidelines = []
    
    for row in cursor.fetchall():
        guidelines.append({
            "path": row[0],
            "title": row[1],
            "category": row[2],
            "content": row[3][:500] + "..." if len(row[3]) > 500 else row[3]
        })
    
    conn.close()
    return {"guidelines": guidelines}

@mcp.tool()
def analyze_document_relationships() -> Dict[str, Any]:
    \"\"\"Analyze relationships and dependencies between documents.\"\"\"
    conn = sqlite3.connect(indexer.db_path)
    
    # Get document cross-references
    cursor = conn.execute(\"\"\"
        SELECT document_type, COUNT(*) as count
        FROM documents
        GROUP BY document_type
    \"\"\")
    
    type_counts = dict(cursor.fetchall())
    
    # Find common tags across document types
    cursor = conn.execute("SELECT tags FROM documents WHERE tags != ''")
    all_tags = []
    for row in cursor.fetchall():
        all_tags.extend(row[0].split(','))
    
    tag_frequency = {}
    for tag in all_tags:
        tag = tag.strip()
        tag_frequency[tag] = tag_frequency.get(tag, 0) + 1
    
    conn.close()
    
    return {
        "document_type_distribution": type_counts,
        "common_tags": dict(sorted(tag_frequency.items(), key=lambda x: x[1], reverse=True)[:10]),
        "total_documents": sum(type_counts.values())
    }

@mcp.resource("strategy://document/{doc_id}")
def get_strategy_document(doc_id: str) -> str:
    \"\"\"Retrieve a strategy document by ID.\"\"\"
    conn = sqlite3.connect(indexer.db_path)
    cursor = conn.execute(
        "SELECT full_text FROM documents WHERE id = ? AND document_type = 'strategy'",
        [doc_id]
    )
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return "Document not found"

@mcp.resource("brand://guidelines/{section}")
def get_brand_section(section: str) -> str:
    \"\"\"Retrieve brand guidelines for a specific section.\"\"\"
    conn = sqlite3.connect(indexer.db_path)
    cursor = conn.execute(
        \"\"\"SELECT full_text FROM documents 
           WHERE document_type = 'brand_guideline' 
           AND (category = ? OR full_text LIKE ?)\"\"\",
        [section, f'%{section}%']
    )
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return f"Brand guidelines for '{section}' not found"

@mcp.resource("templates://messaging/{template_type}")
def get_messaging_template(template_type: str) -> str:
    \"\"\"Retrieve a messaging template by type.\"\"\"
    conn = sqlite3.connect(indexer.db_path)
    cursor = conn.execute(
        \"\"\"SELECT full_text FROM documents 
           WHERE document_type = 'messaging_template' 
           AND category = ?\"\"\",
        [template_type]
    )
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return f"Messaging template for '{template_type}' not found"

def classify_document(file_path: str) -> str:
    \"\"\"Classify document type based on path and content.\"\"\"
    path_lower = file_path.lower()
    
    if '/strategy/' in path_lower or 'strategy' in path_lower:
        return DocumentType.STRATEGY.value
    elif '/brand/' in path_lower or 'brand' in path_lower:
        return DocumentType.BRAND_GUIDELINE.value
    elif '/messaging/' in path_lower or 'template' in path_lower:
        return DocumentType.MESSAGING_TEMPLATE.value
    elif 'positioning' in path_lower:
        return DocumentType.POSITIONING.value
    elif 'campaign' in path_lower:
        return DocumentType.CAMPAIGN_BRIEF.value
    elif 'voice' in path_lower:
        return DocumentType.BRAND_VOICE.value
    else:
        return "unknown"

if __name__ == "__main__":
    mcp.run(transport="stdio")
"""

# Save the implementation template
with open("domain_specific_mcp_server.py", "w") as f:
    f.write(implementation_template)

print("✅ Domain-specific MCP server implementation template created!")
print("📁 File: domain_specific_mcp_server.py")
print("\n📋 Key features included:")
print("- Document indexing with SQLite backend")
print("- Full-text search capabilities")
print("- Strategy, brand, and messaging document classification")
print("- Resource URIs for structured access")
print("- Relationship analysis tools")
print("- Configurable document paths")
print("- FastMCP integration")