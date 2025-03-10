import numpy as np
from typing import Callable, Tuple, List, Dict, Any, Optional, Union


class NewtonRaphson:
    """
    Implementación del método Newton-Raphson para sistemas de ecuaciones no lineales.

    Atributos:
        system (Callable): Función que define el sistema de ecuaciones F(x) = 0.
        jacobian (Callable): Función que calcula la matriz jacobiana del sistema.
        tolerance (float): Tolerancia para la convergencia.
        max_iterations (int): Número máximo de iteraciones permitidas.
        iterations (int): Número de iteraciones realizadas.
        converged (bool): Indica si el método ha convergido.
        history (List): Historial de iteraciones para análisis.
    """

    def __init__(
            self,
            system: Callable[[np.ndarray], np.ndarray],
            jacobian: Callable[[np.ndarray], np.ndarray],
            tolerance: float = 1e-6,
            max_iterations: int = 100,
    ):
        """
        Inicializa el solucionador Newton-Raphson.

        Args:
            system: Función que devuelve el valor del sistema para un vector x.
            jacobian: Función que devuelve la matriz jacobiana para un vector x.
            tolerance: Tolerancia para determinar la convergencia.
            max_iterations: Número máximo de iteraciones permitidas.
        """
        self.system = system
        self.jacobian = jacobian
        self.tolerance = tolerance
        self.max_iterations = max_iterations

        # Estado
        self.iterations = 0
        self.converged = False
        self.history = []

    def solve(
            self,
            initial_guess: np.ndarray,
            store_history: bool = False
    ) -> np.ndarray:
        """
        Resuelve el sistema de ecuaciones utilizando el método Newton-Raphson.

        Args:
            initial_guess: Vector de valores iniciales.
            store_history: Si es True, almacena el historial de iteraciones.

        Returns:
            np.ndarray: Vector solución del sistema.
        """
        x = initial_guess.copy()
        self.iterations = 0
        self.converged = False
        self.history = []

        if store_history:
            self.history.append({
                'iteration': 0,
                'x': x.copy(),
                'f': self.system(x),
                'distance': float('inf')
            })

        for i in range(self.max_iterations):
            # Calcular F(x) y J(x)
            f = self.system(x)
            J = self.jacobian(x)

            # Resolver el sistema J * delta_x = -f
            try:
                delta_x = np.linalg.solve(J, -f)
            except np.linalg.LinAlgError:
                # Si la matriz es singular, intentamos usar pseudo-inversa
                delta_x = -np.linalg.pinv(J) @ f

            # Actualizar x
            x = x + delta_x

            # Calcular la distancia euclidiana
            distance = np.linalg.norm(delta_x)

            # Guardar historial si se solicita
            if store_history:
                self.history.append({
                    'iteration': i + 1,
                    'x': x.copy(),
                    'f': self.system(x),
                    'distance': distance,
                    'delta_x': delta_x
                })

            # Verificar convergencia
            if distance < self.tolerance:
                self.converged = True
                break

            self.iterations += 1

        return x

    def get_history_df(self):
        """
        Convierte el historial de iteraciones a un DataFrame para análisis.

        Returns:
            DataFrame o None: DataFrame con el historial si está disponible.
        """
        if not self.history:
            return None

        try:
            import pandas as pd

            # Extraer datos
            data = []
            for item in self.history:
                row = {'iteration': item['iteration'], 'distance': item['distance']}

                # Añadir cada variable
                for i, val in enumerate(item['x']):
                    row[f'x{i + 1}'] = val

                # Añadir cada función
                for i, val in enumerate(item['f']):
                    row[f'f{i + 1}'] = val

                data.append(row)

            return pd.DataFrame(data)

        except ImportError:
            print("Pandas no está instalado. No se puede crear DataFrame.")
            return None


