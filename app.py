from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# --- REAL BACKEND STORAGE (In-Memory Database) ---
DATA_STORE = {
    "products": [],
    "account": {
        "business_name": "",
        "mobile": "",
        "address": ""
    },
    "payout": {
        "method": "bank",
        "bank_account": "",
        "ifsc": "",
        "upi_id": ""
    }
}

# --- ULTRA-MODERN PREMIUM FRONTEND UI ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ADY STORE - Full-Stack Enterprise Platform</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { background-color: #f4f6f9; min-height: 100vh; color: #202124; }
        
        /* Auth Screen Styling */
        .auth-container { display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .auth-card { background: white; padding: 40px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 100%; max-width: 440px; text-align: center; border: 1px solid #e0e0e0; }
        .brand-title { color: #1a73e8; font-size: 34px; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.5px; }
        .brand-subtitle { color: #5f6368; font-size: 15px; margin-bottom: 24px; }
        
        /* Role Tabs - Highly Clickable & Responsive */
        .identity-tabs { display: flex; gap: 12px; margin-bottom: 24px; background: #f1f3f4; padding: 6px; border-radius: 8px; }
        .tab-btn { flex: 1; padding: 12px; border: none; border-radius: 6px; background: transparent; cursor: pointer; font-weight: 600; color: #5f6368; font-size: 15px; transition: all 0.2s ease; }
        .tab-btn.active { background: white; color: #1a73e8; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
        
        .google-login-btn { display: flex; align-items: center; justify-content: center; gap: 12px; width: 100%; padding: 14px; border: 1px solid #dadce0; border-radius: 8px; background-color: white; color: #3c4043; font-size: 15px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
        .google-login-btn:hover { background-color: #f8f9fa; }
        .google-login-btn img { width: 22px; height: 22px; }
        
        /* Form Components */
        input, select { padding: 12px 16px; border-radius: 8px; border: 1px solid #dadce0; font-size: 15px; outline: none; background-color: #fff; width: 100%; margin-bottom: 16px; display: block; }
        input:focus, select:focus { border-color: #1a73e8; box-shadow: 0 0 0 2px rgba(26,115,232,0.2); }
        label { display: block; text-align: left; font-weight: 600; font-size: 14px; margin-bottom: 6px; color: #3c4043; }
        
        .action-btn { padding: 14px; border-radius: 8px; border: none; background-color: #1a73e8; color: white; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%; transition: background 0.2s; }
        .action-btn:hover { background-color: #1557b0; }
        .success-btn { background-color: #34a853; }
        .success-btn:hover { background-color: #2d8b44; }
        
        /* Master Dashboard Panel */
        .workspace-wrapper { display: none; flex-direction: column; min-height: 100vh; }
        navbar { display: flex; justify-content: space-between; align-items: center; padding: 16px 40px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
        .nav-brand { font-size: 22px; font-weight: bold; color: #1a73e8; }
        .logout-btn { padding: 8px 16px; border-radius: 6px; border: 1px solid #d93025; background: transparent; color: #d93025; cursor: pointer; font-weight: 600; }
        .logout-btn:hover { background: #fce8e6; }
        
        .container { padding: 40px; max-width: 1240px; margin: 0 auto; width: 100%; }
        .panel-section { display: none; }
        .panel-section.active { display: block; }
        
        /* Grid Layout */
        .grid-system { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 24px; margin-top: 24px; }
        @media (max-width: 900px) { .grid-system { grid-template-columns: 1fr; } }
        
        .card-panel { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); border: 1px solid #e0e0e0; margin-bottom: 24px; }
        .card-panel h3 { margin-bottom: 20px; color: #1a73e8; font-size: 19px; border-bottom: 2px solid #f1f3f4; padding-bottom: 10px; }
        
        /* Metrics Tracker */
        .metrics-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px; }
        .metric-card { background: #e8f0fe; padding: 20px; border-radius: 10px; text-align: center; color: #1a73e8; font-weight: bold; }
        .metric-card span { display: block; font-size: 26px; margin-top: 6px; color: #202124; }
        
        /* Data Presentation */
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px 16px; border-bottom: 1px solid #f1f3f4; font-size: 14px; text-align: left; }
        th { background: #f8f9fa; color: #5f6368; font-weight: 600; }
        .empty-row { text-align: center; color: #9aa0a6; padding: 30px; font-style: italic; }
    </style>
</head>
<body>

    <div id="authViewport" class="auth-container">
        <div class="auth-card">
            <h2 class="brand-title">ADY STORE</h2>
            <p id="flowSubtitle" class="brand-subtitle">अपने ग्राहक अकाउंट में लॉगिन करें</p>
            
            <div class="identity-tabs">
                <button type="button" id="tabCustomer" class="tab-btn active" onclick="updateActiveRole('customer')">🛍️ Customer</button>
                <button type="button" id="tabSeller" class="tab-btn" onclick="updateActiveRole('seller')">🏢 Seller Panel</button>
            </div>

            <div style="margin-bottom: 20px;">
                <button type="button" class="google-login-btn" onclick="simulateGoogleLogin()">
                    <img src="https://fonts.gstatic.com/s/i/productlogos/googleg/v6/web-24dp/copy_of_googleg_standard_color_24dp.png" alt="Google">
                    Google के साथ आगे बढ़ें (OAuth Setup)
                </button>
            </div>
        </div>
    </div>

    <div id="appViewport" class="workspace-wrapper">
        <navbar>
            <div class="nav-brand" id="dynamicBrandText">ADY STORE</div>
            <button class="logout-btn" onclick="performLogout()">लॉगआउट</button>
        </navbar>

        <div class="container">
            <div id="customerSection" class="panel-section">
                <div class="card-panel">
                    <h3>🛍️ कस्टमर मार्केटप्लेस (Storefront)</h3>
                    <p>लॉगिन सफल रहा! आपका customer डैशबोर्ड लाइव है।</p>
                </div>
            </div>

            <div id="sellerSection" class="panel-section">
                <div class="metrics-row">
                    <div class="metric-card">कुल व्यापार <span>₹0</span></div>
                    <div class="metric-card">सक्रिय ऑर्डर्स <span>0</span></div>
                    <div class="metric-card">लाइव प्रोडक्ट्स <span id="liveProductsCounter">0</span></div>
                </div>

                <div class="grid-system">
                    <div class="card-panel">
                        <h3>📦 Product Listing (नया प्रॉдक्ट जोड़ें)</h3>
                        <form onsubmit="submitNewProductBackend(event)">
                            <label>प्रॉडक्ट का नाम:</label>
                            <input type="text" id="prodName" placeholder="उदा. Pro Mechanical Keyboard" required>
                            <label>कीमत (INR):</label>
                            <input type="number" id="prodPrice" placeholder="उदा. 4599" required>
                            <label>श्रेणी (Category):</label>
                            <select id="prodCategory">
                                <option value="Electronics">📱 Electronics</option>
                                <option value="Fashion">👕 Fashion</option>
                                <option value="Home">🏠 Home & Kitchen</option>
                            </select>
                            <button type="submit" class="action-btn success-btn">✓ मार्केटप्लेस पर लाइव करें</button>
                        </form>

                        <h4 style="margin-top: 24px; font-size: 15px; color:#3c4043;">आपके एक्टिव प्रोडक्ट्स:</h4>
                        <table>
                            <thead><tr><th>प्रॉडक्ट नाम</th><th>कैटेगरी</th><th>कीमत</th></tr></thead>
                            <tbody id="productsTableBody"></tbody>
                        </table>
                    </div>

                    <div>
                        <div class="card-panel">
                            <h3>💳 Payout Settings (पेमेंट कैसे लेना चाहेंगे?)</h3>
                            <form onsubmit="submitPayoutSettingsBackend(event)">
                                <label>पैसे传输 करने का माध्यम:</label>
                                <select id="payoutMethod" onchange="togglePayoutFormFields()">
                                    <option value="bank">🏦 Direct Bank Transfer</option>
                                    <option value="upi">📲 UPI Instant Transfer</option>
                                </select>
                                <div id="bankInputs">
                                    <label>बैंक खाता संख्या (Account Number):</label>
                                    <input type="text" placeholder="खाता संख्या दर्ज करें" id="bankAcc">
                                    <label>IFSC कोड:</label>
                                    <input type="text" placeholder="IFSC कोड दर्ज करें" id="bankIfsc">
                                </div>
                                <div id="upiInputs" style="display: none;">
                                    <label>अपनी UPI ID:</label>
                                    <input type="text" placeholder="username@oksbi" id="upiId">
                                </div>
                                <button type="submit" class="action-btn" style="padding: 10px; font-size:14px;">Payout सुरक्षित करें</button>
                            </form>
                        </div>

                        <div class="card-panel">
                            <h3>⚙️ Account Details (प्रोफाइल सेटिंग्स)</h3>
                            <form onsubmit="submitAccountDetailsBackend(event)">
                                <label>व्यापार/दुकान का नाम:</label>
                                <input type="text" id="bizName" placeholder="Legal Business Name" required>
                                <label>मोबाइल नंबर:</label>
                                <input type="tel" id="bizPhone" placeholder="+91 XXXXX XXXXX" required>
                                <label>पिकअप एड्रेस (गोदाम का पता):</label>
                                <input type="text" id="bizAddress" placeholder="पूरा पता भरें" required>
                                <button type="submit" class="action-btn" style="padding: 10px; font-size:14px; background-color: #5f6368;">प्रोफाइल अपडेट करें</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentRoleState = "customer";

        function updateActiveRole(role) {
            currentRoleState = role;
            document.getElementById('tabCustomer').classList.toggle('active', role === 'customer');
            document.getElementById('tabSeller').classList.toggle('active', role === 'seller');
            document.getElementById('flowSubtitle').innerText = role === 'customer' ? "अपने ग्राहक अकाउंट में लॉगिन करें" : "अपने विक्रेता (Seller) पैनल में लॉगिन करें";
        }

        function togglePayoutFormFields() {
            const method = document.getElementById('payoutMethod').value;
            document.getElementById('bankInputs').style.display = (method === 'bank') ? 'block' : 'none';
            document.getElementById('upiInputs').style.display = (method === 'upi') ? 'block' : 'none';
        }

        // --- CORE FETCH SYNCHRONIZATION WITH PYTHON BACKEND ---
        function pullDataFromPythonBackend() {
            fetch('/api/products')
            .then(res => res.json())
            .then(data => {
                const tbody = document.getElementById('productsTableBody');
                document.getElementById('liveProductsCounter').innerText = data.length;
                if(data.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="3" class="empty-row">No real products listed yet.</td></tr>`;
                    return;
                }
                tbody.innerHTML = data.map(p => `<tr><td><strong>${p.name}</strong></td><td>${p.category}</td><td>₹${Number(p.price).toLocaleString('en-IN')}</td></tr>`).join('');
            });

            fetch('/api/account')
            .then(res => res.json())
            .then(data => {
                document.getElementById('bizName').value = data.business_name || "";
                document.getElementById('bizPhone').value = data.mobile || "";
                document.getElementById('bizAddress').value = data.address || "";
            });
        }

        function submitNewProductBackend(e) {
            e.preventDefault();
            const payload = {
                name: document.getElementById('prodName').value,
                price: document.getElementById('prodPrice').value,
                category: document.getElementById('prodCategory').value
            };
            fetch('/api/products', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            }).then(res => res.json()).then(res => {
                alert(res.message);
                document.getElementById('prodName').value = "";
                document.getElementById('prodPrice').value = "";
                pullDataFromPythonBackend();
            });
        }

        function submitPayoutSettingsBackend(e) {
            e.preventDefault();
            const payload = {
                method: document.getElementById('payoutMethod').value,
                bank_account: document.getElementById('bankAcc').value,
                ifsc: document.getElementById('bankIfsc').value,
                upi_id: document.getElementById('upiId').value
            };
            fetch('/api/payout', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            }).then(res => res.json()).then(res => alert(res.message));
        }

        function submitAccountDetailsBackend(e) {
            e.preventDefault();
            const payload = {
                business_name: document.getElementById('bizName').value,
                mobile: document.getElementById('bizPhone').value,
                address: document.getElementById('bizAddress').value
            };
            fetch('/api/account', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            }).then(res => res.json()).then(res => alert(res.message));
        }

        function simulateGoogleLogin() {
            localStorage.setItem('auth_session_role', currentRoleState);
            renderSystemDashboard(currentRoleState);
        }

        function renderSystemDashboard(role) {
            document.getElementById('authViewport').style.display = 'none';
            document.getElementById('appViewport').style.display = 'flex';
            
            document.getElementById('customerSection').classList.toggle('active', role === 'customer');
            document.getElementById('sellerSection').classList.toggle('active', role === 'seller');
            
            if(role === 'seller') {
                document.getElementById('dynamicBrandText').innerText = "ADY CONTROL CENTER (SELLER)";
                pullDataFromPythonBackend();
            } else {
                document.getElementById('dynamicBrandText').innerText = "ADY STORE";
            }
        }

        function performLogout() {
            localStorage.clear();
            location.reload();
        }

        window.onload = function() {
            const currentSession = localStorage.getItem('auth_session_role');
            if(currentSession) {
                renderSystemDashboard(currentSession);
            }
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_LAYOUT)

@app.route('/api/products', methods=['GET', 'POST'])
def handle_products_api():
    if request.method == 'POST':
        DATA_STORE["products"].append(request.json)
        return jsonify({"status": "success", "message": "🎉 प्रॉडक्ट सफलतापूर्वक डेटाबेस में लाइव हो गया!"})
    return jsonify(DATA_STORE["products"])

@app.route('/api/account', methods=['GET', 'POST'])
def handle_account_api():
    if request.method == 'POST':
        DATA_STORE["account"] = request.json
        return jsonify({"status": "success", "message": "⚙️ प्रोफाइल सेटिंग्स डेटाबेस में अपडेट हो गई हैं!"})
    return jsonify(DATA_STORE["account"])

@app.route('/api/payout', methods=['POST'])
def handle_payout_api():
    DATA_STORE["payout"] = request.json
    return jsonify({"status": "success", "message": "💳 पेमेंट ट्रांसफर डिटेल्स सुरक्षित कर दी गई हैं!"})

if __name__ == '__main__':
    app.run(debug=True)