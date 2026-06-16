from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import agirlik, disli, kesme, oring, kama

app = FastAPI(title="Mühendis Portal API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agirlik.router, prefix="/api/agirlik", tags=["Ağırlık"])
app.include_router(disli.router,   prefix="/api/disli",   tags=["Dişli"])
app.include_router(kesme.router,   prefix="/api/kesme",   tags=["Kesme"])
app.include_router(oring.router,   prefix="/api/oring",   tags=["O-Ring"])
app.include_router(kama.router,    prefix="/api/kama",    tags=["Kama"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Mühendis Portal API çalışıyor."}
