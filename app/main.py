from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.utils.logger import log_api_call
from app.routes import users, posts, search, auth_routes, logs ## Importing our route modules

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    ## Allowed origins, frontend during development, more when deploying.
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://idg2001-social-networking-service.onrender.com",
        "https://idg2001-o1-social-networking-service.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    log_api_call(request.method, request.url.path, response.status_code)
    return response

@app.get("/")
def read_root():
    return {"message": "Server is running."}

## Including the routers from other files.
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(logs.router, tags=["Logs"])

