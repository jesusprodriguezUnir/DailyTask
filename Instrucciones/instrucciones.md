# 📌 Aplicación de Control de Tareas Diarias – Instrucciones

## 🎯 Rol
Actúa como un **arquitecto de software senior y desarrollador full-stack especializado en Python**.

## 🧩 Objetivo General
Diseñar y desarrollar una **aplicación completa de control de tareas diarias** que permita registrar, gestionar y reportar todo el trabajo realizado durante el año **2026**, con persistencia en base de datos y acceso externo seguro.

---

## 🛠️ Requisitos Técnicos

### Backend
- Python
- FastAPI
- API REST documentada con OpenAPI (Swagger)
- Autenticación mediante **API-Key**

### Frontend
- Python
- Streamlit o NiceGUI
- Interfaz moderna, curiosa y fácil de usar
- Accesible desde el exterior (producción)

### Base de Datos
- SQLite
- SQLAlchemy como ORM
- Modelo preparado para escalar

---

## ⚙️ Funcionalidades

1. **Gestión de tareas (CRUD)**
   - Fecha
   - Descripción
   - Duración
   - Etiquetas
   - Estado

2. **Importación de tareas**
   - Desde archivos de texto (`.txt`)
   - Procesamiento automático y validación

3. **API externa**
   - Inserción de tareas mediante API-Key
   - Compatible con integraciones como **n8n**, scripts y automatizaciones

4. **Reportes**
   - Generación de reportes en **PDF**
   - Filtros por rango de fechas

5. **Persistencia**
   - Registro diario de tareas
   - Organización clara por fechas
   - Optimizado para uso continuo durante todo 2026

---

## 🧪 Calidad y Producción

- Tests unitarios con `pytest`
- Estructura de proyecto profesional
- CI/CD con **GitHub Actions**
- Contenedorización con Docker
- Despliegue en producción (Railway / Fly.io / Render)
- Uso de variables de entorno seguras

---

## 📦 Entrega Esperada

- Arquitectura general explicada
- Estructura completa del proyecto
- Código funcional (backend, frontend, tests)
- Ejemplos de uso de la API
- Scripts de despliegue
- Recomendaciones de mejoras futuras

---

## 🚫 Restricciones

- Todo el proyecto debe estar desarrollado en **Python**
- Código limpio, comentado y mantenible
- Buenas prácticas de arquitectura y seguridad

---

## ▶️ Instrucciones de Ejecución

1. Comienza explicando la **arquitectura general**
2. Desarrolla cada componente paso a paso
3. Prioriza claridad, mantenibilidad y calidad del código
4. Piensa en un entorno **real de producción**

