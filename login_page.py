import allure
import time
from base_page import BasePage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv




class LoginPage(BasePage):

    # Локаторы элементов страницы
    EMAIL_INPUT = ('xpath', '//input[@name="email"]')
    PASSWORD_INPUT = ('xpath', '//input[@name="password"]')
    LOGIN_BUTTON = ('xpath', '//button[@type="submit" and (contains(.//div/text(), "Вход") or contains(.//div/text(), "Log In"))]')

    # Локатор кнопки "Сервер Диплом"
    SERVER_DIPLOM_BUTTON = ('xpath', '//div[@aria-hidden="true" and text()="СерверДилом"]')

    # Ожидаемые URL
    CHANNELS_URL = "https://discord.com/channels/@me"
    TEST_CHANNEL_URL = "https://discord.com/channels/1281160246110457919/1281160246110457922"

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Вход в систему с зарегистрированными данными (аутентификация)")
    def login(self):

        email = 'o.pilugin@gmail.com' 
        password = 'VV5DYUeX9,8!j)e'

        with allure.step("Ввод email"):
            self.input_text(LoginPage.EMAIL_INPUT, email)

        with allure.step("Ввод пароля"):
            self.input_text(LoginPage.PASSWORD_INPUT, password)
        time.sleep(1)

        with allure.step("Нажатие на кнопку Вход"):
            self.click_element(LoginPage.LOGIN_BUTTON)

        time.sleep(5)

        with allure.step("Проверка успешного входа"):
            self.verify_login_success()

        with allure.step("Переход на 'Сервер Диплом'"):
            self.navigate_to_diplom_server()

        time.sleep(5)

    @allure.step("Проверка перехода на страницу каналов")
    def verify_login_success(self):
        try:
            self.wait_for_url_to_be(LoginPage.CHANNELS_URL, timeout=20)
            print(f"Успешный вход: переход на {LoginPage.CHANNELS_URL}")
        except TimeoutException:
            print("Ошибка: Не удалось перейти на страницу каналов после логина")
            self.take_screenshot("login_failed")
            raise AssertionError(f"Не удалось перейти на {LoginPage.CHANNELS_URL}")

    time.sleep(5)

    @allure.step("Переход на сервер 'Сервер Диплом'")
    def navigate_to_diplom_server(self):
        try:
            with allure.step("Наведение на кнопку 'Сервер Диплом'"):
                self.hover_element(LoginPage.SERVER_DIPLOM_BUTTON)

            with allure.step("Клик на кнопку 'Сервер Диплом'"):
                self.click_element(LoginPage.SERVER_DIPLOM_BUTTON)

            with allure.step("Проверка перехода на тестовый канал"):
                self.verify_channel_transition()

        except TimeoutException:
            print("Ошибка: Не удалось перейти на сервер 'Сервер Диплом'")
            self.take_screenshot("diplom_server_transition_failed")
            raise

    @allure.step("Проверка перехода на тестовый канал")
    def verify_channel_transition(self):
        try:
            self.wait_for_url_to_be(LoginPage.TEST_CHANNEL_URL, timeout=20)
            print(f"Успешный переход на тестовый канал: {LoginPage.TEST_CHANNEL_URL}")
        except TimeoutException:
            print(f"Ошибка: Не удалось перейти на тестовый канал {LoginPage.TEST_CHANNEL_URL}")
            self.take_screenshot("channel_transition_failed")
            raise AssertionError(f"Не удалось перейти на тестовый канал {LoginPage.TEST_CHANNEL_URL}")

    def wait_for_url_to_be(self, url, timeout=20):
        WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))
