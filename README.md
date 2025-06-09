# Mini Blog en Flask

Este es un proyecto simple de un blog creado con Python, Flask, MongoDB y un sistema de templates HTML. Permite a los usuarios agregar publicaciones al blog y almacenarlas en una base de datos MongoDB.

## Características
- **Agregar entradas**: Los usuarios pueden agregar entradas al blog a través de un formulario.
- **Listado de publicaciones**: Se muestran todas las publicaciones con su título y contenido.
- **Persistencia de datos**: Las entradas se almacenan en una base de datos MongoDB.
- **Templates HTML**: Uso de plantillas para renderizar el contenido.
- **Fecha de publicación**: Cada entrada muestra la fecha actual.

---

## Requisitos

Para ejecutar este proyecto, necesitas:
- **Python 3.x**
- **MongoDB** (puede ser local o en la nube)
- Librerías de Python:
  - `Flask`
  - `python-dotenv`
  - `pymongo`

---

## Instalación

1. **Clona el repositorio**  
   Ejecuta el siguiente comando en tu terminal:
   ```bash
   git clone https://github.com/DavidKal29/MiniBlogFlaskMongoDB.git
   cd MiniBlogFlaskMongoDB

2. **Crea un entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv env
   source env/bin/activate    # Linux/Mac
   env\Scripts\activate       # Windows

3. **Instala las dependencias** 
   ```bash
   pip install -r requeriments.txt

4. **Configura las variables de entorno** 
   Crea un archivo .env y pon en él lo siguiente:
   ```env
   endpoint=<TU_ENDPOINT_DE_MONGODB>

5. **Ejectua la aplicacion** 
   ```bash
    python app.py

6. **Abre el navegador** 
   Ve a http://127.0.0.1:5000 para acceder a la aplicación.