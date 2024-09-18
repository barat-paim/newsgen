import os
import random
import logging
import asyncio  # For asynchronous calls (optional)
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import time
from flask import current_app

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set up OpenAI API key for production
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("No OpenAI API key found in environment variables")

client = OpenAI(api_key=openai_api_key)

# Generate image prompt
def generate_image_prompt(refined_concept: str) -> str:
    prompt_strategies = [
        detailed_style_prompt,
        character_focused_prompt,
        situational_prompt,
        metaphorical_prompt,
        ironic_prompt
    ]
    
    # Randomly select two strategies and combine them
    selected_strategies = random.sample(prompt_strategies, 2)
    combined_prompt = " ".join(strategy(refined_concept) for strategy in selected_strategies)

    logger.debug(f"Generated combined prompt: {combined_prompt}")
    return combined_prompt

# Prompt strategies (unchanged)
def detailed_style_prompt(summary: str) -> str:
    return f"Create a detailed style cartoon based on this concept: {summary}. The cartoon should be black and white, hand-drawn style, with a single panel. It should be witty and satirical, capturing the essence of the article in a humorous way. Do not include any text or captions in the image."

def character_focused_prompt(summary: str) -> str:
    characters = ["a confused executive", "a smug academic", "a frazzled parent", "a nonchalant Gen Z", "a tech bro"]
    character = random.choice(characters)
    return f"Draw a New Yorker Magazine styled cartoon with unique characterizations of {character} based on this concept: {summary}. The character usually has a fellow character to interact with. Do not include any text or captions in the image."

def situational_prompt(summary: str) -> str:
    situations = ["a meeting", "a classroom", "a gallery opening", "a restaurant", "a party", "a street"]
    situation = random.choice(situations)
    return f"Illustrate a New Yorker Magazine styled situational cartoon set in {situation}, where the characters are reacting to something related to the concept: {summary}. The humor should come from the juxtaposition of a serious topic with the casual setting. Use typical New Yorker style: black and white, single panel. Do not include any text or captions in the image."

def metaphorical_prompt(summary: str) -> str:
    metaphors = ["a sinking ship", "a house of cards", "a tightrope walk", "a Rube Goldberg machine", "a Rubik's Cube", "a garden with both flourishing and wilting plants"]
    metaphor = random.choice(metaphors)
    return f"Create a New Yorker Magazine styled metaphorical cartoon based on the concept: {summary} represented as {metaphor}. The cartoon should be black and white, hand-drawn style, with a single panel. Do not include any text or captions in the image."

def ironic_prompt(summary: str) -> str:
    return f"Design a New Yorker Magazine styled ironic cartoon based on the concept: {summary}. It presents an ironic or paradoxical situation related to this concept. The irony should be subtle but clear to an informed viewer. The setting should contrast the profound or complex nature of the concept. Do not include any text or captions in the image."

# Generate image (unchanged)
def generate_image(prompt: str) -> dict:
    try:
        logger.debug(f"Sending prompt to OpenAI: {prompt}")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1,
        )
        logger.debug(f"Received response from OpenAI: {response}")
        return {"url": response.data[0].url}
    except Exception as e:
        logger.error(f"An error occurred while generating the image: {str(e)}")
        return None

# New function: Combine concept extraction, refinement, and caption generation
def generate_concept_and_caption(text: str):
    logger.debug(f"Generating concept and caption from text using OpenAI...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a creative writer for cartoons. Read the following article and perform the following steps:\n"
                        "1. Extract a key cartoon concept from the article, focusing on themes that can be satirized or visualized in a cartoon.\n"
                        "2. Refine the concept to make it witty, satirical, and appropriate for a single-panel white background minimalistic New Yorker cartoon. no text in the image.\n"
                        "3. Generate a brief, witty caption for the cartoon, no more than 15 words.\n"
                        "Provide your response in the following format:\n"
                        "Concept: <extracted concept>\n"
                        "Refined Concept: <refined concept>\n"
                        "Caption: <caption>"
                    )
                },
                {"role": "user", "content": text}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        output = response.choices[0].message.content.strip()
        logger.debug(f"OpenAI response: {output}")
        
        # Parse the output
        concept = ''
        refined_concept = ''
        caption = ''
        lines = output.split('\n')
        for line in lines:
            if line.startswith('Concept:'):
                concept = line[len('Concept:'):].strip()
            elif line.startswith('Refined Concept:'):
                refined_concept = line[len('Refined Concept:'):].strip()
            elif line.startswith('Caption:'):
                caption = line[len('Caption:'):].strip()
        
        if not (concept and refined_concept and caption):
            logger.error("Failed to parse OpenAI response properly.")
            return "", "", "Caption generation failed"
        
        logger.debug(f"Extracted concept: {concept}")
        logger.debug(f"Refined concept: {refined_concept}")
        logger.debug(f"Generated caption: {caption}")
        return concept, refined_concept, caption
    except Exception as e:
        logger.error(f"Error generating concept and caption: {str(e)}")
        return "", "", "Caption generation failed"

