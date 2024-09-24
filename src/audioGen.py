import os
import logging
from openai import OpenAI
from pydub import AudioSegment
import time

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set up OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("No OpenAI API key found in environment variables")

client = OpenAI(api_key=openai_api_key)

def generate_news_script(article_text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a news script writer. Convert the given article into a dialogue between two news anchors discussing the main points. Keep it concise and engaging."
                },
                {"role": "user", "content": article_text}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating news script: {str(e)}")
        return ""

def generate_audio(script: str, voice: str) -> str:
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=script
        )
        
        output_path = f"static/audio/{voice}_{int(time.time())}.mp3"
        with open(output_path, "wb") as audio_file:
            audio_file.write(response.content)
        
        return output_path
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        return ""

def combine_audio_files(file1: str, file2: str) -> str:
    try:
        audio1 = AudioSegment.from_mp3(file1)
        audio2 = AudioSegment.from_mp3(file2)
        
        combined = AudioSegment.empty()
        for a1, a2 in zip(audio1, audio2):
            combined += a1
            combined += a2
        
        output_path = f"static/audio/combined_{int(time.time())}.mp3"
        combined.export(output_path, format="mp3")
        return output_path
    except Exception as e:
        logger.error(f"Error combining audio files: {str(e)}")
        return ""

def generate_news_audio(article_text: str) -> dict:
    try:
        script = generate_news_script(article_text)
        if not script:
            return {"error": "Failed to generate script"}
        
        # Split script for two voices
        lines = script.split('\n')
        voice1_lines = [line for i, line in enumerate(lines) if i % 2 == 0]
        voice2_lines = [line for i, line in enumerate(lines) if i % 2 != 0]
        
        voice1_audio = generate_audio('\n'.join(voice1_lines), "alloy")
        voice2_audio = generate_audio('\n'.join(voice2_lines), "echo")
        
        if not voice1_audio or not voice2_audio:
            return {"error": "Failed to generate audio"}
        
        combined_audio = combine_audio_files(voice1_audio, voice2_audio)
        if not combined_audio:
            return {"error": "Failed to combine audio files"}
        
        return {
            "audio_url": f"/audio/{os.path.basename(combined_audio)}",
            "script": script
        }
    except Exception as e:
        logger.error(f"Error in generate_news_audio: {str(e)}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
