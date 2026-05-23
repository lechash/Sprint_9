import pytest
import allure
from pages.register_page import RegisterPage
from helpers import data_generator


@allure.feature("Авторизация")
class TestRegistration:
    
    @allure.story("Создание аккаунта")
    @allure.title("Нажатие кнопки 'Создать аккаунт' перенаправляет на страницу входа")
    def test_register_redirects_to_login(self, driver, filled_registration_form):
        reg_page, user_data = filled_registration_form
        
        with allure.step(f"Нажать кнопку 'Создать аккаунт' для пользователя {user_data['email']}"):
            reg_page.click_create_account_button()
        
        with allure.step("Ожидать перехода на страницу авторизации (/signin)"):
            reg_page.wait_for_login_url()
            
        with allure.step("Проверить, что текущий URL содержит 'signin'"):
            assert "signin" in reg_page.get_current_url(), f"Ожидался URL с 'signin', получен: {reg_page.get_current_url()}"


    @allure.story("Создание аккаунта")
    @allure.title("После регистрации отображается форма авторизации")
    def test_login_form_is_visible_after_register(self, driver, filled_registration_form):
        reg_page, user_data = filled_registration_form
        
        with allure.step(f"Нажать кнопку 'Создать аккаунт' для пользователя {user_data['email']}"):
            reg_page.click_create_account_button()
        
        with allure.step("Ожидать перехода на страницу авторизации"):
            reg_page.wait_for_login_url()
            
        with allure.step("Проверить отображение формы авторизации (поля Email и Password)"):
            assert reg_page.is_login_form_visible(), "Форма авторизации не отображается после перехода"