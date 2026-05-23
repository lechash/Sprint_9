import pytest
import allure
from pathlib import Path
from pages.recipe_create_page import RecipeCreatePage
from data import RecipeData
from helpers import data_generator


@allure.feature("Рецепты")
class TestRecipeCreation:
    
    @allure.story("Создание рецепта")
    @allure.title("После создания рецепта отображается карточка рецепта")
    def test_recipe_card_is_visible_after_creation(self, driver, existing_user_login):

        recipe_name = f"Автотест: Карточка {data_generator.fake.random_int(min=1000, max=9999)}"
        project_root = Path(__file__).parent.parent
        image_path = str(project_root / "assets" / RecipeData.IMAGE_FILE)
        
        with allure.step("Перейти на страницу создания рецепта"):
            recipe_page = RecipeCreatePage(driver)
            recipe_page.open() 
            
        with allure.step("Создать рецепт"):
            recipe_page.create_recipe(
                name=recipe_name,
                time_minutes=RecipeData.DEFAULT_COOKING_TIME,
                description="Рецепт для проверки отображения карточки.",
                ingredient_name="Кофе",
                ingredient_weight=50,
                file_path=image_path
            )
        
        with allure.step("Проверить, что карточка рецепта отображается"):
            assert recipe_page.is_recipe_card_visible(recipe_name), \
                "Карточка созданного рецепта не отображается"


    @allure.story("Создание рецепта")
    @allure.title("Карточка рецепта содержит корректное название")
    def test_recipe_card_contains_correct_name(self, driver, existing_user_login):

        expected_name = f"Автотест: Название {data_generator.fake.random_int(min=1000, max=9999)}"
        project_root = Path(__file__).parent.parent
        image_path = str(project_root / "assets" / RecipeData.IMAGE_FILE)
        
        with allure.step("Перейти на страницу создания рецепта"):
            recipe_page = RecipeCreatePage(driver)
            recipe_page.open() 
            
        with allure.step(f"Создать рецепт с названием: {expected_name}"):
            recipe_page.create_recipe(
                name=expected_name,
                time_minutes=RecipeData.DEFAULT_COOKING_TIME,
                description="Рецепт для проверки корректности названия.",
                ingredient_name="Кофе",
                ingredient_weight=100,
                file_path=image_path
            )
        
        with allure.step(f"Проверить, что карточка содержит название '{expected_name}'"):
            assert recipe_page.is_recipe_card_visible(expected_name), \
                f"Карточка не содержит ожидаемое название '{expected_name}'"
            