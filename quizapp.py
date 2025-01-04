import random
import json
import html
import requests
import time

class TriviaQuizApp:
    def __init__(self):
        self.questions = []
        self.score = 0
        self.total_questions = 0
        
    def get_categories(self):
        """Fetch available categories from the Open Trivia Database"""
        try:
            response = requests.get("https://opentdb.com/api_category.php")
            if response.status_code == 200:
                return response.json()['trivia_categories']
            return None
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return None

    def display_categories(self):
        """Display all available categories"""
        categories = self.get_categories()
        if categories:
            print("\nAvailable Categories:")
            print("0. Any Category (Random)")
            for cat in categories:
                print(f"{cat['id']}. {cat['name']}")
            return categories
        return None

    def fetch_questions(self, num_questions: int = 5, category_id: int = None, difficulty: str = "medium"):
        """Fetch questions from Open Trivia Database API"""
        url = "https://opentdb.com/api.php"
        params = {
            "amount": num_questions,
            "type": "multiple"
        }
        if category_id and category_id > 0:
            params["category"] = category_id
        if difficulty in ["easy", "medium", "hard"]:
            params["difficulty"] = difficulty

        try:
            response = requests.get(url, params=params)
            data = response.json()
            if data['response_code'] == 0:  # Success
                return data['results']
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_category_choice(self, categories):
        """Get user's category choice"""
        while True:
            try:
                choice = int(input("\nChoose a category number: "))
                if choice == 0:
                    return None
                for cat in categories:
                    if cat['id'] == choice:
                        return choice
                print("Please select a valid category number.")
            except ValueError:
                print("Please enter a valid number.")

    def run_quiz(self):
        print("\n=== Welcome to the Trivia Quiz! ===\n")
        
        # Show categories and get user's choice
        categories = self.display_categories()
        if not categories:
            print("Failed to fetch categories. Using random categories instead.")
            category_id = None
        else:
            category_id = self.get_category_choice(categories)
        
        # Get user preferences for number of questions
        while True:
            try:
                num_questions = int(input("\nHow many questions would you like? (1-50): "))
                if 1 <= num_questions <= 50:
                    break
                print("Please enter a number between 1 and 50.")
            except ValueError:
                print("Please enter a valid number.")

        # Fetch questions
        questions_data = self.fetch_questions(num_questions, category_id)
        
        if not questions_data:
            print("Failed to fetch questions. Please try again.")
            return

        # Start the quiz
        score = 0
        for i, q in enumerate(questions_data, 1):
            # Clean up the text
            question = html.unescape(q['question'])
            correct_answer = html.unescape(q['correct_answer'])
            incorrect_answers = [html.unescape(ans) for ans in q['incorrect_answers']]
            
            # Create options list and shuffle it
            options = incorrect_answers + [correct_answer]
            random.shuffle(options)
            
            # Display question and options
            print(f"\nQuestion {i}: {question}")
            print("\nOptions:")
            for idx, option in enumerate(options, 1):
                print(f"{idx}. {option}")
            
            # Get user's answer
            while True:
                try:
                    answer = int(input("\nYour answer (1-4): "))
                    if 1 <= answer <= 4:
                        break
                    print("Please enter a number between 1 and 4.")
                except ValueError:
                    print("Please enter a valid number.")
            
            # Check if answer is correct
            user_answer = options[answer - 1]
            if user_answer == correct_answer:
                print("\n✅ Correct!")
                score += 1
            else:
                print("\n❌ Wrong!")
                print(f"The correct answer was: {correct_answer}")
            
            # Show category and difficulty
            print(f"Category: {q['category']}")
            print(f"Difficulty: {q['difficulty'].capitalize()}")
            time.sleep(1)  # Brief pause between questions

        # Show final results
        print("\n=== Quiz Complete! ===")
        print(f"Your score: {score}/{num_questions}")
        percentage = (score / num_questions) * 100
        print(f"Percentage: {percentage:.1f}%")

if __name__ == "__main__":
    quiz = TriviaQuizApp()
    quiz.run_quiz()