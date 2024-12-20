from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
#creating an instance of fastapi 
app = FastAPI()


@app.get('/blog')
def index(limit: int = 10, published: bool = False, sort: Optional[str] = None):
    if published:
        return {'data':f'{limit} published blogs'}
    else:
        return {'data':f'{limit}  blogs'}



@app.get('/blog/unpublished')
def unpublished():
    return {'data':'all unpublished blogs'}

@app.get('/blog/{id}')
#specifying the type to accept
def show(id: int):
    # fetch blog with id
    return {'data':id}



@app.get('/blog/{id}/comments')
def comments(id, limit = 10):
    return {'data':{'1','2'}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(blog: Blog):
    return {'data':f'Blog is created with title as {blog.title}'}