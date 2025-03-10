from fastapi import FastAPI, Request, HTTPException, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import numpy as np
import os
from typing import List, Optional
from schemas import (InputModelCircuitDiode,OutputModelCircuitDiode)
from services.newton_raphson import *

app = FastAPI(
    title="NuMaaS - Numerical Methods as a Software",
    description="the first Numerical Methods as a Software development",
    version="0.0.1"
)

templates_dir=os.path.join(os.path.dirname(__file__),"templates")
templates = Jinja2Templates(directory=templates_dir)

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(
        request=request,name= "home.html"
    )


@app.post("/api/diode-circuit")
async def calculate_diode_circuit(
        vs: float = Form(...),
        r: float = Form(...),
        is1: float = Form(...),
        is2: float = Form(...),
        vt: float = Form(...),
        i1_0: float = Form(...),
        i2_0: float = Form(...),
        vd_0: float = Form(...),
        tolerance: float = Form(...),
        iter_max: int = Form(...),
        historial: bool = Form(...)
):

    try:
        # Validar entrada usando el modelo Pydantic
        input_data = InputModelCircuitDiode(
            vs=vs,
            r=r,
            is1=is1,
            is2=is2,
            vt=vt,
            i1_0=i1_0,
            i2_0=i2_0,
            vd_0=vd_0,
            tolerance=tolerance,
            iter_max=iter_max,
            historial=historial
        )

        # Preparar valores iniciales
        initial_values = np.array([input_data.i1_0, input_data.i2_0, input_data.vd_0])

        # Resolver el circuito
        result, iterations, converged = solve_diode_circuit(
            input_data.vs,
            input_data.r,
            input_data.is1,
            input_data.is2,
            input_data.vt,
            initial_values,
            input_data.tolerance,
            input_data.iter_max,
            input_data.historial
        )

        # Extraer resultados
        i1, i2, vd = result

        # Preparar historial si se solicitó
        historial_data = None
        if input_data.historial and isinstance(solve_diode_circuit.__globals__['NewtonRaphson'], type):
            solver = solve_diode_circuit.__globals__.get('solver', None)
            if hasattr(solver, 'history') and solver.history:
                historial_data = []
                for item in solver.history:
                    historial_data.append({
                        "iteracion": item['iteration'],
                        "i1": float(item['x'][0]),
                        "i2": float(item['x'][1]),
                        "vd": float(item['x'][2]),
                        "distancia": float(item.get('distance', 0))
                    })

        # Crear objeto de respuesta
        output_data = OutputModelCircuitDiode(
            i1=float(i1),
            i2=float(i2),
            vd=float(vd),
            iterations=iterations,
            converged=converged,
            historial=historial_data
        )

        return output_data.dict()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el cálculo: {str(e)}")



