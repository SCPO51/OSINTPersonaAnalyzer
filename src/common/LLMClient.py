from tenacity import retry, wait_random, stop_after_attempt
from openai import OpenAI


class LLMClient:
    @staticmethod
    @retry(wait=wait_random(min=3, max=8), stop=stop_after_attempt(3))
    def ask(config, context, system=None, temperature=0):
        client = OpenAI(api_key=config["api_key"], base_url=config["base_url"])

        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": context})

        response = client.chat.completions.create(
            model=config["model"], messages=messages, temperature=temperature
        )

        return response.choices[0].message.content
