from pydantic import BaseModel

class UserSchema(BaseModel):
    username : str
    password : str
    
class AddItemInCart(BaseModel):
    product_id : str
    itemcount : int
    
class DeleteItemFromCart(BaseModel):
    product_id : str