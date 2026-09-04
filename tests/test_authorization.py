from playwright.sync_api import expect, Page
import pytest
import allure
from pages.login_page import LoginPage


@allure.epic("Authentication")
@allure.feature("Login")
@allure.story("Invalid credentials")
@allure.title("Проверка ошибки при неверных email или пароле")
@allure.id("TC-004")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    'email, password',
    [
        ('user.name@gmail.com', 'password'),
        ('user.name@gmail.com', '  '),
        ('  ', 'password')
    ]
)
def test_wrong_email_or_password_authorization(login_page: LoginPage, email: str, password: str):
    with allure.step("Открыть страницу логина"):
        login_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")

    with allure.step(f"Заполнить форму логина: email='{email}', password='{password}'"):
        login_page.fill_login_form(email=email, password=password)

    with allure.step("Нажать кнопку входа"):
        login_page.click_login_button()

    with allure.step("Проверить, что появилось сообщение об ошибке"):
        login_page.check_visible_wrong_email_or_password_alert()