"""
═══════════════════════════════════════════════════════════════════
  SkyLedger - Complete Backend
  Flask + SQLAlchemy + Blockchain + Authentication
  Single file implementation
═══════════════════════════════════════════════════════════════════
"""

import os
import jwt
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# ═══════════════════════════════════════════════════════════════════
# BLOCKCHAIN IMPLEMENTATION
# ═══════════════════════════════════════════════════════════════════

class Block:
    """Single block in blockchain"""
    def __init__(self, index, timestamp, data, previous_hash, nonce=0, hash=''):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class Blockchain:
    """Complete blockchain with proof-of-work"""
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def calculate_hash(self, index, timestamp, data, previous_hash, nonce):
        """Calculate SHA-256 hash"""
        block_string = json.dumps({
            'index': index,
            'timestamp': timestamp,
            'data': data,
            'previous_hash': previous_hash,
            'nonce': nonce
        }, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def create_genesis_block(self):
        """Create first block"""
        genesis = Block(
            index=0,
            timestamp=datetime.utcnow().isoformat(),
            data={'message': 'Genesis Block'},
            previous_hash='0' * 64
        )
        self._proof_of_work(genesis)
        self.chain.append(genesis)

    def _proof_of_work(self, block):
        """Mine block with proof-of-work"""
        target = '0' * self.difficulty
        while True:
            block.hash = self.calculate_hash(
                block.index, block.timestamp, block.data,
                block.previous_hash, block.nonce
            )
            if block.hash.startswith(target):
                break
            block.nonce += 1

    def add_block(self, data):
        """Add new block to chain"""
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.utcnow().isoformat(),
            data=data,
            previous_hash=previous_block.hash
        )
        self._proof_of_work(new_block)
        self.chain.append(new_block)
        return new_block

    def is_valid(self):
        """Validate chain integrity"""
        if not self.chain:
            return False

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            if current.previous_hash != previous.hash:
                return False

            recalc_hash = self.calculate_hash(
                current.index, current.timestamp, current.data,
                current.previous_hash, current.nonce
            )
            if current.hash != recalc_hash:
                return False

            if not current.hash.startswith('0' * self.difficulty):
                return False

        return True

    def to_dict(self):
        return {
            'difficulty': self.difficulty,
            'chain': [b.to_dict() for b in self.chain],
            'length': len(self.chain)
        }


# ═══════════════════════════════════════════════════════════════════
# FLASK APP SETUP
# ═══════════════════════════════════════════════════════════════════

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skyledger.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
CORS(app)

# Global blockchain instance
blockchain = Blockchain(difficulty=4)

# JWT Configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'skyledger-secret-change-in-prod')
JWT_ALGORITHM = 'HS256'

