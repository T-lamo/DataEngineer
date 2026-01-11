from typing import List
from fastapi import APIRouter, Depends, Path, status
from sqlmodel import Session

from src.conf.db.database import Database
from src.models.tag import Tag, TagBase, TagPatch
from src.services.tag_service import TagService

router = APIRouter(prefix="/tags", tags=["tags"])


# ---------------------------
# Dépendance pour le service
# ---------------------------
def get_tag_service() -> TagService:
    session = Session(Database.get_engine())
    return TagService(session)


# ---------------------------
# GET /tags
# ---------------------------
@router.get("/", response_model=List[Tag])
def list_tags(service: TagService = Depends(get_tag_service)):
    """
    Récupérer tous les tags
    """
    return service.list_tags()


# ---------------------------
# GET /tags/{tag_id}
# ---------------------------
@router.get("/{tag_id}", response_model=Tag)
def get_tag(
    tag_id: int = Path(..., gt=0),
    service: TagService = Depends(get_tag_service)
):
    """
    Récupérer un tag par ID
    """
    return service.get_tag_by_id(tag_id)


# ---------------------------
# POST /tags
# ---------------------------
@router.post("/", response_model=Tag, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_data: TagBase,
    service: TagService = Depends(get_tag_service)
):
    """
    Créer un nouveau tag
    """
    print("tag data",tag_data)
    return service.create_tag(tag_data)


# ---------------------------
# PATCH /tags/{tag_id}
# ---------------------------
@router.patch("/{tag_id}", response_model=TagPatch)
def update_tag(
    tag_id: int = Path(..., gt=0),
    tag_patch: TagPatch = ...,
    service: TagService = Depends(get_tag_service)
):
    """
    Mettre à jour partiellement un tag
    """
    return service.update_tag(tag_id, tag_patch)


# ---------------------------
# DELETE /tags/{tag_id}
# ---------------------------
@router.delete("/{tag_id}", status_code=status.HTTP_200_OK)
def delete_tag(
    tag_id: int = Path(..., gt=0),
    service: TagService = Depends(get_tag_service)
):
    """
    Supprimer un tag par ID
    """
    success = service.delete_tag(tag_id)
    return {"ok": success}
