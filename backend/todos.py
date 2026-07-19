from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select 
from sqlalchemy.orm import Session
from database import User, Note, get_db
from schemas import NoteRead, NoteBase, NoteDelete, NoteUpdate
from OAuth import get_current_user
from typing import Annotated

router = APIRouter(
    prefix="/todos", 
    tags=["todos"]
)

@router.post("/notes")
def create_notes(
    note: NoteBase,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    try: 
        db_note = Note(
            title=note.title,
            user_id=current_user.id
        )

        db.add(db_note)
        db.commit()
        db.refresh(db_note)

        return db_note

    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/notes", response_model=list[NoteRead])
def get_notes(current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),):
    try: 
        user_id = current_user.id
        stmt = select(Note).where(Note.user_id == user_id)
        notes = db.scalars(stmt).all() 
        return notes
    
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update")
def update_note(
    update_note: NoteUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    try:
        stmt = select(Note).where(
            Note.user_id == current_user.id,
            Note.id == update_note.id
        )
        note = db.scalars(stmt).first()

        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")

        note.title = update_note.title
        db.commit()
        db.refresh(note)
        return note

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/delete")
def delete_note(note: NoteDelete, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    try: 
        stmt = select(Note).where(Note.user_id == current_user.id, Note.id == note.id)
        note = db.scalars(stmt).first()

        db.delete(note)
        db.commit()
        return {
            "status": "success"
        }
        
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))



    
