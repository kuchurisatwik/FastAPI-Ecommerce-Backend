from sqlalchemy import Column, String, Integer,Float ,DateTime,text, ForeignKey,Enum as SqlEnum
from enum import Enum
from sqlalchemy.orm import Session,DeclarativeBase,relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Base(DeclarativeBase):
    pass


class ProductCategoryItems(str,Enum):
    ELECTRONICS = "electronics"
    FASHION = "fashion"
    BOOKS = "books"
    HOME = "home"
    TOYS  = "toys"


class OrderStatusChoice(str,Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    FAILED = "Failed"

class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class UserRole(str,Enum):
    ADMIN = "admin"
    USER = "user"


# class RolesToSelect(Emun):

    

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,nullable = False,primary_key = True)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False, unique = True)
    
    role = Column(SqlEnum(UserRole))

    created_at = Column(TIMESTAMP(timezone = True),
                        nullable = False, server_default = text('now()'))
    orders = relationship("Order",back_populates = "user")
    


class Products(Base):
    __tablename__ =  "products"
    id = Column(Integer,nullable = False,primary_key = True)
    name  = Column(String, nullable = False, unique = True)
    description = Column(String, nullable = True)
    price = Column(Float, nullable = False, default = 0.0)
    
    stock  = Column(Integer, nullable= False)  # IMP must decrement, whenever the orders are created on orders table

    category = Column(SqlEnum(ProductCategoryItems),nullable = False) #It's a list of elements to choose for filtering and more.

    created_at  = Column(TIMESTAMP(timezone =  True)
                         ,nullable = False, server_default=text("now()"))
    order_items = relationship("OrderItems", back_populates = "product")



class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer,primary_key = True,nullable  = False)
    user_id = Column(Integer,ForeignKey(
        "users.id"),nullable = False)
    status = Column(SqlEnum(OrderStatusChoice),default = OrderStatusChoice.PENDING,nullable= False) 

    created_at  = Column(TIMESTAMP(timezone =  True)
                         ,nullable = False, server_default=text("now()"))
    
    

    user  = relationship("User",back_populates = "orders")
    order_items = relationship("OrderItems",back_populates ="order",cascade = "all, delete-orphan" )
    payments = relationship("Payment",back_populates = "order",cascade = "all, delete-orphan")
    @property
    def total_price(self) -> float:
        return sum(item.quantity * item.product.price for item in self.order_items)
    

    
    #I guess to create multiple products one order, we need to update our pydantic schemas to list format.

class OrderItems(Base):
    __tablename__ = "order_items"
    id = Column(Integer,primary_key = True)
    order_id = Column(Integer, ForeignKey(
        "orders.id",ondelete = "CASCADE"),
        nullable = False
        )
    product_id = Column(Integer, ForeignKey(
        "products.id",ondelete  = "CASCADE"),
        nullable = False
        )     
    quantity  = Column(Integer, nullable = False, default = 1)
    price  = Column(Float, nullable  = False, default = 0.00)
    

    order = relationship("Order",back_populates = "order_items")
    product = relationship("Products", back_populates = "order_items")
    

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer,primary_key = True)
    order_id = Column(Integer, ForeignKey(
        "orders.id",ondelete = "CASCADE"),
        nullable = False
    )
    # status = Column(choice)
    amount = Column(Float, nullable = False)
    status = Column(SqlEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    payment_method = Column(String, nullable=True)  # CARD, UPI, COD
    created_at  = Column(TIMESTAMP(timezone =  True)
                         ,nullable = False, server_default=text("now()"))

    order = relationship("Order", back_populates="payments")