import os
from PIL import Image
os.chdir(os.path.dirname(os.path.realpath(__file__)))  # Set the current directory to the folder where the script is located

def display_images(image_paths):
    """Open multiple images in external viewers."""
    if not image_paths:
        return  # No images to display
    for path in image_paths:
        try:
            # Debugging: print the current working directory
            print(f"Current working directory: {os.getcwd()}")
            
            # Build the full path relative to the current directory
            full_path = os.path.join("images", path)  # Images folder is "images"
            print(f"Opening image: {full_path}")  # Debugging: Print the image path
            image = Image.open(full_path)
            image.show()  # Opens the image in the default image viewer
        except FileNotFoundError:
            print(f"Error: Image file '{path}' not found.")

def main():
    # List of questions, some with multiple images
    questions = [
        {
            "question": "What does this sign mean?",
            "options": [
                "A. Hump bridge",
                "B. Humps in the road",
                "C. Entrance to tunnel",
                "D. Soft verges"
            ],
            "images": ["curvedarrowmarking.gif", "instrumentpanel1.gif"],  # List of image paths
            "answer": "D"  # Example correct answer
        },
        {
            "question": "What should you do when you're approaching traffic lights that have red and amber showing together?",
            "options": [
                "A. Pass the lights if the road is clear",
                "B. Take care because there's a fault with the lights",
                "C. Wait for the green light",
                "D. Stop because the lights are changing to red"
            ],
            "images": None,  # No images for this question
            "answer": "D"  # Example correct answer
        }
    ]

    score = 0  # Initialize score
    print("Welcome to the Driving Theory Quiz!\n")

    while True:  # Main loop
        for i, q in enumerate(questions, 1):
            print(f"Question {i}: {q['question']}")
            
            # Display images if available
            if q.get("images"):
                print("Opening images for this question...")
                display_images(q["images"])
            
            for option in q['options']:
                print(option)
            user_answer = input("Enter the letter of your answer: ").strip().upper()
            if user_answer == q['answer']:
                print("Correct!\n")
                score += 1
            else:
                print(f"Wrong. The correct answer was {q['answer']}.\n")

        print(f"Quiz finished! Your score: {score}/{len(questions)}")
        retry = input("Would you like to try again? (yes/no): ").strip().lower()
        if retry != "yes":
            print("Thanks for playing! Goodbye!")
            break

        # Wait for the user to close the image viewer before continuing
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()