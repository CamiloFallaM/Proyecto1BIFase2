from typing import Optional

from fastapi import FastAPI

from DataModel import DataModel

from FinalModel import Modelo

app = FastAPI()


@app.post("/predict/")
def predict(dataModel: DataModel):
   modelo = Modelo()
   resp = modelo.predict(dataModel.descripcion)
   return resp


