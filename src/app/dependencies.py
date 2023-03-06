from fastapi import Response, Header, HTTPException
from dotenv import load_dotenv
import jwt
import os


load_dotenv()

async def verify_token(user_id, authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="No Authorization header provided! Obtain header and come back again"
        )
    else:
        auth_header_parts = authorization.split()
        if len(auth_header_parts) != 2:
            raise HTTPException(
                status_code=401,
                detail=f"Authorization header consist of {len(auth_header_parts)} parts."
                f" But should be 2! Check it out"
            )

        access_token = auth_header_parts[1]

        try:
            payload = jwt.decode(
                access_token, os.getenv("SECRET_KEY"),
                algorithms = os.getenv("JWT_ALGORITHM")
            )
        except jwt.ExpiredSignatureError:
            return Response('Access token is expired!', status_code=401)
        except (jwt.exceptions.DecodeError, jwt.InvalidTokenError):
            return Response('Invalid access token! Please send valid token', status_code=401)
        token_user_id = str(payload.get("user_id"))


        if token_user_id != user_id:
            raise HTTPException(
                status_code=401,
                detail="You're not allowed to see statistics from this page!"
            )
