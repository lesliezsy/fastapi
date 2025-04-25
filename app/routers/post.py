from fastapi import FastAPI, Path, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional

from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    # prefix for all the endpoints in this router
    tags=["Posts"]
    # tags=["Posts"] is to group the endpoints in the documentation
)


# @router.get("/", response_model=list[schemas.Post])
@router.get("/", response_model=list[schemas.PostOut])
# path operation function
def get_posts(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # skip means how many records to skip
    # limit means how many records to return
    # limit and skip are for frontend pagination
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # only show the posts that belong to the current logined user
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):

    # find first instance of the post and return it
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} was not found")


    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
   # bring user id from the authenticated user
   new_post = models.Post(owner_id = current_user.id, **post.model_dump())
   db.add(new_post)
   db.commit()
   # retrieve the new data and store back to the new_post
   db.refresh(new_post)
   # return the sqlalchemy model
   return new_post

# status_code in the @app.delete decorator specifies the HTTP status code that the endpoint will return when the operation is successful
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post is a query object
    # post.first() is an app.models.Post object (the object that is returned from the database)
    post_query = db.query(models.Post).filter(models.Post.id == id)
  
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    # synchronize_session=False is to avoid the need to synchronize the session with the database   
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
# post: Post - ensure that the request body comes from a right schema
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    
    return post_query.first()