import pytest
import allure
from main_page import MainPage



@pytest.mark.parametrize("driver", ["chrome", "firefox", "edge"], indirect=True)
@pytest.mark.usefixtures("setup")
class TestDiscordMessageActions:

    @pytest.mark.order(1)
    def test_send_and_delete_message_1_with_attachment(self, driver):
        main_page = MainPage(driver)

        with allure.step("Отправка Сообщения 1 с файлом"):
            main_page.send_message_1()

        with allure.step("Удаление Сообщения 1"):
            main_page.delete_message_1()

    @pytest.mark.order(2)
    def test_send_message_2_add_remove_reactions_and_cleanup(self, driver):
        main_page = MainPage(driver)

        with allure.step("Отправка Сообщения 2"):
            main_page.send_message_2()

        with allure.step("Отправка Сообщения 3"):
            main_page.send_message_3()

        with allure.step("Добавление реакции 'exploding_head' к Сообщению 2"):
            main_page.add_reaction(main_page.MESSAGE_2, "exploding_head")

        with allure.step("Добавление реакции 'disappointed' к Сообщению 3"):
            main_page.add_reaction(main_page.MESSAGE_3, "disappointed")

        with allure.step("Добавление реакции 'smile' к Сообщению 2"):
            main_page.add_reaction(main_page.MESSAGE_2, "smile")

        with allure.step("Удаление Сообщения 3"):
            main_page.delete_message_3()

        with allure.step("Удаление Сообщения 2"):
            main_page.delete_message_2()
