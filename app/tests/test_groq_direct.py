import asyncio
import os
from dotenv import load_dotenv

# Load explicitly to ensure we pick up changes
load_dotenv(override=True)

from app.core.config import get_settings
from app.services.ai.groq_service import GroqService

async def test_groq():
    settings = get_settings()
    service = GroqService(api_key=settings.groq_api_key, timeout_seconds=10)
    print("Testing Groq API directly...")
    
    try:
        response = await service.complete(
            prompt="Explain the difference between Grok and Groq in 20 words.",
            system="You are a helpful AI assistant.",
            model=settings.groq_model,
            max_tokens=100
        )
        print("\nSUCCESS!")
        print("Response:", response)
    except Exception as e:
        print("\nFAILED!")
        print("Error:", str(e))

if __name__ == "__main__":
    asyncio.run(test_groq())
