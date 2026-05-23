# Автоматизированное тестирование UI Foodgram

Проект содержит набор автоматизированных тестов для веб‑интерфейса сервиса рецептов Foodgram. Тесты проверяют основные пользовательские сценарии: регистрацию, авторизацию и создание рецептов с загрузкой изображений.

## Содержание

- Технологии
- Структура проекта
- Тестовые сценарии
- Архитектурные решения
- Установка и запуск
- Запуск в Docker с Selenoid
- CI/CD с GitHub Actions
- Отчёты
- Конфигурация

## Технологии

|    Инструмент   |               Назначение            |
|-----------------|-------------------------------------|
| Python 3.11+    | Язык программирования               |
| pytest 9.0.2    | Фреймворк для запуска тестов        |
| Selenium 4.41.0 | Автоматизация браузера              |
| Allure 2.15.3   | Генерация отчётов                   |
| Faker 40.5.1    | Генерация тестовых данных           |
| Docker          | Контейнеризация тестового окружения |
| Selenoid        | Запуск браузеров в контейнерах      |

## Структура проекта

/
├── assets/                             # Тестовые файлы
│ └── breakfast_with_coffee.jpg         # Изображение для загрузки в рецепт
│
├── locators/                           # Хранилище локаторов элементов
│ ├── init.py
│ ├── create_recipe_page_locators.py    # Элементы страницы создания рецепта
│ ├── login_page_locators.py            # Элементы страницы авторизации
│ ├── recipe_card_locators.py           # Элементы карточки рецепта
│ └── registration_page_locators.py     # Элементы страницы регистрации
│
├── pages/                              # Page Objects — основные страницы
│ ├── init.py
│ ├── base_page.py                      # Базовый класс с общими методами
│ ├── login_page.py                     # Страница авторизации
│ ├── recipe_create_page.py             # Страница создания рецепта
│ └── register_page.py                  # Страница регистрации
│
├── tests/                              # Тестовые сценарии (pytest)
│ ├── init.py
│ ├── test_login.py                     # Тесты авторизации
│ ├── test_recipe.py                    # Тесты создания рецептов
│ └── test_registration.py              # Тесты регистрации
│
├── selenoid/                           # Конфигурация Selenoid
│ └── browsers.json                     # Конфигурация браузеров
│
├── .github/workflows/                  # GitHub Actions пайплайны
│ └── ci.yml                            # Конфигурация CI/CD
│
├── conftest.py                         # Фикстуры pytest и настройка WebDriver
├── data.py                             # URL и тестовые данные
├── helpers.py                          # Генератор тестовых данных (Faker)
├── Dockerfile                          # Образ для запуска тестов в Docker
├── docker-compose.yml                  # Оркестрация: Selenoid + тесты
├── requirements.txt                    # Зависимости проекта
└── README.md                           # Документация


## Тестовые сценарии

### 1. Регистрация (`test_registration.py`)

- `test_register_redirects_to_login` — проверка редиректа на страницу входа после нажатия «Создать аккаунт».
- `test_login_form_is_visible_after_register` — проверка отображения формы авторизации после успешной регистрации.

### 2. Авторизация (`test_login.py`)

- `test_login_redirects_to_main_page` — проверка перехода на главную страницу после входа.
- `test_logout_button_visible_on_main_page` — проверка отображения кнопки «Выход» после авторизации.

### 3. Создание рецепта (`test_recipe.py`)

- `test_recipe_card_is_visible_after_creation` — проверка отображения карточки созданного рецепта.
- `test_recipe_card_contains_correct_name` — проверка, что карточка содержит корректное название рецепта.

**Особенности сценария создания рецепта:**

- Заполнение всех полей формы: название, время приготовления, описание.
- Добавление ингредиента из автодополнения (требует ввода текста для отображения списка).
- Загрузка изображения через `input[type="file"]`.
- Проверка редиректа на страницу рецепта после создания.

## Архитектурные решения

### Паттерн Page Object Model

- Каждая страница сайта представлена отдельным классом в папке `pages/`.
- Локаторы элементов вынесены в отдельный пакет `locators/` для удобства поддержки.
- Базовая логика взаимодействия с элементами (ожидания, клики, ввод текста) инкапсулирована в `BasePage`.

### Фикстуры и подготовка данных (`conftest.py`)

- `driver` — параметризованная фикстура, поддерживает локальный и удалённый (Selenoid) запуск WebDriver.
- `filled_registration_form` — заполняет форму регистрации тестовыми данными (не отправляет).
- `filled_login_form` — заполняет форму входа данными существующего пользователя.
- `existing_user_login` — выполняет полную авторизацию для тестов, требующих вход.

### Хелперы для генерации данных (`helpers.py`)

`DataGenerator` — класс для генерации уникальных тестовых данных через Faker:

- `generate_user_data()` — создаёт словарь с именем, фамилией, email, паролем.
- Использует русскую локаль (`ru_RU`) для реалистичных имён.

### Ожидания и стабильность

- Запрещено использование `time.sleep()` — только `WebDriverWait` через методы `BasePage`.
- Все ожидания элементов вынесены в приватные методы `_find_element`, `_wait_for_url_contains`.
- Методы действий (`_click`, `_send_keys`) не возвращают `self` — чистое разделение ответственности.

