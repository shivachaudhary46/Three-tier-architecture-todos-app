from fastapi import FastAPI, Depends, HTTPException, Request
from mangum import Mangum 
import boto3

from backend.shared.auth import get_current_user_id
from backend.shared.schemas import NoteRead

app = FastAPI() 
table = boto3.resource("dynamodb").Table("notes")

@app.get("/todos/notes", response_model=list[NoteRead])
def get_notes(
    request: Request,
    user_id: str = Depends(get_current_user_id)
):
    try:
        resp = table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={":pk": f"USER#{user_id}"},
        )
        return [
            {
                "id": item["SK"].split("#")[1], 
                "title": item["title"]
            }
            for item in resp["Items"]
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)