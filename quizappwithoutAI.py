import random
import time

class SimpleQuiz:
    def __init__(self):
        self.question_bank = {
            "Python": [
                {
                    "question": "What is the output of: print(2 + 3 * 4)?",
                    "options": ["14", "20", "32", "Error"],
                    "correct": 0,
                    "explanation": "Python follows PEMDAS - multiplication happens before addition."
                },
                {
                    "question": "Which of these is NOT a Python data type?",
                    "options": ["List", "Array", "Tuple", "Dictionary"],
                    "correct": 1,
                    "explanation": "Array is not a built-in Python data type. Python uses Lists instead."
                },
                {
                    "question": "How do you create an empty list in Python?",
                    "options": ["list()", "[]", "Both A and B", "{}"],
                    "correct": 2,
                    "explanation": "Both list() and [] create empty lists in Python."
                }
            ],
            "History": [
                {
                    "question": "Which ancient wonder was located in Egypt?",
                    "options": ["Colossus of Rhodes", "Great Pyramid of Giza", "Hanging Gardens", "Temple of Artemis"],
                    "correct": 1,
                    "explanation": "The Great Pyramid of Giza was built around 2560 BCE."
                },
                {
                    "question": "Who was the first President of the United States?",
                    "options": ["Thomas Jefferson", "John Adams", "Benjamin Franklin", "George Washington"],
                    "correct": 3,
                    "explanation": "George Washington served as the first President from 1789 to 1797."
                }
            ],
            "Science": [
                {
                    "question": "What is the chemical symbol for gold?",
                    "options": ["Ag", "Fe", "Au", "Cu"],
                    "correct": 2,
                    "explanation": "Au comes from the Latin word for gold, 'aurum'."
                },
                {
                    "question": "Which planet is known as the Red Planet?",
                    "options": ["Venus", "Mars", "Jupiter", "Mercury"],
                    "correct": 1,
                    "explanation": "Mars appears red due to iron oxide (rust) on its surface."
                },
                {
                    "question": "What is the hardest natural substance?",
                    "options": ["Diamond", "Ruby", "Iron", "Titanium"],
                    "correct": 0,
                    "explanation": "Diamond ranks 10 on the Mohs scale of mineral hardness."
                }
            ]
        }
        self.score = 0
        self.total_questions = 0

    def display_categories(self):
        print("\nAvailable Categories:")
        for i, category in enumerate(self.question_bank.keys(), 1):
            print(f"{i}. {category}")

    def get_category_choice(self):
        categories = list(self.question_bank.keys())
        while True:
            try:
                choice = int(input("\nChoose a category number: "))
                if 1 <= choice <= len(categories):
                    return categories[choice - 1]
                print(f"Please enter a number between 1 and {len(categories)}")
            except ValueError:
                print("Please enter a valid number")

    def get_num_questions(self, category):
        max_questions = len(self.question_bank[category])
        while True:
            try:
                num = int(input(f"\nHow many questions would you like? (1-{max_questions}): "))
                if 1 <= num <= max_questions:
                    return num
                print(f"Please enter a number between 1 and {max_questions}")
            except ValueError:
                print("Please enter a valid number")

    def run_quiz(self):
        print("\n=== Welcome to the Simple Quiz! ===")
        
        # Get category choice
        self.display_categories()
        category = self.get_category_choice()
        
        # Get number of questions
        num_questions = self.get_num_questions(category)
        
        # Get random questions from chosen category
        questions = random.sample(self.question_bank[category], num_questions)
        
        print(f"\nStarting {category} Quiz!")
        print("=======================")
        
        for i, q in enumerate(questions, 1):
            # Display question
            print(f"\nQuestion {i}: {q['question']}")
            print("\nOptions:")
            for idx, option in enumerate(q['options'], 1):
                print(f"{idx}. {option}")
            
            # Get answer
            while True:
                try:
                    answer = int(input("\nYour answer (1-4): "))
                    if 1 <= answer <= 4:
                        break
                    print("Please enter a number between 1 and 4")
                except ValueError:
                    print("Please enter a valid number")
            
            # Check answer
            if answer - 1 == q['correct']:
                print("\n✅ Correct!")
                self.score += 1
            else:
                print("\n❌ Wrong!")
                print(f"The correct answer was: {q['options'][q['correct']]}")
            
            # Show explanation
            print(f"Explanation: {q['explanation']}")
            time.sleep(1)
            
        # Show final results
        print("\n=== Quiz Complete! ===")
        print(f"Your score: {self.score}/{num_questions}")
        percentage = (self.score / num_questions) * 100
        print(f"Percentage: {percentage:.1f}%")

if __name__ == "__main__":
    quiz = SimpleQuiz()
    quiz.run_quiz()