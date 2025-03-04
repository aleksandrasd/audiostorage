import datetime
from http.cookies import SimpleCookie
import jwt
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.authentication import AuthenticationBackend
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from core.config import config

class CurrentUser(BaseModel):
    id: int = Field(None, description="ID")

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
        
    
class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[bool, CurrentUser | None]:
        current_user = CurrentUser()
        if not hasattr(conn.state, "token"):
            return False, current_user
        
        credentials: str = conn.state.token

        if not credentials:
            return False, current_user

        user_id = TokenMiddlewareHelper.extract_user_id(credentials)
        if not user_id:
          return False, current_user

        current_user.id = user_id
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass



class CustomMiddleware(BaseHTTPMiddleware):
    def create_refresh_token(self, encoded_refresh_token) -> str | None:
        user_id = TokenMiddlewareHelper.extract_user_id(encoded_refresh_token) 
        if not user_id:
            return None
        
        exp = datetime.now() + datetime.timedelta(seconds=config.JWT_TOKEN_EXPIRE_PERIOD)
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
        cookies = SimpleCookie()
        cookies.load(request.cookies)
        
        token: str | None = cookies.get("token")
        refresh_token: str | None = cookies.get("refresh_token")
        if not token or not refresh_token:
            return await call_next(request) 

        user_id: str | None = TokenMiddlewareHelper.extract_user_id(token) 
        if user_id:
           request.state.token = token
           return await call_next(request)  

        token: str | None = self.create_refresh_token(refresh_token)

        if not token:
            return await call_next(request)  

        response = await call_next(request)
        response.set_cookie(key="token", value=token)
        
        return response
