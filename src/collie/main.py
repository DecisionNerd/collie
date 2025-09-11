import asyncio
import os
import sys

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

# Load environment variables from .env file
load_dotenv()


def check_api_key():
    """Check if GOOGLE_API_KEY is set and provide helpful error message if not."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        sys.exit(1)
    return api_key


async def main():
    # Check API key before proceeding
    api_key = check_api_key()

    provider = GoogleProvider(api_key=api_key)
    model = GoogleModel("gemini-2.0-flash-001", provider=provider)
    agent = Agent(model)

    # Asynchronous call for Italy
    await agent.run("What is the capital of Italy?")
    # > The capital of Italy is Rome.

    # Asynchronous call
    await agent.run("What is the capital of France?")
    # > The capital of France is Paris.

    # Streaming call
    async with agent.run_stream("What is the capital of the UK?") as response:
        async for _text in response.stream_text():
            pass
            # > The capital of
            # > The capital of the UK is
            # > The capital of the UK is London.


def cli():
    """Command line interface entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    cli()
