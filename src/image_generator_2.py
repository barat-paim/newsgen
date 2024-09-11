# Summary: High Level Design
# 1. Generate a random number between 1 and 4
# 2. Select the corresponding prompt strategy based on the random number
# 3. Generate the image prompt using the selected strategy
# 4. Return the generated image prompt  

#necessary imports, libraries, and dependencies 
from openai import OpenAI   
from dotenv import load_dotenv
import os   
import random
from image_generator import read_article_from_file, generate_image, extract_cartoon_concepts

# Load environment variables
load_dotenv()

# Set up OpenAI API key
client = OpenAI()  # This will automatically use the OPENAI_API_KEY from your environment

def generate_image_prompt(summary: str) -> str:
    prompt_strategies = [
        detailed_style_prompt,
        character_focused_prompt,
        situational_prompt,
        metaphorical_prompt,
        ironic_prompt
    ]
    
    # Randomly select two strategies and combine them
    selected_strategies = random.sample(prompt_strategies, 2)
    combined_prompt = " ".join(strategy(summary) for strategy in selected_strategies)
    
    return combined_prompt

def detailed_style_prompt(summary: str) -> str:
    return f"Create a New Yorker style cartoon based on this concept: {summary}. The cartoon should be black and white, with a hand-drawn style featuring fine, precise linework. Include subtle crosshatching for shading. The scene should be set in a typical New Yorker environment like a city apartment, office, or cafe. Incorporate witty and satirical elements that capture the essence of the article in a humorous way."

def character_focused_prompt(summary: str) -> str:
    characters = ["a confused executive", "a smug academic", "a frazzled parent", "a nonchalant millennial", "a perplexed scientist"]
    character = random.choice(characters)
    return f"Draw a New Yorker cartoon featuring {character} reacting to the following situation: {summary}. The character's expression and body language should convey their attitude towards the concept. Include minimal background details to focus on the character's reaction."

def situational_prompt(summary: str) -> str:
    situations = ["at a dinner party", "in a board meeting", "at a art gallery opening", "during a family gathering", "in a therapy session"]
    situation = random.choice(situations)
    return f"Illustrate a New Yorker style cartoon set {situation}, where the characters are discussing or reacting to this concept: {summary}. The humor should come from the juxtaposition of the serious topic with the casual setting. Use typical New Yorker style: black and white, single panel, with sharp, witty dialogue if needed."

def metaphorical_prompt(summary: str) -> str:
    metaphors = ["a sinking ship", "a house of cards", "a tightrope walk", "a Rube Goldberg machine", "a garden with both flourishing and wilting plants"]
    metaphor = random.choice(metaphors)
    return f"Create a New Yorker cartoon that metaphorically represents the concept of '{summary}' as {metaphor}. The cartoon should be in classic black and white style, with clean lines and possibly some crosshatching. The metaphor should be clever and not too on-the-nose, allowing viewers to make the connection themselves."

def ironic_prompt(summary: str) -> str:
    return f"Design a New Yorker style cartoon that presents an ironic or paradoxical situation related to this concept: {summary}. The irony should be subtle but clear to an informed viewer. Use black and white imagery with clean, precise lines. The setting should be mundane to contrast with the profound or complex nature of the concept."


# generarte cartoon
def generate_cartoon(text: str) -> dict:
    try:
        concept = extract_cartoon_concepts(text)
        prompt = generate_image_prompt(concept)
        print(f"Generated prompt: {prompt}")
        print(f"*" * 100)
        
        # Add this line to check the prompt
        print(f"Prompt being sent to API: {prompt}")
        
        image_response = generate_image(prompt)
        if image_response:
            return {
                "image_url": image_response['url'],
                "concept": concept,
                "prompt": prompt
            }
        else:
            return {"error": "Failed to generate image"}
    except Exception as e:
        return {"error": str(e)}
    

# Example usage
if __name__ == "__main__":
    test_summary = "The increasing reliance on AI in everyday decision-making"
    prompt = generate_image_prompt(test_summary)
    print(prompt)