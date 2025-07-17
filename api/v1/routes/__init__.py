from fastapi import APIRouter

from api.v1.routes.auth import auth
from api.v1.routes.user import user
from api.v1.routes.group import group
from api.v1.routes.messaging import message
from api.v1.routes.event import event
from api.v1.routes.rsvp import rsvp_router
from api.v1.routes.categories import router as router



api_version_one = APIRouter(prefix="/api/v1")
api_version_one.include_router(auth)
api_version_one.include_router(user)
api_version_one.include_router(group)
api_version_one.include_router(message)
api_version_one.include_router(event)
api_version_one.include_router(rsvp_router)
api_version_one.include_router(router)
