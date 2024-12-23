from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, Sessionlocal
from sqlalchemy.orm import Session

app= FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


#post method for posting a new a blog using orm to map the to the database
@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):

    new_blog = models.Blog(title= request.title, body= request.body)

    db.add(new_blog)

    db.commit()

    db.refresh(new_blog)

    return new_blog

# get method to retrieve the data from the database
@app.get('/blog')
def all_blogs(db: Session = Depends(get_db)):

    blogs = db.query(models.Blog).all()
    
    return blogs


# get method to retrieve a blog with an id
@app.get('/blog/{id}',status_code=200)
def show(id,response: Response, db: Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id ==id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id {id} is not available")
    return blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):

    db.query(models.Blog).filter(models.Blog.id ==id).delete(synchronize_session=False)

    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request:schemas.Blog, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).update(request.model_dump())

    db.commit()
    
    return 'updated successfully'

    
