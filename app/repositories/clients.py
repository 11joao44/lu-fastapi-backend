from sqlalchemy.ext.asyncio import AsyncSession
from app.models.clients import ClientModel
from sqlalchemy.future import select
from pydantic import EmailStr

from app.schemas.clients import CreateClientSchema

class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, name: str):
        query = select(ClientModel).where(ClientModel.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_phone(self, phone: str):
        query = select(ClientModel).where(ClientModel.phone == phone)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_address(self, address: str):
        query = select(ClientModel).where(ClientModel.address == address)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_cpf_cnpj(self, cpf_cnpj: str):
        query = select(ClientModel).where(ClientModel.cpf_cnpj == cpf_cnpj)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: EmailStr):
        query = select(ClientModel).where(ClientModel.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, client: ClientModel) -> ClientModel:
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)
        return client
     
    async def update_client_repository(self, id: int, client: CreateClientSchema) -> ClientModel:
        result = await self.session.execute(select(ClientModel).where(ClientModel.id == id))
        db_client = result.scalar_one_or_none()

        if not db_client:
            return None

        for key, value in client.model_dump(exclude_unset=True).items():
            setattr(db_client, key, value)

        await self.session.commit()
        await self.session.refresh(db_client)

        return db_client

    async def get_by_id(self, id: str) -> ClientModel:
        query = select(ClientModel).where(ClientModel.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_client_all(self, name: str, email: EmailStr, limit: int = 10, offset: int = 0) -> list[ClientModel]:
        query = select(ClientModel)

        if name:
            query = select(ClientModel).where(ClientModel.name.ilike(f"%{name}%"))
        if email:
            query = select(ClientModel).where(ClientModel.email.ilike(f"%{email}%"))

        query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
        
    async def delete_client_repository(self, client: ClientModel):
        await self.session.delete(client)
        await self.session.commit()
