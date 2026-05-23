from selenium.webdriver.common.by import By

class LoginPageLocators:
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    ENTER_ACCOUNT_BTN = (By.XPATH, "//button[text()='Войти']")
    LOGOUT_BTN = (By.XPATH, ".//*[text()='Выход']")
    SIGNUP_LINK = (By.XPATH, "//a[text()='Создать аккаунт']")
