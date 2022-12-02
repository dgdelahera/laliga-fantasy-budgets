import sys
import requests
import logging


def get_code(username, password):
    """Returns the authorization code required to request an auth token
    """
    auth_url = "https://api.laligafantasymarca.com/login/v3/email/auth"
    auth_payload = {"policy": "B2C_1A_ResourceOwnerv2",
                    "username": username,
                    "password": password}
    response = requests.post(auth_url, data=auth_payload).json()
    if "error" in response:
        logging.error(response['error_description'])
        sys.exit(1)
    code = response["code"]
    logging.info(f"Received auth code {code[:10]}...")
    return code


def get_token(username, password):
    """Returns an authorization token
    """
    token_url = "https://api.laligafantasymarca.com/login/v3/email/token"
    token_payload = {"code": get_code(username, password),
                     "policy": "B2C_1A_ResourceOwnerv2"}
    token = requests.post(token_url, data=token_payload).json()["access_token"]
    logging.info(f"Received token {token[:10]}...")
    return token
