from enum import StrEnum

from utils.get_env_var import get_env_var


class LLMDeployment(StrEnum):
    GPT_4_1 = "gpt-4.1"


class LLM:
    _deployment_to_env = {
        LLMDeployment.GPT_4_1: "GPT_41_ENDPOINT",
    }

    def __init__(self, model_deployment: LLMDeployment):
        if model_deployment not in self._deployment_to_env:
            raise ValueError(f"Unsupported model deployment: {model_deployment}")

        self.deployment = model_deployment
        self.api_key = get_env_var("AZURE_OPENAI_KEY")
        self.endpoint = get_env_var(self._deployment_to_env[model_deployment])
