from fastapi import FastAPI

from app.service.map import MapService

app = FastAPI()


@app.post("/fillMap")
def fill_map():
    MapService().fill_map()
    return {}


@app.post("/resetMap")
def reset_map():
    MapService().reset_map()
    return {}
