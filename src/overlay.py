import os
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import math

# Get the absolute path to the font files
font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'fonts', 'Caslon.otf')
italic_font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'fonts', 'CaslonItalic.ttf')

def add_caption_to_image(image_url: str, caption: str, output_path: str):
    try:
        # Download the image
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        
        # Create a drawing context
        draw = ImageDraw.Draw(image)
        
        # Choose the Irvin font and size
        try:
            if os.path.exists(italic_font_path):
                font = ImageFont.truetype(italic_font_path, size=24)
            else:
                font = ImageFont.truetype(font_path, size=24)
                print("Italic font not found. Using regular font with simulated italics.")
        except IOError:
            print(f"Irvin font not found. Using default font.")
            font = ImageFont.load_default()
        
        # Calculate text size
        text_bbox = draw.textbbox((0, 0), f'"{caption}"', font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Image dimensions
        image_width, image_height = image.size
        
        # Position the text at the bottom center
        x = (image_width - text_width) / 2
        y = image_height - text_height - 20  # 20 pixels from the bottom
        
        # Add a semi-transparent white background
        background_shape = [(0, y - 10), (image_width, image_height)]
        draw.rectangle(background_shape, fill=(255, 255, 255, 200))
        
        # Add the caption text
        if not os.path.exists(italic_font_path):
            # Simulate italics by shearing the text
            shear_factor = 0.3
            w, h = font.getsize(f'"{caption}"')
            m = Image.new('RGBA', (int(w + h*shear_factor), h), (0, 0, 0, 0))
            ImageDraw.Draw(m).text((0, 0), f'"{caption}"', font=font, fill=(0, 0, 0, 255))
            m = m.transform((int(w + h*shear_factor), h), Image.AFFINE, (1, shear_factor, 0, 0, 1, 0), Image.BICUBIC)
            image.paste(m, (int(x), int(y)), m)
        else:
            draw.text((x, y), f'"{caption}"', font=font, fill=(0, 0, 0, 255))
        
        # Save the edited image
        image.save(output_path)
        print(f"Image saved with caption at: {output_path}")
    except Exception as e:
        print(f"Error adding caption to image: {str(e)}")

# Test function
def test_add_caption_to_image():
    image_url = 'https://via.placeholder.com/800x600.png?text=Sample+Image'
    caption = "What I Did During My Summer Flight Delays."
    output_path = 'test_image_with_caption.png'
    add_caption_to_image(image_url, caption, output_path)

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    test_add_caption_to_image()
