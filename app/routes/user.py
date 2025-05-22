from datetime import datetime
from fastapi import FastAPI
from http import HTTPStatus

from app.schemas.user import UserSchema, UserOut, UserRegister

def users_routes(router: FastAPI) -> None:

    @router.get('/users', status_code=HTTPStatus.OK)
    def users(user: UserSchema):
        return user
    
    @router.post('/users', status_code=HTTPStatus.CREATED, response_model=UserOut)
    def users(user: UserRegister):
        return UserOut( id=1, username=user.username, email=user.email, is_active=True, is_admin=False, created_in=datetime.now(), updated_in=None )
    
    @router.put('/users', status_code=HTTPStatus.OK)
    def users(user: UserSchema):
        return user
    
    @router.delete('/users', status_code=HTTPStatus.NO_CONTENT)
    def users(user: UserSchema):
        return user