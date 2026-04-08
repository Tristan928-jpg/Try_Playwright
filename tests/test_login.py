import pytest
from playwright.sync_api import Page, expect
from pages.login import LoginPage

@pytest.fixture
def login_page(page: Page):
    login = LoginPage(page)
    login.navigate()
    return login

valid_login_credentials = ["felix_pecayo@solenergy.com.ph", "501Energy"]

def test_login_required_fields(login_page):
    login_page.verify_login_emptyfields()

def test_loginwithemail_btn(login_page):
    login_page.verify_loginwithemail_btn()

test_data_missing_email = [
    ("alice", "123Password"),                 
    ("alice@domain", "123Password"),             
    ("@domain.com", "Pass1234"),       
    ("bob@.com", "Password1"), 
]
@pytest.mark.parametrize(
    "username, password",
    test_data_missing_email,
    ids=["missing_email_1", "missing_email_2", "missing_email_3", "missing_email_4"]
)

def test_email_missing(login_page, username, password):
    login_page.verify_invalid_email(username, password)

invalid_chars_email_data = [
    ("alice!@domain.com", "501Energy"),
    ("bob#smith@domain.com", "123Password"),
    ("john doe@domain.com", "Pass1234"),
]

@pytest.mark.parametrize(
    "username, password",
    invalid_chars_email_data,
    ids=["invalid_char_email_1", "invalid_char_email_2", "invalid_char_email_3"]
)

def test_invalid_email(login_page, username, password):
    login_page.verify_invalid_email(username, password)

def test_unregistered_email(login_page):
    login_page.verify_unregistered_email("JohnDoe@solenergy.com.ph", "Password123")

def test_different_email_domain(login_page):
    login_page.verify_using_different_domain("JohnDoe@gmail.com.ph", "Password123")

def test_unverified_email(login_page):
    login_page.verify_unverified_email("felix.pecayo@solenergy.com.ph", "Password123")

def test_verified_wrongpass(login_page):
    login_page.verify_verified_email_wrong_password(valid_login_credentials[0], "Password123")

def test_valid_credentials(login_page):
    login_page.verify_valid_credentials(valid_login_credentials[0], valid_login_credentials[1])

def test_logout(login_page):
    login_page.verify_logout(valid_login_credentials[0], valid_login_credentials[1])