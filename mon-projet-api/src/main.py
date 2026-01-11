from fastapi import FastAPI
from src.conf.db.database import Database

from src.conf.db.settings import settings
from src.routes.user_route import router as user_router
from src.routes.ticket_router import router as ticket_router    
from src.routes.tag_router import router as tag_router

print(settings.DB_USER)
print(settings.DB_PASSWORD)

app = FastAPI()
app.include_router(user_router)
app.include_router(ticket_router)
app.include_router(tag_router)


@app.on_event("startup")
def on_startup():
    Database.init_db()
    #Database.recreate_db()
    print("Application has started")




@app.get("/health")
async def health_check():
    """
    Crée un nouvel utilisateur.

    Le corps de la requête (payload) doit contenir :
    - email
    - full_name
    - age
    - is_active (optionnel)
    """
    return {"status": "ok"}