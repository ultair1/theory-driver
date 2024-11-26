import json
import os
import subprocess
import time
from PIL import Image

def load_questions(file_path):
    """Load questions from a JSON file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def resize_images(images, target_width, target_height):
    """Resize all images to a fixed size."""
    resized_images = []
    for img in images:
        resized_images.append(img.resize((target_width, target_height)))  # Resize image
    return resized_images

def combine_images(image_paths, target_width, target_height):
    """Combine multiple resized images side by side."""
    images = []
    for path in image_paths:
        try:
            full_path = os.path.join("images", path)
            image = Image.open(full_path)
            images.append(image)
        except FileNotFoundError:
            print(f"Error: Image file '{path}' not found.")
            return None

    # Resize images to the same size before combining
    resized_images = resize_images(images, target_width, target_height)

    # Combine images side by side
    total_width = sum(img.width for img in resized_images)
    max_height = max(img.height for img in resized_images)

    combined_image = Image.new("RGB", (total_width, max_height))

    # Paste images side by side
    current_width = 0
    for img in resized_images:
        combined_image.paste(img, (current_width, 0))
        current_width += img.width

    # Save the combined image to a temporary file
    combined_image_path = "combined_image.png"
    combined_image.save(combined_image_path)

    return combined_image_path

def display_images(image_paths):
    """Open combined image in MS Paint."""
    combined_image_path = combine_images(image_paths, target_width=200, target_height=200)  # Resize all images to 200x200
    if combined_image_path:
        subprocess.Popen(["mspaint", combined_image_path])  # Open combined image in MS Paint

def main():
    questions = load_questions("questions.json")

    if not questions:
        print("No questions available. Exiting.")
        return

    while True:
        score = 0
        print("Welcome to the Driving Theory Quiz!\n")

        for i, q in enumerate(questions, 1):
            print(f"Question {i}: {q['question']}")

            # Display images (if any) for the current question
            if q.get("images"):
                print("Displaying images for this question...")
                display_images(q["images"])

                # Wait for a moment to allow the user to view the images
                time.sleep(2)

            # Display question options
            for option in q["options"]:
                print(option)

            user_answer = input("Enter the letter of your answer: ").strip().upper()

            if user_answer == q["answer"]:
                print("Correct!\n")
                score += 1
            else:
                print(f"Wrong. The correct answer was {q['answer']}.\n")

        print(f"Quiz finished! Your score: {score}/{len(questions)}")
        retry = input("Would you like to try again? (yes/no): ").strip().lower()
        if retry != "yes":
            print("Thanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
