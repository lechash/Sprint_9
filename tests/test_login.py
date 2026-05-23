import pytest
import allure
from data import ExistingUser


@allure.feature("Авторизация")
class TestLogin:
    
    @allure.story("Вход в систему")
    @allure.title("Нажатие кнопки 'Войти' перенаправляет на главную страницу")
    def test_login_redirects_to_main_page(self, driver, filled_login_form):

        with allure.step(f"Нажать кнопку 'Войти' для пользователя {ExistingUser.USERNAME}"):
            filled_login_form.click_enter_button()
        
        with allure.step("Ожидать перехода на главную страницу (/recipes)"):
            filled_login_form.wait_for_recipes_url()
            
        with allure.step("Проверить, что текущий URL содержит 'recipes'"):
            assert "recipes" in filled_login_form.get_current_url(), \
                f"Ожидался URL с 'recipes', получен: {filled_login_form.get_current_url()}"


    @allure.story("Вход в систему")
    @allure.title("После входа на главной странице отображается кнопка Выход")
    def test_logout_button_visible_on_main_page(self, driver, filled_login_form):

        with allure.step(f"Нажать кнопку 'Войти' для пользователя {ExistingUser.USERNAME}"):
            filled_login_form.click_enter_button()
        
        with allure.step("Ожидать перехода на главную страницу"):
            filled_login_form.wait_for_recipes_url()

        with allure.step("Ожидать появления кнопки Выход"):
            filled_login_form.wait_for_logout_button()
            
        with allure.step("Проверить отображение кнопки 'Выход'"):
            assert filled_login_form.is_logout_button_visible(), \
                "Кнопка 'Выход' не отображается на главной странице после входа"
            