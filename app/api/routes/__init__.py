from fastapi import APIRouter

from app.api.routes import auth, interview, jobs, users, analysis

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(jobs.router)
api_router.include_router(users.router)
api_router.include_router(interview.router)
api_router.include_router(analysis.router)
