import time
import requests
from jose import jwt
from jose.exceptions import JWTError
from flask import request, jsonify, g
from functools import wraps

def has_role(role_allowed:list[str] = None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            roles = g.user.get('realm_access',{}).get('roles',[])

            for role in roles:
                if role in role_allowed:
                    return f(*args, **kwargs)

            return jsonify({"error": "Invalid Authorization header"}), 403

        return wrapper

    return decorator


class Oauth:

    def __init__(self, app):
        self.jwks_cache = {"keys": None, "expires_at": 0}

        self.init_app(app)

    def init_app(self, app):
        self.jwks_url = app.config["JWKS_URL"]
        self.issuer = app.config["JWT_ISSUER"]
        self.client_id = app.config["JWT_CLIENT_ID"]

        app.before_request(self._middleware)

    def _get_jwks(self):
        if self.jwks_cache["keys"] and self.jwks_cache["expires_at"] > time.time():
            return self.jwks_cache["keys"]

        jwks = requests.get(self.jwks_url).json()

        self.jwks_cache["keys"] = jwks
        self.jwks_cache["expires_at"] = time.time() + 3600

        return jwks

    def _verify_token(self, token):
        jwks = self._get_jwks()

        unverified_header = jwt.get_unverified_header(token)

        rsa_key = None
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = key
                break

        if not rsa_key:
            raise Exception("Public key not found")

        unverified_claims = jwt.get_unverified_claims(token)

        if unverified_claims["azp"] != self.client_id:
            raise Exception("Invalid client ID")

        payload = jwt.decode(
            token=token,
            key=rsa_key,
            algorithms=["RS256"],
            issuer=self.issuer,
            options={"verify_aud": False}
        )

        return payload

    def _middleware(self):

        if not request.path.startswith("/api/"):
            return

        # Permitir preflight CORS
        if request.method == "OPTIONS":
            return

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Missing Authorization header"}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid Authorization header"}), 401

        try:
            payload = self._verify_token(token)

            g.user = payload

        except JWTError as e:
            return jsonify({"error": "Invalid token", "details": str(e)}), 401
        except Exception as e:
            return jsonify({"error": "Auth error", "details": str(e)}), 401
