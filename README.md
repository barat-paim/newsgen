# New Yorker Style Cartoon Generator

This project generates New Yorker style cartoons based on article inputs using the DALL-E 2 API.

## Setup

## Features

- Generates New Yorker style cartoons based on article text inputs
- Uses OpenAI's DALL-E 3 API for image generation
- Extracts key concepts from the input article to create relevant cartoon prompts
- Provides a user-friendly command-line interface

## Requirements

- Python 3.x
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/new-yorker-cartoon-generator.git
   cd new-yorker-cartoon-generator
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key to the file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```


To set up the project environment:

1. Ensure you have Python 3.x installed.
2. Run the setup script:
   ```
   ./setup.sh
   ```
3. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

## Usage

[Add usage instructions here once the project is more developed]

## Project Structure

```
.
├── README.md
├── requirements.txt
├── setup.sh
├── src
│   ├── main.py
│   └── image_generator.py
└── venv
```

## Contributing

[Add contribution guidelines here if applicable]

## License

[Add license information here]

## Running the Project
1. Start the backend server (from the backend directory):
   ```
   python src/app.py
   ```
2. Start the frontend development server (from the frontend directory):
   ```
   npm start
   ```