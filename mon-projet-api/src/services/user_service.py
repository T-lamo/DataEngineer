from sqlmodel import Session
from src.models.user import User, UserCreate, UserPatch, UserBase, UserRead
from fastapi import HTTPException, status


from src.repositories.user_repository import UserRepository
from src.utils.security import hash_password , verify_password # Hypothetical utility for password hashing

class UserService:
    def __init__(self, session: Session):
        # On passe la session à la couche repository
        self.repo = UserRepository()
        self.session = session

    def list_users(self) -> list[User]:
        """Récupérer tous les utilisateurs"""
        with self.session as session:
            return self.repo.get_all_users()

    def get_user_by_id(self, user_id: int) -> UserRead:
        """Récupérer un utilisateur par ID"""
        with self.session as session:
            user = self.repo.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Utilisateur non trouvé"
                )
            return user


    def get_user_by_email(self, email: str) -> UserRead | None:
        """Récupérer un utilisateur par email"""
        with self.session as session:
            return self.repo.get_user_by_email(email)

    def create_user(self, user_data: UserCreate) -> User:
        """Créer un nouvel utilisateur"""
        with self.session as session:
            # Vérifier si l'utilisateur existe déjà par email
            existing = self.repo.get_user_by_email(user_data.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists"
                )
            hash_password(user_data.password)  
            user = User(
                email=user_data.email,
                firstname=user_data.firstname,
                lastname=user_data.lastname,
                age=user_data.age,
                password=hash_password(user_data.password),
                is_active=user_data.is_active,
            )
            return self.repo.create_user(user)

    def update_user(self, user_id: int, user_data: UserBase) -> UserBase | None:
        """Mettre à jour un utilisateur existant"""
        with self.session as session:
            updated = self.repo.update_user(user_id, user_data)
            if not updated:
                raise ValueError("User not found")
            return updated

    def delete_user(self, user_id: int) -> bool:
        """Supprimer un utilisateur par ID"""
        with self.session as session:
            success = self.repo.delete_user(user_id)
            if not success:
                raise ValueError("User not found")
            return True
