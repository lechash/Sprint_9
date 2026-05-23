from selenium.webdriver.common.by import By

class RecipeCardLocators:
   
    RECIPE_CARD_TITLE = (By.CSS_SELECTOR, "h1[class*='single-card__title']")
    RECIPE_CARD_CONTAINER = (By.CSS_SELECTOR, "div[class*='single-card__info']")