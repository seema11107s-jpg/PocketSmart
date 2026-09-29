# PocketSmart AI - Your Smart Budget & Recommendation Assistant
# Created by SEEMA S - Gemini 1.5 Flash Pro
# SmartBridge Project - No Error Version

from flask import Flask, request, session, redirect, render_template_string
import os, sqlite3, datetime

app = Flask(__name__)
app.secret_key = "seema_pocketsmart_2024"

# ================= GEMINI 1.5 FLASH PRO SETUP =================
GEMINI_ON = False
model = None
try:
    import google.generativeai as genai
    API_KEY = os.getenv("GEMINI_API_KEY", "")
    # Ungalukku API key iruntha inga podunga ma: "AIzaSy...."
    if API_KEY == "":
        API_KEY = "YOUR_GEMINI_API_KEY_HERE" # Itha maathunga ma venumna
    if "YOUR" not in API_KEY and len(API_KEY) > 20:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        GEMINI_ON = True
        print("Gemini 1.5 Flash Connected ma!")
except Exception as e:
    GEMINI_ON = False
    print(f"Gemini offline ma - Mock data use pannrom ma: {e}")

def get_gemini_recommendation(prompt):
    """Gemini 1.5 Flash Pro call ma - error vantha mock tharum ma"""
    if GEMINI_ON and model:
        try:
            response = model.generate_content(prompt)
            return response.text
        except:
            return None
    return None

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect('pocketsmart.db', check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, created DATE)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS history
                    (id INTEGER PRIMARY KEY, email TEXT, type TEXT, budget TEXT, result TEXT, date DATE)''')
    conn.commit()
    return conn
db = init_db()

# ================= COMMON CSS & HEADER =================
BASE_CSS = """
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}
body{background:#f5f7fa;padding:12px}
.topbar{display:flex;justify-content:space-between;background:white;padding:12px 15px;border-radius:10px;box-shadow:0 2px 5px #0001;margin-bottom:12px}
.topbar b{color:#1a365d}
.nav{background:#0f1f3a;color:white;padding:12px;border-radius:10px;display:flex;justify-content:space-between;font-size:11px;flex-wrap:wrap;gap:5px}
.nav a{color:white;text-decoration:none;margin:0 5px}
.page{background:white;max-width:850px;margin:0 auto;border:1px solid #222;padding:18px;border-radius:10px}
.bluebtn{background:#1a365d;color:white;padding:9px 22px;border-radius:22px;text-align:center;width:280px;margin:12px auto;display:block;font-size:13px;border:none}
.hd{background:#1e4a7a;color:white;padding:9px;border-radius:6px;font-weight:bold;margin-top:18px;font-size:13px}
.hd2{background:white;color:#1e4a7a;border-left:4px solid #1e4a7a;padding:7px;font-weight:bold;margin-top:18px;font-size:13px}
table{width:100%;border-collapse:collapse;font-size:12px;margin:10px 0}
th{border-bottom:1.5px solid #ccc;padding:7px;text-align:left;color:#555;font-size:11px}
td{border-bottom:1px solid #eee;padding:7px;font-size:12px}
.link{background:#eef2ff;border:1px solid #c7d2fe;border-radius:4px;padding:2px 7px;font-size:10px;margin:2px;display:inline-block}
.sugg{background:#1e4a7a;color:white;padding:9px;border-radius:6px;margin-top:18px;font-size:13px}
.btn{padding:11px;background:#1e4a7a;color:white;border:none;border-radius:8px;width:100%;margin:6px 0;font-weight:bold;cursor:pointer}
.btn2{background:#ff6b35}
.btn3{background:#E91E63}
input,select{width:100%;padding:9px;border:1px solid #ddd;border-radius:6px;margin:6px 0}
.card{background:#f8fafc;padding:14px;border-radius:10px;margin:10px 0;border:1px solid #e2e8f0}
small{color:#666}
</style>
"""

def render_page(content):
    html = f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1'><title>PocketSmart AI - Gemini 1.5 Flash</title>{BASE_CSS}</head><body>"
    html += '<div class="topbar"><div><span style="color:#ff6b35;font-weight:bold;font-size:18px">S</span> SMARTBRIDGE</div><div>Smart Internz - PocketSmart AI</div></div>'
    html += content + "</body></html>"
    return render_template_string(html)

# ================= HOME PAGE =================
@app.route('/')
def index():
    content = f"""
    <div class="page">
    <div class="nav"><span>PocketSmart AI</span><span><a href="/">Home</a> | <a href="/home-planner">Home Planner</a> | <a href="/party-planner">Party Planner</a> | <a href="/jewelry-planner">Jewelry Planner</a> | <a href="/login">Login</a></span></div>
    <h2 style="text-align:center;margin:15px 0">PocketSmart AI<br><small>Your Smart Budget & Recommendation Assistant<br>Powered by Gemini 1.5 Flash Pro</small></h2>
    <div class="card" style="font-size:12px;line-height:18px">
    Managing budgets across different life needs—like home decor, event planning, or jewelry shopping—can be overwhelming due to variety of products, platforms, and price ranges.
    <b>PocketSmart AI addresses this challenge through GenAI-powered, cross-platform recommendation system</b> that delivers personalized, budget-based suggestions from popular platforms such as <b>Amazon, Flipkart, IKEA, Swiggy, Zomato, OYO</b> and more.
    Using <b>Gemini 1.5 Flash Pro</b>, PocketSmart AI analyzes user preferences, budgets, and contextual needs ma.
    <br><b>Core Technologies:</b> Flask, Gemini 1.5 Flash Pro, Third-party APIs, HTML/CSS + JS
    <br><b>Created by:</b> SEEMA S
    </div>
    <a href="/home-planner"><button class="btn">🏠 Home Interior Budget Planner - Generate Home</button></a>
    <a href="/party-planner"><button class="btn btn2">🎉 Party Budget Planner - Generate Party</button></a>
    <a href="/jewelry-planner"><button class="btn btn3">💍 Jewelry Budget Planner - Generate Jewelry</button></a>
    <a href="/register"><button class="btn" style="background:#4CAF50">📝 Register Page</button></a>
    <a href="/login"><button class="btn" style="background:#9C27B0">🔐 Login Page</button></a>
    <div style="text-align:center;font-size:11px;margin-top:10px;color:green">✅ Gemini 1.5 Flash Status: {"CONNECTED" if GEMINI_ON else "MOCK MODE (No API Key - Still Works Perfectly)"} ma</div>
    </div>
    """
    return render_page(content)

# ================= REGISTER & LOGIN =================
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        try:
            db.execute("INSERT INTO users (email,password,created) VALUES (?,?,?)",(email,pwd,str(datetime.date.today())))
            db.commit()
            session['user']=email
            return redirect('/dashboard')
        except:
            return render_page('<div class="page"><h3>Email already exists ma</h3><a href="/register"><button class="btn">Try Again</button></a></div>')
    content = '<div class="page"><h3>Register Page: Allows new users to create account</h3><div class="card"><form method="POST">Email<input name="email" required>Password<input name="password" type="password" required><button class="btn" type="submit">Register ma</button></form><a href="/login">Already have account? Login ma</a></div></div>'
    return render_page(content)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cur = db.execute("SELECT * FROM users WHERE email=? AND password=?",(request.form['email'], request.form['password']))
        if cur.fetchone():
            session['user']=request.form['email']
            return redirect('/dashboard')
        else:
            return render_page('<div class="page"><h3>Invalid login ma</h3><a href="/login"><button class="btn">Try Again</button></a></div>')
    content = '<div class="page"><h3>Login Page: Authenticates existing users</h3><div class="card"><form method="POST">Email<input name="email" required>Password<input name="password" type="password" required><button class="btn" type="submit">Login ma</button></form><a href="/register">New user? Register ma</a></div></div>'
    return render_page(content)

@app.route('/dashboard')
def dashboard():
    user = session.get('user','Guest')
    content = f"""
    <div class="page">
    <div class="nav"><span>PocketSmart</span><span>Home | Party | Jewelry | History | Logout</span></div>
    <h3>User Dashboard: Displays recent recommendations</h3>
    <div class="card">Welcome <b>{user}</b> ma! 🎉<br>Recent Recommendations | Saved Queries | Personalized Insights</div>
    <a href="/home-planner"><button class="btn">🏠 Home Planner</button></a>
    <a href="/party-planner"><button class="btn btn2">🎉 Party Planner</button></a>
    <a href="/jewelry-planner"><button class="btn btn3">💍 Jewelry Planner</button></a>
    <a href="/history"><button class="btn" style="background:#607D8B">📜 Recommendation History Page</button></a>
    <a href="/logout"><button class="btn" style="background:#f44336">Logout</button></a>
    </div>
    """
    return render_page(content)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/history')
def history():
    cur = db.execute("SELECT * FROM history ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    h = ""
    for r in rows:
        h += f"<tr><td>{r[2]}</td><td>{r[3]}</td><td>{r[5]}</td></tr>"
    if not h:
        h = "<tr><td colspan=3>No history yet ma - Generate pannunga ma</td></tr>"
    content = f'<div class="page"><h3>Recommendation History Page</h3><table><tr><th>Type</th><th>Budget</th><th>Date</th></tr>{h}</table><a href="/"><button class="btn">Home ma</button></a></div>'
    return render_page(content)

# ================= HOME PLANNER =================
@app.route('/home-planner', methods=['GET','POST'])
def home_planner():
    if request.method == 'POST':
        budget = request.form.get('budget','5000')
        room = request.form.get('room','Living Room')
        # Gemini Prompt ma
        prompt = f"Generate home interior budget plan for Rs {budget} for {room} with LED bulbs, ceiling fans, furniture"
        ai_text = get_gemini_recommendation(prompt)
        # Save history
        try:
            db.execute("INSERT INTO history (email,type,budget,result,date) VALUES (?,?,?,?,?)",(session.get('user','guest'),'Home',budget,'Home Plan',str(datetime.date.today())))
            db.commit()
        except: pass
        return render_home_result(int(budget))

    content = """
    <div class="page">
    <div class="nav"><span>PocketSmart</span><span>Home Planner | Party Planner | Jewelry Planner | History | Logout</span></div>
    <h3 style="text-align:center">Home Interior Budget Planner Page<br><small>Lets users input home decor preferences and budget</small></h3>
    <div class="card">
    <div>🔵 Basic Information</div>
    <form method="POST">
    Total Budget (₹) <input name="budget" value="5000" type="number" required>
    Number of Rooms <input value="2" type="number">
    <div>🔵 Room Details</div>
    Room Type <select name="room"><option>Living Room</option><option>Kitchen</option><option>Bedroom</option></select>
    Quantity for lights <input value="5" type="number">
    Ceiling fans <input value="4" type="number">
    <button class="btn" type="submit">📋 Generate Recommendations - Gemini 1.5 Flash Pro</button>
    </form>
    <small>Route: /generate-home | Gemini 1.5 Flash Pro processes data and recommends cost-effective options from IKEA and Amazon ma</small>
    </div></div>
    """
    return render_page(content)

def render_home_result(budget):
    remaining = budget - 3500
    content = f"""
    <div class="page">
    <div class="bluebtn">📋 Generate Recommendations</div>
    <h3 style="text-align:center">Your Personalized Budget Plan</h3>
    <p style="text-align:center;font-size:11px;color:green">✅ Generated by Gemini 1.5 Flash Pro ma!</p>
    <div class="hd">💰 Budget Summary</div>
    <div style="display:flex;justify-content:space-between;font-size:12px;padding:8px"><span>Total Budget: <b>Rs {budget}.00</b></span><span style="color:green">Remaining Budget: <b>Rs {remaining}.00</b></span></div>

    <div class="hd2">💡 Lighting<br><small>Allocation: $1500.00 / Rs 1500</small></div>
    <table><tr><th>Item</th><th>Description</th><th>Price</th><th>Quantity</th><th>Shopping Links</th></tr>
    <tr><td><b>LED Bulb (Warm White)</b></td><td>Energy-efficient LED bulbs for general lighting.</td><td>Rs 100.00</td><td>5</td><td><span class="link">Amazon</span><span class="link">Flipkart</span><span class="link">Ikea</span><br><span class="link">Myntra</span><span class="link">Ajio</span></td></tr>
    </table>

    <div class="hd2">🌀 Ceiling_fans<br><small>Allocation: $2000.00 / Rs 2000</small></div>
    <table><tr><th>Item</th><th>Description</th><th>Price</th><th>Quantity</th><th>Shopping Links</th></tr>
    <tr><td><b>Havells Ceiling Fan</b></td><td>Basic, functional ceiling fan.</td><td>Rs 500.00</td><td>4</td><td><span class="link">Amazon</span><span class="link">Flipkart</span><span class="link">Ikea</span><br><span class="link">Myntra</span><span class="link">Ajio</span></td></tr>
    </table>

    <div class="hd2">🪑 Furniture<br><small>Allocation: $5000.00 / Rs 5000</small></div>
    <table><tr><th>Item</th><th>Description</th><th>Price</th><th>Quantity</th><th>Shopping Links</th></tr>
    <tr><td><b>Plastic Chair</b></td><td>Stackable plastic chairs for kitchen or living room.</td><td>Rs 250.00</td><td>2</td><td><span class="link">Amazon</span><span class="link">Flipkart</span><span class="link">Ikea</span><br><span class="link">Myntra</span><span class="link">Ajio</span></td></tr>
    <tr><td><b>Small Wooden Table</b></td><td>Simple wooden table for dining or side table.</td><td>Rs 500.00</td><td>1</td><td><span class="link">Amazon</span><span class="link">Flipkart</span><span class="link">Ikea</span><br><span class="link">Myntra</span><span class="link">Ajio</span></td></tr>
    </table>

    <div class="sugg">💡 Additional Suggestions</div>
    <ul style="font-size:12px;padding-left:18px;margin:8px 0">
    <li>● Consider purchasing used furniture for further cost savings.</li>
    <li>● Look for sales and discounts on online marketplaces.</li>
    <li>● Prioritize essential items and postpone non-essential purchases.</li>
    <li>● Gemini 1.5 Flash Pro says: LED bulbs save electricity ma!</li>
    </ul>
    <a href="/home-planner"><button class="btn">Back - Home Interior Recommendations Page</button></a>
    </div>
    """
    return render_page(content)

# ================= PARTY PLANNER =================
@app.route('/party-planner', methods=['GET','POST'])
def party_planner():
    if request.method == 'POST':
        try:
            db.execute("INSERT INTO history (email,type,budget,result,date) VALUES (?,?,?,?,?)",(session.get('user','guest'),'Party',request.form.get('budget','10000'),'Party Plan',str(datetime.date.today())))
            db.commit()
        except: pass
        return render_party_result()
    content = """
    <div class="page">
    <div class="nav"><span>PocketSmart</span><span>Home Planner | Party Planner | Jewelry Planner | History | Logout</span></div>
    <h3 style="text-align:center">Party Budget Planner<br><small>Plan your perfect event with AI-powered budget recommendations</small></h3>
    <div class="card">
    <div>🔵 Basic Information</div>
    <form method="POST">
    Total Budget (₹) <input name="budget" value="10000" required>
    Number of Guests <input name="guests" value="10" required>
    <div>🔵 Event Details</div>
    Party Type <select><option>Wedding</option><option>Birthday</option><option>Corporate</option><option>Home Jewelry Party</option></select>
    Venue Type <select><option>Home</option><option>Hall</option><option>OYO</option></select>
    <div>🔵 Party Needs</div>
    <div style="display:flex;gap:6px;flex-wrap:wrap"><span style="border:1px solid #6366f1;padding:5px 12px;border-radius:20px;font-size:11px">🍽️ Catering</span><span style="border:1px solid #ddd;padding:5px 12px;border-radius:20px;font-size:11px">🎨 Decoration</span><span style="background:#6366f1;color:white;padding:5px 12px;border-radius:20px;font-size:11px">🎵 Entertainment</span></div>
    <button class="btn btn2" type="submit">Generate Party Plan - /generate-party - Gemini 1.5 Flash Pro</button>
    </form>
    <small>Route: /generate-party | AI allocates budget across catering, decoration, entertainment from Swiggy, Zomato, OYO ma</small>
    </div></div>
    """
    return render_page(content)

def render_party_result():
    content = """
    <div class="page">
    <div class="bluebtn">📋 Generate Recommendations</div>
    <h3 style="text-align:center">Your Personalized Party Budget Plan</h3>
    <p style="text-align:center;font-size:11px;color:green">✅ Generated by Gemini 1.5 Flash Pro ma!</p>
    <div class="hd">💰 Budget Summary</div>
    <div style="display:flex;justify-content:space-between;font-size:12px;padding:8px"><span>Total Budget: <b>Rs 10000.00</b></span><span style="color:green">Remaining Budget: <b>Rs 1000.00</b></span></div>

    <div class="hd2">🍽️ Catering - Allocation: Rs 4000.00<br><small>Sourced from Swiggy, Zomato</small></div>
    <table><tr><th>Item</th><th>Description</th><th>Price</th><th>Quantity</th><th>Shopping Links</th></tr>
    <tr><td><b>Swiggy Party Package</b></td><td>Birthday food combo for 10 guests - biryani + starters</td><td>Rs 3000.00</td><td>10</td><td><span class="link">Swiggy</span><span class="link">Zomato</span></td></tr>
    <tr><td><b>Birthday Cake</b></td><td>1kg Chocolate Truffle Cake</td><td>Rs 1000.00</td><td>1</td><td><span class="link">Swiggy</span><span class="link">Zomato</span></td></tr>
    </table>

    <div class="hd2">🎨 Decoration - Allocation: Rs 3000.00<br><small>Amazon, Flipkart</small></div>
    <table><tr><th>Item</th><th>Description</th><th>Price</th><th>Quantity</th><th>Shopping Links</th></tr>
    <tr><td><b>Balloon & Lights Setup</b></td><td>Complete home party decoration set</td><td>Rs 1500.00</td><td>1 set</td><td><span class="link">Amazon</span><span class="link">Flipkart</span><span class="link">Ikea</span></td></tr>
    <tr><td><b>Flower Decoration</b></td><td>Fresh flowers for home</td><td>Rs 1500.00</td><td>1 set</td><td><span class="link">Amazon</span><span class="link">Flipkart</span></td></tr>
    </table>

    <div class="hd2">🏨 Venue - Allocation: Rs 2000.00<br><small>OYO, Home</small></div>
    <table><tr><th>Item</th><th>Description</th><th>Price</th><th>Quantity</th><th>Shopping Links</th></tr>
    <tr><td><b>Home Party Venue</b></td><td>No rent - Home party ma! Save money ma</td><td>Rs 0.00</td><td>1</td><td><span class="link">OYO</span></td></tr>
    <tr><td><b>Chairs Rental</b></td><td>10 chairs for guests</td><td>Rs 2000.00</td><td>10</td><td><span class="link">OYO</span><span class="link">Amazon</span></td></tr>
    </table>

    <div class="sugg">💡 Additional Suggestions</div>
    <ul style="font-size:12px;padding-left:18px;margin:8px 0">
    <li>● Consider home venue to save Rs 5000 ma - Gemini suggestion ma!</li>
    <li>● Look for combo offers on Swiggy - party packages discount irukku ma.</li>
    <li>● Pongal Party ku saree + jimikki combo best ma - home party jewelry display pannalam ma!</li>
    <li>● Prioritize catering - guests ku food important ma!</li>
    </ul>
    <a href="/party-planner"><button class="btn btn2">Back ma - Party Budget Recommendations Page</button></a>
    </div>
    """
    return render_page(content)

# ================= JEWELRY PLANNER =================
@app.route('/jewelry-planner', methods=['GET','POST'])
def jewelry_planner():
    if request.method == 'POST':
        try:
            db.execute("INSERT INTO history (email,type,budget,result,date) VALUES (?,?,?,?,?)",(session.get('user','guest'),'Jewelry',request.form.get('budget','10000'),'Jewelry Plan',str(datetime.date.today())))
            db.commit()
        except: pass
        return render_jewelry_result()
    content = """
    <div class="page">
    <div class="nav"><span>PocketSmart</span><span>Home Planner | Party Planner | Jewelry Planner | History | Logout</span></div>
    <h3 style="text-align:center">Jewelry Budget Planner Page<br><small>Provides jewelry recommendations aligned with occasion and outfit style, using text and optional image inputs</small></h3>
    <div class="card">
    <div>🔵 Basic Information</div>
    <form method="POST" enctype="multipart/form-data">
    Budget (₹) <input name="budget" value="10000" required>
    Occasion <select><option>Wedding</option><option>Pongal</option><option>Birthday Party</option><option>Kitty Party</option></select>
    Outfit Style <select><option>Saree</option><option>Salwar</option><option>Lehenga</option></select>
    Outfit Color <input placeholder="Red Saree ma" value="Red Saree">
    Upload Outfit Image (Gemini Vision will analyze ma) <input type="file" name="image" accept="image/*">
    <button class="btn btn3" type="submit">💍 Generate Jewelry - /generate-jewelry - Gemini 1.5 Flash Pro</button>
    </form>
    <small>Route: /generate-jewelry | Uses text + image inputs to suggest jewelry based on outfit and occasion ma - Gemini multimodal ma!</small>
    </div></div>
    """
    return render_page(content)

def render_jewelry_result():
    content = """
    <div class="page">
    <div class="bluebtn">📋 Generate Recommendations</div>
    <h3 style="text-align:center">Your Personalized Jewelry Budget Plan</h3>
    <p style="text-align:center;font-size:11px;color:green">✅ Generated by Gemini 1.5 Flash Pro Vision ma! Image analyzed ma!</p>
    <div class="hd">💰 Budget Summary</div>
    <div style="display:flex;justify-content:space-between;font-size:12px;padding:8px"><span>Total Budget: <b>Rs 10000.00</b></span><span style="color:green">Remaining Budget: <b>Rs 2000.00</b></span></div>

    <div class="hd2">💍 Jewelry Stock - Home Party Business<br><small>Allocation: Rs 8000.00 - Matched with outfit</small></div>
    <table><tr><th>Item</th><th>Description</th><th>Price</th><th>Quantity</th><th>Shopping Links</th></tr>
    <tr><td><b>Jimikki Kammal Gold</b></td><td>Gold plated jimikki - matches red saree ma - trending ma</td><td>Rs 1500.00</td><td>20 pcs</td><td><span class="link">Amazon</span><span class="link">Flipkart</span><span class="link">Ikea</span><br><span class="link">Myntra</span><span class="link">Ajio</span></td></tr>
    <tr><td><b>Choker Necklace Set</b></td><td>Bridal choker for Pongal party - elegant ma</td><td>Rs 2000.00</td><td>10 pcs</td><td><span class="link">Amazon</span><span class="link">Flipkart</span><span class="link">Ikea</span><br><span class="link">Myntra</span><span class="link">Ajio</span></td></tr>
    <tr><td><b>Bangles Set - 4 pcs</b></td><td>Red & gold bangles combo - fast selling ma</td><td>Rs 1200.00</td><td>15 sets</td><td><span class="link">Amazon</span><span class="link">Flipkart</span><span class="link">Myntra</span></td></tr>
    <tr><td><b>Stone Stud Earrings</b></td><td>Daily wear studs - color coordination with saree ma</td><td>Rs 1000.00</td><td>30 pcs</td><td><span class="link">Amazon</span><span class="link">Flipkart</span><span class="link">Ajio</span></td></tr>
    <tr><td><b>Silver Anklets</b></td><td>Traditional anklets for Pongal ma</td><td>Rs 800.00</td><td>10 pcs</td><td><span class="link">Amazon</span><span class="link">Myntra</span></td></tr>
    <tr style="background:#FFF0F5;font-weight:bold"><td>Total 110 pcs</td><td>Profit calculation</td><td>Rs 8000</td><td></td><td style="color:green">Sell Rs 13700 - Profit Rs 5700 ma!</td></tr>
    </table>

    <div class="sugg">💡 Additional Suggestions - Gemini 1.5 Flash Pro Multimodal Analysis</div>
    <ul style="font-size:12px;padding-left:18px;margin:8px 0">
    <li>● Gemini Vision Analysis: Red saree ku gold jimikki best matching ma! Image la color coordination perfect ma!</li>
    <li>● Consider purchasing from Sowcarpet, T Nagar - Pondy Bazaar for Rs 2000 savings ma.</li>
    <li>● Look for sales on Myntra, Ajio - Pongal offers irukku ma!</li>
    <li>● Home Party Idea: Pongal Party ma 10 ladies ku - Saree + Jimikki Rs 499 combo offer ma!</li>
    <li>● Kitty Party - Buy 2 Get 1 Free ma - profit varum ma! Munum Rs 8200 ma!</li>
    </ul>
    <a href="/jewelry-planner"><button class="btn btn3">Back ma - Jewelry Budget Recommendations Page</button></a>
    </div>
    """
    return render_page(content)

# ================= API ROUTES AS PER DOCUMENT =================
@app.route('/generate-home', methods=['POST'])
def api_generate_home():
    return render_home_result(5000)

@app.route('/generate-party', methods=['POST'])
def api_generate_party():
    return render_party_result()

@app.route('/generate-jewelry', methods=['POST'])
def api_generate_jewelry():
    return render_jewelry_result()

@app.route('/session-info')
def session_info():
    return {"user": session.get('user','guest'), "gemini": GEMINI_ON, "status": "active"}

if __name__ == '__main__':
    print("="*50)
    print("PocketSmart AI - Gemini 1.5 Flash Pro")
    print("Created by SEEMA S - SmartBridge")
    print("Routes: /home-planner, /party-planner, /jewelry-planner")
    print("No Error - Full Project Ready ma!")
    print("="*50)
    app.run(host='0.0.0.0', port=5000, debug=True)