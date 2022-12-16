from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup
import time


from zemberek import (
    TurkishSpellChecker,
    TurkishSentenceNormalizer,
    TurkishSentenceExtractor,
    TurkishMorphology,
    TurkishTokenizer
)

service = ChromeService(executable_path=ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--window-size=1024,768')
# options.add_argument("--no-sandbox")
# options.headless = True
driver = webdriver.Chrome(service=service, options=options)
time.sleep(1)
link = "https://twitter.com/i/flow/login"
messagebox_link = "https://twitter.com/messages"
message_request_link = "https://twitter.com/messages/requests"
driver.get(link)
# soup = BeautifulSoup(driver.page_source, 'lxml')
wait = WebDriverWait(driver, 10)

twitter_username = "***"
twitter_password = "***"


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


# Function that gets the other user's messages
def accept_messages_from_req():
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

# check is there any new message by using "len"
def check_number_of_div_on_messagebox(old_len):
    new_len = len(driver.find_elements(By.XPATH, "//div[@role='tablist']/div"))
    print(new_len)
    diff_len = 0
    if old_len != new_len:
        diff_len = new_len - old_len
    return new_len, diff_len

# open a specific message by the index of the element's div
def open_messagebox(index_for_message_box_dix, refresh_link=True):
    try:
        if (refresh_link == True):
            driver.get(messagebox_link)
        time.sleep(1)
        chat_label = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@role='tablist']/div[{2+index_for_message_box_dix}]"))
        )
        chat_label.click()
    except Exception as e:
        print(e)
        print("Error while opening messagebox")
        driver.quit()


# Return an array of messages that we get
def get_message_from_chat():
    try:
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        message_texts = []  # To hold messages
        all_divs = soup.find_all("div", {"data-testid": "cellInnerDiv"})
        for div in all_divs:
            temp_div = div.find("div", {"data-testid": "messageEntry"})
            if (temp_div != None):
                temp_div = temp_div.find("div", {"role": "presentation"})  # !!!
                temp_div = temp_div.find("div", {"data-testid": "tweetText"})  # !!!
                message_texts.append(temp_div.find("span").get_text())

        return message_texts
    except Exception as e:
        print(e)
        print("Error while getting message from the chat")
        driver.quit()


# Function that reply the messages of the other user
def reply_message(message):
    try:
        _ = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='DraftEditor-editorContainer']"))
        )
        reply_message_box = driver.find_element(By.XPATH, "//div[@data-contents='true']/div/div/span")
        reply_message_box.send_keys(message)
        reply_message_box.send_keys(Keys.ENTER)
    except Exception as e:
        print(e)



login(twitter_username, twitter_password)

morphology = TurkishMorphology.create_with_defaults()
normalizer = TurkishSentenceNormalizer(morphology)

# get_messages_from_req()
open_messagebox(2)
last_list = []
mes_index = 0
new_len = 0
dif_len = 0
while True:
    new_len, diff_len = check_number_of_div_on_messagebox(new_len)
    if diff_len != 0:  # check is there is new message
        for i in range(diff_len):  # loop over the new messages and reply them
            open_messagebox(i, False)
            arr_message = get_message_from_chat()
            mess_len = len(arr_message)
            if mess_len >= 1:
                if last_list != arr_message:
                    message = "Merhaba size nasıl yardımcı olabilirim?"  # our reply message text
                    reply_message(message)
                    arr_message.append(message)
                    last_list = arr_message
                    for i in arr_message[mes_index:-1]:  # loop over the new messages from a user
                        print(normalizer.normalize(i))   # fix the typos on the messages and print them
                        print(" ")
                    mes_index = mess_len

            time.sleep(15)

        time.sleep(15)


