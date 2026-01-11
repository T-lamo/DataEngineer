from src.conf.db.database import Database
from src.models.user import User, UserCreate
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload


class UserRepository:
    @staticmethod
    def get_all_users() -> list[User]:
        """Récupérer tous les utilisateurs"""
        with Session(Database.get_engine()) as session:
            statement = select(User).options(selectinload(User.tickets))
            return session.exec(statement).all()

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        """Récupérer un utilisateur par son ID"""
        with Session(Database.get_engine()) as session:
            print("user id in repo",user_id, type(user_id))
            return session.get(User, user_id)

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        """Récupérer un utilisateur par son email"""
        with Session(Database.get_engine()) as session:
            statement = select(User).where(User.email == email)
            return session.exec(statement).first()

    @staticmethod
    def create_user(user: User) -> User:
        """Créer un nouvel utilisateur"""
        with Session(Database.get_engine()) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    @staticmethod
    def update_user(user_id: int, updated_user: User) -> User | None:
        """Mettre à jour un utilisateur existant"""
        with Session(Database.get_engine()) as session:
            user = session.get(User, user_id)
            if not user:
                return None
            # Mettre à jour les champs
            user.email = updated_user.email
            user.firstname = updated_user.firstname
            user.lastname = updated_user.lastname
            user.is_active = updated_user.is_active
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Supprimer un utilisateur par ID"""
        with Session(Database.get_engine()) as session:
            user = session.get(User, user_id)
            if not user:
                return False
            session.delete(user)
            session.commit()
            return True
