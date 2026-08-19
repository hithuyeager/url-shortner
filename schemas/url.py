from pydantic import BaseModel,HttpUrl

class URLCreate(BaseModel):
    original_url: HttpUrl

class URLResponse(BaseModel):
    short_url: str

class URLNotFoundError(Exception):
    pass
