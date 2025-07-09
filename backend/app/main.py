from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.api import routes

app = FastAPI(title="Spectron Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirect from root "/" to "/api"
@app.get("/", include_in_schema=False)
async def redirect_to_api():
    return RedirectResponse(url="/api")

app.include_router(routes.router, prefix="/api")