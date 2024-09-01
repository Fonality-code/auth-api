from beanie import Document


class Token(Document):
    token: str
    user_id: str
    type: str
    expires_at: int

    class Config:
        collection = "tokens"