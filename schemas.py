from pydantic import BaseModel

class AddressCreate(BaseModel):
    adr: str
    lat : float
    lon : float


class Address(BaseModel):
    id: int
    adr: str
    lat : float
    lon : float

    class Config:
        orm_mode = True
