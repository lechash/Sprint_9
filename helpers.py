from faker import Faker


class DataGenerator:
    """Генератор тестовых данных с использованием Faker"""
    
    def __init__(self):
        self.fake = Faker('ru_RU')  # Используем русскую локаль для имен
        self.fake.seed_instance()   # Инициализация случайного seed для каждого экземпляра
    
    def generate_user_data(self):
        """
        Генерирует полный набор данных для регистрации пользователя.
        Возвращает словарь с данными.
        """
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        
        # Генерируем username на основе имени и случайных цифр для уникальности
        username = f"{first_name.lower()}_{self.fake.random_int(min=1000, max=9999)}"
        
        # Генерируем уникальный email (Faker гарантирует уникальность в рамках сессии)
        email = self.fake.unique.email()
        
        # Пароль фиксированный для удобства проверки
        password = "PasswordCha987654321189"
        
        return {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "password": password
        }


# Глобальный экземпляр для импорта
data_generator = DataGenerator()