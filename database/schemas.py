from pydantic import BaseModel


class URLShortern(BaseModel):
    original_url: str
    short_url: str | None

    class Config:
        orm_mode = True