# Function to add text overlay to the image


logger = logging.getLogger(__name__)

font_path = os.path.join(current_app.root_path, 'assets', 'fonts', 'CaslonItalic.ttf')

def add_caption_to_image(image_url: str, caption: str, output_path: str, app):
    try:
        # Download the image
        response = requests.get(image_url)
        original_image = Image.open(BytesIO(response.content))
        
        # Create a new white background image
        new_width = int(original_image.width * 1.1)  # 10% wider
        new_height = int(original_image.height * 1.2)  # 20% taller
        new_image = Image.new('RGB', (new_width, new_height), 'white')
        
        # Paste the original image onto the new image, centered horizontally and towards the top
        paste_x = (new_width - original_image.width) // 2
        paste_y = int(new_height * 0.05)  # 5% from the top
        new_image.paste(original_image, (paste_x, paste_y))
        
        draw = ImageDraw.Draw(new_image)
        
        with app.app_context():
            font_path = os.path.join(app.root_path, 'assets', 'fonts', 'CaslonItalic.ttf')
        
        try:
            font = ImageFont.truetype(font_path, size=int(new_height * 0.03))  # Adjust size as needed
            logger.debug(f"Loaded Caslon Italic font from {font_path}")
        except IOError:
            logger.warning(f"Caslon Italic font not found at {font_path}. Using default font.")
            font = ImageFont.load_default()
        
        # Calculate text size and position
        text_bbox = draw.textbbox((0, 0), f'"{caption}"', font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (new_width - text_width) / 2
        y = new_height - text_height - int(new_height * 0.05)  # 5% from the bottom
        
        # Add text to image
        draw.text((x, y), f'"{caption}"', font=font, fill=(0, 0, 0, 255))
        
        # Save the edited image
        new_image.save(output_path)
        logger.debug(f"Image saved with caption at: {output_path}")
    except Exception as e:
        logger.error(f"Error adding caption to image: {str(e)}")

# Main function to generate the cartoon
def generate_cartoon(text: str, app) -> dict:
    try:
        logger.debug(f"Generating cartoon for text: {text[:100]}...")
        
        concept, refined_concept, caption = generate_concept_and_caption(text)
        
        if not refined_concept:
            logger.error("Failed to generate refined concept.")
            return {"error": "Failed to generate refined concept"}
        
        prompt = generate_image_prompt(refined_concept)
        logger.debug(f"Generated image prompt: {prompt}")
        
        image_response = generate_image(prompt)
        
        if image_response:
            original_image_url = image_response['url']
            filename = f"final_cartoon_{int(time.time())}.png"
            
            with app.app_context():
                output_path = os.path.join(app.root_path, 'static', 'images', filename)
            
            # Add caption to the image
            add_caption_to_image(original_image_url, caption, output_path, app)
            
            # Return the URL path for the saved image
            return {
                "image_url": f"/images/{filename}",
                "caption": caption
            }
        else:
            logger.error("Failed to generate image")
            return {"error": "Failed to generate image"}
    except Exception as e:
        logger.error(f"Error in generate_cartoon: {str(e)}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    test_text = """
    The increasing reliance on AI in everyday decision-making is transforming how we interact with technology.
    New smartphones are incorporating AI features that can predict user behavior and automate tasks, raising 
    concerns about privacy and data security. As AI becomes more ingrained in daily life, society must 
    navigate the benefits of increased efficiency and the risks of handing over control to machines.
    """
    result = generate_cartoon(test_text)
    print(result)