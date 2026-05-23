from selenium.webdriver.common.by import By

class RegistrationPageLocators:

    NAME_INPUT = (By.NAME, "first_name")
    SURNAME_INPUT = (By.NAME, "last_name")
    USERNAME_INPUT = (By.NAME, "username")
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    CREATE_ACCOUNT_BUTTON = (By.XPATH, "//button[text()='Создать аккаунт']")