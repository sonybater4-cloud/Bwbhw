from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional

class ContentCreate(BaseModel):
    title: str
    kind: str = "movie"
    language: str = "Hindi"
    category: str = "Drama"
    poster_url: Optional[HttpUrl] = None
    stream_url: Optional[HttpUrl] = None
    is_premium: bool = False
    published: bool = True

class ContentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    kind: str
    language: str
    category: str
    poster_url: Optional[str] = None
    stream_url: Optional[str] = None
    is_premium: bool
    published: bool
