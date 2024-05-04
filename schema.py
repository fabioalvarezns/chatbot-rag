from pydantic import BaseModel

class userMessage(BaseModel):
    message: str
