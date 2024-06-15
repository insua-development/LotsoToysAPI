from datetime import datetime
from data_validator import product as ip
from firebase_admin import firestore
from google.api_core import exceptions as google_exceptions




def read_product_db(db: firestore.client, name: str):
    product = db.collection('Products').document(name).get()
    if product.exists:
        product = product.to_dict()
        print(f"Product data: {product}")
    else:
        product = { 'is_active': None, 'error': "No existe ningún producto con el nombre " + name }
    return product



def read_products_db(db: firestore.client, only_active: bool):
    if only_active:
        products_db = db.collection("Products").where("is_active", "==", True).stream()
    else:
        products_db = db.collection("Products").stream()
    products: list = list()
    for product in products_db:
        product_data = product.to_dict()
        product_data["name"] = product.id
        products.append(product_data)
    return products


def read_products_sizes_db(db: firestore.client, product_name: str, only_active: bool):
    if only_active:
        products_db = db.collection("Products").document(product_name).collection("Sizes").where("is_active", "==", True).stream()
    else:
        products_db = db.collection("Products").document(product_name).collection("Sizes").stream()
    product_sizes: list = list()
    for product_size in products_db:
        product_size_data = product_size.to_dict()
        product_size_data["size"] = product_size.id
        product_sizes.append(product_size_data)
    return product_sizes


def read_product_size_db(db: firestore.client, product_name: str, size: str):
    product_size_db = db.collection("Products").document(product_name).collection("Sizes").document(size).get()
    if product_size_db.exists:
        product_size = product_size_db.to_dict()
    else:
        product_size = { 'is_active': None, 'error': "No existe ningún tamaño con el nombre " + size + " para el peluche " + product_name}
    return product_size


def generate_product_data(product: ip.Product):
    product_data_db = {
        'image': product.image,
        'description': product.description,
        'created_time': product.created_time,
        'updated_time': product.updated_time,
        'is_active': product.is_active
    }
    return product_data_db

def create_product_db(db: firestore.client, product: ip.Product):
    response = None
    product_data_db = generate_product_data(product=product)
    try:
        db.collection("Products").add(document_id=product.name, document_data=product_data_db)
        response = product
    except google_exceptions.AlreadyExists:
       response = 'El producto con nombre ' + name + ' ya existe.'
    return response


def generate_product_size_data(product_size: ip.ProductSize):
    product_size_data_db = {
        'stock': product_size.stock,
        'price': product_size.price,
        'created_time': product_size.created_time,
        'updated_time': product_size.updated_time,
        'is_active': product_size.is_active
    }
    return product_size_data_db


def create_product_size_db(db: firestore.client, product_size: ip.ProductSize):
    response = None
    product_size_db = generate_product_size_data(product_size=product_size)
    try:
        db.collection("Products").document(product_size.product_name).collection("Sizes").add(
            document_id=product_size.size,
            document_data=product_size_db
        )
        response = product_size
    except google_exceptions.AlreadyExists:
       response = 'El tamaño con nombre ' + product_size.size + ' ya existe para el producto ' + product_size.product_name + '.'
    return response



def delete_product_db(db: firestore.client, product_name: str):
    response: bool = True
    product_db = read_product_db(db=db, name=product_name)
    if product_db["is_active"] != None:
        product_db["is_active"] = False
        try:
            db.collection("Products").document(product_name).set(product_db)
        except:
            response = False
    return response


def delete_product_size_db(db: firestore.client, product_name: str, size: str):
    response: bool = True
    product_size_db = read_product_size_db(db=db, product_name=product_name, size=size)
    if product_size_db["is_active"] != None:
        product_size_db["is_active"] = False
        try:
            db.collection("Products").document(product_name).collection("Sizes").document(size).set(product_size_db)
        except:
            response = False
    return response



def update_product_db(db: firestore.client, product: ip.Product):
    response = True
    product_db = read_product_db(db=db, name=product.name)
    if product_db["is_active"] != None:
        product_data_db = generate_product_data(product=product)
        product_data_db["created_time"] = product_db["created_time"]
        try:
            db.collection("Products").document(product.name).set(product_data_db)
            product_data_db["name"] = product.name
            response = product_data_db
        except:
            response = False
    return response




def upgrade_product_db(db: firestore.client, product: ip.Product, old_name: str):
    response: bool = True
    product_db = read_product_db(db=db, name=old_name)
    if product_db["is_active"] != None:
        product_data_db = generate_product_data(product=product)
        response = 'new name alredy exists'
        new_product_db = read_product_db(db=db, name=product.name)
        if new_product_db["is_active"] == None:
            try:
                product_data_db["created_time"] = product_db["created_time"]
                db.collection("Products").document(old_name).delete()
                db.collection("Products").add(document_id=product.name, document_data=product_data_db)
                product_data_db["name"] = product.name
                response = product_data_db
            except:
                response = False
    return response



def update_product_size_db(db: firestore.client, product_size: ip.ProductSize):
    response = True
    product_size_db = read_product_size_db(db=db, product_name=product_size.product_name, size=product_size.size)
    if product_size_db["is_active"] != None:
        product_size_data_db = generate_product_size_data(product_size=product_size)
        product_size_data_db["created_time"] = product_size_db["created_time"]
        try:
            db.collection("Products").document(product_size.product_name).collection("Sizes").document(product_size.size).set(product_size_data_db)
            product_size_data_db["product_name"] = product_size.product_name
            product_size_data_db["size"] = product_size.size
            response = product_size_data_db
        except:
            response = False
    return response


def upgrade_product_size_db(db: firestore.client, product_size: ip.ProductSize, old_size: str):
    response: bool = True
    product_size_db = read_product_size_db(db=db, product_name=product_size.product_name, size=old_size)
    if product_size_db["is_active"] != None:
        product_size_data_db = generate_product_size_data(product_size=product_size)
        new_product_size_db = read_product_size_db(db=db, product_name=product_size.product_name, size=product_size.size)
        if new_product_size_db["is_active"] == None:
            try:
                product_size_data_db["created_time"] = product_size_db["created_time"]
                db.collection("Products").document(product_size.product_name).collection("Sizes").document(old_size).delete()
                db.collection("Products").document(product_size.product_name).collection("Sizes").add(
                    document_id=product_size.size,
                    document_data=product_size_db
                )
                product_size_data_db["product_name"] = product_size.product_name
                product_size_data_db["size"] = product_size.size
                response = product_size_data_db
            except:
                response = False
    return response



