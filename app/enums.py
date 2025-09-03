from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class ProductCategoryItems(str, Enum):
    ELECTRONICS = "Electronics"
    FASHION = "Fashion"
    BOOKS = "Books"
    HOME = "Home"
    TOYS  = "Toys"