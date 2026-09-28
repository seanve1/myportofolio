import os
import sys
import django

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "portofolio.settings"
)

django.setup()
load_dotenv()

USER_PASSWORD = os.getenv("E2E_USER_PASSWORD")
ADMIN_PASSWORD = os.getenv("E2E_ADMIN_PASSWORD")

from django.contrib.auth.models import User
BASE_URL = "http://127.0.0.1:8000"


def setup_users():
    user, _ = User.objects.get_or_create(
        username="test_user"
    )

    user.set_password(USER_PASSWORD)
    user.is_superuser = False
    user.is_staff = False
    user.save()

    admin, _ = User.objects.get_or_create(
        username="test_admin"
    )

    admin.set_password(ADMIN_PASSWORD)
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()

def main():
    setup_users()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        options=options
    )

    wait = WebDriverWait(driver, 10)

    try:
        # 1. Cek CSRF login
        driver.get(
            f"{BASE_URL}/login/"
        )

        csrf = wait.until(
            EC.presence_of_element_located(
                (
                    By.NAME,
                    "csrfmiddlewaretoken"
                )
            )
        )

        assert csrf.get_attribute("value")

        print(
            "[PASS] CSRF login"
        )

        # 2. Login user biasa
        driver.find_element(
            By.NAME,
            "username"
        ).send_keys(
            "test_user"
        )

        driver.find_element(
            By.NAME,
            "password"
        ).send_keys(
            USER_PASSWORD
        )

        driver.find_element(
            By.XPATH,
            "//button[@type='submit']"
        ).click()

        wait.until(
            EC.url_to_be(
                f"{BASE_URL}/"
            )
        )

        assert driver.get_cookie(
            "sessionid"
        )

        assert driver.get_cookie(
            "last_login"
        )

        print(
            "[PASS] Login user + cookie"
        )

        # 3. User biasa tidak boleh add organization
        driver.get(
            f"{BASE_URL}/organization/add/"
        )

        assert (
            "403" in driver.title
            or
            "Forbidden" in driver.page_source
        )

        print(
            "[PASS] User biasa dibatasi"
        )

        # 4. Login superuser
        driver.get(
            f"{BASE_URL}/logout/"
        )

        driver.get(
            f"{BASE_URL}/login/"
        )

        driver.find_element(
            By.NAME,
            "username"
        ).send_keys(
            "test_admin"
        )

        driver.find_element(
            By.NAME,
            "password"
        ).send_keys(
            ADMIN_PASSWORD
        )

        driver.find_element(
            By.XPATH,
            "//button[@type='submit']"
        ).click()

        wait.until(
            EC.url_to_be(
                f"{BASE_URL}/"
            )
        )

        driver.get(
            f"{BASE_URL}/organization/add/"
        )

        assert (
            "organization-form"
            in driver.page_source
        )

        print(
            "[PASS] Superuser access"
        )

        # 5. Logout hapus cookie
        driver.get(
            f"{BASE_URL}/logout/"
        )

        assert driver.get_cookie(
            "last_login"
        ) is None

        print(
            "[PASS] Logout cookie removed"
        )

        print(
            "\nAll E2E tests passed!"
        )

    finally:
        driver.quit()

if __name__ == "__main__":
    main()