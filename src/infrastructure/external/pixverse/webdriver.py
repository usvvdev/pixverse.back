# coding utf-8

from json import dumps, loads

import undetected_chromedriver as uc

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
        options = uc.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        options.binary_location = "/usr/bin/google-chrome"

        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"},
        )

        self._driver = uc.Chrome(options=options)
        self._token = token
        self._wait = WebDriverWait(
            self._driver,
            timeout,
        )

    def open_web(
        self,
    ) -> None:
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
        logs = self._driver.get_log("performance")
        for entry in logs:
            log = loads(entry["message"])["message"]
            if log["method"] == "Network.responseReceived":
                url = log["params"]["response"]["url"]
                if api_uri in url:
                    return dumps(log, indent=2)

    def quit(
        self,
    ) -> None:
        self._driver.quit()
