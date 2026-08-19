from pydantic import BaseModel,HttpUrl

class URLCreate(BaseModel):
    original_url: HttpUrl

class URLResponse(BaseModel):
    short_url: HttpUrl

class URLNotFoundError(Exception):
    pass
