from enum import StrEnum

from utils.get_env_var import get_env_var


class LLMDeployment(StrEnum):
    GPT_5_CHAT = "gpt-5-chat"
    GPT_5_MINI = "gpt-5-mini"
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_4_1_NANO = "gpt-4.1-nano"
    O3_MINI = "o3-mini"
    MODEL_ROUTER = "model-router"


class LLM:
    _deployment_to_env = {
        LLMDeployment.GPT_5_CHAT: "GPT_5_CHAT_ENDPOINT",
        LLMDeployment.GPT_5_MINI: "GPT_5_MINI_ENDPOINT",
        LLMDeployment.GPT_4_1: "GPT_41_ENDPOINT",
        LLMDeployment.GPT_4_1_MINI: "GPT_41_MINI_ENDPOINT",
        LLMDeployment.GPT_4_1_NANO: "GPT_41_NANO_ENDPOINT",
        LLMDeployment.O3_MINI: "O3_MINI_ENDPOINT",
        LLMDeployment.MODEL_ROUTER: "MODEL_ROUTER_ENDPOINT",
    }

    def __init__(self, model_deployment: LLMDeployment):
        if model_deployment not in self._deployment_to_env:
            raise ValueError(f"Unsupported model deployment: {model_deployment}")

        self.deployment = model_deployment
        self.api_key = get_env_var("AZURE_OPENAI_KEY")
        self.endpoint = get_env_var(self._deployment_to_env[model_deployment])