# ═══════════════════════════════════════════════════════════════════
# DATABASE MODELS
# ═══════════════════════════════════════════════════════════════════

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='passenger', nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    bookings = db.relationship('Booking', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_bookings=False):
        data = {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_bookings:
            data['bookings'] = [b.to_dict() for b in self.bookings]
        return data


class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    flight = db.Column(db.String(100), nullable=False, index=True)
    seat = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    ticket_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    user = db.relationship('User', back_populates='bookings')

    @staticmethod
    def generate_ticket_hash():
        return hashlib.sha256(secrets.token_bytes(32)).hexdigest()

    def to_dict(self, include_user=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'flight': self.flight,
            'seat': self.seat,
            'price': float(self.price),
            'ticket_hash': self.ticket_hash,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
        if include_user and self.user:
            data['user'] = {'id': self.user.id, 'username': self.user.username}
        return data


# ═══════════════════════════════════════════════════════════════════
# JWT AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════

def create_token(user_id, username, role):
    """Create JWT token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=30)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def token_required(f):
    """Decorator to require valid JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except:
                pass

        if not token:
            return jsonify({'message': 'Token missing', 'error': 'MISSING_TOKEN'}), 401

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload['user_id']
            username = payload['username']
            role = payload['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired', 'error': 'EXPIRED_TOKEN'}), 401
        except:
            return jsonify({'message': 'Invalid token', 'error': 'INVALID_TOKEN'}), 401

        return f(user_id, username, role, *args, **kwargs)
    return decorated


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(user_id, username, role, *args, **kwargs):
        if role != 'admin':
            return jsonify({'message': 'Admin access required', 'error': 'ADMIN_REQUIRED'}), 403
        return f(user_id, username, role, *args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════════════════════════
# AUTHENTICATION ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing fields', 'error': 'MISSING_FIELDS'}), 400

    username = data.get('username').strip()
    password = data.get('password')
    role = data.get('role', 'passenger').lower()

    if len(password) < 6:
        return jsonify({'message': 'Password too short', 'error': 'SHORT_PASSWORD'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username exists', 'error': 'USERNAME_EXISTS'}), 409

    user = User(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = create_token(user.id, user.username, user.role)
    return jsonify({
        'message': 'User registered',
        'user': user.to_dict(),
        'token': token
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing fields', 'error': 'MISSING_FIELDS'}), 400

    user = User.query.filter_by(username=data.get('username')).first()

    if not user or not user.verify_password(data.get('password')):
        return jsonify({'message': 'Invalid credentials', 'error': 'AUTH_FAILED'}), 401

    token = create_token(user.id, user.username, user.role)
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'token': token
    }), 200


@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(user_id, username, role):
    """Logout user (token-based, just clear client-side)"""
    return jsonify({'message': 'Logout successful'}), 200


@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(user_id, username, role):
    """Get current user"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found', 'error': 'NOT_FOUND'}), 404
    return jsonify({'user': user.to_dict(include_bookings=True)}), 200


# ═══════════════════════════════════════════════════════════════════
# FLIGHT ROUTES (MOCK DATA)
# ═══════════════════════════════════════════════════════════════════

DEMO_FLIGHTS = [
    {
        'id': 'SG101', 'airline': 'Singapore Airlines', 'departure': 'BLR', 'arrival': 'DEL',
        'departure_time': '2026-04-14T10:00:00', 'arrival_time': '2026-04-14T12:30:00',
        'price': 199.99, 'available_seats': 45, 'aircraft': 'Boeing 737', 'duration': 150
    },
    {
        'id': 'SG202', 'airline': 'Singapore Airlines', 'departure': 'DEL', 'arrival': 'BOM',
        'departure_time': '2026-04-14T14:00:00', 'arrival_time': '2026-04-14T16:15:00',
        'price': 249.99, 'available_seats': 32, 'aircraft': 'Airbus A320', 'duration': 135
    },
    {
        'id': 'SG303', 'airline': 'Singapore Airlines', 'departure': 'BOM', 'arrival': 'BLR',
        'departure_time': '2026-04-15T08:00:00', 'arrival_time': '2026-04-15T10:00:00',
        'price': 149.99, 'available_seats': 60, 'aircraft': 'Boeing 737', 'duration': 120
    },
    {
        'id': 'SG404', 'airline': 'Singapore Airlines', 'departure': 'BLR', 'arrival': 'HYD',
        'departure_time': '2026-04-15T11:00:00', 'arrival_time': '2026-04-15T12:30:00',
        'price': 99.99, 'available_seats': 78, 'aircraft': 'Airbus A320', 'duration': 90
    }
]


@app.route('/api/flights', methods=['GET'])
def get_flights():
    """Get all flights"""
    flights = DEMO_FLIGHTS.copy()
    departure = request.args.get('departure', '').upper()
    arrival = request.args.get('arrival', '').upper()

    if departure:
        flights = [f for f in flights if f['departure'] == departure]
    if arrival:
        flights = [f for f in flights if f['arrival'] == arrival]

    return jsonify({'message': 'Flights retrieved', 'count': len(flights), 'flights': flights}), 200


@app.route('/api/flights/search', methods=['POST'])
def search_flights():
    """Search flights"""
    data = request.get_json()
    departure = data.get('departure', '').upper()
    arrival = data.get('arrival', '').upper()

    flights = [f for f in DEMO_FLIGHTS if f['departure'] == departure and f['arrival'] == arrival]
    return jsonify({'message': 'Search complete', 'count': len(flights), 'flights': flights}), 200


# ═══════════════════════════════════════════════════════════════════
# BOOKING ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/bookings', methods=['POST'])
@token_required
def create_booking(user_id, username, role):
    """Create booking and add to blockchain"""
    data = request.get_json()

    if not data or not data.get('flight') or not data.get('seat') or not data.get('price'):
        return jsonify({'message': 'Missing fields', 'error': 'MISSING_FIELDS'}), 400

    try:
        ticket_hash = Booking.generate_ticket_hash()
        booking = Booking(
            user_id=user_id,
            flight=data['flight'],
            seat=data['seat'],
            price=float(data['price']),
            ticket_hash=ticket_hash
        )
        db.session.add(booking)
        db.session.commit()

        # Add to blockchain
        booking_data = {
            'booking_id': booking.id,
            'user_id': booking.user_id,
            'flight': booking.flight,
            'seat': booking.seat,
            'price': float(booking.price),
            'ticket_hash': booking.ticket_hash
        }
        block = blockchain.add_block(booking_data)

        return jsonify({
            'message': 'Booking created',
            'booking': booking.to_dict(),
            'blockchain': {
                'block_index': block.index,
                'block_hash': block.hash,
                'nonce': block.nonce,
                'ticket_hash': ticket_hash
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Booking failed', 'error': str(e)}), 500


@app.route('/api/bookings', methods=['GET'])
@token_required
def get_user_bookings(user_id, username, role):
    """Get user's bookings"""
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify({
        'message': 'Bookings retrieved',
        'count': len(bookings),
        'bookings': [b.to_dict() for b in bookings]
    }), 200


@app.route('/api/bookings/stats', methods=['GET'])
@token_required
def get_booking_stats(user_id, username, role):
    """Get user booking stats"""
    bookings = Booking.query.filter_by(user_id=user_id).all()
    total_price = sum(float(b.price) for b in bookings) if bookings else 0
    
    return jsonify({
        'message': 'Stats retrieved',
        'stats': {
            'total_bookings': len(bookings),
            'total_spent': round(total_price, 2),
            'unique_flights': len(set(b.flight for b in bookings)),
            'average_price': round(total_price / len(bookings), 2) if bookings else 0
        }
    }), 200


@app.route('/api/bookings/verify-ticket', methods=['POST'])
def verify_ticket():
    """Verify ticket by hash"""
    data = request.get_json()
    ticket_hash = data.get('ticket_hash')

    booking = Booking.query.filter_by(ticket_hash=ticket_hash).first()
    if not booking:
        return jsonify({'message': 'Ticket not found', 'valid': False, 'error': 'NOT_FOUND'}), 404

    # Find in blockchain
    blockchain_record = None
    for block in blockchain.chain:
        if isinstance(block.data, dict) and block.data.get('ticket_hash') == ticket_hash:
            blockchain_record = {
                'block_index': block.index,
                'block_hash': block.hash,
                'nonce': block.nonce,
                'timestamp': block.timestamp
            }
            break

    return jsonify({
        'message': 'Ticket verified',
        'valid': blockchain_record is not None,
        'booking': booking.to_dict(),
        'blockchain_record': blockchain_record
    }), 200


# ═══════════════════════════════════════════════════════════════════
# ADMIN ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.route('/api/admin/bookings', methods=['GET'])
@token_required
@admin_required
def get_all_bookings(user_id, username, role):
    """Get all bookings (admin only)"""
    bookings = Booking.query.all()
    return jsonify({
        'message': 'Bookings retrieved',
        'count': len(bookings),
        'bookings': [b.to_dict(include_user=True) for b in bookings]
    }), 200


@app.route('/api/admin/bookings/stats', methods=['GET'])
@token_required
@admin_required
def get_admin_stats(user_id, username, role):
    """Get booking statistics (admin only)"""
    bookings = Booking.query.all()
    total_revenue = sum(float(b.price) for b in bookings) if bookings else 0

    return jsonify({
        'message': 'Stats retrieved',
        'stats': {
            'total_bookings': len(bookings),
            'total_revenue': round(total_revenue, 2),
            'average_ticket_price': round(total_revenue / len(bookings), 2) if bookings else 0,
            'unique_users': len(set(b.user_id for b in bookings)),
            'unique_flights': len(set(b.flight for b in bookings))
        }
    }), 200


@app.route('/api/admin/users', methods=['GET'])
@token_required
@admin_required
def get_all_users(user_id, username, role):
    """Get all users (admin only)"""
    users = User.query.all()
    return jsonify({
        'message': 'Users retrieved',
        'count': len(users),
        'users': [u.to_dict() for u in users]
    }), 200


@app.route('/api/admin/users/<int:target_id>/role', methods=['PUT'])
@token_required
@admin_required
def update_user_role(user_id, username, role, target_id):
    """Update user role (admin only)"""
    if target_id == user_id:
        return jsonify({'message': 'Cannot change own role', 'error': 'SELF_MODIFY'}), 403

    data = request.get_json()
    new_role = data.get('role', '').lower()

    if new_role not in ['passenger', 'admin']:
        return jsonify({'message': 'Invalid role', 'error': 'INVALID_ROLE'}), 400

    user = User.query.get(target_id)
    if not user:
        return jsonify({'message': 'User not found', 'error': 'NOT_FOUND'}), 404

    user.role = new_role
    db.session.commit()

    return jsonify({'message': 'Role updated', 'user': user.to_dict()}), 200


@app.route('/api/admin/blockchain', methods=['GET'])
@token_required
@admin_required
def get_blockchain(user_id, username, role):
    """Get blockchain data (admin only)"""
    format_type = request.args.get('format', 'full')

    if format_type == 'summary':
        return jsonify({
            'message': 'Blockchain summary',
            'blockchain': {
                'blocks_count': len(blockchain.chain),
                'difficulty': blockchain.difficulty,
                'is_valid': blockchain.is_valid()
            }
        }), 200

    return jsonify({
        'message': 'Blockchain data',
        'blockchain': blockchain.to_dict()
    }), 200


@app.route('/api/admin/validate', methods=['GET'])
@token_required
@admin_required
def validate_blockchain(user_id, username, role):
    """Validate blockchain (admin only)"""
    is_valid = blockchain.is_valid()

    return jsonify({
        'message': 'Blockchain valid' if is_valid else 'Blockchain invalid',
        'status': 'valid' if is_valid else 'invalid',
        'validation': {
            'total_blocks': len(blockchain.chain),
            'difficulty': blockchain.difficulty,
            'is_valid': is_valid
        }
    }), 200


@app.route('/api/admin/system/info', methods=['GET'])
@token_required
@admin_required
def get_system_info(user_id, username, role):
    """Get system info (admin only)"""
    return jsonify({
        'message': 'System info',
        'system': {
            'blockchain': {
                'blocks': len(blockchain.chain),
                'difficulty': blockchain.difficulty,
                'is_valid': blockchain.is_valid()
            },
            'database': {
                'total_users': User.query.count(),
                'total_bookings': Booking.query.count()
            },
            'status': 'healthy' if blockchain.is_valid() else 'warning'
        }
    }), 200


# ═══════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'blockchain_blocks': len(blockchain.chain)
    }), 200


# ═══════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Endpoint not found', 'error': 'NOT_FOUND'}), 404


@app.errorhandler(500)
def server_error(error):
    db.session.rollback()
    return jsonify({'message': 'Server error', 'error': 'INTERNAL_ERROR'}), 500


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✈️ SkyLedger Backend Starting...")
        print("📍 API: http://localhost:5000")
        print("📊 Blockchain Blocks:", len(blockchain.chain))
        print("🔗 Difficulty:", blockchain.difficulty)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
