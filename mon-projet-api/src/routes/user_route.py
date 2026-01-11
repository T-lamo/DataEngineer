from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from src.conf.db.database import Database
from src.services.user_service import UserService
from src.models.user import User, UserBase, UserPatch, UserCreate,UserRead

# Création du routeur FastAPI
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Dépendance pour injecter le service
def get_user_service(session: Session = Depends(Database.get_session)) -> UserService:
    return UserService(session)

# -------------------------------
# GET /users - Liste tous les utilisateurs
# -------------------------------
@router.get("/", response_model=list[User])
def list_users(service: UserService = Depends(get_user_service)):
    return service.list_users()

# -------------------------------
# GET /users/{id} - Récupérer un utilisateur par ID
# -------------------------------
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# -------------------------------
# POST /users - Créer un nouvel utilisateur
# -------------------------------
@router.post("/", response_model=User)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.create_user(user)
    except ValueError as e:
        pass
        # raise HTTPException(status_code=400, detail=str(e))

# -------------------------------
# PATCH /users/{id} - Mettre à jour un utilisateur existant
# -------------------------------
@router.patch("/{user_id}", response_model=UserPatch)
def update_user(user_id: int, user_data: UserPatch, service: UserService = Depends(get_user_service)):
    try:
        return service.update_user(user_id, user_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# -------------------------------
# DELETE /users/{id} - Supprimer un utilisateur
# -------------------------------
@router.delete("/{user_id}")
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        service.delete_user(user_id)
        return {"detail": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
