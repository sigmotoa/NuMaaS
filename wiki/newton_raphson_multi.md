## Introducción
Los métodos numéricos para la solución de sistemas de ecuaciones no lineales multivariados 
permiten resolver problemas donde las ecuaciones no pueden despejarse de manera analítica. 

El ideal es a través de aproximaciones iterativas (lograr) la convergencia de soluciones precisas
con una tolerancia o de error aceptables.

En el siguiente ejemplo/ejercicio se ilustra, el método Newton-Raphson multivariado.

## Planteamiento del Problema

## **Análisis de un Circuito con Diodos en Paralelo**

# Aquí imagen del circuito

## **Contexto Industrial**
Algunas industrias requieren ofrecer sus servicios con disponibilidades 24/7,
centros de datos, telecomunicaciones, atención de salud.
Es común utilizar fuentes de alimentación redundantes en estas industrias
para garantizar un suministro continuo de energía.

En estos sistemas, los diodos en paralelo permiten:

✅ Compartir la carga entre fuentes de alimentación.
✅ Evitar flujo inverso de corriente.
✅ Proteger la carga en caso de falla de una fuente.

Para modelar este circuito, se usa la ecuación de Shockley para los diodos:

$$ I = I_s \left( e^{V_D / V_T} - 1 \right) $$

## **Planteamiento del Problema**
El circuito consta de dos fuentes redundantes de 5V,
protegidas por dos diodos en paralelo antes de alimentar una carga de 1kΩ. 
Los parámetros del sistema son:

- **Voltaje de la fuente:** $V_s = 5V $
- **Resistencia de carga:** $ R = 1kΩ $
- **Diodo 1:** $I_{s1} = 2 \times 10^{-12} A$
- **Diodo 2:** $I_{s2} = 5 \times 10^{-12} A $
- **Voltaje térmico:** $V_T = 25.85mV$


---

## **Desarrollo del Método Newton-Raphson Multivariado**

En el presente ejemplo se proponen 8 pasos para el desarrollo. Al llegar al paso 8, será necesario evaluar y definir si 
se termina la ejecución el método, o si se itera desde el paso 4. 

### **Definir las ecuaciones**
Las ecuaciones del sistema se plantean en términos de las corrientes $I_1, I_2$ y el de voltaje de diodo $V_D$:

$$ I_1 = I_{s1} \left( e^{V_D / V_T} - 1 \right) $$
$$ I_2 = I_{s2} \left( e^{V_D / V_T} - 1 \right) $$
$$ I_1 + I_2 = \frac{V_s - V_D}{R} $$

### Paso 1: Construcción de la Matriz Jacobiana

Las ecuaciones del sistema se expresan como:

1. Ley de Kirchhoff de corrientes:
   
   $$   I_1 + I_2 - \frac{V_s - V_D}{R} = 0 $$
   

2. Característica del primer diodo:
   
   $$
   I_1 - I_{s1} \left( e^{V_D / V_T} - 1 \right) = 0
   $$

3. Característica del segundo diodo:
   
   $$
   I_2 - I_{s2} \left( e^{V_D / V_T} - 1 \right) = 0
   $$

Expresando en la forma  $F(x) = 0$:

$$
F_1(I_1, I_2, V_D) = I_1 + I_2 - \frac{V_s - V_D}{R} $$
$$
F_2(I_1, I_2, V_D) = I_1 - I_{s1} e^{V_D / V_T} + I_{s1}$$
$$
F_3(I_1, I_2, V_D) = I_2 - I_{s2} e^{V_D / V_T} + I_{s2}
$$

La matriz jacobiana \( J \) del sistema:

$$ J = \begin{bmatrix}
\frac{\partial f_1}{\partial I_1} & \frac{\partial f_1}{\partial I_2} & \frac{\partial f_1}{\partial V_D} \\
\frac{\partial f_2}{\partial I_1} & \frac{\partial f_2}{\partial I_2} & \frac{\partial f_2}{\partial V_D} \\
\frac{\partial f_3}{\partial I_1} & \frac{\partial f_3}{\partial I_2} & \frac{\partial f_3}{\partial V_D}
\end{bmatrix} $$

