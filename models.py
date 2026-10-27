from sqlalchemy import Column, Integer, String, Text, Boolean
from .database import Base

class Content(Base):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False, index=True)
    kind = Column(String(30), nullable=False, default="movie")  # movie, show, short, live
    language = Column(String(60), nullable=False, default="Hindi")
    category = Column(String(100), nullable=False, default="Drama")
    poster_url = Column(Text, nullable=True)
    stream_url = Column(Text, nullable=True)  # only authorized stream URLs
    is_premium = Column(Boolean, default=False, nullable=False)
    published = Column(Boolean, default=True, nullable=False)
