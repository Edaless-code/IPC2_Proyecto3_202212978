# Backend - Tecnologías Chapinas S.A.

Sistema de gestión de infraestructura en la nube con facturación automática.

## 📋 Estructura del Proyecto

```
backend/
├── app.py                          # API Flask principal
├── models.py                       # Clases POO del sistema
├── xml_parser.py                   # Procesamiento de XML
├── database.py                     # Gestor de base de datos XML
├── requirements.txt                # Dependencias
├── test_api.py                     # Script de pruebas
├── ejemplo_configuracion.xml       # XML de ejemplo (configuración)
├── ejemplo_consumos.xml            # XML de ejemplo (consumos)
├── data/                           # Base de datos XML
│   ├── recursos.xml
│   ├── clientes.xml
│   └── ...
└── README.md                       # Este archivo
```

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/IPC2_Proyecto3_tucarnet.git
cd IPC2_Proyecto3_tucarnet/backend
```

### 2. Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🎯 Ejecutar el API

```bash
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

## 📡 Endpoints del API

### Gestión de Datos

#### `GET /consultarDatos`
Consulta todos los datos del sistema.

**Respuesta:**
```json
{
  "status": "success",
  "data": {
    "recursos": [...],
    "categorias": [...],
    "configuraciones": [...],
    "clientes": [...],
    "facturas": [...]
  }
}
```

#### `POST /crearRecurso`
Crea un nuevo recurso.

**Body (JSON):**
```json
{
  "id": 1,
  "nombre": "Memoria RAM",
  "abreviatura": "RAM",
  "metrica": "GiB",
  "tipo": "Hardware",
  "valorXhora": 0.75
}
```

#### `POST /crearCategoria`
Crea una nueva categoría.

**Body (JSON):**
```json
{
  "id": 1,
  "nombre": "Máquinas virtuales para desarrollo",
  "descripcion": "Configuraciones para desarrollo",
  "cargaTrabajo": "Desarrollo web"
}
```

#### `POST /crearConfiguracion`
Crea una nueva configuración.

**Body (JSON):**
```json
{
  "id": 1,
  "nombre": "VM Básica",
  "descripcion": "Máquina virtual básica",
  "idCategoria": 1,
  "recursos": {
    "1": 4,
    "2": 2
  }
}
```

#### `POST /crearCliente`
Crea un nuevo cliente.

**Body (JSON):**
```json
{
  "nit": "12345678-9",
  "nombre": "Empresa ABC S.A.",
  "usuario": "empresa_abc",
  "clave": "pass123",
  "direccion": "Zona 10, Guatemala",
  "correoElectronico": "contacto@empresaabc.com"
}
```

#### `POST /crearInstancia`
Crea una nueva instancia.

**Body (JSON):**
```json
{
  "nitCliente": "12345678-9",
  "id": 1,
  "idConfiguracion": 1,
  "nombre": "Servidor Web",
  "fechaInicio": "01/01/2025",
  "estado": "Vigente"
}
```

#### `POST /cancelarInstancia`
Cancela una instancia existente.

**Body (JSON):**
```json
{
  "nitCliente": "12345678-9",
  "idInstancia": 1,
  "fechaFinal": "31/01/2025"
}
```

### Procesamiento de XML

#### `POST /procesarConfiguracion`
Procesa un archivo XML de configuración completo.

**Headers:** `Content-Type: application/xml`

**Body:** Contenido XML según el formato del enunciado

**Respuesta:**
```json
{
  "status": "success",
  "message": "Configuración procesada exitosamente",
  "estadisticas": {
    "recursos": 5,
    "categorias": 2,
    "configuraciones": 3,
    "clientes": 2,
    "instancias": 4
  }
}
```

#### `POST /procesarConsumos`
Procesa un archivo XML de consumos.

**Headers:** `Content-Type: application/xml`

**Body:** Contenido XML de consumos

**Respuesta:**
```json
{
  "status": "success",
  "message": "6 consumos procesados exitosamente",
  "cantidad": 6
}
```

### Facturación

#### `POST /generarFacturas`
Genera facturas para un rango de fechas.

**Body (JSON):**
```json
{
  "fechaInicio": "01/01/2025",
  "fechaFin": "31/01/2025"
}
```

