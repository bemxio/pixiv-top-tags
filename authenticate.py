#!/usr/bin/env python

import re
import json
import time
import base64
import hashlib
import secrets
from urllib.parse import urlencode

import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# constants
USER_AGENT = "PixivIOSApp/7.13.3 (iOS 14.6; iPhone13,2)"

REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback"
LOGIN_URL = "https://app-api.pixiv.net/web/v1/login"
AUTH_TOKEN_URL = "https://oauth.secure.pixiv.net/auth/token"

CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT"
CLIENT_SECRET = "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"

def sha256(data: bytes) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode("ascii")

def oauth_pkce() -> tuple[str, str]: 
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = sha256(code_verifier.encode("ascii"))

    return (code_verifier, code_challenge)

def save_token(response: dict) -> None:
    if "response" in response:
        data = response["response"]
    else:
        data = response.copy()

    with open("credentials.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def main() -> None:
    DesiredCapabilities.CHROME["goog:loggingPrefs"] = {
        "performance": "ALL", # enable performance logs
    }

    driver = webdriver.Chrome()
    code_verifier, code_challenge = oauth_pkce()

    login_params = {
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "client": "pixiv-android",
    }

    driver.get(LOGIN_URL + "?" + urlencode(login_params))

    # wait for login
    while True:
        if driver.current_url[:40] == "https://accounts.pixiv.net/post-redirect":
            break

        time.sleep(1)

    # filter code URL from performance logs
    code = None

    for row in driver.get_log("performance"):
        data = json.loads(row.get("message", {}))

        message = data.get("message", {})
        method = message.get("method", "")

        if method == "Network.requestWillBeSent":
            url = message.get("params", {}).get("documentURL")

            if url[:8] != "pixiv://":
                continue
            
            code = re.search(r"code=([^&]*)", url).groups()[0]
            break

    driver.close()

    response = requests.post(
        AUTH_TOKEN_URL,

        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,

            "code": code,
            "code_verifier": code_verifier,

            "grant_type": "authorization_code",

            "include_policy": "true",
            "redirect_uri": REDIRECT_URI,
        },
        headers={
            "user-agent": USER_AGENT,
            "app-os-version": "14.6",
            "app-os": "ios",
        }
    )

    save_token(response.json())

if __name__ == "__main__":
    main()