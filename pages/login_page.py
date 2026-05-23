import allure
from pages.base_page import BasePage
from locators.login_page_locators import LoginPageLocators
from data import URLs


class LoginPage(BasePage):
    
    @allure.step("Открыть страницу входа")
    def open(self):
        self._open(URLs.LOGIN)

    @allure.step("Заполнить форму входа: Email={username}, Password=***")
    def fill_credentials(self, username, password):
        self._send_keys(LoginPageLocators.EMAIL_INPUT, username)
        self._send_keys(LoginPageLocators.PASSWORD_INPUT, password)

    @allure.step("Нажать кнопку 'Войти'")
    def click_enter_button(self):
        self._click(LoginPageLocators.ENTER_ACCOUNT_BTN)

    @allure.step("Ожидать перехода на страницу рецептов (/recipes)")
    def wait_for_recipes_url(self):
        self.wait_for_url_contains("recipes")

    @allure.step("Ожидать появления кнопки 'Выход'")
    def wait_for_logout_button(self):
        self._find_element(LoginPageLocators.LOGOUT_BTN)
        
    @allure.step("Проверить видимость кнопки 'Выход'")
    def is_logout_button_visible(self):
        return self._is_visible(LoginPageLocators.LOGOUT_BTN)