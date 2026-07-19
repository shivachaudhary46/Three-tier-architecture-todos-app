from typing import List
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

hasher = PasswordHash.recommended() 

class Base(DeclarativeBase):
    pass

DATABASE_URL = "postgresql://postgres:shivachaudhary@db/todos"
engine = create_engine(DATABASE_URL, echo=True)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    notes: Mapped[List["Note"]] = relationship(back_populates="user", cascade="all, delete")

class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user: Mapped["User"] = relationship(back_populates="notes")

def create_all_database_tables():
    # Creates the tables in postgres if they don't already exist
    Base.metadata.create_all(bind=engine)

def get_db(): 
    with Session(engine) as session: 
        yield session