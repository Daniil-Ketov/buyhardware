from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.config import db
from app.service.auth_service import generate_role


origins = ["http://localhost:3000"]


def init_app():
    db.init()

    app = FastAPI(
        title="buyhardware",
        description="Buy hardware",
        version="1"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()
        await generate_role()

    @app.on_event("shutdown")
    async def shutdown():
        await db.close()

    from app.controller import authentication, users, hardware, orders, status_changes, hardware_orders, contracts

    app.include_router(authentication.router)
    app.include_router(users.router)
    app.include_router(hardware.router)
    app.include_router(orders.router)
    app.include_router(status_changes.router)
    app.include_router(hardware_orders.router)
    app.include_router(contracts.router)

    return app


app = init_app()


def start():
    """ Launched with 'poetry run start' at root level """
    uvicorn.run("app.main:app", host="localhost", port=8888, reload=True)
