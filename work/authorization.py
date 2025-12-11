import math
import time

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import EMAIL, PASSWORD

links = [
    "https://stepik.org/lesson/236895/step/1",
    "https://stepik.org/lesson/236896/step/1",
    "https://stepik.org/lesson/236897/step/1",
    "https://stepik.org/lesson/236898/step/1",
    "https://stepik.org/lesson/236899/step/1",
    "https://stepik.org/lesson/236903/step/1",
    "https://stepik.org/lesson/236904/step/1",
    "https://stepik.org/lesson/236905/step/1",
]


def login(browser, link, email, password):
    # 1. открываем страницу с параметром auth=login
    login_url = link + "?auth=login"
    browser.get(login_url)

    # 2. ждём поля логина/пароля и вводим их
    email_input = WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located((By.ID, "id_login_email"))
    )
    email_input.clear()
    email_input.send_keys(email)

    password_input = browser.find_element(By.ID, "id_login_password")
    password_input.clear()
    password_input.send_keys(password)

    browser.find_element(By.CSS_SELECTOR, "button.sign-form__btn").click()

    # 3. ждём, пока модалка исчезнет (означает, что мы залогинились)
    WebDriverWait(browser, 30).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-dialog"))
    )


@pytest.mark.parametrize("link", links)
def test_alien_message(browser, link):
    # сначала логинимся под нужным аккаунтом
    login(browser, link, EMAIL, PASSWORD)

    # теперь открываем сам шаг задания уже авторизованными
    browser.get(link)

    try:
        textarea = WebDriverWait(browser, 30).until(
           EC.element_to_be_clickable(
             (By.CSS_SELECTOR, "textarea.ember-text-area")
        )
    )
    except TimeoutException:
        pytest.fail(f"Не дождались textarea на странице: {link}")

    answer = math.log(int(time.time()))
    textarea.clear()
    textarea.send_keys(str(answer))

    browser.find_element(
        By.CSS_SELECTOR, "button.submit-submission"
    ).click()

    feedback = WebDriverWait(browser, 30).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".smart-hints__hint")
        )
    )

    feedback_text = feedback.text
    print(link, "→", feedback_text)
    assert feedback_text == "Correct!", f"Получен текст: '{feedback_text}'"
