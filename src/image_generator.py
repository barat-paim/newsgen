import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(prompt: str) -> dict:
    """
    Generate an image using DALL-E 2 API based on the given prompt.
    
    Args:
    prompt (str): The text prompt to generate the image from.
    
    Returns:
    dict: A dictionary containing the API response, including the image URL.
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response
    except Exception as e:
        print(f"An error occurred while generating the image: {str(e)}")
        return None

def generate_image_prompt(summary: str) -> str:
    """
    Generate a prompt for DALL-E 2 based on the article summary.
    
    Args:
    summary (str): A summary of the article content.
    
    Returns:
    str: A prompt for generating a New Yorker style cartoon.
    """
    return f"A New Yorker style cartoon depicting: {summary}"

def generate_cartoon(text: str) -> dict:
    """
    Generate a New Yorker style cartoon based on the input text.
    
    Args:
    text (str): The input article text.
    
    Returns:
    dict: A dictionary containing the generated image information.
    """
    # TODO: Implement text summarization
    summary = text  # Placeholder, replace with actual summarization

    prompt = generate_image_prompt(summary)
    image_response = generate_image(prompt)
    
    if image_response:
        return {
            "prompt": prompt,
            "image_url": image_response['data'][0]['url']
        }
    else:
        return {"error": "Failed to generate image"}

if __name__ == "__main__":
    # Simple test
    test_text = "A robot learning to paint in an art studio."
    result = generate_cartoon(test_text)
    print(result)