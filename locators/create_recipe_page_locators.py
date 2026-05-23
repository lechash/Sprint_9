from selenium.webdriver.common.by import By

class CreateRecipePageLocators:
    CREATE_TAB = (By.XPATH, "//a[contains(text(), 'Создать рецепт')]")
    RECIPE_NAME_INPUT = (By.XPATH, ".//div[text()='Название рецепта']/../input")

    COOKING_TIME_INPUT = (By.XPATH, ".//div[text()='Время приготовления']/../input")
    DESCRIPTION_TEXTAREA = (By.XPATH, ".//div[text()='Описание рецепта']/../textarea")
    
    INGREDIENT_INPUT = (By.XPATH, ".//div[text()='Ингредиенты']/../input")
    # Важно: список появляется ПОСЛЕ ввода текста.
    INGREDIENT_DROPDOWN_ITEM = (By.XPATH, ".//div[contains(@class, 'ingredientsInput')]/div[contains(@class, 'styles_container')]") 
    INGREDIENT_WEIGHT = (By.XPATH, ".//input[contains(@class, 'ingredientsAmountValue')]")
    ADD_INGREDIENT_BTN = (By.XPATH, ".//div[text()='Добавить ингредиент']")
    FILE_INPUT = (By.XPATH, ".//input[@type='file']")
    CREATE_RECIPE_BTN = (By.XPATH, ".//button[text()='Создать рецепт']")
