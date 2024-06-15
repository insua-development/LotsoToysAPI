from pydantic import BaseModel
import datetime
from typing import Optional

from datetime import datetime as dtime



class Product(BaseModel):
    name: str
    image: Optional[str] = None
    description: Optional[str] = None
    created_time: Optional[datetime.datetime] = dtime.now()
    updated_time: Optional[datetime.datetime] = dtime.now()
    is_active: Optional[bool] = True



class ProductSize(BaseModel):
    product_name: str
    size: str
    price: float
    stock: int
    created_time: Optional[datetime.datetime] = dtime.now()
    updated_time: Optional[datetime.datetime] = dtime.now()
    is_active: Optional[bool] = True

