# SEM-Web-Advisor

Sistema Inteligente para Auditoría Web basado en Web Semántica, Sistemas Multiagente y Lógica Difusa.

---

## Descripción

SEM-Web-Advisor es una aplicación web desarrollada en Python y Flask que permite analizar automáticamente sitios web para evaluar aspectos relacionados con:

- SEO
- Accesibilidad
- Rendimiento

El sistema utiliza agentes inteligentes para recopilar información del sitio web, un motor de lógica difusa para evaluar su estado general y una ontología OWL para representar conocimiento relacionado con buenas prácticas web.

Además, genera reportes PDF y almacena los resultados en MongoDB utilizando documentos semánticos JSON-LD.

---

## Objetivo General

Desarrollar un sistema inteligente capaz de evaluar sitios web mediante técnicas de Web Semántica, Sistemas Multiagente y Lógica Difusa.

---

## Objetivos Específicos

- Analizar automáticamente sitios web.
- Identificar problemas básicos de accesibilidad.
- Extraer información SEO relevante.
- Evaluar el rendimiento del sitio.
- Aplicar lógica difusa para determinar el estado del sitio.
- Representar conocimiento mediante ontologías OWL.
- Generar recomendaciones inteligentes.
- Almacenar auditorías utilizando MongoDB.
- Generar reportes PDF automáticos.

---

# Tecnologías Utilizadas

## Backend

- Python 3
- Flask

## Análisis Web

- Requests
- BeautifulSoup

## Inteligencia Artificial

- Scikit-Fuzzy

## Web Semántica

- OWL
- RDF/XML
- JSON-LD

## Base de Datos

- MongoDB
- PyMongo

## Reportes

- ReportLab

---

# Arquitectura General

```text
                ┌─────────────┐
                │   Usuario   │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   Flask     │
                └──────┬──────┘
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼

┌───────────┐   ┌───────────┐   ┌──────────────┐
│ Analista  │   │ Experto   │   │ Notificador  │
└─────┬─────┘   └─────┬─────┘   └──────┬───────┘
      │               │                │
      ▼               ▼                ▼

 Extracción     Lógica Difusa   Recomendaciones
 de datos

      │
      ▼

┌─────────────────────┐
│     MongoDB         │
└─────────┬───────────┘
          │
          ▼

    Documento JSON-LD

          │
          ▼

    Reporte PDF
```

---

# Estructura del Proyecto

```text
SEM-Web-Advisor
│
├── agents/
│   ├── analista.py
│   ├── experto.py
│   └── notificador.py
│
├── database/
│   └── conexion.py
│
├── ontology/
│   └── semweb.owl
│
├── static/
│   └── reports/
│
├── templates/
│   └── index.html
│
├── app.py
│
└── README.md
```

---

# Sistema Multiagente

## Agente Analista

Responsable de inspeccionar el sitio web y extraer información relevante.

Obtiene:

- Tiempo de respuesta
- Título SEO
- Meta descripción
- Cantidad de imágenes
- Imágenes sin atributo ALT
- Encabezados H1
- Links detectados
- Scripts externos

---

## Agente Experto

Utiliza lógica difusa para evaluar:

- Tiempo de carga
- Porcentaje de errores detectados

Genera:

- Nivel difuso
- Estado del sitio
- Prioridad de atención

Estados posibles:

- Al día
- Regular
- Crítico

---

## Agente Notificador

Genera recomendaciones automáticas según el estado obtenido por el agente experto.

Ejemplos:

- Mejorar imágenes sin ALT.
- Optimizar tiempos de carga.
- Revisar metadatos SEO.
- Aplicar mejoras preventivas.

---

# Lógica Difusa

El sistema utiliza lógica difusa para transformar métricas técnicas en una evaluación comprensible para el usuario.

## Variables de Entrada

### Tiempo de carga

- Bajo
- Medio
- Alto

### Porcentaje de errores

- Bajo
- Medio
- Alto

## Variable de Salida

### Estado del sitio

- Al día
- Regular
- Crítico

---

# Ontología OWL

La ontología representa conocimiento relacionado con auditoría web.

## Clases

- BuenasPracticas
- SEO
- Accesibilidad
- Rendimiento
- EstadoSitio
- Recomendacion

---

## Subclases

### EstadoSitio

- Excelente
- Aceptable
- Critico

### BuenasPracticas

- SEO
- Accesibilidad
- Rendimiento

---

## Propiedades de Objeto

### tieneEstado

Relaciona una práctica con un estado.

Ejemplo:

```text
SEO_Critico → EstadoCritico
```

### sugiereAccion

Relaciona una práctica con una recomendación.

Ejemplo:

```text
SEO_Critico → CorregirMetaTags
```

---

# Ejemplos de Individuos

## SEO_Critico

- Estado: EstadoCritico
- Acción: CorregirMetaTags

## Accesibilidad_Critica

- Estado: EstadoCritico
- Acción: AgregarAltImagenes

## Rendimiento_Bajo

- Estado: EstadoAceptable
- Acción: OptimizarVelocidad

---

# Almacenamiento Semántico

Los resultados se almacenan en MongoDB utilizando JSON-LD.

Ejemplo:

```json
{
  "@context": "http://schema.org/",
  "@type": "AuditReport",
  "site": "https://www.ejemplo.com",
  "result": {
    "status": "Regular",
    "priority": "Media",
    "nivel": 4.63,
    "errores": 1,
    "tiempo": 2.21,
    "tags": [
      "SEO",
      "Accesibilidad",
      "Rendimiento"
    ]
  }
}
```

---

# Reporte PDF

El sistema genera automáticamente un reporte PDF con:

- Información del sitio analizado.
- Estado obtenido.
- Nivel difuso.
- Resumen técnico.
- Recomendaciones.
- Conclusiones.

---

# Instalación

## Clonar repositorio

```bash
git clone https://github.com/TU-USUARIO/SEM-Web-Advisor.git
```

## Entrar al proyecto

```bash
cd SEM-Web-Advisor
```

## Crear entorno virtual

```bash
python -m venv venv
```

## Activar entorno

Windows:

```bash
venv\Scripts\activate
```

Linux:

```bash
source venv/bin/activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Configuración de MongoDB

Iniciar MongoDB local:

```bash
mongod
```

Verificar conexión:

```bash
mongodb://localhost:27017
```

---

# Ejecutar Proyecto

```bash
python app.py
```

Abrir en navegador:

```text
http://127.0.0.1:5000
```

---

# Funcionalidades Implementadas

✅ Análisis SEO

✅ Análisis de accesibilidad

✅ Evaluación de rendimiento

✅ Sistema multiagente

✅ Lógica difusa

✅ Ontología OWL

✅ JSON-LD

✅ MongoDB

✅ Reportes PDF

✅ Historial de auditorías

---

# Resultados Esperados

El sistema debe ser capaz de:

- Analizar un sitio web.
- Detectar problemas básicos.
- Clasificar el estado del sitio.
- Generar recomendaciones.
- Almacenar auditorías.
- Generar reportes PDF.
- Representar conocimiento mediante ontologías.

---


Proyecto académico desarrollado para la asignatura de Web Semántica e Inteligencia Artificial.

---

# Licencia

Proyecto con fines académicos y educativos.
