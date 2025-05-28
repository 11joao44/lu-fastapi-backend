from asyncio import get_event_loop
from .conftest import login
from typing import Dict
import pytest

# ======================================================================================
# FUNÇÃO: Realiza cadastro na API e valida status.
# ======================================================================================
def register(client, username: str, email: str, password: str, headers: Dict, expect_status: int):
    """Tenta registrar novo usuário e valida status."""
    body = {
        "username": username,
        "email": email,
        "password": password
    }
    response = client.post("/auth/register", json=body, headers=headers)
    assert response.status_code == expect_status
    return response


# ======================================================================================
# BLOCO AUXILIAR: Cria usuários direto no banco para preparar o teste.
# ======================================================================================
async def create_user_in_db(db_session, username, email, password, is_admin):
    """Cria usuário no banco direto (usado para seed do teste)."""
    from app.models.users import UserModel
    from app.services.users import UserService

    user = UserModel(
        username=username,
        email=email,
        hashed_password=UserService(None).hash_password(password),
        is_admin=is_admin,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


# ====================================================================================== #
# ------------- TESTE: Valida login bem-sucedido de usuário normal. -------------------- #
# ====================================================================================== #
@pytest.mark.asyncio
async def test_login(client, db_session):
    # ----------- PREPARAÇÃO: Cria usuário -----------
    await create_user_in_db(db_session, "login", "login@email.com", "login_user", is_admin=False)
    
    # ----------- Cenário 3: Login sucesso com usuário login -----------
    login(client, email="login@email.com", password="login_user", expect_status=200)


# ====================================================================================== #
# ---------- TESTE: Verifica tentativa de login com e-mail inexistente. ---------------- #
# ====================================================================================== #
@pytest.mark.asyncio
async def test_login_email_inexistente(client, db_session):
    # ----------- PREPARAÇÃO: Cria usuário normal (não admin) -----------
    await create_user_in_db(db_session, "normal", "normal@email.com", "normal_user", is_admin=False)

    # ----------- Cenário 1: Login com email inexistente -----------
    login(client, email="naoexiste@email.com", password="normal_user", expect_status=401)


# ====================================================================================== #
# ------------- TESTE: Verifica login com senha incorreta para usuário. ---------------- #
# ====================================================================================== #
@pytest.mark.asyncio
async def test_login_senha_errada(client, db_session):
    # ----------- PREPARAÇÃO: Cria usuário normal (não admin) -----------
    await create_user_in_db(db_session, "normal", "normal@email.com", "normal_user", is_admin=False)
    
    # ----------- Cenário 2: Login com senha errada -----------
    login(client, email="normal@email.com", password="errada", expect_status=401)


# ====================================================================================== #
# ------- TESTE: Usuário comum tenta registrar novo usuário (sem permissão). ----------- #
# ====================================================================================== #
@pytest.mark.asyncio
async def test_registrar_usuario_sem_admin(client, db_session):
    # ----------- PREPARAÇÃO: Cria usuário login (não admin) -----------
    await create_user_in_db(db_session, "normal", "normal@email.com", "normal_user", is_admin=False)
    
    # ----------- Cenário 3: Login sucesso com usuário normal -----------
    tk = login(client, email="normal@email.com", password="normal_user", expect_status=200)["token"]["access_token"]

    # ----------- Cenário 4: Tentar registrar usuário novo como user normal (espera 403) -----------
    register(client, "Usuário Tester", "tester@email.com", "admin@123456", {"Authorization": f"Bearer {tk}"}, expect_status=403)


# ====================================================================================== #
# ----- TESTE: Admin registra novo usuário e impede duplicidade de cadastro. ----------- #
# ====================================================================================== #
@pytest.mark.asyncio
async def test_registrar_usuario_com_admin(client, db_session):
    # ----------- PREPARAÇÃO: Cria usuário com admin -----------
    await create_user_in_db(db_session, "admin", "admin@email.com", "adminpass", is_admin=True)

    # ----------- Cenário 5: Login sucesso como admin -----------
    token = login(client, email="admin@email.com", password="adminpass", expect_status=200)["token"]["access_token"]

    headers = {"Authorization":f"Bearer {token}"}
    # ----------- Cenário 6: Registrar novo usuário com admin (espera 201) -----------
    response = register(client, "Usuário Tester", "tester@email.com", "admin@123456", headers, expect_status=201)
    data = response.json()
    assert data["username"] == "Usuário Tester"
    assert data["email"] == "tester@email.com"

    # ----------- Cenário 7: Registrar usuário duplicado (espera 409) -----------
    register(client, "Usuário Tester", "tester@email.com", "admin@123456", headers, expect_status=409)
    
    
# ====================================================================================== #
# ----------- TESTE: Admin não pode registrar um usuário com e-mail repetido. ---------- #
# ====================================================================================== #
@pytest.mark.asyncio
async def test_registrar_usuario_com_admin_duplicado(client, db_session):
    # ----------- PREPARAÇÃO: Cria usuário com admin -----------
    await create_user_in_db(db_session, "admin", "admin@email.com", "adminpass", is_admin=True)
    
    # ----------- Cenário 5: Login sucesso como admin -----------
    token = login(client, email="admin@email.com", password="adminpass", expect_status=200)["token"]["access_token"]
    
    # ----------- Cenário 7: Registrar usuário duplicado (espera 409) -----------
    register(client, "admin", "admin@email.com", "admin@123456", {"Authorization":f"Bearer {token}"}, expect_status=409)
