import requests
import time
import re
import json
import openai
import pyautogui
import warnings
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.keys import Keys

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

    # Configure Edge options for headless browsing
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # Add any other desired options here

    # Specify the path to the msedgedriver executable (replace with your actual path)
    webdriver_path = 'http://go.microsoft.com/fwlink/?LinkId=619687'

    # Create the Edge WebDriver instance
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        driver = Edge(options=options, executable_path=webdriver_path)

    # Open the website in the headless browser
    driver.get(website_url)

    # Wait for the website to load
    time.sleep(5)

    # Find the answer input field on the website using its HTML attribute or CSS selector
    answer_field = driver.find_element_by_id('answer-input')

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

        # Type the answer into the answer input field on the website
        answer_field.clear()
        answer_field.send_keys(answer)

        # Submit the answer by pressing Enter
        answer_field.send_keys(Keys.RETURN)

        # Scroll down to the next question
        pyautogui.press('pagedown')
        time.sleep(0.5)

    # Close the web browser
    driver.quit()

    # Wait for half an hour before checking for new questions again
    time.sleep(1800)
