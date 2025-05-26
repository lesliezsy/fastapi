from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
   hashed_password = utils.hash_password(user.password)
   user.password = hashed_password

   new_user = models.User(**user.model_dump())
   db.add(new_user)
   db.commit()
   # retrieve the new data and store back to the new_user
   db.refresh(new_user)
   # return the sqlalchemy model
   return new_user

# @ method decorator
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")
    
    return user