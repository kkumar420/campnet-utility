import requests
import time
import xml.etree.ElementTree as ET
import sys

URL_LOGIN = "https://campnet.bits-goa.ac.in:8090/login.xml"
URL_LOGOUT = "https://campnet.bits-goa.ac.in:8090/logout.xml"


def get_credentials():
    with open("credentials.txt", "r") as file:
        username = file.readline().strip()
        password = file.readline().strip()

    return username, password


def login():
    username, password = get_credentials()

    data = {
        "mode": "191",
        "username": username,
        "password": password,
        "a": int(time.time() * 1000),
        "producttype": "0"
    }

    response = requests.post(URL_LOGIN, data=data, timeout=10)

    root = ET.fromstring(response.text)

    status = root.findtext("status")
    message = root.findtext("message")

    if status == "LIVE":
        print("Login successful.")
    else:
        print("Login failed.")
        print("Reason:", message)


def logout():
    username, _ = get_credentials()

    data = {
        "mode": "193",
        "username": username,
        "a": int(time.time() * 1000),
        "producttype": "0"
    }

    response = requests.post(URL_LOGOUT, data=data, timeout=10)

    root = ET.fromstring(response.text)

    status = root.findtext("status")
    message = root.findtext("message")

    if "signed out" in message.lower():
        print("Logout successful.")
    else:
        print("Logout failed.")
        print("Reason:", message)


if len(sys.argv) != 2:
    print("Usage: campnet login")
    print("       campnet logout")
    sys.exit(1)

command = sys.argv[1]

if command == "login":
    login()
elif command == "logout":
    logout()
else:
    print(f"Unknown command: {command}")
    print("Usage: campnet login")
    print("       campnet logout")
    sys.exit(1)