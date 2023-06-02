import requests
import time
import re
import json
import openai
import pyautogui

# Set up your OpenAI API credentials
openai.api_key = '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'

# URL of the website containing the questions
website_url = 'https://bytexl.app/lab/3yx3zpf2z'

# Regular expression pattern to extract the questions from the website
question_pattern = r'PATTERN_TO_MATCH_QUESTIONS'

def scrape_questions(url, pattern):
    response = requests.get(url)
    html_content = response.text
    questions = re.findall(pattern, html_content)
    return questions

def generate_answers(question):
    # Set up your ChatGPT parameters
    model = 'gpt-3.5-turbo'
    max_tokens = 50
    temperature = 0.8
    top_p = 1.0

    response = openai.Completion.create(
        engine=model,
        prompt=question,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p
    )

    answer = response.choices[0].text.strip()
    return answer

# Main loop to continuously check for new questions
while True:
    questions = scrape_questions(website_url, question_pattern)

    for question in questions:
        # Scroll down to the question on the webpage using PyAutoGUI
        pyautogui.press('pagedown')
        time.sleep(0.5)

        # Capture the question text using PyAutoGUI (adjust the coordinates as per your screen resolution)
        question_box_coordinates = (x1, y1, x2, y2)  # Specify the coordinates of the question box
        question_screenshot = pyautogui.screenshot(region=question_box_coordinates)
        question_screenshot.save('question.png')

        # Read the question from the screenshot image using OCR or any other suitable library

        # Generate answer using ChatGPT
        answer = generate_answers(question)

        # Print the question and answer
        print("Question:", question)
        print("Answer:", answer)
        print("------")
        # You can save the answers to a file or perform any other desired action

        # Scroll down to the next question
        pyautogui.press('pagedown')
        time.sleep(0.5)

    # Wait for half an hour before checking for new questions again
    time.sleep(1800)
