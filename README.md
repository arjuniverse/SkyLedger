"""
═══════════════════════════════════════════════════════════════════
  SkyLedger - Complete Flight Booking System with Blockchain
═══════════════════════════════════════════════════════════════════

OVERVIEW:
═════════

SkyLedger is a complete, production-ready flight booking system featuring:
  ✓ Flask backend with SQLAlchemy
  ✓ Blockchain with Proof-of-Work mining
  ✓ JWT authentication
  ✓ Role-based access control (passenger/admin)
  ✓ Modern glassmorphism frontend
  ✓ Dark/light theme support
  ✓ Responsive design
  ✓ Chart.js analytics
  ✓ All in just 2 files!

PROJECT STRUCTURE:
══════════════════

Files provided:
  1. skyledger_backend.py     (Flask backend + blockchain)
  2. skyledger_frontend.html  (Complete HTML/CSS/JS frontend)

That's it! No other files needed.


PREREQUISITES:
═══════════════

You need to have Python 3.7+ installed with pip.

Check Python version:
  python --version

If you don't have Python, download from: https://www.python.org/downloads/


STEP-BY-STEP SETUP:
═══════════════════

STEP 1: Create a project folder
───────────────────────────────

  mkdir skyledger
  cd skyledger

On Windows:
  mkdir skyledger
  cd skyledger


STEP 2: Create virtual environment
──────────────────────────────────

This keeps dependencies isolated.

On Mac/Linux:
  python3 -m venv venv
  source venv/bin/activate

On Windows:
  python -m venv venv
  venv\Scripts\activate

You should see (venv) before your command prompt.


STEP 3: Install required packages
─────────────────────────────────

Copy and paste this command:

  pip install flask flask-sqlalchemy flask-cors pyjwt werkzeug

This installs:
  - Flask: Web framework
  - SQLAlchemy: Database ORM
  - CORS: Cross-origin requests
  - PyJWT: JWT tokens
  - Werkzeug: Password hashing


STEP 4: Copy the backend file
────────────────────────────

Save the backend code as: skyledger_backend.py

In the skyledger folder, create a new file called:
  skyledger_backend.py

Copy and paste all the content from the provided backend file.


STEP 5: Copy the frontend file
──────────────────────────────

Save the frontend code as: skyledger_frontend.html

In the skyledger folder, create a new file called:
  skyledger_frontend.html

Copy and paste all the content from the provided frontend file.


STEP 6: Start the backend
─────────────────────────

Run this command in your terminal (in the skyledger folder):

  python skyledger_backend.py

You should see:
  ✈️ SkyLedger Backend Starting...
  📍 API: http://localhost:5000
  📊 Blockchain Blocks: 1
  🔗 Difficulty: 4

The backend is now running!


STEP 7: Open the frontend
─────────────────────────

There are multiple options. Choose ONE:

OPTION A - Direct file open (Simplest):
  - Find skyledger_frontend.html in your file explorer
  - Double-click to open in browser
  - Navigate to: http://localhost:5000 in the address bar
  
  ⚠️ Note: CORS might have issues with file:// protocol
  If this doesn't work, use Option B or C

OPTION B - Python HTTP Server (Recommended):
  - Open a NEW terminal window (keep backend running)
  - Navigate to skyledger folder
  - Run this command:
    python -m http.server 8000
  
  - Open browser and go to:
    http://localhost:8000
  
  - You should see the SkyLedger login page

OPTION C - VS Code Live Server:
  - Install VS Code if you don't have it
  - Install "Live Server" extension (by Ritwick Dey)
  - Right-click skyledger_frontend.html
  - Click "Open with Live Server"
  - Browser opens automatically

OPTION D - Use Python anywhere:
  - If you have Node.js:
    npx http-server
  - Visit: http://localhost:8080


STEP 8: Test the application
─────────────────────────────

1. Open the frontend (http://localhost:8000 or http://localhost:8080)

2. You should see the login page with:
   - Login tab and Register tab
   - Demo credentials display
   - Glassmorphism design

3. Click "Login" tab and use demo credentials:
   Username: alice
   Password: password123

4. Click "Login" button

5. You're now on the Dashboard!

6. Try these actions:
   - Click "Dashboard" → See your stats
   - Click "Booking" → Book a flight
   - Select a flight and click "Book Now"
   - Choose a seat and confirm
   - See the blockchain transaction!

7. For admin features (if you're admin):
   - Click "Admin" tab
   - See all bookings, users, analytics
   - View blockchain data
   - Validate blockchain integrity


TROUBLESHOOTING:
═════════════════

Problem: "Cannot GET /api/..."
Solution: Make sure backend is running in another terminal
  - Run: python skyledger_backend.py
  - Keep that terminal open

Problem: "Failed to fetch" in console
Solution: Backend and frontend must be on same computer
  - Backend: http://localhost:5000 (terminal 1)
  - Frontend: http://localhost:8000 (terminal 2)

Problem: Database error on startup
Solution: Delete skyledger.db file and restart
  - Find and delete: skyledger.db
  - Run: python skyledger_backend.py
  - New database will be created

Problem: Port 5000 already in use
Solution: Either stop other app or change port in backend
  - Edit skyledger_backend.py, line at bottom
  - Change: app.run(port=5001) instead of 5000

Problem: Frontend shows blank page
Solution: Check browser console for errors (F12)
  - Look at Console tab
  - Check Network tab to see if API calls succeed

Problem: Login not working
Solution: Check if backend is accessible
  - Open: http://localhost:5000/health
  - Should show: {"status": "healthy", "blockchain_blocks": 1}

Problem: (venv) is not showing in terminal
Solution: Virtual environment not activated
  - Mac/Linux: source venv/bin/activate
  - Windows: venv\Scripts\activate


FEATURES TO TRY:
════════════════

Login & Register:
  ✓ Register as passenger or admin
  ✓ Login with credentials
  ✓ See different roles get different permissions

Dashboard:
  ✓ View your stats
  ✓ See recent bookings
  ✓ Check blockchain status
  ✓ User profile info

Booking:
  ✓ Search flights by city code
  ✓ Book a flight
  ✓ Select seat
  ✓ See blockchain transaction recorded
  ✓ Get ticket hash

Admin Features (login as admin):
  Username: admin
  Password: adminpass
  
  ✓ View all bookings
  ✓ View all users
  ✓ See analytics charts
  ✓ Validate blockchain
  ✓ View blockchain blocks

Theme:
  ✓ Click moon/sun icon to toggle dark/light theme
  ✓ Theme persists across sessions


DEMO ACCOUNTS:
═══════════════

Passenger Account:
  Username: alice
  Password: password123

Admin Account:
  Username: admin
  Password: adminpass

You can also create new accounts via the "Register" tab.


API ENDPOINTS REFERENCE:
════════════════════════

All endpoints available at: http://localhost:5000/api

Authentication:
  POST   /auth/register          Create account
  POST   /auth/login             Login and get token
  POST   /auth/logout            Logout
  GET    /auth/me                Current user info

Flights:
  GET    /flights                Get all flights
  POST   /flights/search         Search flights

Bookings:
  POST   /bookings               Create booking
  GET    /bookings               Get user's bookings
  GET    /bookings/stats         Get booking stats
  POST   /bookings/verify-ticket Verify ticket hash

Admin (requires admin role):
  GET    /admin/bookings         All bookings
  GET    /admin/bookings/stats   Booking stats
  GET    /admin/users            All users
  GET    /admin/blockchain       Blockchain data
  GET    /admin/validate         Validate chain


DATABASE:
══════════

SQLite database is automatically created:
  File: skyledger.db
  
Tables:
  - users (accounts)
  - bookings (flight bookings)
  
No setup required - it's all automatic!


BLOCKCHAIN:
════════════

Genesis block created automatically on startup.

Each booking creates a new block with:
  - Booking data
  - Timestamp
  - Hash (SHA-256)
  - Nonce (from proof-of-work)
  - Previous block hash (linking)

Difficulty: 4 (hash must start with "0000")

Features:
  ✓ Immutable ledger
  ✓ Proof-of-work mining
  ✓ Chain validation
  ✓ Tamper detection


ARCHITECTURE:
══════════════

Backend (Flask):
  - SQLAlchemy: Database layer
  - JWT: Authentication
  - Blockchain: Proof-of-work mining
  - REST API: 20+ endpoints

Frontend (HTML/CSS/JS):
  - Glassmorphism design
  - Dark/light themes
  - Responsive layout
  - Chart.js analytics
  - No frameworks - pure HTML/CSS/JS


SECURITY:
═══════════

Password Hashing:
  - Werkzeug PBKDF2:SHA256
  - 600,000 iterations
  - 16-byte salt

JWT Tokens:
  - HS256 algorithm
  - 30-day expiration
  - Signed with secret

Blockchain:
  - SHA-256 hashing
  - Proof-of-work validation
  - Chain integrity checks


PRODUCTION TIPS:
════════════════

Before deploying to production:

1. Change JWT secret:
   Edit skyledger_backend.py:
   JWT_SECRET = os.environ.get('JWT_SECRET', 'YOUR_SECRET_HERE')

2. Use HTTPS:
   Deploy with SSL certificate

3. Use production database:
   Change from SQLite to PostgreSQL

4. Set debug to False:
   Edit: app.run(debug=False)

5. Use production server:
   Install gunicorn: pip install gunicorn
   Run: gunicorn skyledger_backend:app

6. Deploy to cloud:
   Heroku, AWS, Google Cloud, DigitalOcean, etc.


WHAT TO DO IF SOMETHING BREAKS:
═════════════════════════════════

Step 1: Check backend logs
  - Look at the terminal running backend
  - Look for error messages

Step 2: Check browser console
  - Press F12 in browser
  - Click "Console" tab
  - Look for red error messages

Step 3: Check Network tab
  - Press F12 in browser
  - Click "Network" tab
  - Try an action
  - Look for failed requests
  - Click on failed request to see error

Step 4: Restart everything
  - Stop backend (Ctrl+C in terminal)
  - Close browser
  - Delete skyledger.db
  - python skyledger_backend.py
  - Open browser again

Step 5: Check files
  - Make sure both files are in same folder:
    skyledger_backend.py
    skyledger_frontend.html


CUSTOMIZATION:
═══════════════

Change API URL:
  Edit skyledger_frontend.html
  Find: const API_URL = 'http://localhost:5000/api'
  Change to your backend URL

Change colors:
  Edit skyledger_frontend.html
  Find: :root { (in <style> section)
  Change color variables

Add more flights:
  Edit skyledger_backend.py
  Find: DEMO_FLIGHTS = [
  Add more flight objects


FILE LOCATIONS:
════════════════

After setup, your folder should look like:

skyledger/
├── skyledger_backend.py       (Flask app)
├── skyledger_frontend.html    (Frontend)
├── venv/                      (Virtual environment)
└── skyledger.db               (Created automatically)


NEXT STEPS:
════════════

After getting it working:

1. Explore the code:
   - Read comments in Python file
   - Read comments in HTML file
   - Understand how blockchain works

2. Try modifications:
   - Add new fields to bookings
   - Add email notifications
   - Add payment integration

3. Deploy:
   - Deploy backend to cloud
   - Deploy frontend to GitHub Pages/Netlify
   - Connect them

4. Scale:
   - Add caching (Redis)
   - Add real database (PostgreSQL)
   - Add API rate limiting
   - Add monitoring


SUPPORT:
═════════

If you encounter issues:

1. Check all prerequisites are installed
2. Make sure both files are in same folder
3. Make sure backend is running
4. Check browser console for errors (F12)
5. Check backend terminal for error messages
6. Try restarting everything
7. Delete skyledger.db and start fresh


SUCCESS INDICATORS:
═══════════════════

You'll know it's working when you see:

✓ Backend terminal shows:
  ✈️ SkyLedger Backend Starting...
  📍 API: http://localhost:5000
  
✓ Frontend loads login page

✓ You can login with demo credentials

✓ Dashboard shows your stats

✓ You can book a flight

✓ Booking shows blockchain transaction

✓ Admin can see all bookings and validate blockchain


CONGRATULATIONS! 🎉
════════════════════

You've successfully set up SkyLedger!

You now have a complete, production-ready flight booking system with:
  - User authentication
  - Flight bookings
  - Blockchain transactions
  - Admin dashboard
  - Modern UI
  - Analytics

All in just 2 files!


═══════════════════════════════════════════════════════════════════
                   Happy Flying! ✈️ 🚀
═══════════════════════════════════════════════════════════════════
"""