**Respuesta:**
```json
{
  "status": "success",
  "message": "2 facturas generadas",
  "facturas": [...]
}
```

#### `GET /obtenerFactura/<numero>`
Obtiene una factura específica por su número.

**Ejemplo:** `GET /obtenerFactura/1`

### Análisis

#### `POST /analizarVentasCategorias`
Analiza ingresos por categoría y configuración.

**Body (JSON):**
```json
{
  "fechaInicio": "01/01/2025",
  "fechaFin": "31/01/2025"
}
```

#### `POST /analizarVentasRecursos`
Analiza ingresos por recurso.

**Body (JSON):**
```json
{
  "fechaInicio": "01/01/2025",
  "fechaFin": "31/01/2025"
}
```

### Sistema

#### `POST /inicializarSistema`
Elimina todos los datos del sistema.

**Respuesta:**
```json
{
  "status": "success",
  "message": "Sistema inicializado correctamente"
}
```

## 🧪 Probar el API

### Opción 1: Script de prueba

```bash
python test_api.py
```

Este script ejecuta todas las pruebas automáticamente.

### Opción 2: Postman

1. Importa los endpoints a Postman
2. Usa los archivos XML de ejemplo para las pruebas
3. Consulta los resultados con los endpoints GET

### Opción 3: curl

```bash
# Consultar datos
curl http://localhost:5000/consultarDatos

# Crear recurso
curl -X POST http://localhost:5000/crearRecurso \
  -H "Content-Type: application/json" \
  -d '{"id":10,"nombre":"Test","abreviatura":"TST","metrica":"unidad","tipo":"Hardware","valorXhora":1.0}'

# Procesar configuración
curl -X POST http://localhost:5000/procesarConfiguracion \
  -H "Content-Type: application/xml" \
  -d @ejemplo_configuracion.xml
```

## 🏗️ Arquitectura POO

### Clases Principales

- **Recurso**: Representa recursos de infraestructura (CPU, RAM, etc.)
- **Configuracion**: Agrupa recursos para crear VMs
- **Categoria**: Organiza configuraciones por tipo de carga
- **Cliente**: Usuarios del servicio
- **Instancia**: Aprovisionamiento de una configuración
- **Consumo**: Registro de uso de instancias
- **Factura**: Documento de cobro
- **DetalleFactura**: Desglose de cargos por instancia

### Módulos

- **models.py**: Definición de todas las clases
- **xml_parser.py**: Procesamiento y validación de XML con regex
- **database.py**: Lógica de negocio y persistencia
- **app.py**: API REST con Flask

## 📝 Validaciones Implementadas

### Expresiones Regulares

- **NIT**: `^\d+-[0-9K]$` (ej: 12345678-9, 11111111-K)
- **Fechas**: `(\d{2})/(\d{2})/(\d{4})` extrae dd/mm/yyyy de cualquier texto
- **Fecha-Hora**: `(\d{2})/(\d{2})/(\d{4})\s+(\d{2}):(\d{2})`

### Validaciones de Negocio

- NITs deben ser válidos
- Fechas deben existir en el calendario
- IDs deben ser únicos
- Configuraciones deben referenciar recursos existentes
- Instancias deben referenciar configuraciones existentes
- Consumos deben referenciar instancias activas

## 💾 Persistencia

Los datos se almacenan en archivos XML en la carpeta `data/`:

- `recursos.xml`: Catálogo de recursos
- `clientes.xml`: Clientes e instancias con consumos

## 🐛 Troubleshooting

### Error: "No se pudo conectar al servidor"
- Verifica que el servidor Flask esté ejecutándose
- Revisa que el puerto 5000 esté disponible

### Error: "XML mal formado"
- Valida que el XML tenga la estructura correcta
- Revisa que todas las etiquetas estén cerradas

### Error: "NIT inválido"
- Verifica el formato: números-dígito (ej: 12345678-9)
- El dígito verificador debe ser 0-9 o K

## 📚 Referencias

- Flask: https://flask.palletsprojects.com/
- XML en Python: https://docs.python.org/3/library/xml.etree.elementtree.html
- Regex en Python: https://docs.python.org/3/library/re.html

## 👤 Autor

[Tu Nombre] - [Tu Carnet]
IPC2 - Proyecto 3
Universidad de San Carlos de Guatemala