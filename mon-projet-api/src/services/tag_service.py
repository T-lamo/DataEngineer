from typing import List
from sqlmodel import Session
from fastapi import HTTPException, status

from src.models.tag import Tag, TagPatch, TagBase
from src.repositories.tag_repository import TagRepository


class TagService:
    def __init__(self, session: Session):
        self.repo = TagRepository()
        self.session = session

    def list_tags(self) -> List[Tag]:
        """Récupérer tous les tags"""
        with self.session as session:
            return self.repo.get_all_tags()

    def get_tag_by_id(self, tag_id: int) -> Tag:
        """Récupérer un tag par son ID"""
        with self.session as session:
            tag = self.repo.get_tag_by_id(tag_id)
            if not tag:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with ID {tag_id} not found"
                )
            return tag

    def get_tag_by_name(self, name: str) -> Tag | None:
        """Récupérer un tag par son nom"""
        with self.session as session:
            return self.repo.get_tag_by_name(name)

    def create_tag(self, tag_data: TagBase) -> Tag:
        """Créer un nouveau tag"""
        with self.session as session:
            # Vérifier si le tag existe déjà
            existing = self.repo.get_tag_by_name(tag_data.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Tag with name '{tag_data.name}' already exists"
                )

            # Créer le tag
            tag = Tag(name=tag_data.name)
            return self.repo.create_tag(tag)

    def update_tag(self, tag_id: int, tag_data: TagPatch) -> Tag:
        """Mettre à jour un tag existant"""
        with self.session as session:
            # Vérifier que le tag existe
            tag = self.repo.get_tag_by_id(tag_id)
            if not tag:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with ID {tag_id} not found"
                )

            # Si le nouveau nom est fourni, vérifier qu’il n’existe pas déjà
            if tag_data.name and tag_data.name != tag.name:
                existing = self.repo.get_tag_by_name(tag_data.name)
                if existing:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Tag with name '{tag_data.name}' already exists"
                    )

            # Mise à jour partielle
            updated_tag = self.repo.update_tag(tag_id, tag_data)
            return updated_tag

    def delete_tag(self, tag_id: int) -> bool:
        """Supprimer un tag par ID"""
        with self.session as session:
            success = self.repo.delete_tag(tag_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tag with ID {tag_id} not found"
                )
            return True
