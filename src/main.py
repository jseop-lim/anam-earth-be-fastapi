from fastapi import FastAPI

from config import Settings
from containers import Container
from map_admin.presentation import apis as map_admin_apis

container = Container()
container.config.from_dict(Settings().model_dump())
container.wire(
    modules=[
        map_admin_apis,
    ],
)

app = FastAPI()
app.include_router(map_admin_apis.router)
