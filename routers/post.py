from fastapi import APIRouter, Depends, Body, HTTPException, status
from pydantic import Required
from sqlalchemy.orm import Session
from db.database import get_db
from sqlalchemy import func
from db.models import Post, User, Like, Dislike
from db.schemas import PostCreate, PostUpdate
from oauth2 import get_current_user

router = APIRouter(tags=["Posts"])


@router.get("/posts")
async def get_posts(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get posts of currently authorized"""
    return (
        db.query(
            Post,
            func.count(Like.post_id).label("likes"),
            func.count(Dislike.post_id).label("dislikes"),
        )
        .filter(Post.owner_id == current_user.id)
        .join(Like, Like.post_id == Post.id, isouter=True)
        .join(Dislike, Dislike.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .all()
    )


@router.get("/{user_id}/posts")
async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    """Get posts of any other user"""
    return db.query(Post).filter(Post.owner_id == user_id).all()


@router.get("/post/{post_id}")
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    """Get single post by id"""

    post = db.query(Post).filter(Post.id == post_id).first()

    print(post)

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post {post_id} not found"
        )

    return (
        db.query(
            Post,
            func.count(Like.post_id).label("likes"),
            func.count(Dislike.post_id).label("dislikes"),
        )
        .filter(Post.id == post_id)
        .join(Like, Like.post_id == Post.id, isouter=True)
        .join(Dislike, Dislike.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .first()
    )


@router.delete("/post/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post {post_id} not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="you can edit only your own post"
        )

    db.query(Post).filter(Post.id == post_id).delete()
    db.commit()

    return status.HTTP_201_CREATED


@router.put("/post")
async def put_post(
    db: Session = Depends(get_db),
    post: PostCreate = Body(default=Required),
    current_user: User = Depends(get_current_user),
):
    new_post = Post(owner_id=current_user.id, **post.dict())

    if new_post.title == "" or new_post.content == "":
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Post must contains content and title",
        )
    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"An error {error} occurred while creating the post",
        )

    return new_post


@router.patch("/post/{post_id}")
async def patch_post(
    post_id: int,
    post: PostUpdate = Body(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_query = db.query(Post).filter(Post.id == post_id)
    _post = post_query.first()

    if not _post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post {post_id} not found"
        )
    if _post.owner_id != current_user.id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="you can edit only your own post"
        )

    if post.title is None and post.content is None:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="to update data in post must contains content or title",
        )

    if post.title is None:
        post.title = _post.title
    elif post.content is None:
        post.content = _post.content

    try:
        db.query(Post).filter(Post.id == post_id).update(post.dict())
        db.commit()
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"An error occurred while editing post: {error}",
        )

    return status.HTTP_201_CREATED


@router.post("/post/{post_id}/like")
async def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post {post_id} not found"
        )
    if post.owner_id == current_user.id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="you cant like own post"
        )

    post_like_query = db.query(Like).filter(
        Like.post_id == post_id, Like.user_id == current_user.id
    )

    try:
        if post_like_query.first():
            post_like_query.delete()
            db.commit()
        else:
            db.add(Like(post_id=post_id, user_id=current_user.id))
            db.query(Dislike).filter(
                Dislike.post_id == post_id, Dislike.user_id == current_user.id
            ).delete()
            db.commit()
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"An error occurred while liking the post: {error}",
        )

    return status.HTTP_201_CREATED


@router.post("/post/{post_id}/dislike")
async def dislike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post {post_id} not found"
        )
    if post.owner_id == current_user.id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="you cant dislike own post"
        )

    post_dislike_query = db.query(Dislike).filter(
        Dislike.post_id == post_id, Dislike.user_id == current_user.id
    )

    try:
        if post_dislike_query.first():
            post_dislike_query.delete()
            db.commit()
        else:
            db.add(Dislike(post_id=post_id, user_id=current_user.id))
            db.query(Like).filter(
                Like.post_id == post_id, Like.user_id == current_user.id
            ).delete()
            db.commit()
    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"An error occurred while disliking the post: {error}",
        )

    return status.HTTP_201_CREATED
