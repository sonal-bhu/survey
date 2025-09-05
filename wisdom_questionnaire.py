#!/usr/bin/env python3
"""
WISDOM Research Survey Questionnaire
Psychology Research Tool

This questionnaire assesses wisdom-related traits and behaviors.
Responses are saved to CSV format for statistical analysis.
"""

import csv
import os
from datetime import datetime
from typing import Dict, List

class WisdomQuestionnaire:
    def __init__(self):
        self.questions = [
            "I enjoy creating things that are new and different.",
            "I do not have many questions.",
            "I consider the positives and negatives of every option when I am making a decision.",
            "If there is a chance to learn something new, I jump right in.",
            "Others tell me that I give good advice.",
            "I see myself as a very creative person.",
            "I am curious about how things work.",
            "I carefully think about the opinions of others before I make a decision.",
            "I get excited when I see there is something new to learn.",
            "My friends ask for my opinion before they make an important decision.",
            "I often figure out different ways of doing things.",
            "I frequently ask questions.",
            "I wait until I have all the facts before I make a decision.",
            "I love learning about how to do different things.",
            "People tell me that I am a wise person.",
            "I always like to do things in different ways.",
            "I am always full of questions.",
            "I think about all my choices before I make a decision.",
            "When I want to learn something, I try to find out everything about it.",
            "I am able to solve problems in a way that is pleasing to everyone."
        ]
        
        self.response_options = {
            '5': 'Very Much Like Me',
            '4': 'Mostly Like Me',
            '3': 'Somewhat Like Me',
            '2': 'A Little Like Me',
            '1': 'Not Like Me At All'
        }
        
        self.responses = {}
        self.participant_info = {}

    def display_welcome(self):
        """Display welcome message and instructions"""
        print("=" * 70)
        print("                    WISDOM RESEARCH SURVEY")
        print("=" * 70)
        print("\nWelcome to the WISDOM questionnaire!")
        print("\nThis survey consists of 20 questions about your thoughts, behaviors,")
        print("and attitudes. Please read each statement carefully and select the")
        print("response that best describes how much each statement is like you.")
        print("\nResponse Options:")
        for key, value in self.response_options.items():
            print(f"  {key} - {value}")
        print("\nPlease be honest in your responses. There are no right or wrong answers.")
        print("Your responses will be kept confidential and used for research purposes only.")
        print("-" * 70)

    def collect_participant_info(self):
        """Collect basic participant information"""
        print("\nParticipant Information (Optional - you may skip any question):")
        
        self.participant_info['participant_id'] = input("Participant ID (or press Enter to auto-generate): ").strip()
        if not self.participant_info['participant_id']:
            self.participant_info['participant_id'] = f"P_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.participant_info['age'] = input("Age (or press Enter to skip): ").strip()
        self.participant_info['gender'] = input("Gender (or press Enter to skip): ").strip()
        self.participant_info['education'] = input("Highest level of education (or press Enter to skip): ").strip()
        self.participant_info['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\nThank you! Your participant ID is: {self.participant_info['participant_id']}")
        print("-" * 70)

    def administer_questionnaire(self):
        """Administer the questionnaire"""
        print("\nBeginning questionnaire...")
        print("Enter the number (1-5) that corresponds to your response.\n")
        
        for i, question in enumerate(self.questions, 1):
            print(f"Question {i}/20:")
            print(f"{question}")
            print()
            
            # Display options
            for key, value in self.response_options.items():
                print(f"  {key} - {value}")
            
            # Get response
            while True:
                response = input(f"\nYour response (1-5): ").strip()
                if response in self.response_options:
                    self.responses[f'Q{i}'] = {
                        'question': question,
                        'numeric_response': int(response),
                        'text_response': self.response_options[response]
                    }
                    break
                else:
                    print("Please enter a valid response (1-5).")
            
            print("-" * 50)

    def calculate_scores(self) -> Dict[str, float]:
        """Calculate various wisdom subscale scores"""
        # Reverse scoring for negatively worded items (Question 2)
        scores = {}
        
        # Total wisdom score
        total_score = 0
        for q_num, response in self.responses.items():
            if q_num == 'Q2':  # Reverse score for "I do not have many questions"
                total_score += (6 - response['numeric_response'])
            else:
                total_score += response['numeric_response']
        
        scores['total_wisdom_score'] = total_score
        scores['average_wisdom_score'] = total_score / len(self.questions)
        
        # Subscale scores (based on common wisdom dimensions)
        # Creativity/Innovation (Questions 1, 6, 11, 16)
        creativity_questions = ['Q1', 'Q6', 'Q11', 'Q16']
        creativity_score = sum(self.responses[q]['numeric_response'] for q in creativity_questions)
        scores['creativity_score'] = creativity_score
        
        # Curiosity/Learning (Questions 2, 4, 7, 9, 12, 14, 17, 19)
        curiosity_questions = ['Q2', 'Q4', 'Q7', 'Q9', 'Q12', 'Q14', 'Q17', 'Q19']
        curiosity_score = sum(
            (6 - self.responses['Q2']['numeric_response']) if q == 'Q2' 
            else self.responses[q]['numeric_response'] 
            for q in curiosity_questions
        )
        scores['curiosity_score'] = curiosity_score
        
        # Judgment/Decision Making (Questions 3, 8, 13, 18)
        judgment_questions = ['Q3', 'Q8', 'Q13', 'Q18']
        judgment_score = sum(self.responses[q]['numeric_response'] for q in judgment_questions)
        scores['judgment_score'] = judgment_score
        
        # Social Wisdom (Questions 5, 10, 15, 20)
        social_questions = ['Q5', 'Q10', 'Q15', 'Q20']
        social_score = sum(self.responses[q]['numeric_response'] for q in social_questions)
        scores['social_wisdom_score'] = social_score
        
        return scores

    def save_results(self, filename='wisdom_survey_results.csv'):
        """Save results to CSV file"""
        file_exists = os.path.exists(filename)
        
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['participant_id', 'timestamp', 'age', 'gender', 'education']
            fieldnames.extend([f'Q{i}_numeric' for i in range(1, 21)])
            fieldnames.extend([f'Q{i}_text' for i in range(1, 21)])
            fieldnames.extend(['total_wisdom_score', 'average_wisdom_score', 
                              'creativity_score', 'curiosity_score', 
                              'judgment_score', 'social_wisdom_score'])
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            # Prepare row data
            row_data = self.participant_info.copy()
            
            # Add question responses
            for i in range(1, 21):
                q_key = f'Q{i}'
                row_data[f'Q{i}_numeric'] = self.responses[q_key]['numeric_response']
                row_data[f'Q{i}_text'] = self.responses[q_key]['text_response']
            
            # Add calculated scores
            scores = self.calculate_scores()
            row_data.update(scores)
            
            writer.writerow(row_data)
        
        print(f"\nResults saved to: {filename}")

    def display_summary(self):
        """Display a summary of responses and scores"""
        scores = self.calculate_scores()
        
        print("\n" + "=" * 70)
        print("                      SURVEY COMPLETE!")
        print("=" * 70)
        print("\nThank you for participating in the WISDOM research survey!")
        
        print(f"\nParticipant ID: {self.participant_info['participant_id']}")
        print(f"Completion Time: {self.participant_info['timestamp']}")
        
        print("\nSUMMARY SCORES:")
        print(f"Total Wisdom Score: {scores['total_wisdom_score']}/100")
        print(f"Average Score: {scores['average_wisdom_score']:.2f}/5.00")
        
        print(f"\nSUBSCALE SCORES:")
        print(f"Creativity/Innovation: {scores['creativity_score']}/20")
        print(f"Curiosity/Learning: {scores['curiosity_score']}/40")
        print(f"Judgment/Decision Making: {scores['judgment_score']}/20")
        print(f"Social Wisdom: {scores['social_wisdom_score']}/20")
        
        print("\nNote: Higher scores indicate stronger agreement with wisdom-related traits.")
        print("Your responses have been saved for analysis.")
        print("=" * 70)

    def run_survey(self):
        """Run the complete survey process"""
        try:
            self.display_welcome()
            
            input("\nPress Enter to begin the survey...")
            
            self.collect_participant_info()
            self.administer_questionnaire()
            
            print("\nProcessing your responses...")
            self.save_results()
            self.display_summary()
            
            return True
            
        except KeyboardInterrupt:
            print("\n\nSurvey interrupted. Your responses have not been saved.")
            return False
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            return False

def main():
    """Main function to run the questionnaire"""
    survey = WisdomQuestionnaire()
    survey.run_survey()
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
