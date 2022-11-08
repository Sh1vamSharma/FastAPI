from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils,database
 

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/create", status_code= status.HTTP_201_CREATED, response_model= schemas.UserResponce)
def create_user(user:schemas.UserCreate, db: Session = Depends(database.get_db)):

    pre_exist_user = db.query(models.User).filter(models.User.email == user.email).first()

    if pre_exist_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="unable to create user, a user is already registerd with this email")
    print(user.dict())
    # creating a hash for password field:
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model= schemas.UserResponce)
def get_user(id: int, db: Session= Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail= f"User with id: {id} does not exist")

    return user

