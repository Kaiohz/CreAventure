from typing import List
import httpx
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from config import LLM_URL, LLM_KEY, MODEL_CHAT, MODEL_EMBEDDINGS

class LLMProxyChatOpenAI(ChatOpenAI):
    def __init__(self) -> None:
        if not MODEL_CHAT:
            raise ValueError("MODEL_CHAT must be set in environment variables")
            
        super().__init__(
            http_client=httpx.Client(http2=True, verify=False),
            http_async_client=httpx.AsyncClient(http2=True, verify=False),
            openai_api_base=LLM_URL,
            model=MODEL_CHAT,
            openai_api_key=LLM_KEY,
            streaming=False,
            callbacks=[],
        )


class LLMProxyOpenAIEmbeddings(OpenAIEmbeddings):
    def __init__(self) -> None:
        super().__init__(
            http_client=httpx.Client(http2=True, verify=False),
            http_async_client=httpx.AsyncClient(http2=True, verify=False),
            openai_api_base=LLM_URL,
            model=MODEL_EMBEDDINGS,
            openai_api_key=LLM_KEY,
        )