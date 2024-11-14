from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import UserAudit, db

def log_user_activity(action):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
            except:
                user_id = None
            
            if user_id:
                audit_log = UserAudit(user_id=user_id, action=action, action_timestamp=db.func.current_timestamp())
                db.session.add(audit_log)
                db.session.commit()
            return func(*args, **kwargs)
        return wrapper
    return decorator
