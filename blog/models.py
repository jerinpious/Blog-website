from .database import Base
from sqlalchemy import Column ,Integer, String

# table model for the blogs
class Blog(Base):

    __tablename__ = 'blogs'

    id = Column(Integer, primary_key= True, index= True)
    title = Column(String)
    body = Column(String)