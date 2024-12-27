from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session


router = APIRouter()

get_db = database.get_db

# get method to retrieve the data from the database
@router.get('/blog',response_model=List[schemas.ShowBlog],tags=['blogs'])
def all_blogs(db: Session = Depends(database.get_db)):

    blogs = db.query(models.Blog).all()
    
    return blogs

#post method for posting a new a blog using orm to map the to the database
@router.post('/blog',status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):

    new_blog = models.Blog(title= request.title, body= request.body, user_id = 3)

    db.add(new_blog)

    db.commit()

    db.refresh(new_blog)

    return new_blog


# get method to retrieve a blog with an id
@router.get('/blog/{id}',status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def show(id,response: Response, db: Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id ==id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id {id} is not available")
    return blog


#function to delete a blog with id
@router.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog(id, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id ==id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session=False)

    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog(id, request:schemas.Blog, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog.update(request.model_dump())

    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)