import asyncio
from fastapi import APIRouter, Response, status, Depends, responses
from sqlalchemy.orm import Session
from .. import schemas, database, models

from ..repositories import short_url

get_db = database.get_db
router = APIRouter(tags=["Short URL"])


@router.post("/short-url", status_code=status.HTTP_201_CREATED)
def http_create_short_url(
    req: schemas.URLShortern, res: Response, db: Session = Depends(get_db)
):
    return asyncio.run(short_url.create_short_url(req, res, db))


@router.get("/{params}")
def http_redirecting_url(params: str, db: Session = Depends(get_db)):
    return asyncio.run(short_url.redirecting_url(params, db))
