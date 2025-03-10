from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional


class InputModelCircuitDiode(BaseModel):
    vs:float = Field(..., gt=0, description="Fuente de Voltaje")
    r:float=Field(...,gt=0, description="Resistencia de carga")
    is1:float=Field(...,gt=0, description="Corriente de saturación en diodo 1")
    is2:float=Field(...,gt=0, description="Corriente de saturación en diodo 2")
    vt:float=Field(...,gt=0, description="Voltaje termico")
    i1_0:float = Field(...,description="supuesto para valor inicial en corriente i1")
    i2_0:float = Field(...,description="supuesto para valor inicial en corriente i2")
    vd_0:float = Field(...,description="supuesto para valor inicial en voltaje de diodo ")
    tolerance:float = Field(1e-6,gt=0,description="tolerancia")
    iter_max:int=Field(100,gt=0,description="Num maximo de iteraciones")
    historial:bool=Field(True, description="Almacenar historial")


class OutputModelCircuitDiode(BaseModel):
    i1:float=Field(...,description="Corriente en diodo 1")
    i2:float=Field(...,description="Corriente en diodo 2")
    vd:float=Field(...,description="Voltaje Diodo")
    iterations: int =Field(..., description="Numero de iteraciones")
    converged:bool=Field(..., description="Convergencia de la solucion")
    historial:Optional[List[Dict[str,Any]]]=Field(None, description="Historial de Iteraciones")


@field_validator('initial_values')
def check_initial_values_length(cls, v, values):
    if 'variables' in values.data and len(v) != len(values.data['variables']):
        raise ValueError("Length of initial_values must match length of variables")
    return v


@field_validator('equations')
def check_equations_length(cls, v, values):
    if 'variables' in values.data and len(v) < len(values.data['variables']):
        raise ValueError("Number of equations must be at least the number of variables")
    return v