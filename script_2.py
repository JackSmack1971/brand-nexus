# Create comprehensive implementation examples and best practices

examples_and_practices = """
# MCP Server Implementation Examples and Best Practices

## Advanced Implementation Examples

### 1. Enhanced Document Classification with ML
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

class MLDocumentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.classifier = MultinomialNB()
        self.is_trained = False
        
    def train_classifier(self, documents, labels):
        \"\"\"Train the ML classifier on existing documents.\"\"\"
        X = self.vectorizer.fit_transform(documents)
        self.classifier.fit(X, labels)
        self.is_trained = True
        
    def predict_document_type(self, content: str) -> str:
        \"\"\"Predict document type using ML.\"\"\"
        if not self.is_trained:
            return self.rule_based_classification(content)
            
        X = self.vectorizer.transform([content])
        prediction = self.classifier.predict(X)[0]
        confidence = max(self.classifier.predict_proba(X)[0])
        
        # Fall back to rule-based if confidence is low
        if confidence < 0.7:
            return self.rule_based_classification(content)
            
        return prediction
        
    def rule_based_classification(self, content: str) -> str:
        \"\"\"Fallback rule-based classification.\"\"\"
        content_lower = content.lower()
        
        strategy_keywords = ['roadmap', 'objectives', 'goals', 'strategy', 'vision']
        brand_keywords = ['brand', 'logo', 'identity', 'guidelines', 'voice']
        messaging_keywords = ['template', 'copy', 'message', 'campaign']
        
        if any(keyword in content_lower for keyword in strategy_keywords):
            return DocumentType.STRATEGY.value
        elif any(keyword in content_lower for keyword in brand_keywords):
            return DocumentType.BRAND_GUIDELINE.value
        elif any(keyword in content_lower for keyword in messaging_keywords):
            return DocumentType.MESSAGING_TEMPLATE.value
        
        return "unknown"

# Enhanced server with ML classification
@mcp.tool()
def train_document_classifier() -> Dict[str, Any]:
    \"\"\"Train ML classifier on existing documents.\"\"\"
    conn = sqlite3.connect(indexer.db_path)
    cursor = conn.execute("SELECT full_text, document_type FROM documents WHERE document_type != 'unknown'")
    
    documents = []
    labels = []
    
    for row in cursor.fetchall():
        documents.append(row[0])
        labels.append(row[1])
    
    if len(documents) < 10:
        return {"error": "Need at least 10 classified documents to train"}
    
    classifier = MLDocumentClassifier()
    classifier.train_classifier(documents, labels)
    
    # Save trained model
    with open('document_classifier.pkl', 'wb') as f:
        pickle.dump(classifier, f)
    
    conn.close()
    return {"message": f"Classifier trained on {len(documents)} documents", "accuracy": "run_validation_needed"}
```

### 2. Semantic Search with Embeddings
```python
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class SemanticSearchEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.document_embeddings = {}
        
    def build_index(self, documents: Dict[str, str]):
        \"\"\"Build FAISS index for semantic search.\"\"\"
        texts = list(documents.values())
        doc_ids = list(documents.keys())
        
        embeddings = self.model.encode(texts)
        dimension = embeddings.shape[1]
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings.astype('float32'))
        
        # Store mapping
        self.document_embeddings = dict(zip(doc_ids, embeddings))
        
    def semantic_search(self, query: str, k: int = 10) -> List[Tuple[str, float]]:
        \"\"\"Perform semantic search.\"\"\"
        if self.index is None:
            return []
            
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        scores, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            doc_id = list(self.document_embeddings.keys())[idx]
            results.append((doc_id, float(score)))
            
        return results

# Enhanced search with semantic capabilities
@mcp.tool()
def semantic_document_search(
    query: str,
    document_type: Optional[str] = None,
    limit: int = 10,
    semantic_weight: float = 0.7
) -> List[Dict[str, Any]]:
    \"\"\"Hybrid search combining keyword and semantic search.\"\"\"
    
    # Load or build semantic index
    semantic_engine = SemanticSearchEngine()
    
    # Get all documents for semantic search
    conn = sqlite3.connect(indexer.db_path)
    cursor = conn.execute("SELECT id, full_text FROM documents")
    documents = {str(row[0]): row[1] for row in cursor.fetchall()}
    
    # Build semantic index if not exists
    semantic_engine.build_index(documents)
    
    # Perform semantic search
    semantic_results = semantic_engine.semantic_search(query, limit * 2)
    
    # Perform keyword search
    keyword_results = search_documents(query, document_type, limit * 2)
    
    # Combine results with weights
    combined_scores = {}
    
    # Add semantic scores
    for doc_id, score in semantic_results:
        combined_scores[doc_id] = semantic_weight * score
    
    # Add keyword scores (binary for now, could be TF-IDF)
    for result in keyword_results:
        doc_path = result['path']
        doc_id = get_doc_id_by_path(doc_path)  # Helper function needed
        
        if doc_id in combined_scores:
            combined_scores[doc_id] += (1 - semantic_weight)
        else:
            combined_scores[doc_id] = (1 - semantic_weight)
    
    # Sort by combined score and return top results
    sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    final_results = []
    for doc_id, score in sorted_results:
        # Get document details
        cursor = conn.execute("SELECT path, title, document_type, summary FROM documents WHERE id = ?", [doc_id])
        row = cursor.fetchone()
        if row:
            final_results.append({
                "path": row[0],
                "title": row[1],
                "document_type": row[2],
                "summary": row[3],
                "relevance_score": score
            })
    
    conn.close()
    return final_results
```

### 3. Real-time Document Monitoring
```python
import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

class DocumentWatcher(FileSystemEventHandler):
    def __init__(self, indexer: DocumentIndexer):
        self.indexer = indexer
        self.processing_queue = []
        
    def on_modified(self, event):
        if not event.is_directory and self.is_supported_file(event.src_path):
            self.queue_for_reindexing(event.src_path)
    
    def on_created(self, event):
        if not event.is_directory and self.is_supported_file(event.src_path):
            self.queue_for_reindexing(event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.remove_from_index(event.src_path)
    
    def is_supported_file(self, path: str) -> bool:
        return path.endswith(('.md', '.txt', '.docx', '.pdf', '.yaml', '.json'))
    
    def queue_for_reindexing(self, path: str):
        \"\"\"Queue file for background reindexing.\"\"\"
        if path not in self.processing_queue:
            self.processing_queue.append(path)
            threading.Thread(target=self.process_file, args=(path,), daemon=True).start()
    
    def process_file(self, path: str):
        \"\"\"Process file in background.\"\"\"
        try:
            time.sleep(1)  # Brief delay to ensure file write is complete
            self.indexer.index_single_file(path)
            if path in self.processing_queue:
                self.processing_queue.remove(path)
        except Exception as e:
            print(f"Error processing {path}: {e}")

# Start file system monitoring
def start_document_monitoring():
    \"\"\"Start monitoring document directories for changes.\"\"\"
    observer = Observer()
    event_handler = DocumentWatcher(indexer)
    
    for path in DOCUMENT_PATHS:
        if os.path.exists(path):
            observer.schedule(event_handler, path, recursive=True)
    
    observer.start()
    return observer

@mcp.tool()
def get_monitoring_status() -> Dict[str, Any]:
    \"\"\"Get status of document monitoring system.\"\"\"
    # This would need to track the observer state
    return {
        "status": "active",
        "monitored_paths": DOCUMENT_PATHS,
        "pending_updates": len(getattr(document_watcher, 'processing_queue', [])),
        "last_update": datetime.datetime.now().isoformat()
    }
```

### 4. Advanced Resource Templates
```python
# Dynamic resource templates with complex parameters
@mcp.resource("strategy://analysis/{time_period}/{focus_area}")
def get_strategic_analysis(time_period: str, focus_area: str) -> str:
    \"\"\"Get strategic analysis for a specific time period and focus area.\"\"\"
    conn = sqlite3.connect(indexer.db_path)
    
    # Complex query based on parameters
    query = \"\"\"
        SELECT d.full_text, d.title, d.last_modified
        FROM documents d
        WHERE d.document_type = 'strategy'
        AND (d.full_text LIKE ? OR d.title LIKE ?)
        AND d.last_modified >= ?
        ORDER BY d.last_modified DESC
    \"\"\"
    
    # Parse time period
    start_date = parse_time_period(time_period)
    focus_pattern = f'%{focus_area}%'
    
    cursor = conn.execute(query, [focus_pattern, focus_pattern, start_date])
    results = cursor.fetchall()
    
    if not results:
        return f"No strategic analysis found for {focus_area} in {time_period}"
    
    # Compile comprehensive analysis
    analysis = f"# Strategic Analysis: {focus_area} ({time_period})\\n\\n"
    
    for text, title, modified in results:
        analysis += f"## {title}\\n"
        analysis += f"*Last updated: {modified}*\\n\\n"
        analysis += extract_relevant_sections(text, focus_area)
        analysis += "\\n---\\n\\n"
    
    conn.close()
    return analysis

@mcp.resource("brand://compliance/{guideline_type}")
def check_brand_compliance(guideline_type: str) -> str:
    \"\"\"Check compliance status for specific brand guidelines.\"\"\"
    conn = sqlite3.connect(indexer.db_path)
    
    # Get guideline document
    cursor = conn.execute(
        \"\"\"SELECT full_text FROM documents 
           WHERE document_type = 'brand_guideline' 
           AND (category = ? OR full_text LIKE ?)\"\"\",
        [guideline_type, f'%{guideline_type}%']
    )
    
    guideline = cursor.fetchone()
    if not guideline:
        return f"No brand guidelines found for {guideline_type}"
    
    # Analyze compliance across other documents
    compliance_report = analyze_brand_compliance(guideline[0], guideline_type)
    
    conn.close()
    return compliance_report

@mcp.resource("templates://generate/{template_type}/{context}")
def generate_contextual_template(template_type: str, context: str) -> str:
    \"\"\"Generate a contextual template based on existing templates and context.\"\"\"
    # Find similar templates
    similar_templates = find_similar_templates(template_type)
    
    if not similar_templates:
        return f"No templates found for {template_type}"
    
    # Generate contextual adaptation
    generated_template = adapt_template_to_context(similar_templates, context)
    
    return generated_template
```

## Best Practices for Production Deployment

### 1. Security Considerations
```python
import hashlib
import jwt
from functools import wraps

class SecurityManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.allowed_paths = set()
    
    def validate_path(self, path: str) -> bool:
        \"\"\"Validate that path is within allowed directories.\"\"\"
        real_path = os.path.realpath(path)
        return any(real_path.startswith(allowed) for allowed in self.allowed_paths)
    
    def generate_token(self, user_id: str) -> str:
        \"\"\"Generate JWT token for authenticated access.\"\"\"
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def validate_token(self, token: str) -> Optional[str]:
        \"\"\"Validate JWT token and return user_id.\"\"\"
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

def require_auth(func):
    \"\"\"Decorator to require authentication for MCP tools.\"\"\"
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check for authentication in environment or context
        token = os.getenv('MCP_AUTH_TOKEN')
        if token and security_manager.validate_token(token):
            return func(*args, **kwargs)
        return {"error": "Authentication required"}
    return wrapper

# Apply security to sensitive operations
@mcp.tool()
@require_auth
def delete_document(path: str) -> Dict[str, Any]:
    \"\"\"Delete a document (requires authentication).\"\"\"
    if not security_manager.validate_path(path):
        return {"error": "Access denied"}
    
    try:
        os.remove(path)
        # Remove from index
        conn = sqlite3.connect(indexer.db_path)
        conn.execute("DELETE FROM documents WHERE path = ?", [path])
        conn.commit()
        conn.close()
        
        return {"message": f"Document {path} deleted successfully"}
    except Exception as e:
        return {"error": f"Failed to delete document: {str(e)}"}
```

### 2. Performance Optimization
```python
import functools
import threading
from concurrent.futures import ThreadPoolExecutor
import redis  # Optional: for distributed caching

class PerformanceOptimizer:
    def __init__(self):
        self.cache = {}
        self.cache_lock = threading.RLock()
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    def cached(self, ttl: int = 300):
        \"\"\"Decorator for caching function results.\"\"\"
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
                
                with self.cache_lock:
                    if cache_key in self.cache:
                        result, timestamp = self.cache[cache_key]
                        if time.time() - timestamp < ttl:
                            return result
                
                result = func(*args, **kwargs)
                
                with self.cache_lock:
                    self.cache[cache_key] = (result, time.time())
                
                return result
            return wrapper
        return decorator
    
    def background_task(self, func):
        \"\"\"Decorator to run function in background.\"\"\"
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            future = self.executor.submit(func, *args, **kwargs)
            return {"message": "Task started", "task_id": id(future)}
        return wrapper

optimizer = PerformanceOptimizer()

# Apply performance optimizations
@mcp.tool()
@optimizer.cached(ttl=600)  # Cache for 10 minutes
def get_document_statistics() -> Dict[str, Any]:
    \"\"\"Get comprehensive document statistics (cached).\"\"\"
    conn = sqlite3.connect(indexer.db_path)
    
    stats = {}
    
    # Document type distribution
    cursor = conn.execute("SELECT document_type, COUNT(*) FROM documents GROUP BY document_type")
    stats['type_distribution'] = dict(cursor.fetchall())
    
    # Recent activity
    cursor = conn.execute(
        "SELECT COUNT(*) FROM documents WHERE last_modified > datetime('now', '-7 days')"
    )
    stats['recent_updates'] = cursor.fetchone()[0]
    
    # Content statistics
    cursor = conn.execute("SELECT AVG(word_count), SUM(word_count) FROM documents")
    avg_words, total_words = cursor.fetchone()
    stats['content_stats'] = {
        'average_words': avg_words,
        'total_words': total_words
    }
    
    conn.close()
    return stats

@mcp.tool()
@optimizer.background_task
def rebuild_full_index() -> Dict[str, Any]:
    \"\"\"Rebuild the entire document index (background task).\"\"\"
    # This would run in background
    return index_documents()
```

### 3. Error Handling and Logging
```python
import logging
import traceback
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('MCP-DocumentServer')

def handle_errors(func):
    \"\"\"Decorator for consistent error handling.\"\"\"
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            logger.error(f"File not found in {func.__name__}: {e}")
            return {"error": f"File not found: {str(e)}"}
        except sqlite3.Error as e:
            logger.error(f"Database error in {func.__name__}: {e}")
            return {"error": f"Database error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            logger.error(traceback.format_exc())
            return {"error": f"Unexpected error: {str(e)}"}
    return wrapper

# Apply error handling to all tools
for tool_name in dir(mcp):
    if hasattr(mcp, tool_name) and callable(getattr(mcp, tool_name)):
        tool = getattr(mcp, tool_name)
        if hasattr(tool, '_is_mcp_tool'):  # Check if it's an MCP tool
            setattr(mcp, tool_name, handle_errors(tool))

@mcp.tool()
@handle_errors
def diagnose_server_health() -> Dict[str, Any]:
    \"\"\"Comprehensive server health diagnostic.\"\"\"
    health_report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "healthy",
        "issues": []
    }
    
    # Check database connection
    try:
        conn = sqlite3.connect(indexer.db_path)
        cursor = conn.execute("SELECT COUNT(*) FROM documents")
        doc_count = cursor.fetchone()[0]
        health_report["database"] = {"status": "healthy", "document_count": doc_count}
        conn.close()
    except Exception as e:
        health_report["database"] = {"status": "error", "error": str(e)}
        health_report["issues"].append("Database connection failed")
    
    # Check document paths
    for path in DOCUMENT_PATHS:
        if os.path.exists(path) and os.access(path, os.R_OK):
            health_report[f"path_{path}"] = {"status": "accessible"}
        else:
            health_report[f"path_{path}"] = {"status": "inaccessible"}
            health_report["issues"].append(f"Cannot access {path}")
    
    # Check disk space
    import shutil
    disk_usage = shutil.disk_usage("/")
    free_gb = disk_usage.free / (1024**3)
    if free_gb < 1:  # Less than 1GB free
        health_report["issues"].append("Low disk space")
        health_report["status"] = "warning"
    
    health_report["disk_space_gb"] = free_gb
    
    return health_report
```

### 4. Configuration Management
```python
import configparser
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ServerConfig:
    document_paths: List[str]
    database_path: str
    server_name: str
    log_level: str
    auto_reindex: bool
    reindex_interval: int
    max_search_results: int
    enable_semantic_search: bool
    enable_ml_classification: bool
    cache_ttl: int
    
    @classmethod
    def from_file(cls, config_path: str) -> 'ServerConfig':
        \"\"\"Load configuration from file.\"\"\"
        config = configparser.ConfigParser()
        config.read(config_path)
        
        return cls(
            document_paths=config.get('paths', 'document_paths', fallback='./strategy/,./brand/,./messaging/').split(','),
            database_path=config.get('database', 'path', fallback='document_index.db'),
            server_name=config.get('server', 'name', fallback='Strategy & Brand Document Server'),
            log_level=config.get('logging', 'level', fallback='INFO'),
            auto_reindex=config.getboolean('indexing', 'auto_reindex', fallback=True),
            reindex_interval=config.getint('indexing', 'reindex_interval', fallback=3600),
            max_search_results=config.getint('search', 'max_results', fallback=10),
            enable_semantic_search=config.getboolean('features', 'semantic_search', fallback=False),
            enable_ml_classification=config.getboolean('features', 'ml_classification', fallback=False),
            cache_ttl=config.getint('performance', 'cache_ttl', fallback=300)
        )
    
    @classmethod
    def from_env(cls) -> 'ServerConfig':
        \"\"\"Load configuration from environment variables.\"\"\"
        return cls(
            document_paths=os.getenv('DOCUMENT_PATHS', './strategy/,./brand/,./messaging/').split(','),
            database_path=os.getenv('DATABASE_PATH', 'document_index.db'),
            server_name=os.getenv('SERVER_NAME', 'Strategy & Brand Document Server'),
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            auto_reindex=os.getenv('AUTO_REINDEX', 'true').lower() == 'true',
            reindex_interval=int(os.getenv('REINDEX_INTERVAL', '3600')),
            max_search_results=int(os.getenv('MAX_SEARCH_RESULTS', '10')),
            enable_semantic_search=os.getenv('ENABLE_SEMANTIC_SEARCH', 'false').lower() == 'true',
            enable_ml_classification=os.getenv('ENABLE_ML_CLASSIFICATION', 'false').lower() == 'true',
            cache_ttl=int(os.getenv('CACHE_TTL', '300'))
        )

# Load configuration at startup
try:
    server_config = ServerConfig.from_file('config.ini')
except FileNotFoundError:
    server_config = ServerConfig.from_env()

# Apply configuration
logging.getLogger().setLevel(getattr(logging, server_config.log_level.upper()))
DOCUMENT_PATHS = server_config.document_paths
```

This comprehensive implementation provides:

1. **Machine Learning Integration**: Advanced document classification
2. **Semantic Search**: Vector-based similarity search
3. **Real-time Monitoring**: File system change detection
4. **Advanced Resource Templates**: Dynamic, parameterized resources
5. **Security**: Authentication and path validation
6. **Performance Optimization**: Caching and background processing
7. **Error Handling**: Comprehensive error management
8. **Configuration Management**: Flexible configuration options

These patterns ensure your MCP server is production-ready, scalable, and maintainable.
"""

# Save the advanced examples
with open("MCP_ADVANCED_EXAMPLES.md", "w") as f:
    f.write(examples_and_practices)

print("✅ Advanced implementation examples and best practices created!")
print("📁 File: MCP_ADVANCED_EXAMPLES.md")
print("\n🎯 Advanced features covered:")
print("- Machine Learning document classification")
print("- Semantic search with embeddings")
print("- Real-time file monitoring")
print("- Advanced resource templates")
print("- Security and authentication")
print("- Performance optimization")
print("- Error handling and logging")
print("- Configuration management")