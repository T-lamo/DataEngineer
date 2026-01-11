from typing import List, Optional
from sqlmodel import Session, select
from src.conf.db.database import Database
from src.models.tag import Tag, TagPatch


class TagRepository:

    @staticmethod
    def get_all_tags() -> List[Tag]:
        """Récupérer tous les tags"""
        with Session(Database.get_engine()) as session:
            statement = select(Tag)
            return session.exec(statement).all()

    @staticmethod
    def get_tag_by_id(tag_id: int) -> Optional[Tag]:
        """Récupérer un tag par son ID"""
        with Session(Database.get_engine()) as session:
            return session.get(Tag, tag_id)

    @staticmethod
    def get_tag_by_name(name: str) -> Optional[Tag]:
        """Récupérer un tag par son nom"""
        with Session(Database.get_engine()) as session:
            statement = select(Tag).where(Tag.name == name)
            return session.exec(statement).first()

    @staticmethod
    def create_tag(tag: Tag) -> Tag:
        """Créer un nouveau tag"""
        with Session(Database.get_engine()) as session:
            # Vérifier si un tag avec le même nom existe déjà
            existing = TagRepository.get_tag_by_name(tag.name)
            if existing:
                raise ValueError(f"Tag with name '{tag.name}' already exists")
            session.add(tag)
            session.commit()
            session.refresh(tag)
            return tag

    @staticmethod
    def update_tag(tag_id: int, updated_tag: TagPatch) -> Optional[Tag]:
        """Mettre à jour un tag existant"""
        with Session(Database.get_engine()) as session:
            tag = session.get(Tag, tag_id)
            if not tag:
                return None
            if updated_tag.name is not None:
                tag.name = updated_tag.name
            session.add(tag)
            session.commit()
            session.refresh(tag)
            return tag

    @staticmethod
    def delete_tag(tag_id: int) -> bool:
        """Supprimer un tag par ID"""
        with Session(Database.get_engine()) as session:
            tag = session.get(Tag, tag_id)
            if not tag:
                return False
            session.delete(tag)
            session.commit()
            return True
