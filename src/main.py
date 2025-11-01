import os
from pathlib import Path

from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPStdioPlugin

from utils.logger import logger


load_dotenv()


async def mcp_connect() -> MCPStdioPlugin:
    """
    Initialises and connects the Model Context Protocol (MCP) server
    for Atlas.

    This method sets up MCPStdioPlugin with the appropriate directory,
    environment variables, and command-line arguments, then connects
    the plugin in STDIO communication mode for use with the Atlas agent.

    Returns:
        MCPStdioPlugin: The connected MCP plugin instance.
    """
    mcp_dir = (
        Path(__file__).resolve().parent.parent / "model_context_protocol"
    )
    load_dotenv()
    env_vars = dict(os.environ.copy())  # get env vars as dict

    logger.debug("Creating MCP Plugin...")
    mcp_plugin = MCPStdioPlugin(
        name="matlas",
        description=(
            "MCP for Matlas: an interface for a Learning Companion "
            "agent guiding students through a course."
        ),
        command="uv",
        args=[
            f"--directory={mcp_dir}",
            "run",
            "server.py",
        ],
        env=env_vars,  # add env vars in MCP server
    )
    await mcp_plugin.connect()
    return mcp_plugin



def main():
    print("Hello from pocket-agent!")


if __name__ == "__main__":
    main()
