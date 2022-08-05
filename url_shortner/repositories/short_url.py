import asyncio
from fastapi import Request, Response, responses, status, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils import (
    check_short_url,
    short_url as short_url_fn,
    check_original_url,
)


async def create_short_url(req: Request, res: Response, db: Session):
    if not req.short_url:
        req.short_url = await short_url_fn(
            req.original_url, db
        )  # if short url is not sent from user, it generates random short url

    # creating task for runnig both task concurrently
    task1 = asyncio.create_task(check_original_url(req.original_url, db))
    task2 = asyncio.create_task(check_short_url(req.short_url, db))
    exist_original = await task1
    exist_short = await task2

    if exist_original:
        res.status_code = status.HTTP_208_ALREADY_REPORTED
        return exist_original  # if already exist shows the same existing short url details without creating new one on db

    if exist_short:
        return exist_short
        # raise an error response

    data = models.ShortURL(
        original_url=req.original_url, short_url=req.short_url
    )  # if all condition matches it creates new database model

    db.add(data)
    db.commit()
    db.refresh(data)

    return req


async def redirecting_url(params, db):
    url_info: schemas.URLShortern = (
        db.query(models.ShortURL)
        .filter(models.ShortURL.short_url == params)
        .first()
    )
    if not url_info:
        print(url_info)
        return {"error": "Invalid Parameter"}
    return responses.RedirectResponse(
        url_info.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
