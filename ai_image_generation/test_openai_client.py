"""
Simple test to verify OpenAI client initialization
"""

import os
from dotenv import load_dotenv
import openai

load_dotenv()

def test_openai_client():
    try:
        # Test with dummy API key
        client = openai.OpenAI(api_key="sk-test-key")
        print("✅ OpenAI client initialized successfully")
        print(f"OpenAI version: {openai.__version__}")
        return True
    except Exception as e:
        print(f"❌ OpenAI client error: {e}")
        return False

if __name__ == "__main__":
    test_openai_client()