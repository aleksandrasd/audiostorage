from datetime import datetime, timedelta
from http.cookies import SimpleCookie
from fastapi import Request
import jwt

from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from core.config import config


class CurrentUser(BaseModel):
    id: int = Field(None, description="ID")


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[bool, CurrentUser | None]:
        current_user = CurrentUser()

        stringified_cookies :str = conn.cookies
        if not conn.cookies:
          return False, current_user
        
        cookies = SimpleCookie()
        cookies.load(conn.cookies)
        token = cookies.get("token")
        if not token:
          return False, current_user
        
        user_id: str | None = TokenMiddlewareHelper.extract_user_id(token.value)

        if not user_id:
            return False, current_user

        current_user.id = user_id
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass



class TokenMiddlewareHelper:
  @staticmethod  
  def extract_user_id(token) -> str | None:
        try:
            payload = jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
            )
            return payload.get("user_id")
        except jwt.exceptions.PyJWTError:
            return None
        
class CustomMiddleware(BaseHTTPMiddleware):
    def create_token(self, encoded_refresh_token) -> str | None:
        user_id = TokenMiddlewareHelper.extract_user_id(encoded_refresh_token) 
        if not user_id:
            return None
        
        exp = datetime.now() + timedelta(seconds=config.JWT_TOKEN_EXPIRE_PERIOD)
        token = jwt.encode(
            payload={
                "user_id": user_id,
                "exp": exp,
            },
            key=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        )
        return token

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)  
        cookies = SimpleCookie()
        cookies.load(request.cookies)

        if not cookies.get("token"):
            return response
    
        token: str | None = cookies.get("token").value
        if not token:
            return response

        user_id: str | None = TokenMiddlewareHelper.extract_user_id(token) 
        if user_id:
           return response
        
        if not cookies.get("refresh_token"):
            return response
        
        refresh_token: str | None = cookies.get("refresh_token").value
        if not refresh_token:
            return response

        token: str | None = self.create_token(refresh_token)
        if not token:
            return response
        
        response.set_cookie(key="token", value=token)
      
        return response
