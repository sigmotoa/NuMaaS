import pytest
import numpy as np
from services.newton_raphson import NewtonRaphson, solve_diode_circuit


class TestNewtonRaphson:
    """Pruebas para el método Newton-Raphson multivariado."""

    def test_basic_system(self):
        """Prueba con un sistema de ecuaciones básico."""

        # Sistema: x^2 + y^2 = 4, x - y = 0
        # Solución esperada: (√2, √2) o (-√2, -√2)

        def system(x):
            return np.array([
                x[0] ** 2 + x[1] ** 2 - 4,  # x^2 + y^2 - 4 = 0
                x[0] - x[1]  # x - y = 0
            ])

        def jacobian(x):
            return np.array([
                [2 * x[0], 2 * x[1]],
                [1, -1]
            ])

        initial_guess = np.array([1.0, 1.0])
        solver = NewtonRaphson(system, jacobian)
        result = solver.solve(initial_guess)

        # Verificar convergencia
        assert solver.converged

        # Verificar resultado (esperamos aproximadamente √2 ≈ 1.414)
        assert abs(result[0] - np.sqrt(2)) < 1e-6
        assert abs(result[1] - np.sqrt(2)) < 1e-6

    def test_multiple_solutions(self):
        """Prueba con un sistema que tiene múltiples soluciones."""

        # El mismo sistema que antes, pero con punto inicial diferente

        def system(x):
            return np.array([
                x[0] ** 2 + x[1] ** 2 - 4,
                x[0] - x[1]
            ])

        def jacobian(x):
            return np.array([
                [2 * x[0], 2 * x[1]],
                [1, -1]
            ])

        initial_guess = np.array([-1.0, -1.0])
        solver = NewtonRaphson(system, jacobian)
        result = solver.solve(initial_guess)

        # Verificar convergencia
        assert solver.converged

        # Verificar resultado (esperamos aproximadamente -√2 ≈ -1.414)
        assert abs(result[0] + np.sqrt(2)) < 1e-6
        assert abs(result[1] + np.sqrt(2)) < 1e-6

    def test_no_convergence(self):
        """Prueba con un sistema que no converge dentro del límite de iteraciones."""

        def system(x):
            return np.array([
                np.tan(x[0]),  # Sistema difícil de converger
                x[1] - np.cos(10 * x[0])
            ])

        def jacobian(x):
            return np.array([
                [1.0 / np.cos(x[0]) ** 2, 0],
                [10 * np.sin(10 * x[0]), 1]
            ])

        initial_guess = np.array([1.0, 1.0])
        solver = NewtonRaphson(system, jacobian, max_iterations=5)  # Pocas iteraciones
        result = solver.solve(initial_guess)

        # Verificar que no converge
        assert not solver.converged

        # Verificar que se realizaron exactamente 5 iteraciones
        assert solver.iterations == 5

    def test_diode_circuit(self):
        """Prueba de resolución del circuito con diodos en paralelo."""
        # Parámetros del circuito
        Vs = 5.0  # Voltaje de la fuente (V)
        R = 1000.0  # Resistencia (Ohm)
        Is1 = 2e-12  # Corriente de saturación del diodo 1 (A)
        Is2 = 5e-12  # Corriente de saturación del diodo 2 (A)
        Vt = 0.02585  # Voltaje térmico (V)

        # Valores iniciales
        initial_values = np.array([0.021, 0.003, 0.7])  # I1, I2, VD

        # Resolver
        result, iterations, converged = solve_diode_circuit(
            Vs, R, Is1, Is2, Vt, initial_values
        )

        # Verificar convergencia
        assert converged

        # Verificar número de iteraciones (debería converger en pocas iteraciones)
        assert iterations <= 10

        # Verificar la coherencia física de los resultados
        I1, I2, VD = result

        # 1. Las corrientes deben ser positivas
        assert I1 > 0
        assert I2 > 0

        # 2. El voltaje del diodo debe estar en un rango razonable
        assert -1.0 < VD < 1.0

        # 3. La suma de las corrientes debe ser igual a la corriente a través de R
        assert abs(I1 + I2 - (Vs - VD) / R) < 1e-6

        # 4. Las corrientes deben seguir la ecuación del diodo
        assert abs(I1 - Is1 * (np.exp(VD / Vt) - 1)) < 1e-6
        assert abs(I2 - Is2 * (np.exp(VD / Vt) - 1)) < 1e-6