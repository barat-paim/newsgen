import os
import random
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables first
load_dotenv()

# Set up OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("No OpenAI API key found in environment variables")

client = OpenAI()

from image_generator import test_prompt_generation

test_text = """
The increasing reliance on AI in everyday decision-making is transforming how we interact with technology.
New smartphones are incorporating AI features that can predict user behavior and automate tasks, raising 
concerns about privacy and data security. As AI becomes more ingrained in daily life, society must 
navigate the benefits of increased efficiency and the risks of handing over control to machines.
"""

try:
    final_prompt = test_prompt_generation(test_text)
    print("Final Prompt:")
    print(final_prompt)
except Exception as e:
    print(f"An error occurred: {str(e)}")
