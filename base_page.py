import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    # Сохранение скриншота
    def take_screenshot(self, name="screenshot"):
        screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_name = f"{timestamp}.png"
        screenshot_path = os.path.join(screenshot_dir, screenshot_name)
        self.driver.save_screenshot(screenshot_path)
        print(f"Скриншот сохранён: {screenshot_path}")

    # Открыть страницу
    def open(self, url):
        print(f"Открытие страницы: {url}")
        self.driver.get(url)

    # Поиск элемента
    def find_element(self, locator, timeout=20):
        try:
            print(f"Поиск элемента: {locator}")
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            print(f"Элемент найден: {locator}")
            return element
        except TimeoutException:
            print(f"Элемент не найден в течение {timeout} секунд: {locator}")
            self.take_screenshot(f"element_not_found_{locator}")
            raise

    # Проверка видимости элемента
    def is_element_visible(self, locator, timeout=10):
        try:
            print(f"Проверка видимости элемента: {locator}")
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            print(f"Элемент виден: {locator}")
            return True
        except TimeoutException:
            print(f"Элемент не виден в течение {timeout} секунд: {locator}")
            self.take_screenshot(f"element_not_visible_{locator}")
            return False

    # Наведение на элемент
    def hover_element(self, locator):
        try:
            print(f"Наведение на элемент: {locator}")
            element = self.find_element(locator)
            ActionChains(self.driver).move_to_element(element).perform()
            print(f"Наведение выполнено на элемент: {locator}")
        except Exception as e:
            print(f"Не удалось навести на элемент: {locator}. Ошибка: {e}")
            self.take_screenshot(f"hover_failed_{locator}")
            raise

    # Клик на элемент
    def click_element(self, locator, timeout=25):
        try:
            print(f"Клик на элемент: {locator}")
            element = self.find_element(locator, timeout)
            element.click()
            print(f"Клик выполнен на элемент: {locator}")
        except Exception as e:
            print(f"Не удалось кликнуть на элемент: {locator}. Ошибка: {e}")
            self.take_screenshot(f"click_failed_{locator}")
            raise

    # Ввод текста в поле
    def input_text(self, locator, text, timeout=10):
        try:
            print(f"Ввод текста '{text}' в элемент: {locator}")
            element = self.find_element(locator, timeout)
            element.click()  # Активируем поле ввода
            time.sleep(1)  # Ожидание для стабильности
            element.send_keys(text)
            print(f"Текст '{text}' введён в элемент: {locator}")
        except Exception as e:
            print(f"Не удалось ввести текст '{text}' в элемент: {locator}. Ошибка: {e}")
            self.take_screenshot(f"input_failed_{locator}")
            raise

    # Ожидание видимости элемента
    def wait_for_element_to_be_visible(self, locator, timeout=20):
        try:
            print(f"Ожидание видимости элемента: {locator}")
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            print(f"Элемент видим: {locator}")
        except TimeoutException:
            print(f"Элемент не появился в течение {timeout} секунд: {locator}")
            self.take_screenshot(f"element_not_visible_{locator}")
            raise

    # Нажатие клавиши Enter
    def press_enter(self, locator, timeout=10):
        try:
            element = self.find_element(locator, timeout)
            self.hover_element(locator)
            time.sleep(1)
            element.send_keys(Keys.RETURN)
            print(f"Нажата клавиша Enter на элемент: {locator}")
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        except Exception as e:
            print(f"Не удалось нажать клавишу Enter на элемент: {locator}. Ошибка: {e}")
            self.take_screenshot(f"press_enter_failed_{locator}")
            raise

    # Загрузка файла
    def upload_file(self, file_path):
        try:
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(file_path)
            print(f"Файл '{file_path}' успешно загружен.")
        except Exception as e:
            print(f"Ошибка при загрузке файла '{file_path}': {e}")
            self.take_screenshot("file_upload_failed")
            raise

    # Клик правой кнопкой мыши на элемент
    def right_click_element(self, locator, timeout=25):
        try:
            print(f"Клик правой кнопкой мыши на элемент: {locator}")
            element = self.find_element(locator, timeout)
            actions = ActionChains(self.driver)
            actions.context_click(element).perform()  # Выполняем клик правой кнопкой
            print(f"Клик правой кнопкой мыши выполнен на элемент: {locator}")
        except Exception as e:
            print(f"Не удалось выполнить клик правой кнопкой мыши на элемент: {locator}. Ошибка: {e}")
            self.take_screenshot(f"right_click_failed_{locator}")
            raise

    # Метод для наведения и клика
    def hover_and_click(self, locator):
        try:
            print(f"Наведение и клик на элемент: {locator}")
            element = self.find_element(locator)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click().perform()
            print(f"Наведение и клик выполнены на элемент: {locator}")
        except Exception as e:
            print(f"Не удалось выполнить наведение и клик на элемент: {locator}. Ошибка: {e}")
            self.take_screenshot(f"hover_and_click_failed_{locator}")
            raise
