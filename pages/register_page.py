import allure
from pages.base_page import BasePage
from locators.registration_page_locators import RegistrationPageLocators
from locators.login_page_locators import LoginPageLocators
from data import URLs


class RegisterPage(BasePage):
    
    @allure.step("Открыть страницу регистрации")
    def open(self):
        self._open(URLs.SIGNUP)

    @allure.step("Заполнить форму регистрации")
    def fill_registration_form(self, first_name, last_name, username, email, password):
        self._send_keys(RegistrationPageLocators.NAME_INPUT, first_name)
        self._send_keys(RegistrationPageLocators.SURNAME_INPUT, last_name)
        self._send_keys(RegistrationPageLocators.USERNAME_INPUT, username)
        self._send_keys(RegistrationPageLocators.EMAIL_INPUT, email)
        self._send_keys(RegistrationPageLocators.PASSWORD_INPUT, password)

    @allure.step("Нажать кнопку 'Создать аккаунт'")
    def click_create_account_button(self):
        # Клик по кнопке создания аккаунта
        self._click(RegistrationPageLocators.CREATE_ACCOUNT_BUTTON)

    @allure.step("Ожидать перехода на страницу входа (/signin)")
    def wait_for_login_url(self):
        # Ждет перехода на страницу signin
        self.wait_for_url_contains("signin")

    @allure.step("Проверить отображение формы авторизации")
    def is_login_form_visible(self):
        # Проверяет видимость полей формы входа (Email и Password)
        # После редиректа мы на странице логина, поэтому используем локаторы LoginPage
        return self._is_visible(LoginPageLocators.EMAIL_INPUT) and \
               self._is_visible(LoginPageLocators.PASSWORD_INPUT)