Sustituyendo las derivadas parciales:



$$
J = \begin{bmatrix}
1 & 1 & \frac{1}{R} \\
1 & 0 & -\frac{I_{s1}}{V_T} e^{V_D / V_T} \\
0 & 1 & -\frac{I_{s2}}{V_T} e^{V_D / V_T}
\end{bmatrix}
$$

Donde:
$$ \frac{\partial F_1}{\partial I_1} = 1 $$
$$ \frac{\partial F_1}{\partial I_2} = 1 $$
$$ \frac{\partial F_1}{\partial V_D} = \frac{1}{R} $$
$$ \frac{\partial F_2}{\partial I_1} = 1 $$
$$ \frac{\partial F_2}{\partial I_2} = 0 $$
$$ \frac{\partial F_2}{\partial V_D} = -\frac{I_{s1}}{V_T} e^{V_D / V_T} $$
$$ \frac{\partial F_3}{\partial I_1} = 0 $$
$$ \frac{\partial F_3}{\partial I_2} = 1 $$
$$ \frac{\partial F_3}{\partial V_D} = -\frac{I_{s2}}{V_T} e^{V_D / V_T} $$

### Paso 2: Construcción de la Matriz Jacobiana Expandida
Agregando la matriz de funciones al sistema para obtener la matriz Jacobiana aumentada:

$$
J * \Delta X = -F
$$

Es importante entender que $\Delta X$ es el vector que se propone hallar para corregir. 

$$ F = \begin{bmatrix}
F_1(I_1, I_2, V_D) \\
F_2(I_1, I_2, V_D) \\
F_3(I_1, I_2, V_D)
\end{bmatrix}
$$

$$ F=
\begin{bmatrix}
1 & 1 & \frac{1}{R} & \Big| &  I_1 + I_2 - \frac{V_s - V_D}{R} \\
1 & 0 & -\frac{I_{s1}}{V_T} e^{V_D / V_T} & \Big| &  I_1 - I_{s1} \left(e^{V_D / V_T} -1 \right)   \\
0 & 1 & -\frac{I_{s2}}{V_T} e^{V_D / V_T} & \Big| & I_2 - I_{s2} \left(e^{V_D / V_T} -1 \right)
\end{bmatrix}$$


### **Paso 3: Determinar de valores iniciales**
Se eligen los valores iniciales teniendo en cuenta valores razonables.
Para diodos se pueden tener $V_D$ entre $0.2V$ y $0.8V$ para diodos en conducción.

Para este proyecto tomaremos $V_D = 0.3V$

Entendiendo que se conocen los valores de las $I_{s1}, I_{s2}$ y se tomo un $V_D = 0.3V$ se
pueden calcular valores de las corrientes en el inicio por medio de la ecuación de diodo.



$I_{s1}=2×10^{−12}A$

$I_{s2}=5×10^{−12}A$

$V_T=25.85mV$


Cálculo de aproximaciones iniciales

$I_1^0 = I_{s1} \times \left(e^{0.3 / 0.02585} -1 \right) \approx 0.0016A = 1.6mA $ ✅

$I_2^0 = I_{s2} \times \left(e^{0.3 / 0.02585} -1 \right) \approx 0.004A = 4mA $ ✅

Para validar que los valores iniciales no sean fuera de operaciones o reglas se valida I en la carga.

$ I_R = \frac{5V-0.3V}{1kΩ} = 4.7mA < I_1^0+I_2^0$ ✅


$  [I_1^0 = 1.6mA, \quad I_2^0 = 4.0mA, \quad V_D^0 = 0.3V]  $

### **Paso 4: Sustitución de valores iniciales en la matriz aumentada**
Sustituimos los valores iniciales en el sistema y resolvemos para delta $$ \Delta X$$

Usamos los valores iniciales:
$$ I_1^0 = 1.6mA $$
 $$ I_2^0 = 4.0 mA $$
 $$ V_D^0 = 0.3  V $$
$$ J \Delta X = -F(X)  $$

