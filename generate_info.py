import random
from typing import Optional
import requests
from wonderwords import RandomWord

w = RandomWord()

month_number_to_name = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}


def get_xsrf() -> str:
    """
    Return a x-csrf-token
    """
    resp = requests.post("https://auth.roblox.com/v1/usernames/validate")
    csrf_token = resp.headers.get("x-csrf-token")
    return csrf_token


def generate_credentials() -> tuple[list, str, str, Optional[str]]:
    """
    Return a tuple containing valid credentials (birthday, username, password, and gender) for a roblox signup.
    The tuple returned is in the format ([year, month, day], username, password, gender).
    """
    year, month, day = str(random.randint(2000, 2005)), str(random.randint(1, 12)), str(random.randint(1, 25))
    if int(day) < 10:
        day = "0" + day
    if int(month) < 10:
        month = "0" + month
    curr_username = w.word(word_min_length=4, word_max_length=8) + w.word(word_min_length=4, word_max_length=8)
    csrf_token = get_xsrf()
    headers = {"X-CSRF-TOKEN": csrf_token}
    payload = {
        "birthday": f"{year}-{month}-{day}T03:00:00.000Z",
        "context": "Signup",
        "username": curr_username
    }
    validate_username = requests.post("https://auth.roblox.com/v1/usernames/validate", json=payload, headers=headers)
    while validate_username.json()["message"] != "Username is valid":
        curr_username = w.word(word_min_length=4, word_max_length=8) + w.word(word_min_length=4, word_max_length=8)
        payload = {
            "birthday": f"{year}-{month}-{day}T03:00:00.000Z",
            "context": "Signup",
            "username": curr_username
        }
        validate_username = requests.post("https://auth.roblox.com/v1/usernames/validate", json=payload,
                                          headers=headers)
    curr_password = w.word(word_min_length=6, word_max_length=9) + w.word(word_min_length=6, word_max_length=9)
    payload = {
        "username": curr_username,
        "password": curr_password
    }
    validate_password = requests.post("https://auth.roblox.com/v2/passwords/validate", json=payload, headers=headers)
    while validate_password.json()["message"] != "Password is valid":
        curr_password = w.word(word_min_length=6, word_max_length=9) + w.word(word_min_length=6, word_max_length=9)
        payload = {
            "username": curr_username,
            "password": curr_password
        }
        validate_password = requests.post("https://auth.roblox.com/v2/passwords/validate", json=payload,
                                          headers=headers)
    gender = random.choice(["female", "male", None])
    print("Successfully generated credentials.")
    return [year, month_number_to_name[month], day], curr_username, curr_password, gender
