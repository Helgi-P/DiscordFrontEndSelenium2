import os
import time
import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from base_page import BasePage


class MainPage(BasePage):
    url = "https://discord.com/channels/1281160246110457919/1281160246110457922"

    # Локаторы
    TEXT_FIELD_LOCATOR = ('xpath', '//div[contains(@class, "editor_") and @role="textbox"]')
    EMOJI_BUTTON_LOCATOR = ('xpath', '//button[@aria-label="Выбрать эмодзи" and contains(@class, "emojiButton")]')
    ATTACH_BUTTON_LOCATOR = ('xpath', '//button[@aria-label="Другие настройки" and contains(@class, "attachButton")]')
    ATTACH_FILE_OPTION_LOCATOR = ('xpath', '//*[@id="channel-attach-upload-file"]')
    MESSAGE_TEXT_LOCATOR = (
        'xpath', "//div[@class='markup_f8f345 messageContent_f9f2ca']/span[text()='{message_text}']"
    )
    ACTIONS_MENU_LOCATOR = (
        'xpath', "//*[@id='app-mount']//div[contains(@class, 'menu')]"
    )
    DELETE_MESSAGE_LOCATOR = (
        'xpath', "//*[@id='message-delete']/div[1]"
    )
    CONFIRM_DELETE_LOCATOR = (
        'xpath', "//*[@id='app-mount']//button[div[contains(text(), 'Удалить')]]"
    )
    ADD_REACTION_LOCATOR = (
        'xpath', "//*[@id='message-add-reaction']"
    )
    EMOJI_PICKER_LOCATOR = (
        'xpath', "//*[@id='emoji-picker-tab-panel']/div[3]/div/div[1]"
    )
    EMOJI_CATEGORY_LOCATOR = (
        'xpath', "//*[@role='listitem' and @aria-label='people']"
    )
    EMOJI_BUTTON_LOCATOR_TEMPLATE = "//button[@data-type='emoji' and @data-name='{emoji_name}']"

    FILE_PATH = os.path.abspath(os.path.join("resources", "Pet1.jpg"))

    # Сообщения
    MESSAGE_1 = "Тестовое сообщение 1"
    MESSAGE_2 = "Test message 2"
    MESSAGE_3 = "Test message 3"

    # Эмодзи
    EMOJI_NAMES = {
        "exploding_head": "exploding_head",
        "smile": "smile",
        "disappointed": "disappointed"
    }

    @allure.step("Открытие тестового канала")
    def open(self):
        super().open(self.url)

    @allure.step("Проверка видимости текстового поля")
    def is_text_field_visible(self):
        return self.is_element_visible(self.TEXT_FIELD_LOCATOR)

    @allure.step("Проверка видимости кнопки эмодзи")
    def is_emoji_button_visible(self):
        return self.is_element_visible(self.EMOJI_BUTTON_LOCATOR)

    @allure.step("Проверка видимости кнопки для вложений")
    def is_attach_button_visible(self):
        return self.is_element_visible(self.ATTACH_BUTTON_LOCATOR)

    @allure.step("Отправка Сообщения 1")
    def send_message_1(self):
        try:
            message = self.MESSAGE_1
            with allure.step(f"Ввод текста сообщения 1: {message}"):
                self.input_text(self.TEXT_FIELD_LOCATOR, message)
                self.send_file_attachment(self.FILE_PATH)
                time.sleep(2)
                self.press_enter(self.TEXT_FIELD_LOCATOR)
                time.sleep(2)
            print(f"Сообщение 1 отправлено: {message}")
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="SendMessage1Error",
                          attachment_type=allure.attachment_type.PNG)
            print(f"Ошибка при отправке сообщения 1: {e}")
            raise

    @allure.step("Отправка Сообщения 2")
    def send_message_2(self):
        try:
            message = self.MESSAGE_2
            with allure.step(f"Ввод текста сообщения 2: {message}"):
                self.input_text(self.TEXT_FIELD_LOCATOR, message)
                self.press_enter(self.TEXT_FIELD_LOCATOR)
            print(f"Сообщение 2 отправлено: {message}")
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="SendMessage2Error",
                          attachment_type=allure.attachment_type.PNG)
            print(f"Ошибка при отправке сообщения 2: {e}")
            raise

    @allure.step("Отправка Сообщения 3")
    def send_message_3(self):
        try:
            message = self.MESSAGE_3
            with allure.step(f"Ввод текста сообщения 3: {message}"):
                self.input_text(self.TEXT_FIELD_LOCATOR, message)
                self.press_enter(self.TEXT_FIELD_LOCATOR)
            print(f"Сообщение 3 отправлено: {message}")
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="SendMessage2Error",
                          attachment_type=allure.attachment_type.PNG)
            print(f"Ошибка при отправке сообщения 3: {e}")
            raise

    @allure.step("Прикрепление файла")
    def send_file_attachment(self, file_path):
        try:
            with allure.step("Нажатие на кнопку для вложений"):
                self.click_element(self.ATTACH_BUTTON_LOCATOR)

            with allure.step("Выбор опции «Отправить файл»"):
                self.wait_for_element_to_be_visible(self.ATTACH_FILE_OPTION_LOCATOR)
                self.click_element(self.ATTACH_FILE_OPTION_LOCATOR)

            with allure.step(f"Прикрепление файла: {file_path}"):
                self.upload_file(file_path)

            print("Файл успешно прикреплён.")

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="SendFileAttachmentError",
                          attachment_type=allure.attachment_type.PNG)
            print(f"Ошибка при прикреплении файла: {e}")
            raise

    @allure.step("Удаление сообщения 1")
    def delete_message_1(self):
        self.delete_message(self.MESSAGE_1)

    @allure.step("Удаление сообщения 2")
    def delete_message_2(self):
        self.delete_message(self.MESSAGE_2)

    @allure.step("Удаление сообщения 3")
    def delete_message_3(self):
        self.delete_message(self.MESSAGE_3)

    @allure.step("Удаление сообщения")
    def delete_message(self, message_text):
        try:
            message_locator = (
                self.MESSAGE_TEXT_LOCATOR[0], self.MESSAGE_TEXT_LOCATOR[1].format(message_text=message_text))
            print(f"Локатор сообщения: {message_locator}")

            with allure.step(f"Ждем, пока сообщение '{message_text}' будет видимо"):
                self.wait_for_element_to_be_visible(message_locator)
                allure.attach(self.driver.get_screenshot_as_png(), name="MessageVisible",
                              attachment_type=allure.attachment_type.PNG)

            with allure.step("Наведение курсора на сообщение"):
                print("Наведение курсора на сообщение...")
                self.hover_element(message_locator)

            with allure.step("Клик правой кнопкой мыши на сообщение"):
                print("Клик правой кнопкой мыши на сообщение...")
                self.right_click_element(message_locator)

            with allure.step("Ждем появления меню действий"):
                self.wait_for_element_to_be_visible(self.ACTIONS_MENU_LOCATOR)

            with allure.step("Клик на кнопку «Удалить сообщение»"):
                print("Клик на кнопку «Удалить сообщение»...")
                self.click_element(self.DELETE_MESSAGE_LOCATOR)

            with allure.step("Клик на кнопку подтверждения удаления"):
                print("Клик на кнопку подтверждения удаления...")
                self.click_element(self.CONFIRM_DELETE_LOCATOR)

            time.sleep(3)
            allure.attach(self.driver.get_screenshot_as_png(), name="MessageDeleted",
                          attachment_type=allure.attachment_type.PNG)
            print(f"Сообщение удалено: {message_text}")

        except TimeoutException:
            print("Время ожидания истекло, сообщение не было найдено.")
            allure.attach(self.driver.get_screenshot_as_png(), name="TimeoutError",
                          attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="DeleteMessageError",
                          attachment_type=allure.attachment_type.PNG)

    @allure.step("Добавление реакции на сообщение")
    def add_reaction(self, message_text, emoji_name):
        try:
            message_locator = (
                self.MESSAGE_TEXT_LOCATOR[0],
                self.MESSAGE_TEXT_LOCATOR[1].format(message_text=message_text)
            )
            print(f"Локатор сообщения: {message_locator}")

            with allure.step(f"Наведение курсора на сообщение '{message_text}'"):
                self.wait_for_element_to_be_visible(message_locator, timeout=20)
                self.hover_element(message_locator)

            with allure.step("Открытие меню действий сообщения"):
                self.right_click_element(message_locator)

            with allure.step("Клик на 'Добавить реакцию'"):
                self.wait_for_element_to_be_visible(self.ACTIONS_MENU_LOCATOR, timeout=10)
                self.click_element(self.ADD_REACTION_LOCATOR)

            with allure.step("Ожидание появления списка эмодзи"):
                self.wait_for_element_to_be_visible(self.EMOJI_PICKER_LOCATOR, timeout=10)
                self.click_element(self.EMOJI_CATEGORY_LOCATOR)

            time.sleep(1)

            emoji_button_locator = (By.XPATH, self.EMOJI_BUTTON_LOCATOR_TEMPLATE.format(emoji_name=emoji_name))
            with allure.step(f"Выбор эмодзи '{emoji_name}'"):
                self.wait_for_element_to_be_visible(emoji_button_locator, timeout=15)
                self.click_element(emoji_button_locator)

            time.sleep(2)

        except TimeoutException:
            print("Время ожидания истекло, эмодзи не было добавлено.")
            allure.attach(self.driver.get_screenshot_as_png(), name="TimeoutError",
                          attachment_type=allure.attachment_type.PNG)
            raise
        except Exception as e:
            print(f"Ошибка при добавлении эмодзи: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="AddReactionError",
                          attachment_type=allure.attachment_type.PNG)
            raise
