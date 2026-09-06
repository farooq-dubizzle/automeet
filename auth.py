import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE, FROZEN, ACCESS_DENIED_MSG


def get_credentials():
    creds = None

    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception:
            creds = None

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save_token(creds)
            return creds
        except Exception:
            creds = None

    if creds and creds.valid:
        return creds

    if not os.path.exists(CREDENTIALS_FILE):
        if FROZEN:
            raise RuntimeError(ACCESS_DENIED_MSG)
        raise FileNotFoundError("Place credentials.json in the project folder.")

    try:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    except Exception as e:
        if FROZEN:
            raise RuntimeError(ACCESS_DENIED_MSG) from None
        raise e

    _save_token(creds)
    return creds


def _save_token(creds):
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())
