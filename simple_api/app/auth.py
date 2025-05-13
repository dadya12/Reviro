from fastapi import Header, HTTPException

API_TOKEN = "mysecrettoken"

def verify_token(x_token: str = Header(...)) -> str:
    if x_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return x_token