$$
F_1(1.6mA, 4.0mA, 0.3V) = 1.6mA + 4.0mA - \frac{5V - 0.3V}{1kΩ} $$
$$
F_2(1.6mA, 4.0mA, 0.3V) = 1.6mA - 2×10^{−12}A \times \left(e^{0.3 / 0.02585} -1 \right)$$
$$
F_3(1.6mA, 4.0mA, 0.3V) = 4.0mA - 5×10^{−12}A \times \left(e^{0.3 / 0.02585} -1 \right)
$$

$$F_1\approx0.9mA$$
$$F_2\approx-3\mu A$$
$$F_1\approx-7\mu A$$

Ahora se debe llevar a la Jacobiana.

$$ J=
\begin{bmatrix}
1 & 1 & \frac{1}{R}  \\
1 & 0 & -\frac{I_{s1}}{V_T} e^{V_D / V_T}   \\
0 & 1 & -\frac{I_{s2}}{V_T} e^{V_D / V_T}
\end{bmatrix}$$

$$\begin{bmatrix}
1 & 1 & 0.001  \\
1 & 0 & -1.652 \times 10^{-6}   \\
0 & 1 & -4.13\times 10^{-6}
\end{bmatrix}$$

$$\begin{bmatrix}
1 & 1 & 0.001 & \Big|   -0.9mA \\
1 & 0 & -1.652 \times 1 0^{-6} & \Big| 3\mu A \\
0 & 1 & -4.13\times 10^{-6} &\Big| 7\mu A
\end{bmatrix}$$

### **Paso 5: Resolución del sistema de ecuaciones**
Se resuelve $$ J \Delta X = -F  $$ usando la técnica que se tenga a la mano, sustitución, 
eliminación de Gauss.

Se obtienen los valores:

$$\Delta I_1 = 1.505\times 1 0^{-6}mA$$
$$\Delta I_2 = 3.263\times 1 0^{-6}mA$$
$$\Delta V_D = -0.905V$$


### **Paso 6: Sustitución de valores en ecuaciones de recurrencia**
Son los valores con los que se realizará la siguiente iteración y se dan por:

$$ I_1^{k+1} = I_1^k + \Delta I_1 $$
$$ I_2^{k+1} = I_2^k + \Delta I_2 $$
$$ V_D^{k+1} = V_D^k + \Delta V_D $$

Para el actual proceso se logran obtener

$$I_1^1=1.6015mA$$
$$I_2^1=4.0033mA$$
$$V_D^1=-0.605V$$

### **Paso 7: Cálculo de la distancia**
Para identificar la convergencia se debe verificar los cambios de $\Delta X$ se usa la norma Euclidiana: 


$$ d = \sqrt{(I_1^{k+1} - I_1^k)^2 + (I_2^{k+1} - I_2^k)^2 + (V_D^{k+1} - V_D^k)^2} $$

$$ d \approx 0.905 $$


### **Paso 8: Repetición hasta convergencia**
Es valido tener un criterio de parada, bien sea por cantidad de iteraciones o por una tolerancia.
En este caso se propone usar una tolerancia en la distancia de forma que se itera hasta:
$$ d < 10^{-6} $$

Con el valor de $d$ que se tiene, se hace necesario retornar al paso 4 y continuar iterando.


---

## **Resultados Numéricos**

| Iteración | \( I_1 \) (mA) | \( I_2 \) (mA) | \( V_D \) (V) | Distancia |
|-----------|--------------|--------------|--------------|------------|
| 0         | 1.6000       | 4.0000       | 0.3000       | -          |
| 1         | 1.6015       | 4.0033       | -0.6050      | 0.905      |
| 2         | 1.6030       | 4.0066       | -0.6020      | 0.0030     |
| 3         | 1.6033       | 4.0069       | -0.6015      | 0.0005     |
| 4         | 1.6033       | 4.0069       | -0.6015      | 0.0000     |

---



Se invita para conocer otros métodos como la bisección, punto fijo y demás.
Ahora bien, para los más estudiosos, también se les motiva para consultar otras aplicaciones del método
como por ejemplo la búsqueda de la estabilidad de circuitos DC. Se recomienda 

[Estabilidad de Voltajes](https://ieeexplore.ieee.org/abstract/document/8664198)