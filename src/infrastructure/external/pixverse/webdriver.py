# coding utf-8

from json import loads

from io import BytesIO

from gzip import GzipFile

from seleniumwire import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support.expected_conditions import (
    WebElement,
    presence_of_element_located,
    element_to_be_clickable,
)

from ....domain.constants import PIXVERSE_BASE_URL

from ....domain.entities import ICookie


class PixVerseDriver:
    def __init__(
        self,
        token: str | None = None,
        timeout: int = 2,
        headless: bool = True,
    ) -> None:
        """
        Инициализация драйвера.
            :param token: токен для авторизации (кука)
            :param timeout: таймаут ожидания элементов
            :param headless: запуск без GUI (True по умолчанию)
        """
        options = Options()
        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=0")

        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"},
        )
        options.binary_location = "/usr/bin/google-chrome"

        seleniumwire_options = {
            "disable_encoding": True,
        }

        service = Service(executable_path="/usr/local/bin/chromedriver")

        self._driver = webdriver.Chrome(
            service=service,
            options=options,
            seleniumwire_options=seleniumwire_options,
        )
        self._token = token
        self._wait = WebDriverWait(
            self._driver,
            timeout,
        )

    def open_web(
        self,
    ) -> None:
        """
        Открыть сайт и авторизоваться через куку.
        """

        self._driver.execute_cdp_cmd(
            "Network.enable",
            {},
        )
        self._driver.get(
            PIXVERSE_BASE_URL,
        )
        self._driver.add_cookie(
            cookie_dict=ICookie(
                value=self._token,
            ).dict,
        )
        self._driver.refresh()

    def enter_prompt(
        self,
        text: str,
    ) -> None:
        """
        Ввести текст в поле ввода.
        """

        textarea: WebElement = self._wait.until(
            presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "ant-input",
                ),
            )
        )
        textarea.clear()

        textarea.send_keys(
            text,
        )

    def upload_image(
        self,
        path: str,
    ) -> None:
        """
        Загрузить изображение.
        """

        file_input: WebElement = self._wait.until(
            presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'input[type="file"]',
                ),
            )
        )
        file_input.send_keys(
            path,
        )

    def create_generation(
        self,
    ) -> None:
        """
        Нажать кнопку создания генерации.
        """

        button: WebElement = self._wait.until(
            element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "button.ant-btn.css-x07deh",
                ),
            )
        )
        button.click()

    def get_logs(
        self,
        api_uri: str,
    ) -> None:
        """
        Получить логи с ответами от API с указанным URI.
        """

        for request in self._driver.requests:
            if api_uri in request.url and request.response:
                body_bytes = request.response.body
                if not body_bytes:
                    continue

                try:
                    with GzipFile(fileobj=BytesIO(body_bytes)) as f:
                        text = f.read().decode("utf-8")
                except OSError:
                    text = body_bytes.decode("utf-8")

                return loads(text)

    def quit(
        self,
    ) -> None:
        """
        Закрыть драйвер.
        """

        self._driver.quit()
