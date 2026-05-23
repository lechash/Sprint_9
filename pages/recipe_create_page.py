import allure
from pages.base_page import BasePage
from locators.create_recipe_page_locators import CreateRecipePageLocators
from locators.recipe_card_locators import RecipeCardLocators
from data import URLs
from selenium.webdriver.support import expected_conditions as EC


class RecipeCreatePage(BasePage):
    
    @allure.step("Открыть страницу создания рецепта")
    def open(self):
        self._open(URLs.RECIPE_CREATE)
        # Ждем загрузки ключевого элемента формы
        self._wait.until(EC.presence_of_element_located(CreateRecipePageLocators.RECIPE_NAME_INPUT))

    @allure.step("Ввести название рецепта: {name}")
    def enter_recipe_name(self, name):
        self._send_keys(CreateRecipePageLocators.RECIPE_NAME_INPUT, name)

    @allure.step("Ввести время приготовления: {time_minutes} мин.")
    def enter_recipe_time(self, time_minutes):
        self._send_keys(CreateRecipePageLocators.COOKING_TIME_INPUT, time_minutes)

    @allure.step("Ввести название ингредиента: {ingredient_name}")
    def enter_ingredient_name(self, ingredient_name):
        ingredient_name_lower = ingredient_name.lower()
        self._send_keys(CreateRecipePageLocators.INGREDIENT_INPUT, ingredient_name_lower)
        
    @allure.step("Выбрать первый подходящий ингредиент из выпадающего списка")
    def select_ingredient_from_dropdown(self):
        dropdown_item = self._wait.until(EC.element_to_be_clickable(CreateRecipePageLocators.INGREDIENT_DROPDOWN_ITEM))
        dropdown_item.click()

    @allure.step("Ввести вес ингредиента: {weight}")
    def enter_ingredient_weight(self, weight):
        weight_input = self._find_visible_element(CreateRecipePageLocators.INGREDIENT_WEIGHT)
        weight_input.clear()
        weight_input.send_keys(str(weight))

    @allure.step("Нажать кнопку 'Добавить ингредиент'")
    def click_add_ingredient_button(self):
        self._click(CreateRecipePageLocators.ADD_INGREDIENT_BTN)

    @allure.step("Добавить ингредиент: {ingredient_name} ({weight}г)")
    def add_ingredient(self, ingredient_name, weight=100):
        self.enter_ingredient_name(ingredient_name)
        self.select_ingredient_from_dropdown()
        self.enter_ingredient_weight(weight)
        self.click_add_ingredient_button()

    @allure.step("Ввести описание рецепта")
    def enter_description(self, description):
        self._send_keys(CreateRecipePageLocators.DESCRIPTION_TEXTAREA, description)

    @allure.step("Загрузить изображение рецепта")
    def upload_image(self, file_path):
        self._send_keys_file(CreateRecipePageLocators.FILE_INPUT, file_path)

    @allure.step("Нажать кнопку 'Создать рецепт'")
    def submit_recipe(self):
        self._click(CreateRecipePageLocators.CREATE_RECIPE_BTN)
        self._wait.until(lambda d: '/recipes/' in d.current_url and d.current_url.split('/')[-1].isdigit())

    @allure.step("Проверить наличие карточки рецепта с названием: {recipe_name}")
    def is_recipe_card_visible(self, recipe_name):
        def recipe_title_present(driver):
            elements = driver.find_elements(*RecipeCardLocators.RECIPE_CARD_TITLE)
            for el in elements:
                if el.is_displayed() and recipe_name in el.text:
                    return True
            return False
        
        return self._wait.until(recipe_title_present)

    @allure.step("Создать полный рецепт с изображением")
    def create_recipe(self, name, time_minutes, description, ingredient_name, ingredient_weight, file_path):
        self.enter_recipe_name(name)
        self.add_ingredient(ingredient_name, ingredient_weight)
        self.enter_recipe_time(time_minutes)
        self.enter_description(description)
        self.upload_image(file_path)
        self.submit_recipe()
