from flask import Flask, request, redirect
import requests

app = Flask(__name__)

GOOGLE_CLIENT_ID = "49492231528-gegickrhhuj96p7jnetv7lvrrnna4va1.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8080/auth/callback"

@app.route("/")
def index():
    return 'Login with <a href="/login">Google</a>'

@app.route("/login")
def login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        "?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=email%20profile"
    )
    return redirect(google_auth_url)

@app.route("/auth/callback")
def auth_callback():
    code = request.args.get("code")
    if not code:
        return "Error: No code received", 400

    # Exchange code for access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data)
    token_info = response.json()

    if "access_token" not in token_info:
        return f"Error: {token_info}", 400

    return f"Access Token: {token_info['access_token']}"

if __name__ == "__main__":
    app.run(port=8080, debug=True)
