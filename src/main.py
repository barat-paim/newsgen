from image_generator import generate_cartoon

def main():
    print("Welcome to the New Yorker Style Cartoon Generator!")
    article_text = input("Please enter the article text: ")
    
    result = generate_cartoon(article_text)
    
    if "error" in result:
        print(f"An error occurred: {result['error']}")
    else:
        print(f"Cartoon generated successfully!")
        print(f"Prompt used: {result['prompt']}")
        print(f"Image URL: {result['image_url']}")

if __name__ == "__main__":
    main()