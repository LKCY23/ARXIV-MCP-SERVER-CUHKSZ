"""List functionality for the arXiv MCP server."""

import json
from pathlib import Path
import arxiv
from typing import Dict, Any, List, Optional
import mcp.types as types
from ..config import Settings

settings = Settings()

list_tool = types.Tool(
    name="list_papers",
    description="List all existing papers available as resources",
    inputSchema={
        "type": "object",
        "properties": {},
        "required": [],
    },
)


def list_papers() -> list[str]:
    """List all stored paper IDs."""
    return [p.stem for p in Path(settings.STORAGE_PATH).glob("*.md")]


def _normalize_paper_id(paper_id: str) -> str:
    """Normalize paper ID by removing version suffix if present.
    
    arXiv paper IDs may be stored with version suffix (e.g., '2201.00978v1'),
    but the API accepts both formats. However, we normalize to base ID for consistency.
    """
    # Remove version suffix like 'v1', 'v2', etc.
    if 'v' in paper_id and paper_id.rindex('v') > 0:
        # Check if it's a version suffix (v followed by digits at the end)
        parts = paper_id.rsplit('v', 1)
        if len(parts) == 2 and parts[1].isdigit():
            return parts[0]
    return paper_id


async def handle_list_papers(
    arguments: Optional[Dict[str, Any]] = None,
) -> List[types.TextContent]:
    """Handle requests to list all stored papers."""
    try:
        papers = list_papers()

        # 如果没有已下载的论文，直接返回友好消息
        if not papers:
            response_data = {
                "total_papers": 0,
                "papers": [],
                "message": "No papers have been downloaded yet. Use the download_paper tool to download papers first."
            }
            return [
                types.TextContent(type="text", text=json.dumps(response_data, indent=2))
            ]

        # 只有当有论文时才调用 arXiv API
        # 规范化论文ID（去掉版本号后缀）
        normalized_papers = [_normalize_paper_id(pid) for pid in papers]
        client = arxiv.Client()

        try:
            results = client.results(arxiv.Search(id_list=normalized_papers))
            
            response_data = {
                "total_papers": len(papers),
                "papers": [
                    {
                        "id": result.entry_id.split("/")[-1] if result.entry_id else "unknown",
                        "title": result.title,
                        "summary": result.summary,
                        "authors": [author.name for author in result.authors],
                        "links": [link.href for link in result.links],
                        "pdf_url": result.pdf_url,
                    }
                    for result in results
                ],
            }
        except Exception as api_error:
            # 如果 arXiv API 调用失败，至少返回本地存储的论文ID列表
            response_data = {
                "total_papers": len(papers),
                "papers": [{"id": paper_id} for paper_id in papers],
                "warning": f"Could not fetch full paper details from arXiv API: {str(api_error)}. Showing paper IDs only.",
            }

        return [
            types.TextContent(type="text", text=json.dumps(response_data, indent=2))
        ]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]
