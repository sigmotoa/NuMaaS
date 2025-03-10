# NuMaaS Numerical Methods as a Software

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![CI/CD](https://img.shields.io/badge/CI/CD-Render-purple.svg)

Una API moderna herramienta para resolver sistemas de ecuaciones no lineales utilizando diversos métodos númericos.

Perfecta para aplicaciones de ingeniería eléctrica, mecánica, física y más.

## 🚀 Características (Por ahora)

- 🧮 Implementación del método Newton-Raphson multivariado
- 🔌 Resolución de circuitos con diodos en paralelo
- 📊 Visualización de las iteraciones y convergencia
- 📝 Documentación completa con Swagger UI
- ✅ Pruebas automatizadas con pytest

## 📋 Casos de uso implementados

- Análisis de circuitos con diodos en paralelo
- Resolución de sistemas de ecuaciones no lineales genéricas

## 🛠️ Instalación (Para correr en local)

```bash
# Clonar el repositorio
git clone https://github.com/sigmotoa/numaas.git
cd numaas

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
uvicorn app.main:app --reload
```

## 📖 Documentación

La API está documentada usando Swagger UI. Una vez que la aplicación esté en ejecución, puedes acceder a la documentación en:

```
http://localhost:8000/docs
```

## 🧪 Pruebas

Ejecuta las pruebas automatizadas con:

```bash
pytest
```

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, siente libre de abrir un issue o enviar un pull request.

## 📜 Licencia (Pendiente)

Este proyecto (pueda ser que) está licenciado bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📚 Para más información

Consulta nuestra [Wiki](https://github.com/sigmotoa/numaas/wiki) para obtener información detallada sobre los métodos implementados.
