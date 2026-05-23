from playwright.sync_api import expect, Page
import pytest
from pages.login_page import LoginPage

@pytest.mark.parametrize(
    'email, password',
    [
        ('user.name@gmail.com', 'password'),
        ('user.name@gmail.com', '  '),
        ('  ', 'password')
    ]
)
def test_wrong_email_or_password_authorization(login_page: LoginPage, email: str, password: str):
    login_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")
    login_page.fill_login_form(email=email, password=password)
    login_page.click_login_button()
    login_page.check_visible_wrong_email_or_password_alert()

    # chromium_page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login")
    # email_input = chromium_page.get_by_test_id('login-form-email-input').locator('input')
    # email_input.fill(email)
    #
    # password_input = chromium_page.get_by_test_id('login-form-password-input').locator('input')
    # password_input.fill(password)
    #
    # login_button = chromium_page.get_by_test_id('login-page-login-button')
    # login_button.click()
    #
    # wrong_email_password_alert = chromium_page.get_by_test_id('login-page-wrong-email-or-password-alert')
    # expect(wrong_email_password_alert).to_be_visible()
    # expect(wrong_email_password_alert).to_have_text('Wrong email or password')