# Mocked auth module with insecure patterns (demo only)
# Purposefully includes weak hashing and a hardcoded JWT secret to exercise analyzers.

import hashlib

JWT_SECRET = 'demo_jwt_secret'

USERS = {
    'dr.jones': {'password_hash': hashlib.md5('password123'.encode()).hexdigest(), 'role': 'clinician'}
}

# login endpoint would exist here in a real repo
