import pytest
import allure

from pages.registration_page import RegistrationPage
from pages.dashboard_page import DashboardPage


@allure.epic("Authentication")
@allure.feature("Registration")
@allure.story("User registration")
@allure.title("Успешная регистрация нового пользователя")
@allure.id("TC-003")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.regression
@pytest.mark.registration
def test_successful_registration(dashboard_page: DashboardPage, registration_page: RegistrationPage):
    with allure.step("Открыть страницу регистрации"):
        registration_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")

    with allure.step("Заполнить форму регистрации"):
        registration_page.fill_registration_form(
            email="user.name@gmail.com",
            username="username",
            password="password"
        )

    with allure.step("Нажать кнопку регистрации"):
        registration_page.click_registration_button()

    with allure.step("Проверить, что дашборд отобразился"):
        dashboard_page.check_visible_dashboard_title()