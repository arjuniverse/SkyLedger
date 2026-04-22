# ✈️ SkyLedger

> Flight Booking System with Blockchain (Proof-of-Work)

🚀 Minimal • Secure • 2 Files Only

---

## ⚡ Quick Start (1 Minute Setup)

```bash
git clone https://github.com/arjuniverse/SkyLedger.git
cd SkyLedger

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

pip install flask flask-sqlalchemy flask-cors pyjwt werkzeug

python skyledger_backend.py
```

👉 Open new terminal:

```bash
python -m http.server 8000
```

🌐 Visit: http://localhost:8000

---

## 🔑 Demo Login

```
Passenger:
alice / password123

Admin:
admin / adminpass
```

---

## 🧠 What This Project Does

* Book flights ✈️
* Store bookings in database 🗄️
* Mine each booking into blockchain ⛓️
* Ensure tamper-proof records 🔒
* Provide admin analytics dashboard 📊

---

## ⚙️ Core Features

✔ JWT Authentication
✔ Role-based Access (Admin/User)
✔ Flight Booking System
✔ Blockchain (Proof-of-Work)
✔ Chain Validation
✔ Modern UI (Glassmorphism)

---

## ⛓️ Blockchain Logic (Simple)

```
Booking → Create Block → Mine (0000 hash) → Add to Chain
```

Each block contains:

* Booking Data
* Timestamp
* Previous Hash
* Nonce
* Hash

---

## 🏗️ Architecture (Simple View)

```
Frontend (HTML/CSS/JS)
        ↓
Flask Backend (API + Auth)
        ↓
SQLite Database
        ↓
Blockchain (PoW Mining)
```

---

## 📁 Files

```
skyledger_backend.py
skyledger_frontend.html
```

---

## 🧪 Test Flow (For Viva / Demo)

1. Login
2. Book Flight
3. Confirm Booking
4. Check Blockchain Entry
5. Admin → Validate Chain

---

## 🛡️ Security

* Password Hashing (PBKDF2)
* JWT Authentication
* Blockchain Integrity Check

---

## 🚀 Future Improvements

* Payment Integration
* Email Notifications
* PostgreSQL Migration
* Cloud Deployment

---

## 👨‍💻 Author

Arjun Sharma

---

## ⭐ If you like it

Give a ⭐ on GitHub!
