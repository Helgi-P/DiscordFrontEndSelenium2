import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from login_page import LoginPage
from main_page import MainPage


@pytest.fixture(scope="class")
def driver(request):
    browser = request.param if hasattr(request, 'param') else "chrome"
    driver = None

    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    elif browser == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)

    elif browser == "edge":
        edge_options = EdgeOptions()
        edge_options.add_argument("--headless")
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)

    driver.implicitly_wait(30)
    yield driver
    driver.quit()


@pytest.fixture(scope="class", autouse=True)
def setup(driver):
    login_page = LoginPage(driver)

    with allure.step("Открытие страницы логина"):
        login_page.open("https://discord.com/login")

        if not login_page.is_element_visible(LoginPage.EMAIL_INPUT):
            raise AssertionError("Поле для ввода email не найдено.")

    with allure.step("Вход в систему"):
        login_page.login()

    main_page = MainPage(driver)
    with allure.step("Открытие тестового канала"):
        main_page.open()
        assert main_page.is_text_field_visible(), "Текстовое поле не видно на главной странице"
        assert main_page.is_emoji_button_visible(), "Кнопка эмодзи не видна на главной странице"
        assert main_page.is_attach_button_visible(), "Кнопка вложений не видна на главной странице"

    return main_page