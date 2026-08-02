from fastapi import Request
from slowapi import Limiter


def get_user_key(request: Request):

    user = getattr(request.state, "user", None)

    if user:
        return str(user.user_id)

    return request.client.host


limiter = Limiter(key_func=get_user_key)
