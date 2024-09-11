from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
client = OpenAI()  # This will automatically use the OPENAI_API_KEY from your environment

def generate_image(prompt: str) -> dict:
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        print("Image generated successfully!")
        return {"url": image_url}
    except Exception as e:
        print(f"An error occurred while generating the image: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {e.args}")
        return None

# Test with a simple prompt
simple_prompt = "A cat sitting on a windowsill"
result = generate_image(simple_prompt)

if result:
    print(f"Image URL: {result['url']}")
else:
    print("Failed to generate image")

# Print the API key (first few characters)
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"API key (first 10 characters): {api_key[:10]}...")
else:
    print("API key not found in environment variables")
