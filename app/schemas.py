from pydantic import BaseModel,Field,EmailStr
from datetime import datetime
from typing import Annotated, List
from enum import Enum

basemodel = BaseModel

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class ProductCategoryItems(str, Enum):
    ELECTRONICS = "electronics"
    FASHION = "fashion"
    BOOKS = "books"
    HOME = "home"
    TOYS  = "toys"

class OrderStatusChoice(str,Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    FAILED = "Failed"



# followed by client
class CreateUser(basemodel):
    email :  Annotated[EmailStr,Field(...)]
    password :  Annotated[str,Field(...,min_length = 8,max_length  = 20)]
    role: UserRole 

class CreateProduct(basemodel):  
    name: str
    description: str
    price: float
    stock : int
    category : ProductCategoryItems


class CreateOrder(basemodel):
    user_id :  int


class CreateOrderItems(basemodel):
    order_id: int
    product_id : int
    quantity : Annotated[int,Field(...,gt=0)]

class DeleteOrderItems(basemodel):
    order_id : int
    product_id: int


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class CreatePayment(BaseModel):
    order_id: int
    amount: float
    payment_method: str












# followed by API for Response to users(RESPONSE_MODELS)
class ResToUser(basemodel):
    id : int
    email:EmailStr
    role: UserRole 
    created_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

class ResToProducts(basemodel):
    
    id :int
    name : str
    description :str
    price :float
    stock  : int
    category : ProductCategoryItems
    created_at  : datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True

class ResToOrderItems(basemodel):
    id: int
    quantity: int
    price: float
    product: ResToProducts

    class Config:
        from_attributes = True

class ResToOrders(basemodel):

    id: int
    user_id: int
    status: OrderStatusChoice
    created_at: datetime
    total_price : float
    order_items: List[ResToOrderItems]


    class Config:
        from_attributes = True
        use_enum_values = True
        arbitrary_types_allowed = True

class ResOrderItems(basemodel):
    id: int
    order_id: int
    product_id : int
    quantity : int
    price: float


    class Config:
        from_attributes = True



class ResPayment(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    status: PaymentStatus

    class Config:
        orm_mode = True

class Token(basemodel):
    access_token: str
    token_type: str

class TokenData(basemodel):
    email: str | None = None

class LoginUser(basemodel):
    email: EmailStr
    password: str
