# lambda_auth/main.py
import os
import boto3
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel

app = FastAPI()
client = boto3.client("cognito-idp")

CLIENT_ID = os.environ["COGNITO_CLIENT_ID"]

class SignupRequest(BaseModel):
    email: str
    password: str

class ConfirmRequest(BaseModel):
    email: str
    code: str

class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str


@app.post("/auth/signup")
def signup(req: SignupRequest):
    try:
        client.sign_up(
            ClientId=CLIENT_ID,
            Username=req.email,
            Password=req.password,
            UserAttributes=[{"Name": "email", "Value": req.email}],
        )
        return {"status": "confirmation code sent"}
    except client.exceptions.UsernameExistsException:
        raise HTTPException(status_code=409, detail="User already exists")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/confirm")
def confirm(req: ConfirmRequest):
    try:
        client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=req.email,
            ConfirmationCode=req.code,
        )
        return {"status": "confirmed"}
    except client.exceptions.CodeMismatchException:
        raise HTTPException(status_code=400, detail="Invalid code")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login")
def login(req: LoginRequest):
    try:
        resp = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": req.email, "PASSWORD": req.password},
        )
        tokens = resp["AuthenticationResult"]
        return {
            "id_token": tokens["IdToken"],
            "access_token": tokens["AccessToken"],
            "refresh_token": tokens["RefreshToken"],
        }
    except client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    except client.exceptions.UserNotConfirmedException:
        raise HTTPException(status_code=403, detail="Account not confirmed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/refresh")
def refresh(req: RefreshRequest):
    try:
        resp = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": req.refresh_token},
        )
        tokens = resp["AuthenticationResult"]
        return {"id_token": tokens["IdToken"], "access_token": tokens["AccessToken"]}
    except client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Refresh token expired")

handler = Mangum(app)