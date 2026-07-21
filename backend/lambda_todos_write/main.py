import uuid
import boto3
from fastapi import FastAPI, HTTPException, Depends, Request
from mangum import Mangum

from shared.auth import get_current_user_id
from shared.schemas import NoteBase, NoteUpdate, NoteDelete

app = FastAPI()
table = boto3.resource("dynamodb").Table("notes")

@app.post("/todos/notes")
def create_notes(note: NoteBase, user_id: str = Depends(get_current_user_id)):
    try:
        note_id = str(uuid.uuid4())
        table.put_item(Item={
            "PK": f"USER#{user_id}",
            "SK": f"NOTE#{note_id}",
            "title": note.title,
        })
        return {"id": note_id, "title": note.title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/todos/update")
def update_note(update_note: NoteUpdate, user_id: str = Depends(get_current_user_id)):
    try:
        table.update_item(
            Key={"PK": f"USER#{user_id}", "SK": f"NOTE#{update_note.id}"},
            UpdateExpression="SET title = :t",
            ExpressionAttributeValues={":t": update_note.title},
            ConditionExpression="attribute_exists(PK)",  # fails if note doesn't exist
        )
        return {"id": update_note.id, "title": update_note.title}
    except table.meta.client.exceptions.ConditionalCheckFailedException:
        raise HTTPException(status_code=404, detail="Note not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/todos/delete")
def delete_note(note: NoteDelete, user_id: str = Depends(get_current_user_id)):
    try:
        table.delete_item(Key={"PK": f"USER#{user_id}", "SK": f"NOTE#{note.id}"})
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)