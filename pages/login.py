from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        #Login Locators
        self.loginbtn = page.locator('//*[@id="options-page"]/div[2]/button')
        self.username_input = page.locator('//*[@id="login-page"]/form/div[2]/div[1]/input')
        self.password_input = page.locator('//*[@id="login-page"]/form/div[2]/div[2]/input')
        self.login_button = page.locator('//*[@id="login-page"]/form/button')
        self.error_message = page.locator('//*[@id="login-page"]/form/div[2]/div/div')
        self.loading_spinner = page.locator('//*[@id="__next"]/div[3]')
        self.map = page.locator('//*[@id="__next"]/div[3]/div/div[1]/div[1]/div')
        self.account_btn = page.locator('//*[@id="__next"]/div[2]/div/div[2]/button')
        self.logoutbtn = page.locator('//*[@id="contentBodyScrollable"]/ul[3]/li[2]')

    def navigate(self):
        self.page.goto("https://dev.evcharging.ph/")

    def verify_login_emptyfields(self):
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        self.login_button.click()
        is_invalid = self.username_input.evaluate("el => !el.checkValidity()")
        print(f"Firstname invalid: {is_invalid}")
        message = self.password_input.evaluate("el => el.validationMessage")
        print(f"Validation message: '{message}'")

        assert is_invalid is True
        assert message != ""

    #Verify Login Page
    def verify_loginwithemail_btn(self):
        expect(self.loginbtn).to_be_visible()
        self.loginbtn.click()
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()

    # Verify Login with invalid Email
    def verify_invalid_email(self, username: str, password: str):
        self.verify_loginwithemail_btn()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text("Please provide a valid email address.")

    # Verify Login with Unregistered email
    def verify_unregistered_email(self, username: str, password: str):
        self.verify_loginwithemail_btn()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        expect(self.loading_spinner).to_be_hidden(timeout=10000)
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text("We couldn't find an account matching this email address.")

    # Verify Login with Unregistered email
    def verify_using_different_domain(self, username: str, password: str):
        self.verify_loginwithemail_btn()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        expect(self.loading_spinner).to_be_hidden(timeout=10000)
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text("We couldn't access your account. If you think this is a mistake, please contact our support.")

    # Verify Login with Unverified Email
    def verify_unverified_email(self, username: str, password: str):
        self.verify_loginwithemail_btn()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        expect(self.loading_spinner).to_be_hidden(timeout=10000)
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text("Account is not yet verified. Please verify your account to proceed.")

    # Verify Valid Email with wrong password
    def verify_verified_email_wrong_password(self, username: str, password: str):
        self.verify_loginwithemail_btn()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        expect(self.loading_spinner).to_be_hidden(timeout=10000)
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text("Your email and password do not match.")

    # Verify Login with valid email and password
    def verify_valid_credentials(self, username: str, password: str):
        self.page.wait_for_load_state()
        self.verify_loginwithemail_btn()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_load_state(timeout=10000)
        expect(self.map).to_be_visible()

    # Verify Login and Logout
    def verify_logout(self, username: str, password: str):
        self.verify_loginwithemail_btn()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_load_state()
        expect(self.map).to_be_visible()
        self.account_btn.click()
        self.logoutbtn.click()
        self.page.wait_for_load_state(timeout=15000)
        expect(self.loginbtn).to_be_visible()

    
