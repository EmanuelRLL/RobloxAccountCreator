import csv
from seleniumbase import SB
from config_loader import load_config
from generate_info import generate_credentials


def create_account() -> None:
    """
    Creates a roblox account with random credentials.
    """
    birthday, username, password, gender = generate_credentials()
    with SB(uc=True, incognito=True, locale_code="en") as sb:
        url = "https://www.roblox.com"
        sb.activate_cdp_mode(url)
        sb.cdp.select_option_by_text("#MonthDropdown", birthday[1])
        sb.cdp.select_option_by_text("#YearDropdown", birthday[0])
        sb.cdp.select_option_by_text("#DayDropdown", birthday[2])
        sb.cdp.click("#signup-username")
        sb.cdp.type("#signup-username", username)
        sb.cdp.click("#signup-password")
        sb.cdp.type("#signup-password", password)
        if gender == "female":
            sb.cdp.click("button#FemaleButton")
        elif gender == "male":
            sb.cdp.click("button#MaleButton")
        sb.sleep(5)
        sb.cdp.click("button#signup-button")
        sb.sleep(4)
        while sb.cdp.is_text_visible("An unknown error occurred."):
            sb.sleep(5)
            sb.cdp.click("button#signup-button")
            print("Error while pressing the signup button.")
            sb.sleep(5)
        sb.sleep(20)
        current_url = sb.cdp.get_current_url()
        if current_url == "https://www.roblox.com/home":
            print("Successfully created an account.")
            roblosecurity = "".join(
                [cookie["value"] for cookie in sb.get_cookies() if cookie["name"] == ".ROBLOSECURITY"])
            print(roblosecurity)
            with open("accounts.csv", "a", newline="") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow([username, password, roblosecurity])
            return


while True:
    create_account()
