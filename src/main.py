from fastapi import FastAPI

from containers import Container
from map_admin.presentation import apis as map_admin_apis
from settings import Settings

container = Container()
container.config.from_dict(Settings().model_dump())
container.wire(
    modules=[
        map_admin_apis,
    ],
)

app = FastAPI()
app.include_router(map_admin_apis.router)
