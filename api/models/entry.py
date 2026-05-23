from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import uuid4

class EntryCreate(BaseModel):
    """Model for creating a new journal entry (user input)."""
    work: str = Field(
        max_length=256,
        description="What did you work on today?",
        json_schema_extra={"example": "Studied FastAPI and built my first API endpoints"}
    )
    struggle: str = Field(
        max_length=256,
        description="What's one thing you struggled with today?",
        json_schema_extra={"example": "Understanding async/await syntax and when to use it"}
    )
    intention: str = Field(
        max_length=256,
        description="What will you study/work on tomorrow?",
        json_schema_extra={"example": "Practice PostgreSQL queries and database design"}
    )

    @field_validator("work", "struggle", "intention")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        """
        Sanitizes input strings by stripping leading/trailing whitespace
        and explicitly rejects completely empty entries.
        """
        # 1. Clean up hidden whitespace padding on both ends
        cleaned_value = value.strip()
        
        # 2. Halt processing if the input is empty or just blank spaces
        if not cleaned_value:
            raise ValueError("Text field cannot be blank or contain only empty whitespace strings.")
            
        return cleaned_value


class Entry(BaseModel):
    """Full data database entity representing a persistent journal item."""
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the entry (UUID)."
    )
    work: str = Field(
        ...,
        max_length=256,
        description="What did you work on today?"
    )
    struggle: str = Field(
        ...,
        max_length=256,
        description="What’s one thing you struggled with today?"
    )
    intention: str = Field(
        ...,
        max_length=256,
        description="What will you study/work on tomorrow?"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the entry was created."
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the entry was last updated."
    )

    # Apply the same strict validation scanner logic to the database entry class
    @field_validator("work", "struggle", "intention")
    @classmethod
    def validate_database_fields(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Database entity fields cannot contain empty or corrupt string blocks.")
        return cleaned_value

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }