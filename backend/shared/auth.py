from fastapi import Request, HTTPException

def get_current_user_id(request: Request) -> str: 
    try: 
        claims = request.scope["aws.event"]["requestContext"]["authorizer"]["claims"]
        return claims["sub"]
    except KeyError: 
        raise HTTPException(status_code=401, detail="Not Authenticated")