### Работа с файлами и путями

- Загрузка файлов реализована через `send_keys()` на элементе `input[type="file"]`.
- Пути к файлам формируются через `pathlib.Path` для кросс‑платформенной совместимости.


# Установка и запуск

## Локальный запуск (без Docker)

### 1. Клонирование и установка зависимостей

```bash
git clone <repository_url>
cd foodgram-tests
pip install -r requirements.txt
```

### 2. Запуск всех тестов

**Все тесты в локальном Chrome:**

```bash
pytest tests/ -v
```

**Запуск конкретного теста:**

```bash
pytest tests/test_registration.py::TestRegistration::test_register_redirects_to_login -v
```

### 3. Запуск с генерацией отчёта Allure

**Запуск тестов с сохранением результатов:**

```bash
pytest tests/ --alluredir=./allure-results -v
```

**Генерация и открытие отчёта:**

```bash
allure generate ./allure-results -o ./allure-report --clean
allure open ./allure-report
```

## Запуск в Docker с Selenoid

### Предварительные требования

* Установлен Docker и Docker Compose.
* Доступ к Docker Hub для скачивания образов.

### Порядок запуска

1. **Скачайте необходимые образы:**

   ```bash
   docker pull aerokube/selenoid:latest-release
   docker pull selenoid/chrome:128.0
   docker pull aerokube/selenoid-ui:latest-release
   ```

2. **Запустите проект:**

   ```bash
   # Сборка и запуск всех сервисов
   docker-compose up --build
   ```

3. **Просмотр логов в реальном времени:**

   ```bash
   docker-compose logs -f foodgram_tests
   ```

4. **Остановка и очистка:**

   * Остановка контейнеров:
     ```bash
     docker-compose down
     ```
   * Полная очистка (образы, тома, сети):
     ```bash
     docker-compose down --rmi all --volumes --remove-orphans
     ```

### Сервисы в `docker-compose`

|     Сервис     | Порт |                   Назначение                    |
|----------------|------|-------------------------------------------------|
| selenoid       | 4444 | Оркестратор браузеров (WebDriver Hub)           |
| selenoid-ui    | 8080 | Веб‑интерфейс для мониторинга сессий            |
| foodgram_tests | —    | Контейнер с тестами (запускается и завершается) |

---

## CI/CD с GitHub Actions

Проект настроен для автоматического запуска тестов при:
* Push в ветки `master` и `develop`.
* Создании Pull Request в `master`.

### Что происходит в пайплайне (`./github/workflows/ci.yml`)

1. **Checkout** — загрузка кода репозитория.
2. **Setup Python** — установка Python 3.11.
3. **Install dependencies** — установка зависимостей из `requirements.txt`.
4. **Start Selenoid** — запуск Selenoid в Docker‑сервисе с healthcheck.
5. **Run tests** — выполнение тестов с Remote WebDriver и Allure.
6. **Upload artifacts** — сохранение результатов тестов и скриншотов.
7. **Generate Allure Report** — публикация отчёта на GitHub Pages.

### Просмотр результатов

* **Логи выполнения**: вкладка *Actions* → выбранный workflow → логи шагов.
* **Артефакты**: вкладка *Actions* → workflow → раздел *Artifacts* (`allure-results`, `screenshots`).
* **Allure Report**: если настроена публикация на GitHub Pages, отчёт доступен по ссылке в комментариях к коммиту.

---

## Отчёты

Отчёты генерируются с помощью инструмента **Allure**.

### Локально

После запуска тестов:

```bash
# Способ 1
allure serve allure-results

# Способ 2
allure generate allure-results -o allure-report --clean
allure open allure-report
```

### В CI/CD

* Результаты сохраняются в артефакты пайплайна.
* При настроенной интеграции с GitHub Pages отчёт публикуется автоматически.

### Преимущества Allure

* 📊 Наглядная статистика: прошло/упало/пропущено.
* 🔍 Детальные шаги каждого теста с скриншотами.
* 🏷️ Группировка по фичам (`@allure.feature`) и историям (`@allure.story`).
* 📎 Вложение скриншотов и логов при падениях.

---

## Конфигурация

* Файл `data.py` — централизованное хранение данных.

### Параметры командной строки (через `conftest.py`)

|     Параметр     |            Описание           |     Значение по умолчанию      |
|------------------|-------------------------------|--------------------------------|
| `--browser`      | Браузер для тестов            | `chrome`                       |
| `--remote`       | Использовать Remote WebDriver | `False`                        |
| `--selenoid-uri` | URI Selenoid                  | `http://localhost:4444/wd/hub` |

#### Примеры использования

* Локальный запуск:
  ```bash
  pytest tests/ --browser chrome -v
  ```
* Запуск через Selenoid:
  ```bash
  pytest tests/ --remote --selenoid-uri http://localhost:4444/wd/hub -v
  ```
* Запуск в Docker (параметры задаются в `docker-compose.yml`):
  ```bash
  docker-compose up --build
  ```

### Переменные окружения для Docker

В `docker-compose.yml` заданы переменные для fallback‑конфигурации:

```yaml
environment:
  - SELENOID_URI=http://selenoid:4444/wd/hub
  - BROWSER=chrome
  - USE_REMOTE=true