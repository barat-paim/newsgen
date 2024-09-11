# Summary of the image_generator.py file:
# necessary imports, libraries, and dependencies    
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
client = OpenAI()  # This will automatically use the OPENAI_API_KEY from your environment

# read_article_from_file(filename) -> str: reads article text from a file
### purpose: load article text from a specified file
### input: string filename
### process: opens and reads the content of the file
### returns: string containing the article text
def read_article_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# generate_image(prompt) -> dict: generates an image from OpenAI(DALL-E 3) based on the given prompt
### purpose: create final image in dictionary format with URL
### input: string prompt
### process: OpenAI API function call using prompt
### returns: dictionary with image URL or None if error
### note: includes error handling to catch and report any issues during API call
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
        print("Here is your cartoon!")
        return {"url": image_url} # returns the URL of the generated image because the main.py file needs it but not necessarily for the function to work    
    except Exception as e:
        print(f"An error occurred while generating the image: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {e.args}")
        return None

# generate_image_prompt(summary) -> str: builds a prompt for the generate_image(prompt) function    
### purpose: create a New Yorker style cartoon prompt for the generate_image(prompt) function
### input: string summary or concept for the cartoon
### process: formats the input into a prompt specifically for New Yorker style cartoons
### returns: string prompt that can be used in the generate_image(prompt) function
def generate_image_prompt(summary: str) -> str:
    return f"Create a New Yorker style cartoon based on this concept: {summary}. The cartoon should be black and white, hand-drawn style, with a single panel. It should be witty and satirical, capturing the essence of the article in a humorous way."

# generate_cartoon(text) -> dict: main entry point for generating an image based on the article text
### purpose: orchestrate the entire image generation process
### input: string text (can be multiple lines) representing the article or concept

### process: 
###   1. calls extract_cartoon_concepts(text) to generate a concept (specific to the iPhone article)    
###   2. calls generate_image_prompt(concept) to generate a prompt
###   3. calls generate_image(prompt) to generate an image

### returns: dictionary with the prompt and image URL
### note: handles the flow from user input to final image generation
def generate_cartoon(text: str) -> dict:
    concept = extract_cartoon_concepts(text)
    prompt = generate_image_prompt(concept)
    image_response = generate_image(prompt)
    
    if image_response:
        return {"concept": concept, "prompt": prompt, "image_url": image_response['url']}
    else:
        return {"error": "Failed to generate image"}

# Example usage
if __name__ == "__main__":
    test_text = "A robot learning to paint in an art studio."
    result = generate_cartoon(test_text)
    print(result)

# This script uses the OpenAI API to generate New Yorker style cartoons based on article text from a file.
# Ensure that the OPENAI_API_KEY is properly set in the environment variables before running.


##### specific to the iPhone article ##### standardize this later   
# extract_cartoon_concepts(text: str) -> str:
### purpose: extract the concept of the article for the generate_image_prompt(summary) function
### input: string text (can be multiple lines) representing the article or concept
### process: 
###   1. List of key themes or elements to look for
###   2. Extract sentences containing key themes
###   3. Combine the relevant sentences, limiting to 2-3 for brevity
### returns: string concept that can be used in the generate_image_prompt(summary) function 

def extract_cartoon_concepts(text: str) -> str:
    # List of key themes or elements to look for
    key_themes = [
        "new technology", "smartphone features", "consumer behavior",
        "social media", "privacy", "AI", "camera improvements",
        "battery life", "design changes", "price", "release date"
    ]
    
    # Extract sentences containing key themes
    relevant_sentences = []
    for sentence in text.split('.'):
        if any(theme in sentence.lower() for theme in key_themes):
            relevant_sentences.append(sentence.strip())
    
    # Combine the relevant sentences, limiting to 2-3 for brevity
    concept = '. '.join(relevant_sentences[:3])
    
    return f"New iPhone release: {concept}"