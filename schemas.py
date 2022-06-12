from pydantic import BaseModel

# For creation
class AddressCreate(BaseModel):
    adr: str
    lat: float
    lon: float

# For updation
class AddressUP(BaseModel):
    adr: str | None = None
    lat: float | None = None
    lon: float | None = None

    class Config:
        orm_mode = True

# Base
class Address(BaseModel):
    id: int
    adr: str
    lat: float
    lon: float

    class Config:
        orm_mode = True
