from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re
import time

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

link = "https://twitter.com/i/flow/login"
messagebox_link = "https://twitter.com/messages"
message_request_link = "https://twitter.com/messages/requests"
driver.get(link)
# soup = BeautifulSoup(driver.page_source, 'lxml')
wait = WebDriverWait(driver, 10)

twitter_username = "Ata_Procat"
twitter_password = "Penguen123"


# Clicking accept button to chat with foreign person
def click_accept_foreign_message():
    try:
        accept_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Accept']"))
        )
        accept_button.click()

        _ = wait.until(
            EC.url_contains("https://twitter.com/messages/")
        )
    except:
        print("Error of accepting a message from the foreign people")
        driver.quit()


# Login Twitter account automatically
def login(username, password):
    # Enter the username
    try:
        login_label = wait.until(
            EC.element_to_be_clickable((By.TAG_NAME, "input"))
        )
        # driver.find_element(By.TAG_NAME, "input")
        login_label.click()
        login_label.send_keys(username)
        login_label.send_keys(Keys.ENTER)
    except:
        print("Login page Error")
        driver.quit()

    # Enter the password
    try:
        password_label = wait.until(
            EC.element_to_be_clickable((By.NAME, "password"))
        )
        # password_label = driver.find_element(By.NAME, "password")
        password_label.click()
        password_label.send_keys(password)
        password_label.send_keys(Keys.ENTER)
    except:
        print("Login password Error")
        driver.quit()

        # Login Check

    try:
        _ = wait.until(
            EC.url_matches("https://twitter.com/home")
        )
    except:
        print("Login did not successfully done.")
        driver.quit()


### write a funct. that gets the other user's messages
def get_messages_from_req():
    # Open message requests link
    try:
        driver.get(messagebox_link)
        message_req_label = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/messages/requests']"))
        )
        message_req_label.click()
    except:
        print("Opening message request link Error")
        driver.quit()

    # Check if the message request page opened successfully
    try:
        _ = wait.until(
            EC.url_matches(message_request_link)
        )
    except:
        print("Message requests link cannot be opened successfully.")
        driver.quit()

    # Click the new message label
    try:
        new_message_label = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Timeline: Message requests']"))
        )
        new_message_label.click()
    except:
        print("Opening new message Error")
        driver.quit()

    # Click accept button if there is one to accept the foreign message
    click_accept_foreign_message()


# Return an array of messages that we get
def get_message_from_chat():
    try:
        driver.get(messagebox_link)
        chat_label = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='tablist']/div[2]"))
        )
        chat_label.click()

        soup = BeautifulSoup(driver.page_source, 'lxml')

        time.sleep(2)

        message_texts = []  # To hold messages
        all_divs = soup.find_all("div", {"data-testid": "cellInnerDiv"})
        for div in all_divs:
            temp_div = div.find("div", {"data-testid": "messageEntry"}) # !!!! Div içindeki istenilen yeni div e erişilemiyor !!!
            if (temp_div != None):
                temp_div = temp_div.find("div", {"role": "presentation"})  # !!!
                temp_div = temp_div.find("div", {"data-testid": "tweetText"})  # !!!
                message_texts.append(temp_div.find("span").get_text())

        return message_texts
    except:
        print("Error while getting message from the chat")
        driver.quit()


### write a funct. that reply the messages of the other user


login(twitter_username, twitter_password)

# get_messages_from_req()

arr_message = get_message_from_chat()

for i in arr_message:
    print(i)
