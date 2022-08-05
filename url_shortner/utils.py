from fastapi import HTTPException, status
from uuid import uuid4
from . import models


async def get_random_hex():
    return uuid4().hex[5:10]


async def extract_domain(url: str):
    main_site = url.split("/")[2]
    domain = main_site.split(".")[1]
    return domain


async def short_url(url: str, db):
    domain = await extract_domain(url)
    random_hex = await get_random_hex()

    short_url = domain + random_hex

    exist_short = await check_short_url(short_url, db)

    # check if the url already exist by chance
    if exist_short:
        # re generate different  random value if generated value already exists
        return await short_url(url, db)

    return short_url


async def check_original_url(original_url, db):
    url = db.query(models.ShortURL).filter(
        models.ShortURL.original_url == original_url
    )
    if url.first():
        return url.first()
    return None


async def check_short_url(short_url, db):
    url = db.query(models.ShortURL).filter(
        models.ShortURL.short_url == short_url
    )
    if url.first():
        raise HTTPException(
            detail={"error": "This short url is already taken"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return None
