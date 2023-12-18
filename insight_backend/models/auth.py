from pydantic import BaseModel


class TokenBearer(BaseModel):
    token: str


class TokenData(BaseModel):
    telegram_id: str
