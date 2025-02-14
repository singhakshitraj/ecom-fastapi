from fastapi import FastAPI
from .routers import auth,products,cart,checkout,admin
instance = FastAPI()

instance.include_router(auth.router)
instance.include_router(products.router)
instance.include_router(cart.router)
instance.include_router(checkout.router)
instance.include_router(admin.router)
@instance.get('/')
def get():
    return {
        'message':'Here'
    }