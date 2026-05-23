import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

@pytest.fixture
def login_page(chromium_page) -> LoginPage:
    return LoginPage(page=chromium_page)