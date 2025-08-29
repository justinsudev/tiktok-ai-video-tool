# Semantic Search Engine 🧠

> **AI-Powered Semantic Search Engine with Modern Web Interface**

Semantic Search Engine is a sophisticated search engine that combines traditional information retrieval techniques with cutting-edge AI-powered semantic understanding. Built with Python, Flask, and modern machine learning libraries, it delivers intelligent search results that understand user intent, not just keywords.

![Semantic Search Engine Demo](https://img.shields.io/badge/SemanticSearchEngine-v2.0-blue?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1+-green.svg?style=for-the-badge&logo=flask)
![PyTorch](https://img.shields.io/badge/PyTorch-2.5+-red.svg?style=for-the-badge&logo=pytorch)

## ✨ Features

### 🧠 **Intelligent Search Modes**
- **Traditional Search**: Fast TF-IDF + PageRank ranking for exact keyword matching
- **Semantic Search**: AI-powered understanding using sentence transformers
- **Hybrid Search**: Smart combination of both approaches for comprehensive results

### 🎨 **Modern User Experience**
- **Responsive Design**: Beautiful, professional interface that works on all devices
- **Interactive Controls**: Real-time PageRank weight adjustment and search mode selection
- **Visual Feedback**: Loading states, hover effects, and intuitive navigation
- **Neural Network Theme**: Inspired by AI and machine learning aesthetics

### ⚡ **Technical Excellence**
- **High Performance**: Optimized embeddings and efficient similarity computation
- **Scalable Architecture**: Designed for production deployment and high traffic
- **Robust Error Handling**: Graceful fallbacks and comprehensive error management
- **Memory Efficient**: Smart caching and batch processing for large document sets

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Interface │    │  Search Server   │    │  Index Server   │
│   (Flask + UI)  │◄──►│   (Flask API)    │◄──►│ (TF-IDF + AI)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   SQLite DB      │    │  Document       │
                       │  (Metadata)      │    │  Embeddings     │
                       └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **2GB+ RAM** (for AI models and embeddings)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/justinsudev/semantic-search-engine.git
   cd semantic-search-engine
   ```

2. **Set up semantic search capabilities**
   ```bash
   ./bin/setup_semantic
   ```
   This script will:
   - Install all required dependencies
   - Build the document database
   - Generate AI embeddings for semantic search
   - Initialize the search engine

3. **Start the search engine**
   ```bash
   # Start index servers (in separate terminals)
   ./bin/index start
   
   # Start the web interface
   ./bin/search start
   ```

4. **Open your browser**
   Navigate to [http://localhost:8000](http://localhost:8000)

## 🔍 How to Use

### **Search Modes Explained**

#### Traditional Search
- **Best for**: Exact keywords, technical terms, specific names
- **Example**: "tensorflow machine learning"
- **How it works**: Fast keyword matching using TF-IDF scoring

#### Semantic Search
- **Best for**: Natural language, conceptual queries, meaning-based search
- **Example**: "How does artificial intelligence work?"
- **How it works**: AI understands query intent and finds semantically similar documents

#### Hybrid Search
- **Best for**: General purpose searching, comprehensive results
- **Example**: "data analysis tools for large datasets"
- **How it works**: Combines keyword precision with semantic understanding

### **Search Controls**

#### PageRank Weight Slider
- **Left (TF-IDF)**: Emphasizes content relevance and term frequency
- **Center**: Balanced approach between content and authority
- **Right (PageRank)**: Emphasizes document authority and popularity

#### Query Tips
- **Be specific**: "machine learning algorithms for image recognition"
- **Use natural language**: "What are the best practices for data preprocessing?"
- **Try different modes**: Switch between traditional and semantic for different results

## 📊 Performance & Scalability

### **Speed Benchmarks**
- **Traditional Search**: 10-50ms per query
- **Semantic Search**: 20-100ms per query  
- **Hybrid Search**: 30-150ms per query

### **Memory Usage**
- **Base System**: ~100MB
- **AI Models**: ~100MB
- **Document Embeddings**: ~1-5MB per 1000 documents
- **Total**: ~200-500MB for typical deployments

### **Scalability Features**
- **Batch Processing**: Efficient handling of large document collections
- **Caching**: Smart caching of popular queries and embeddings
- **Parallel Processing**: Multi-threaded search across document segments
- **Fallback Mechanisms**: Graceful degradation under high load

## 🛠️ Development & Customization

### **Project Structure**
```
semantic-search-engine/
├── bin/                    # Control scripts
├── index_server/          # Search indexing and AI backend
│   ├── index/
│   │   ├── api/          # REST API endpoints
│   │   └── semantic_search.py  # AI search engine
├── search_server/         # Web interface
│   ├── search/
│   │   ├── static/       # CSS, JavaScript, assets
│   │   ├── templates/    # HTML templates
│   │   └── views/        # Flask view functions
├── var/                   # Database and logs
└── requirements.txt       # Python dependencies
```

### **Adding New Documents**
1. Place HTML files in `inverted_index/crawl/`
2. Run `./bin/searchdb` to rebuild the database
3. Run `./bin/setup_semantic` to regenerate embeddings

### **Customizing Search Algorithms**
- Modify scoring functions in `index_server/index/api/main.py`
- Adjust semantic model parameters in `index_server/index/semantic_search.py`
- Customize UI behavior in `search_server/search/views/main.py`

### **Extending the UI**
- Edit templates in `search_server/search/templates/`
- Modify styles in `search_server/search/static/css/style.css`
- Add JavaScript functionality in the template files

## 🔧 Configuration

### **Environment Variables**
```bash
# Search server configuration
export SEARCH_PORT=8000
export SEARCH_HOST=0.0.0.0

# Index server configuration  
export INDEX_PORT=9000
export INDEX_HOST=localhost

# Database paths
export SEARCH_DB_PATH=var/search.sqlite3
export INDEX_DATA_PATH=index_server/index/
```

### **Advanced Settings**
- **Model Selection**: Change the sentence transformer model in `semantic_search.py`
- **Embedding Dimensions**: Adjust vector dimensions for different accuracy/speed trade-offs
- **Scoring Weights**: Modify hybrid search algorithm parameters
- **Cache Settings**: Configure embedding and result caching behavior

## 📈 Monitoring & Analytics

### **Built-in Metrics**
- Search response times by mode
- Query frequency and popularity
- Semantic search availability status
- Error rates and fallback usage

### **Log Files**
- `var/log/search.log` - Web interface logs
- `var/log/index.log` - Search engine logs
- `debug.log` - General system debugging

### **Performance Monitoring**
```bash
# Check system status
./bin/search status
./bin/index status

# Monitor logs in real-time
tail -f var/log/search.log
tail -f var/log/index.log
```

## 🚀 Deployment

### **Production Considerations**
- **Memory**: Ensure 2GB+ RAM allocation
- **Storage**: Plan for embedding storage (typically 1-5MB per 1000 documents)
- **Networking**: Configure proper firewall rules for web access
- **Monitoring**: Set up health checks and alerting

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["./bin/search", "start"]
```

### **Cloud Deployment**
- **AWS**: Deploy on EC2 with proper security groups
- **Google Cloud**: Use Compute Engine with load balancing
- **Azure**: Deploy on Virtual Machines with Application Gateway
- **Heroku**: Use custom buildpacks for AI dependencies

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **Getting Started**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit with descriptive messages: `git commit -m 'Add amazing feature'`
5. Push to your branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

### **Development Guidelines**
- Follow PEP 8 Python style guidelines
- Add comprehensive tests for new features
- Update documentation for any API changes
- Ensure backward compatibility when possible

### **Areas for Contribution**
- **Performance**: Optimize embedding generation and search algorithms
- **UI/UX**: Improve interface design and user experience
- **AI Models**: Integrate new transformer models or fine-tune existing ones
- **Testing**: Add comprehensive test coverage and CI/CD pipelines
- **Documentation**: Improve guides, examples, and API documentation

## 📚 API Reference

### **Search Endpoint**
```
GET /api/v1/hits/?q=<query>&w=<weight>&semantic=<mode>
```

**Parameters:**
- `q`: Search query string (required)
- `w`: PageRank weight factor 0.0-1.0 (default: 0.5)
- `semantic`: Search mode: `traditional`, `semantic`, or `hybrid` (default: `traditional`)

**Response:**
```json
{
  "hits": [
    {
      "docid": 12345,
      "score": 0.875,
      "title": "Document Title",
      "url": "https://example.com/doc",
      "summary": "Document summary..."
    }
  ],
  "search_mode": "hybrid",
  "semantic_available": true
}
```

### **Status Endpoint**
```
GET /api/v1/
```

**Response:**
```json
{
  "hits": "/api/v1/hits/",
  "url": "/api/v1/"
}
```

## 🐛 Troubleshooting

### **Common Issues**

#### Semantic Search Not Available
```bash
# Check if embeddings exist
ls -la index_server/index/semantic_embeddings.npy

# Rebuild embeddings
./bin/setup_semantic
```

#### High Memory Usage
- Reduce batch size in `semantic_search.py`
- Use smaller transformer models
- Implement embedding compression

#### Slow Search Performance
- Check if embeddings are properly cached
- Monitor system resources
- Consider using GPU acceleration for large deployments

#### Database Errors
```bash
# Rebuild database
./bin/searchdb

# Check database integrity
sqlite3 var/search.sqlite3 "PRAGMA integrity_check;"
```

### **Getting Help**
- Check the logs in `var/log/`
- Review this README and documentation
- Open an issue on GitHub with detailed error information
- Include system information and error logs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Sentence Transformers**: For powerful semantic understanding capabilities
- **PyTorch**: For efficient deep learning inference
- **Flask**: For the robust web framework
- **Open Source Community**: For the amazing tools and libraries that make this possible

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/justinsudev/semantic-search-engine/issues)
- **Discussions**: [Join community discussions](https://github.com/justinsudev/semantic-search-engine/discussions)
- **Documentation**: [Browse comprehensive docs](https://github.com/justinsudev/semantic-search-engine/wiki)

---

*Transform your search experience with the power of AI*
