from functools import wraps
import secrets
from flask import request, jsonify
import json
import decimal

from models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        # Get token from header
        if 'x-access-token' in request.headers:
            header_value = request.headers['x-access-token']
            if ' ' in header_value:
                token = header_value.split(' ')[1]  # e.g., 'Bearer abc123'
            else:
                token = header_value  # if sent without 'Bearer'

        if not token:
            return jsonify({'message': 'Token is missing.'}), 401

        try:
            current_user_token = User.query.filter_by(token=token).first()
            print(f"Token received: {token}")
            print(f"User found: {current_user_token}")
            
            if not current_user_token:
                return jsonify({'message': 'Token is invalid or expired.'}), 401

        except Exception as e:
            print(f"Exception during token validation: {e}")
            return jsonify({'message': 'An error occurred while validating token.'}), 500

        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated



class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super().default(obj)

