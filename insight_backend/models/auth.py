from pydantic import BaseModel


class JwtBearer:
    token: str
