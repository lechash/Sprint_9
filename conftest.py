import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from helpers import data_generator
from data import ExistingUser


def pytest_addoption(parser):
    # Добавляем опции командной строки
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome", 
        help="Browser to use: chrome"
    )
    parser.addoption(
        "--remote", 
        action="store_true", 
        default=False, 
        help="Use remote WebDriver (Selenoid)"
    )
    parser.addoption(
        "--selenoid-uri", 
        action="store", 
        default="http://localhost:4444/wd/hub", 
        help="Selenoid URI"
    )


@pytest.fixture(scope="function")
def driver(request):
    # Фикстура для создания WebDriver.
    # Поддерживает локальный и удалённый (Selenoid) запуск
    # Приоритет: аргументы CLI > переменные окружения
    
    # Получаем настройки из CLI
    browser = request.config.getoption("--browser")
    use_remote = request.config.getoption("--remote")
    selenoid_uri = request.config.getoption("--selenoid-uri")
    
    # Fallback на переменные окружения (для Docker)
    if not use_remote and os.getenv("USE_REMOTE", "").lower() == "true":
        use_remote = True
    if os.getenv("SELENOID_URI"):
        selenoid_uri = os.getenv("SELENOID_URI")
    if os.getenv("BROWSER"):
        browser = os.getenv("BROWSER")
    
    if use_remote:
        # Remote WebDriver для Selenoid
        capabilities = {
            "browserName": browser,
            "browserVersion": "128.0",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": False,
                "enableLog": True,
                "logName": "test.log",
                "videoName": "test.mp4"
            }
        }
        
        driver = webdriver.Remote(
            command_executor=selenoid_uri,
            options=_get_browser_options(browser, capabilities)
        )
    else:
        # Локальный WebDriver
        driver = _create_local_driver(browser)
    
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    yield driver
    

def _get_browser_options(browser, capabilities):
    # Получаем опции для браузера
    if browser == "chrome":
        options = Options()
        options.set_capability("browserVersion", capabilities["browserVersion"])
        options.set_capability("selenoid:options", capabilities["selenoid:options"])
        return options
    raise ValueError(f"Unsupported browser: {browser}")


def _create_local_driver(browser):
    # Создаёт локальный WebDriver
    if browser == "chrome":
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)
    raise ValueError(f"Unsupported browser: {browser}")


@pytest.fixture(scope="function")
def filled_registration_form(driver):
    # Фикстура: заполненная форма регистрации
    user_data = data_generator.generate_user_data()
    
    reg_page = RegisterPage(driver)
    reg_page.open()
    
    reg_page.fill_registration_form(
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"]
    )
    
    return reg_page, user_data


@pytest.fixture(scope="function")
def filled_login_form(driver):
    # Фикстура: заполненная форма входа
    login_page = LoginPage(driver)
    login_page.open()
    
    login_page.fill_credentials(
        ExistingUser.USERNAME,
        ExistingUser.PASSWORD
    )
    
    return login_page


@pytest.fixture(scope="function")
def existing_user_login(driver):
    # Фикстура: авторизованный пользователь
    login_page = LoginPage(driver)
    login_page.open()
    
    login_page.fill_credentials(
        ExistingUser.USERNAME,
        ExistingUser.PASSWORD
    )
    login_page.click_enter_button()
    login_page.wait_for_recipes_url()
    
    return login_page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Хук для отслеживания результатов тестов
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)