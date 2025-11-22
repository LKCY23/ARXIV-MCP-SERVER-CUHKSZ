"""Handlers for prompt-related requests with paper analysis functionality."""

from typing import List, Dict, Optional
from mcp.types import Prompt, PromptMessage, TextContent, GetPromptResult
from .prompts import PROMPTS
from .deep_research_analysis_prompt import PAPER_ANALYSIS_PROMPT
from .research_discovery_prompt import RESEARCH_DISCOVERY_PROMPT
from .literature_synthesis_prompt import LITERATURE_SYNTHESIS_PROMPT
from .research_question_prompt import RESEARCH_QUESTION_PROMPT


# Legacy global research context - used as fallback when no session_id is provided
class ResearchContext:
    """Maintains context throughout a research session."""

    def __init__(self):
        self.expertise_level = "intermediate"  # default
        self.explored_papers = {}  # paper_id -> basic metadata
        self.paper_analyses = {}  # paper_id -> analysis focus and summary

    def update_from_arguments(self, args: Dict[str, str]) -> None:
        """Update context based on new arguments."""
        if "expertise_level" in args:
            self.expertise_level = args["expertise_level"]
        if "paper_id" in args and args["paper_id"] not in self.explored_papers:
            self.explored_papers[args["paper_id"]] = {"id": args["paper_id"]}


# Global research context for backward compatibility
_research_context = ResearchContext()

# Output structure for deep paper analysis
OUTPUT_STRUCTURE = """
Present your analysis with the following structure:
1. Executive Summary: 3-5 sentence overview of key contributions
2. Detailed Analysis: Following the specific focus requested
3. Visual Breakdown: Describe key figures/tables and their significance
4. Related Work Map: Position this paper within the research landscape
5. Implementation Notes: Practical considerations for applying these findings
"""


async def list_prompts() -> List[Prompt]:
    """Handle prompts/list request - returns all available prompts."""
    return list(PROMPTS.values())


async def get_prompt(
    name: str, arguments: Dict[str, str] | None = None, session_id: Optional[str] = None
) -> GetPromptResult:
    """Handle prompts/get request for all prompt types.

    Args:
        name: The name of the prompt to get
        arguments: The arguments to use with the prompt
        session_id: Optional user session ID for context persistence

    Returns:
        GetPromptResult: The resulting prompt with messages

    Raises:
        ValueError: If prompt not found or arguments invalid
    """
    if name not in PROMPTS:
        raise ValueError(f"Prompt not found: {name}. Available prompts: {list(PROMPTS.keys())}")

    prompt = PROMPTS[name]
    if arguments is None:
        raise ValueError(f"No arguments provided for prompt: {name}")

    # Validate required arguments
    for arg in prompt.arguments:
        if arg.required and (arg.name not in arguments or not arguments.get(arg.name)):
            raise ValueError(f"Missing required argument: {arg.name}")

    # Update research context
    _research_context.update_from_arguments(arguments)

    # Route to appropriate prompt handler based on name
    if name == "deep-paper-analysis":
        return _handle_deep_paper_analysis(arguments)
    elif name == "research-discovery":
        return _handle_research_discovery(arguments)
    elif name == "literature-synthesis":
        return _handle_literature_synthesis(arguments)
    elif name == "research-question":
        return _handle_research_question(arguments)
    else:
        raise ValueError(f"Prompt handler not implemented for: {name}")


def _handle_deep_paper_analysis(arguments: Dict[str, str]) -> GetPromptResult:
    """Handle deep-paper-analysis prompt."""
    paper_id = arguments.get("paper_id", "")
    
    # Add context from previous papers if available
    previous_papers_context = ""
    if len(_research_context.explored_papers) > 1:
        previous_ids = [
            pid for pid in _research_context.explored_papers.keys() if pid != paper_id
        ]
        if previous_ids:
            previous_papers_context = f"\nI've previously analyzed papers: {', '.join(previous_ids)}. If relevant, note connections to these works."

    # Track this analysis in context
    _research_context.paper_analyses[paper_id] = {"analysis": "complete"}

    return GetPromptResult(
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"Analyze paper {paper_id}.{previous_papers_context}\n\n{OUTPUT_STRUCTURE}\n\n{PAPER_ANALYSIS_PROMPT}",
                ),
            )
        ]
    )


def _handle_research_discovery(arguments: Dict[str, str]) -> GetPromptResult:
    """Handle research-discovery prompt."""
    topic = arguments.get("topic", "")
    expertise_level = arguments.get("expertise_level", "intermediate")
    time_period = arguments.get("time_period", "")
    domain = arguments.get("domain", "")
    
    context_info = []
    if expertise_level:
        context_info.append(f"User's expertise level: {expertise_level}")
    if time_period:
        context_info.append(f"Time period: {time_period}")
    if domain:
        context_info.append(f"Domain: {domain}")
    
    context_str = "\n".join(context_info) if context_info else ""
    
    prompt_text = f"""Explore and discover research on the topic: "{topic}"

{context_str}

{RESEARCH_DISCOVERY_PROMPT}
"""
    
    return GetPromptResult(
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=prompt_text),
            )
        ]
    )


def _handle_literature_synthesis(arguments: Dict[str, str]) -> GetPromptResult:
    """Handle literature-synthesis prompt."""
    paper_ids = arguments.get("paper_ids", "")
    synthesis_type = arguments.get("synthesis_type", "comprehensive")
    domain = arguments.get("domain", "")
    
    # Parse paper IDs (comma-separated)
    paper_id_list = [pid.strip() for pid in paper_ids.split(",") if pid.strip()]
    
    context_info = []
    if synthesis_type:
        context_info.append(f"Synthesis type: {synthesis_type}")
    if domain:
        context_info.append(f"Domain: {domain}")
    
    context_str = "\n".join(context_info) if context_info else ""
    
    prompt_text = f"""Synthesize findings across the following papers: {', '.join(paper_id_list)}

{context_str}

{LITERATURE_SYNTHESIS_PROMPT}
"""
    
    return GetPromptResult(
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=prompt_text),
            )
        ]
    )


def _handle_research_question(arguments: Dict[str, str]) -> GetPromptResult:
    """Handle research-question prompt."""
    paper_ids = arguments.get("paper_ids", "")
    topic = arguments.get("topic", "")
    domain = arguments.get("domain", "")
    
    # Parse paper IDs (comma-separated)
    paper_id_list = [pid.strip() for pid in paper_ids.split(",") if pid.strip()]
    
    context_info = []
    if domain:
        context_info.append(f"Domain: {domain}")
    
    context_str = "\n".join(context_info) if context_info else ""
    
    prompt_text = f"""Based on the following papers and research topic, formulate research questions:

Papers to analyze: {', '.join(paper_id_list)}
Research topic: {topic}

{context_str}

{RESEARCH_QUESTION_PROMPT}
"""
    
    return GetPromptResult(
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=prompt_text),
            )
        ]
    )
