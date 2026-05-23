class URLs:
    # Хранение всех URL-адресов приложения
    BASE_URL = "https://foodgram-frontend-1.foodgram.education-services.ru"
    LOGIN = f"{BASE_URL}/signin"
    SIGNUP = f"{BASE_URL}/signup"
    RECIPE_CREATE = f"{BASE_URL}/recipes/create/"
    RECIPES_LIST = f"{BASE_URL}/recipes/"


class ExistingUser:
    # Данные уже зарегистрированного пользователя для тестов входа
    USERNAME = "Helena_Cha2"  # Фактически используется как email
    PASSWORD = "QA9ZP1XOofNsen89"


class RecipeData:
    # Статические данные для рецептов
    DEFAULT_COOKING_TIME = "10"
    IMAGE_FILE = "breakfast_with_coffee.jpg"