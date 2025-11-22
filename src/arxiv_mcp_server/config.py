"""Configuration settings for the arXiv MCP server."""

import sys
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Server configuration settings."""

    APP_NAME: str = "arxiv-mcp-server-cuhksz"
    APP_VERSION: str = "0.3.1"
    MAX_RESULTS: int = 50
    BATCH_SIZE: int = 20
    REQUEST_TIMEOUT: int = 60
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    model_config = SettingsConfigDict(extra="allow")

    @property
    def STORAGE_PATH(self) -> Path:
        """Get the resolved storage path and ensure it exists.
        
        Priority order:
        1. Command line argument --storage-path
        2. Environment variable ARXIV_STORAGE_PATH
        3. Default path ~/.arxiv-mcp-server/papers

        Returns:
            Path: The absolute storage path.
        """
        # Priority 1: Command line argument
        path = self._get_storage_path_from_args()
        
        # Priority 2: Environment variable
        if path is None:
            env_path = os.getenv("ARXIV_STORAGE_PATH")
            if env_path:
                path = Path(env_path)
        
        # Priority 3: Default path
        if path is None:
            path = Path.home() / ".arxiv-mcp-server" / "papers"
        
        path = path.resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _get_storage_path_from_args(self) -> Path | None:
        """Extract storage path from command line arguments.

        Returns:
            Path | None: The storage path if specified in arguments, None otherwise.
        """
        args = sys.argv[1:]

        # If not enough arguments
        if len(args) < 2:
            return None

        # Look for the --storage-path option
        try:
            storage_path_index = args.index("--storage-path")
        except ValueError:
            return None

        # Early return if --storage-path is the last argument
        if storage_path_index + 1 >= len(args):
            return None

        # Try to resolve the path
        try:
            path = Path(args[storage_path_index + 1])
            return path.resolve()
        except (TypeError, ValueError) as e:
            # TypeError: If the path argument is not string-like
            # ValueError: If the path string is malformed
            logger.warning(f"Invalid storage path format: {e}")
        except OSError as e:
            # OSError: If the path contains invalid characters or is too long
            logger.warning(f"Invalid storage path: {e}")

        return None
