from fastapi import APIRouter
from .admins import products,user

router = APIRouter(
    prefix='/admin',
    tags=['Admin-Panel']
)

router.include_router(products.product_router)
router.include_router(user.router)
""" 
@router.post('/addsuperuser')
def addSuperUser():
    pass

@router.post('/addproduct')
def addProduct():
    pass


to_implement = '''
    users - view,edit and delete, 
            see order_details, payment_details
    superuser - change status
    create database on startup
''' """