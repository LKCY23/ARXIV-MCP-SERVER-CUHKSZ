[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# ArXiv MCP Server

> 🔍 Enable AI assistants to search and access arXiv papers through a simple MCP interface.

The ArXiv MCP Server provides a bridge between AI assistants and arXiv's research repository through the Model Context Protocol (MCP). It allows AI models to search for papers and access their content in a programmatic way.

## 👥 About This Fork

This repository is maintained by the **港中深智慧校园开发团队**. 

We created this independent repository (rather than forking) to better accommodate our team's specific development needs and workflow requirements. However, we deeply respect and acknowledge the original work by [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server), upon which this project is based.

## 🙏 Acknowledgments

This project is built upon the excellent work of the original [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) project by [@blazickjp](https://github.com/blazickjp) and the Pearl Labs Team. We are grateful for their contributions to the open-source community and for providing a solid foundation for our development work.

**Original Project**: [https://github.com/blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server)
<div align="center">
  
📝 **[Report Bug](https://github.com/LKCY23/ARXIV-MCP-SERVER-CUHKSZ/issues)** • 
🔗 **[Original Project](https://github.com/blazickjp/arxiv-mcp-server)**

</div>

## ✨ Core Features

- 🔎 **Paper Search**: Query arXiv papers with filters for date ranges and categories
- 📄 **Paper Access**: Download and read paper content
- 📋 **Paper Listing**: View all downloaded papers
- 🗃️ **Local Storage**: Papers are saved locally for faster access
- 📝 **Prompts**: A Set of Research Prompts

## 🚀 Quick Start

### Installing via Smithery

To install ArXiv Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/arxiv-mcp-server):

```bash
npx -y @smithery/cli install arxiv-mcp-server-cuhksz --client claude
```

### Installing Manually
Install using uv:

```bash
uv tool install arxiv-mcp-server-cuhksz
```

For development:

```bash
# Clone and set up development environment
git clone https://github.com/LKCY23/ARXIV-MCP-SERVER-CUHKSZ.git
cd ARXIV-MCP-SERVER-CUHKSZ

# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install with test dependencies
uv pip install -e ".[test]"
```

### 🔌 MCP Integration

Add this configuration to your MCP client config file:

```json
{
    "mcpServers": {
        "arxiv-mcp-server-cuhksz": {
            "command": "uv",
            "args": [
                "tool",
                "run",
                "arxiv-mcp-server-cuhksz",
                "--storage-path", "/path/to/paper/storage"
            ]
        }
    }
}
```

For Development:

```json
{
    "mcpServers": {
        "arxiv-mcp-server-cuhksz": {
            "command": "uv",
            "args": [
                "--directory",
                "path/to/cloned/ARXIV-MCP-SERVER-CUHKSZ",
                "run",
                "arxiv-mcp-server-cuhksz",
                "--storage-path", "/path/to/paper/storage"
            ]
        }
    }
}
```

## 💡 Available Tools

The server provides four main tools:

### 1. Paper Search
Search for papers with optional filters:

```python
result = await call_tool("search_papers", {
    "query": "transformer architecture",
    "max_results": 10,
    "date_from": "2023-01-01",
    "categories": ["cs.AI", "cs.LG"]
})
```

### 2. Paper Download
Download a paper by its arXiv ID:

```python
result = await call_tool("download_paper", {
    "paper_id": "2401.12345"
})
```

### 3. List Papers
View all downloaded papers:

```python
result = await call_tool("list_papers", {})
```

### 4. Read Paper
Access the content of a downloaded paper:

```python
result = await call_tool("read_paper", {
    "paper_id": "2401.12345"
})
```

## 📝 Research Prompts

The server offers specialized prompts to help analyze academic papers:

### Paper Analysis Prompt
A comprehensive workflow for analyzing academic papers that only requires a paper ID:

```python
result = await call_prompt("deep-paper-analysis", {
    "paper_id": "2401.12345"
})
```

This prompt includes:
- Detailed instructions for using available tools (list_papers, download_paper, read_paper, search_papers)
- A systematic workflow for paper analysis
- Comprehensive analysis structure covering:
  - Executive summary
  - Research context
  - Methodology analysis
  - Results evaluation
  - Practical and theoretical implications
  - Future research directions
  - Broader impacts

## ⚙️ Configuration

Configure through environment variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| `ARXIV_STORAGE_PATH` | Paper storage location | ~/.arxiv-mcp-server/papers |

## 🧪 Testing

Run the test suite:

```bash
python -m pytest
```

## 📄 License

Released under the MIT License. See the LICENSE file for details.

---

<div align="center">

Made with ❤️ by 港中深智慧校园开发团队 (CUHKSZ Smart Campus Development Team)

Based on the original work by [Pearl Labs Team](https://github.com/blazickjp/arxiv-mcp-server)

<a href="https://glama.ai/mcp/servers/04dtxi5i5n"><img width="380" height="200" src="https://glama.ai/mcp/servers/04dtxi5i5n/badge" alt="ArXiv Server MCP server" /></a>
</div>
