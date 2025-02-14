from pydantic import BaseModel

class addProduct(BaseModel):
    name : str
    product_category_id : int
    price : float
    available_items : int

class deleteProduct(BaseModel):
    id : str
    
class addSuperUserValidation(BaseModel):
    username : str