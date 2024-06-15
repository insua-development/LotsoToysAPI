from fastapi import FastAPI
# from class_database.connection import DatabaseConnection
# import class_database.crud.activitie_crud as activitie_crud

# ip is input products
from data_validator import product as ip
from fastapi.middleware.cors import CORSMiddleware
from class_database import db_connection as db_connect

from class_database.crud import activitie_crud as acrud

from firebase_admin import firestore




## IMPORT LIBRARIES



app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)

db: firestore.client = db_connect.connect_database()


## Implement functions
## -------------------



@app.get('/products/{name}')
async def get_product(name: str):
    return acrud.read_product_db(db=db, name=name)


@app.get('/products/{name}/sizes')
async def get_product_sizes(name: str):
    return acrud.read_products_sizes_db(db=db, product_name=name, only_active=False)


@app.get('/products/{name}/sizes_active')
async def get_product_sizes_active(name: str):
    return acrud.read_products_sizes_db(db=db, product_name=name, only_active=True)


@app.get('/products_active')
async def get_products_active():
    return acrud.read_products_db(db=db, only_active=True)


@app.get('/products')
async def get_products():
    return acrud.read_products_db(db=db, only_active=False)



@app.post('/products')
async def create_product(product: ip.Product):
    return acrud.create_product_db(db=db, product=product)



@app.post('/product_sizes')
async def create_product_size(product_size: ip.ProductSize):
    return acrud.create_product_size_db(db=db, product_size=product_size)


@app.delete('/products/{name}')
async def delete_product(name: str):
    return acrud.delete_product_db(db=db, product_name=name)


@app.delete('/products/{name}/sizes/{size}')
async def delete_product_size(product_name: str, size: str):
    return acrud.delete_product_size_db(db=db, product_name=product_name, size=size)


@app.put('/products/')
async def upgrade_product(product: ip.Product, old_name:str):
    acrud.upgrade_product_db(db=db, product=product, old_name=old_name)


@app.put('/product_sizes/')
async def upgrade_product_size(product_size: ip.ProductSize, old_size: str):
    return acrud.upgrade_product_size_db(db=db, product_size=product_size, old_size=old_size)


@app.patch('/products/')
async def update_product(product: ip.Product):
    return acrud.update_product_db(db=db, product=product)


@app.patch('/product_sizes/')
async def update_product_size(product_size: ip.ProductSize):
    return acrud.update_product_size_db(db=db, product_size=product_size)



