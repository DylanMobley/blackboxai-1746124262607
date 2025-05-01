import jwt
import argparse
import os
from datetime import datetime, timedelta

# Load from .env or fallback
JWT_SECRET = os.getenv("JWT_SECRET", "changeme-super-secret")
JWT_EXPIRY_HOURS = 24

def generate_token(user_id="demo_user", role="default"):
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate JWT token for testing")
    parser.add_argument("--user", default="demo_user", help="User ID / Subject")
    parser.add_argument("--role", default="default", help="Role or tier")

    args = parser.parse_args()
    token = generate_token(user_id=args.user, role=args.role)
    print("\n🛡️  Your JWT Token:\n")
    print(token)
    print("\n📎 Use as HTTP Header:\nAuthorization: Bearer <token>\n")