def solve_diode_circuit(
        Vs: float,
        R: float,
        Is1: float,
        Is2: float,
        Vt: float,
        initial_values: np.ndarray,
        tolerance: float = 1e-6,
        max_iterations: int = 100,
        store_history: bool = False
) -> Tuple[np.ndarray, int, bool]:
    """
    Resuelve el circuito con diodos en paralelo utilizando Newton-Raphson.

    Args:
        Vs: Voltaje de la fuente (V)
        R: Resistencia (Ohm)
        Is1: Corriente de saturación del diodo 1 (A)
        Is2: Corriente de saturación del diodo 2 (A)
        Vt: Voltaje térmico (V)
        initial_values: Vector de valores iniciales [I1, I2, VD]
        tolerance: Tolerancia para la convergencia
        max_iterations: Número máximo de iteraciones
        store_history: Si es True, almacena el historial de iteraciones

    Returns:
        Tuple con [I1, I2, VD], número de iteraciones y estado de convergencia
    """

    # Definir el sistema de ecuaciones
    def system(x):
        I1, I2, VD = x
        return np.array([
            I1 + I2 - (Vs - VD) / R,  # Ecuación de corriente de Kirchhoff
            I1 - Is1 * (np.exp(VD / Vt) - 1),  # Ecuación del diodo 1
            I2 - Is2 * (np.exp(VD / Vt) - 1)  # Ecuación del diodo 2
        ])

    # Definir la matriz jacobiana
    def jacobian(x):
        I1, I2, VD = x
        return np.array([
            [1, 1, 1 / R],
            [1, 0, -Is1 / Vt * np.exp(VD / Vt)],
            [0, 1, -Is2 / Vt * np.exp(VD / Vt)]
        ])

    # Crear y ejecutar el solucionador
    solver = NewtonRaphson(system, jacobian, tolerance, max_iterations)
    result = solver.solve(initial_values, store_history)

    return result, solver.iterations, solver.converged


def parse_and_solve_system(
        variables: List[str],
        ecuaciones: List[str],
        valores_iniciales: List[float],
        tolerancia: float = 1e-6,
        max_iteraciones: int = 100
) -> Dict[str, Any]:
    """
    Parsea y resuelve un sistema de ecuaciones definido como strings.

    Args:
        variables: Lista de nombres de variables
        ecuaciones: Lista de ecuaciones como strings
        valores_iniciales: Lista de valores iniciales
        tolerancia: Tolerancia para la convergencia
        max_iteraciones: Número máximo de iteraciones

    Returns:
        Dict con la solución, iteraciones y estado de convergencia
    """
    import sympy as sp
    import numpy as np

    # Crear símbolos para las variables
    symbols = sp.symbols(variables)

    # Convertir ecuaciones a expresiones simbólicas
    expr_list = [sp.sympify(eq) for eq in ecuaciones]

    # Crear función lambda para el sistema
    system_lambda = sp.lambdify(symbols, expr_list, 'numpy')

    # Calcular jacobiano simbólico
    jacobian_matrix = sp.Matrix([[sp.diff(expr, var) for var in symbols] for expr in expr_list])
    jacobian_lambda = sp.lambdify(symbols, jacobian_matrix, 'numpy')

    # Adaptar a la interfaz esperada por NewtonRaphson
    def system(x):
        return np.array(system_lambda(*x), dtype=float)

    def jacobian(x):
        return np.array(jacobian_lambda(*x), dtype=float)

    # Resolver usando Newton-Raphson
    solver = NewtonRaphson(system, jacobian, tolerancia, max_iteraciones)
    result = solver.solve(np.array(valores_iniciales, dtype=float), store_history=True)

    # Preparar resultados
    solution_dict = {var: float(val) for var, val in zip(variables, result)}

    # Historia de iteraciones
    iterations_data = []
    for i, item in enumerate(solver.history):
        iter_data = {"iteracion": i}
        for j, var in enumerate(variables):
            iter_data[var] = float(item['x'][j])
        if i > 0:
            iter_data["distancia"] = float(item['distance'])
        iterations_data.append(iter_data)

    return {
        "solucion": solution_dict,
        "iteraciones": solver.iterations,
        "convergencia": solver.converged,
        "historia": iterations_data
    }