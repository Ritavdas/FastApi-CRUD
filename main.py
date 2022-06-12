from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
import geopy.distance


# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()



@app.post("/address", response_model=schemas.Address, status_code=status.HTTP_201_CREATED)
def create_address(address: schemas.AddressCreate, session: Session = Depends(get_session)):

    # create an instance of the address database model
    addressdb = models.Address(
        adr=address.adr, lat=address.lat, lon=address.lon)

    # add it to the session and commit it
    session.add(addressdb)
    session.commit()
    session.refresh(addressdb)

    # return the address object
    return addressdb


@app.get("/address/{id}", response_model=schemas.Address)
def read_address(id: int, session: Session = Depends(get_session)):

    # get the address item with the given id
    address = session.query(models.Address).get(id)

    # check if address item with given id exists. If not, raise exception and return 404 not found response
    if not address:
        raise HTTPException(
            status_code=404, detail=f"address item with id {id} not found")

    return address


@app.put("/address/{id}", response_model=schemas.Address)
def update_address(id: int, adr: str, long: float, lat: float, session: Session = Depends(get_session)):

    # get the address item with the given id
    address = session.query(models.Address).get(id)

    # update address item with the given task (if an item with the given id was found)
    if address:
        address.adr = adr
        address.long = long
        address.lat = lat

        session.commit()

    # check if address item with given id exists. If not, raise exception and return 404 not found response
    if not address:
        raise HTTPException(
            status_code=404, detail=f"address item with id {id} not found")

    return address


@app.delete("/address/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(id: int, session: Session = Depends(get_session)):

    # get the address item with the given id
    address = session.query(models.Address).get(id)

    # if address item with given id exists, delete it from the database. Otherwise raise 404 error
    if address:
        session.delete(address)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"address item with id {id} not found")

    return None


@app.get("/address", response_model=List[schemas.Address])
def read_address_list(session: Session = Depends(get_session)):

    # get all address items
    address_list = session.query(models.Address).all()

    return address_list


@app.get("/address/nearby/{id}", response_model=List[schemas.Address])
def read_nearby_address(id: int, km: float, session: Session = Depends(get_session)):
    address_list = session.query(models.Address).all()
    # get all address items
    address = session.query(models.Address).get(id)
    address_list.remove(address)

    main_lat, main_long = address.lat, address.lon

    close = []
    for i in address_list:
        distance = geopy.distance.geodesic(
            (i.lat, i.lon), (main_lat, main_long)).km
        if distance <= km:
            close.append(i)

    # check if address item with given id exists. If not, raise exception and return 404 not found response
    if not address:
        raise HTTPException(
            status_code=404, detail=f"address item with id {id} not found")

    return close
    # f'These are the address which are within a {km} radius of the {address.adr} ${address_list}'
