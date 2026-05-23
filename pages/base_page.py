import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, timeout=15):
        self._driver = driver
        self._wait = WebDriverWait(driver, timeout)

    @allure.step("Открыть страницу по URL: {url}")
    def _open(self, url):
        self._driver.get(url)

    def _find_element(self, locator):
        return self._wait.until(EC.presence_of_element_located(locator))

    def _find_visible_element(self, locator):
        return self._wait.until(EC.visibility_of_element_located(locator))

    def _find_elements(self, locator):
        return self._wait.until(EC.presence_of_all_elements_located(locator))

    @allure.step("Кликнуть по элементу: {locator}")
    def _click(self, locator):
        element = self._wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Ввести текст '{text}' в поле: {locator}")
    def _send_keys(self, locator, text):
        element = self._find_visible_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Загрузить файл '{file_path}' в поле: {locator}")
    def _send_keys_file(self, locator, file_path):
        self._find_element(locator).send_keys(file_path)

    def _is_visible(self, locator):
        try:
            self._wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
            
    def get_current_url(self):
       # Возвращает текущий URL страницы
        return self._driver.current_url

    def wait_for_url_contains(self, substring):
        # Ждет, пока URL будет содержать подстроку
        self._wait.until(lambda d: substring in d.current_url)