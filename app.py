import os
from flask import Flask, render_template_string, redirect, url_for, session, request, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key-change-me")

# HTML Template jisme saare Login Options aur Ad Spaces hain
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADY Store - Login</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; margin: 0; padding: 0; display: flex; flex-direction: column; min-height: 100vh; }
        .ad-space { background-color: #eef2f5; border: 2px dashed #b2bec3; text-align: center; padding: 15px; color: #636e72; font-weight: bold; font-size: 14px; margin: 10px auto; width: 90%; max-width: 728px; border-radius: 8px; }
        .container { flex: 1; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .login-card { background: white; padding: 35px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); width: 100%; max-width: 400px; text-align: center; }
        h2 { color: #2d3436; margin-bottom: 25px; font-size: 28px; font-weight: 600; }
        .input-group { margin-bottom: 15px; text-align: left; }
        .input-group label { display: block; margin-bottom: 5px; color: #636e72; font-size: 14px; }
        .input-group input { width: 100%; padding: 12px; border: 1px solid #dfe6e9; border-radius: 6px; box-sizing: border-box; font-size: 15px; }
        .btn-primary { width: 100%; padding: 12px; background-color: #0984e3; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; margin-top: 10px; }
        .btn-primary:hover { background-color: #074b83; }
        .divider { margin: 20px 0; position: relative; text-align: center; }
        .divider::before { content: ""; position: absolute; top: 50%; left: 0; right: 0; height: 1px; background: #dfe6e9; z-index: 1; }
        .divider span { background: white; padding: 0 15px; color: #b2bec3; font-size: 14px; position: relative; z-index: 2; }
        .btn-google { width: 100%; padding: 12px; background-color: white; color: #2d3436; border: 1px solid #dfe6e9; border-radius: 6px; font-size: 15px; font-weight: 500; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: 0.2s; }
        .btn-google:hover { background-color: #fbfbfb; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .btn-google img { width: 18px; height: 18px; }
        footer { margin-top: auto; }
    </style>
</head>
<body>

    <div class="ad-space">🚀 AD BANNER SPACE (TOP)</div>

    <div class="container">
        <div class="login-card">
            <h2>ADY Store</h2>
            
            <form action="/login-submit" method="POST">
                <div class="input-group">
                    <label>Email or Mobile Number</label>
                    <input type="text" name="identity" placeholder="Enter email or 10-digit mobile" required>
                </div>
                <div class="input-group">
                    <label>Password</label>
                    <input type="password" name="password" placeholder="Enter password" required>
                </div>
                <button type="submit" class="btn-primary">Sign In</button>
            </form>

            <div class="divider">
                <span>OR</span>
            </div>

            <button class="btn-google" onclick="loginWithGoogle()">
                <img src="https://fonts.gstatic.com/s/i/productlogos/googleg/v6/web-24dp/copy_of_googleg_standard_color_24dp.png" alt="Google Logo">
                Continue with Google
            </button>
        </div>
    </div>

    <div class="ad-space">💰 AD BANNER SPACE (BOTTOM)</div>

    <script>
        function loginWithGoogle() {
            // Google Login API Popup URL
            const clientId = "{{ google_client_id }}";
            if (!clientId || clientId === "NONE") {
                alert("Google Client ID configure nahi hai! Kirpa karke Render me Environment Variable set karein.");
                return;
            }
            
            const redirectUri = encodeURIComponent(window.location.origin + '/google-callback');
            const googleUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=email%20profile`;
            
            // Popup window open karna
            window.location.href = googleUrl;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    google_client_id = os.environ.get("GOOGLE_CLIENT_ID", "NONE")
    return render_template_string(LOGIN_PAGE, google_client_id=google_client_id)

@app.route('/login-submit', methods=['POST'])
@app.route('/login-submit', methods=['POST'])
def login_submit():
    identity = request.form.get('identity')
    password = request.form.get('password')
    # Abhi ke liye normal dummy check (Aap ise baad me database se connect kar sakte hain)
    return f"<h1>Login Successful!</h1><p>Welcome to ADY Store. You logged in using: {identity}</p><a href='/'>Go Back</a>"

@app.route('/google-callback')
def google_callback():
    code = request.args.get('code')
    return f"<h1>Google Login Successful!</h1><p>Google Auth Code Received. Welcome to ADY Store!</p><a href='/'>Go Back</a>"

if __name__ == '__main__':
    app.run(debug=True)
