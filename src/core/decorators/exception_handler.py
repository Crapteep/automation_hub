
from fastapi import HTTPException
from functools import wraps
from src.utils.exceptions import CommandExecutionError, HttpAwareException


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except CommandExecutionError as e:
            cause = e.cause
            if isinstance(cause, HttpAwareException):
                raise HTTPException(status_code=cause.status_code, detail=cause.message)
            print(e)
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return wrapper
