#User Inputs Article
 #      ↓
#Extract Key Concepts → Summarize Gist of Article
 #      ↓
#Refine Concepts and Summary (Make Witty, Satirical)
 #      ↓
#**Apply Prompt Strategies** (e.g., character-focused, situational, etc.)
 #      ↓
#Combine Concepts & Style into Final Prompt
 #      ↓
#Feed Final Prompt into DALL-E to Generate Cartoon

# necessary imports, libraries, and dependencies    
from openai import OpenAI
import os
from dotenv import load_dotenv
import random
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set up OpenAI API key
client = OpenAI()  # This will automatically use the OPENAI_API_KEY from your environment

# generate_image_prompt() -> str: generates an image prompt based on a refined concept
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

# generate detailed style prompt
def detailed_style_prompt(summary: str) -> str:
    return f"Create a detailed style cartoon based on this concept: {summary}. The cartoon should be black and white, hand-drawn style, with a single panel. It should be witty and satirical, capturing the essence of the article in a humorous way."

def character_focused_prompt(summary: str) -> str:
    characters = ["a confused executive", "a smug academic", "a frazzled parent", "a nonchalant genz", "a tech bro"]
    character = random.choice(characters)
    return f"Draw a NewYorker Magazine Styled cartoon with unique characterizations of {character} based on this concept: {summary}. The character usually has a fellow character to interact with. Include a caption with the interaction. Minimal text is best with a punchline."

def situational_prompt(summary: str) -> str:
    situations = ["a meeting", "a classroom", "at a gallery opening", "at a restaurant", "a party", "a street"]
    situation = random.choice(situations)
    return f"Illustrate a NewYorker Magazine Styled situational cartoon based on this {situation}, where the characters are reacting to something that is happening in the Concept: {summary}. The humor should come from the juxtaposition of a serious topic with the casual setting. Use typical NewYorker Style: black and white, single panel, with sharp, witty dialogue if needed."

def metaphorical_prompt(summary: str) -> str:
    metaphors = ["a sinking ship", "a house of cards", "a tightrope walk", "a Rube Goldberg machine", "a Rubik's Cube", "a garden with both flourishing and wilting plants"]
    metaphor = random.choice(metaphors)
    return f"Create a NewYorker Magazine Styled metaphorical cartoon based on this concept: {summary} as a {metaphor}. The cartoon should be black and white, hand-drawn style, with a single panel. Possibly crosshatching, clever representation, not too on the nose, allowing the viewers to make the connection themselves."

def ironic_prompt(summary: str) -> str:
    return f"Design a NewYorker Magazine Styled ironic cartoon based on this concept: {summary}. It presents an ironic or paradoxical situation related to this concept. The irony should be subtle but clear to an informed viewer. The setting should be a mundane contrast with the profound or complex nature of the concept."

# GENERATE IMAGE - IMPORTANT SECTION BECAUSE IT CALLS THE OPENAI API FOR THE IMAGE GENERATION
def generate_image(prompt: str) -> dict:
    try:
        logger.debug(f"Sending prompt to OpenAI: {prompt}")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        logger.debug(f"Received response from OpenAI: {response}")
        return {"url": response.data[0].url}
    except Exception as e:
        logger.error(f"An error occurred while generating the image: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {e.args}")
        return None

# EXTRACT CONCEPT FROM ARTICLE
# FEEDS THE CONCEPT AS INPUT (PROMPT) TO THE IMAGE GENERATION FUNCTION
def extract_cartoon_concepts(text: str) -> str:
    logger.debug(f"Extracting concepts from text using OpenAI: {text[:100]}...")  # Log first 100 characters
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract key cartoon concepts from the given article. Focus on themes that can be satirized or visualized in a cartoon."},
                {"role": "user", "content": text}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        concept = response.choices[0].message.content.strip()
        logger.debug(f"Extracted concept from OpenAI: {concept}")
        return concept
    except Exception as e:
        logger.error(f"Error extracting concept using OpenAI: {str(e)}")
        return "Error extracting concept"

def refine_concept_for_humor(concept: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Refine this concept to make it witty, satirical, and appropriate for a single-panel New Yorker cartoon."},
                {"role": "user", "content": concept}
            ],
            max_tokens=100,
            temperature=0.7,
        )
        refined_concept = response.choices[0].message.content.strip()
        logger.debug(f"Refined concept for humor: {refined_concept}")
        return refined_concept
    except Exception as e:
        logger.error(f"Error refining concept for humor: {str(e)}")
        return concept  # Return the original if an error occurs

def generate_cartoon(text: str) -> dict:
    try:
        logger.debug(f"Generating cartoon for text: {text[:100]}...")
        
        concept = extract_cartoon_concepts(text)
        logger.debug(f"Extracted concept: {concept}")
        
        refined_concept = refine_concept_for_humor(concept)
        logger.debug(f"Refined concept: {refined_concept}")
        
        prompt = generate_image_prompt(refined_concept)
        logger.debug(f"Generated prompt: {prompt}")
        
        image_response = generate_image(prompt)
        if image_response:
            return {
                "image_url": image_response['url'],
                "concept": refined_concept,
                "prompt": prompt
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