import os
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel import Kernel

from utils.llm import LLM, LLMDeployment
from utils.logger import logger


load_dotenv()


class Agent:
    def __init__(self, name: str, instruction: str, llm_deployment: LLMDeployment, mcp_plugin: MCPStdioPlugin):
        self.llm = LLM(llm_deployment)
        kernel = Kernel()  # init kernel
        service = AzureChatCompletion(
            deployment_name=self.llm.deployment,
            api_key=self.llm.api_key,
            endpoint=self.llm.endpoint,
        )
        kernel.add_service(service)
        kernel.add_plugin(
            mcp_plugin,
            plugin_name="mcp_server",
        )

        self.agent = ChatCompletionAgent(
            kernel=kernel,
            name=name,
            instructions=instruction,
        )

    async def init_chat(self):
        thread = ChatHistoryAgentThread()
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == "exit":
                print("Exiting chat.")
                break
            async for response in self.agent.invoke_stream(messages=user_input, thread=thread):
                print(f"\n{self.agent.name}: {response}")



async def mcp_connect(server_name: str, server_path: Path, run_cmd: str, run_args: list[str]) -> MCPStdioPlugin:
    logger.debug("Creating MCP Plugin...")
    mcp_plugin = MCPStdioPlugin(
        name=server_name,
        command=run_cmd,
        args=[
            f"--directory={str(server_path)}",
            *run_args,
        ],
        # env=env_vars, if needed
    )
    await mcp_plugin.connect()
    return mcp_plugin

async def mcp_disconnect(mcp_plugin: MCPStdioPlugin) -> None:
    if mcp_plugin is not None:
        await mcp_plugin.close()
    else:
        logger.warning("MCP Plugin is None, nothing to disconnect.")


async def main():
    mcp_server = await mcp_connect(
        server_name="excel_mcp",
        server_path=Path("/Users/dh324/Desktop/MISC/projects/mcp_servers/excel-mcp-server"),
        run_cmd="uvx",
        run_args=["excel-mcp-server", "stdio"],
    )

    agent = Agent(
        name="excel_agent",
        instruction="You are an expert in Excel spreadsheet manipulation.",
        llm_deployment=LLMDeployment.GPT_4_1,
        mcp_plugin=mcp_server,
    )

    await agent.init_chat()
    await mcp_disconnect(mcp_server)


if __name__ == "__main__":
    asyncio.run(main())
