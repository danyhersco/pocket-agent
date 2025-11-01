import base64
from typing import TypeVar, Union
from pathlib import Path

from openai import AsyncAzureOpenAI
from pydantic import BaseModel

from utils.llm import LLMDeployment


T = TypeVar("T", bound=BaseModel)


def encode_image(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def chat_completion_generate(
    client: AsyncAzureOpenAI,
    model_deployment: LLMDeployment,
    system_prompt: str,
    user_prompt: str | None = None,
    output_format: type[T] | None = None,
    image_paths: list[Path] = [],
) -> Union[str, T]:
    if not user_prompt and not image_paths:
        raise ValueError("Either user_prompt or image_paths must be provided.")

    content = [{"type": "text", "text": user_prompt}] if user_prompt else []
    for image_path in image_paths:
        base64_image = encode_image(image_path)
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"},
            }  # type: ignore
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content},
    ]

    if output_format is not None:
        response = await client.beta.chat.completions.parse(
            messages=messages,  # type: ignore
            model=model_deployment.value,
            response_format=output_format,  # type: ignore
            temperature=0.0,
        )
        output = response.choices[0].message.parsed
    else:
        response = await client.chat.completions.create(
            messages=messages,  # type: ignore
            model=model_deployment.value,
            temperature=0.0,
        )
        output = response.choices[0].message.content

    if output is None:
        raise ValueError("Error generating Chat Completion: None returned.")

    return output
