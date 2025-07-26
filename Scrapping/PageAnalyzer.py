import configparser
import re
from openai import AzureOpenAI
from bs4 import BeautifulSoup
import tiktoken
from typing import Optional
from textwrap import wrap


class PageAnalyzer:
    def __init__(self, config_path="config.ini"):
        self._config = configparser.ConfigParser()
        self._config.read(config_path)
        self._client = self.InitializeOpenAIClient()
        self.token_limit = 8192  # For gpt-4o use a safe limit well below 128k max

    def InitializeOpenAIClient(self) -> AzureOpenAI:
        endpoint = self._config.get("OpenAIModel", "url", fallback="https://azure-openai-rosh.openai.azure.com/")
        deployment = self._config.get("OpenAIModel", "model_name", fallback="gpt-4o")
        api_key = self._config.get("OpenAIModel", "api_key", fallback="")
        api_version = self._config.get("OpenAIModel", "api_version", fallback="2024-12-01-preview")

        return AzureOpenAI(
            azure_endpoint=endpoint,
            azure_deployment=deployment,
            api_version=api_version,
            api_key=api_key
        )

    def analyze(self, html_content: str, product: str) -> str:
        filtered = extract_price_context(html_content)

        # Try regex-based quick match
        quick_price = quick_price_regex(filtered)
        if quick_price:
            return quick_price

        # Count tokens, split if too long
        chunks = split_by_tokens(filtered, model="gpt-4o", limit=self.token_limit)
        for chunk in chunks:
            result = self._analyze_with_model(chunk, product)
            if result and "price not found" not in result.lower():
                return result.strip()

        return "Price not found"

    def _analyze_with_model(self, filtered_content: str, product: str) -> str:
        deployment = self._config.get("OpenAIModel", "deployment", fallback="gpt-4o")
        try:
            response = self._client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert at extracting product prices from HTML or text snippets. "
                            "Only use the content provided to you—do not rely on external knowledge. "
                            "If you cannot find a price in the provided content, respond with 'Price not found.' "
                            "Only return the price as plain text, without any explanation or symbols."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Extract the price of '{product}' from this content:\n{filtered_content}"
                    }
                ],
                max_tokens=100,
                temperature=0.2,
                top_p=1.0,
                model=deployment,
                timeout=20
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Model analysis failed: {str(e)}"


# ------------------------------
# Utility functions
# ------------------------------

def extract_price_context(html: str, context_window: int = 1) -> str:
    keywords = ["price", "₹", "$", "amount", "cost", "rs.", "usd", "inr", "eur"]
    pattern = re.compile(r'|'.join(re.escape(k) for k in keywords), re.IGNORECASE)

    # Clean HTML: remove scripts, styles, comments
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()

    lines = soup.get_text().splitlines()
    relevant_indices = [i for i, line in enumerate(lines) if pattern.search(line)]

    context_lines = set()
    for idx in relevant_indices:
        start = max(0, idx - context_window)
        end = min(len(lines), idx + context_window + 1)
        for i in range(start, end):
            if len(lines[i].strip()) > 5:
                context_lines.add(i)

    filtered = "\n".join([lines[i] for i in sorted(context_lines)])
    return filtered


def quick_price_regex(text: str) -> Optional[str]:
    match = re.search(r'(₹|\$|Rs\.?)\s?\d[\d,]*(\.\d{1,2})?', text)
    return match.group(0) if match else None


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def split_by_tokens(text: str, model: str = "gpt-4o", limit: int = 8192) -> list:
    tokens = []
    encoding = tiktoken.encoding_for_model(model)
    raw_tokens = encoding.encode(text)

    if len(raw_tokens) <= limit:
        return [text]

    chunks = []
    for i in range(0, len(raw_tokens), limit):
        chunk_tokens = raw_tokens[i:i + limit]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks

