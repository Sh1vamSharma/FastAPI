from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2,database


router = APIRouter(
    prefix="/posts",
    tags= ["Posts"]
)


@router.get("/", response_model=List[schemas.PostResponceVote])
def get_posts(db: Session=Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user),
                limit: int = 100, skip: int=0, search: Optional[str]= ""):

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.Count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    return posts

@router.get("/myposts", response_model=List[schemas.PostResponceVote])
def get_posts(db: Session=Depends(database.get_db), 
            current_user: int = Depends(oauth2.get_current_user)):
    
    posts = db.query(models.Post, func.Count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id).all()

    return posts


@router.get("/latest", response_model=schemas.PostResponceVote)   # order of function call with path operation matters
def get_latest_latest(db: Session=Depends(database.get_db), 
            current_user: int = Depends(oauth2.get_current_user)):
    #obj = session.query(ObjectRes).order_by(ObjectRes.id.desc()).first()
    latest = db.query(models.Post, func.Count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by(models.Post.created_at.desc()).first()
    return latest


@router.get("/{id}", response_model=schemas.PostResponceVote)
def get_post(id:int, db: Session=Depends(database.get_db), 
            current_user: int = Depends(oauth2.get_current_user)):

    post= db.query(models.Post, func.Count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Post with ID:{id} was not found")
    
    return post


@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponce)                              #Create
def create_post(post:schemas.CreatePost, db: Session=Depends(database.get_db), 
            current_user: int = Depends(oauth2.get_current_user)):

    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())          #unpacking the python dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=schemas.PostResponce)                              #Update
def update_post(id:int, updated_post:schemas.UpdatePost, db: Session=Depends(database.get_db), 
            current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                        detail="Not autherized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)                     #Delete
def delete_post(id:int, db: Session=Depends(database.get_db), 
            current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                        detail="Not autherized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

