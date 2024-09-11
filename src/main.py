# Summary of the main.py file:
# necessary imports, libraries, and dependencies
import os
import time
from image_generator_2 import read_article_from_file, generate_cartoon

# main() -> None: orchestrates the entire process of generating a cartoon
### purpose: to generate a cartoon based on the article text
### input: article text
### process: 
###   1. prints a welcome message
###   2. prompts the user to enter the article text
###   3. calls the generate_cartoon function with the article text
###   4. prints the result  

def main():
    print("Welcome to the New Yorker Style Cartoon Generator!")
    filename = input("Please enter the article filename (in the 'articles' folder): ")
    filename = os.path.join('articles', filename)

    try:
        article_text = read_article_from_file(filename)
        
        # count the time while it generates (optional and not necessary for the function to work)   
        print("Generating your cartoon...")
        
        start_time = time.time()
        spinner = "|/-\\"
        i = 0
        while time.time() - start_time < 30:  # Assuming a 30-second timeout
            print(f"\rPlease wait {spinner[i % len(spinner)]}", end="", flush=True)
            time.sleep(0.1)
            i += 1
        print("\rGeneration complete!     ")
        print("-" * 100) # divider  

        # generate cartoon and print the result 
        result = generate_cartoon(article_text) 
        print("-" * 100) # divider 

        if "error" in result:
            print(f"Article Related Error: {result['error']}")
        else:
            print(f"HOPE YOU LIKE IT!")
            print("-" * 100)  # divider
            print(f"Image URL: {result['image_url']}")
            print("-" * 100)  # divider
            print(f"Concept: {result['concept']}")  
            print("-" * 100)  # divider
            print(f"Prompt: {result['prompt']}")  # Add this line to display the generated prompt
            print("-" * 100)  # divider

    except FileNotFoundError:
        print("Filename not found. Please check the filename and try again.") # Error is printed here if the file is not found
    except Exception as e:
        print(f"Code Error:{e}") # Error is printed here if there is an error in the code   
    
if __name__ == "__main__":
    main()