# KRAFTBOOST

Esta es una tienda online especializada en **pesas, mancuernas y equipamiento para el entrenamiento de fuerza**, diseñada para ofrecer una experiencia de compra fluida, completa y segura tanto para usuarios como para administradores.

### Funcionalidades para el Usuario:

- **Autenticación completa**: registro, login y recuperación de contraseña por email.
- **Exploración de productos** con buscador inteligente y filtros por categoría, marca, precio y orden.
- **Carrito de compras** con sistema de pasarela de pago ficticio pero funcional.
- **Confirmación de pedidos** vía email, junto a mensajes de bienvenida y todo personalizado.
- **Gestión de perfil**: edición de datos personales, direcciones, favoritos y visualización del historial de pedidos con sus respectivos detalles.
- **Diseño intuitivo**, responsivo y enfocado en una experiencia de usuario amigable y eficiente.

### Panel de Administración:

- **Gestión de pedidos**: ver, activar/desactivar y actualizar su estado.
- **Control de usuarios**: editar información o eliminar cuentas.
- **Gestión de productos**: editar, dar de baja o activar productos con total control.
- **Interfaz segura**, protegida y separada de las funciones de usuario normal.

### Extras Técnicos:

- Control de errores personalizado con páginas para códigos **401 (no autorizado)** y **404 (página no encontrada)**.
- Sistema de envío de **emails automáticos** para distintas acciones.
- Uso de **tokens** para proteger algunas rutas como la recuperación de contraseña o pasarela de pago.
- Estructura modular con Blueprints de Flask para mantener el proyecto organizado y escalable.

En resumen, esta tienda online no solo permite comprar artículos deportivos de manera sencilla, sino que también ofrece un backend robusto y potente para una administración total del sistema.

---

## Requisitos

Para ejecutar este proyecto, necesitas:

- **Python 3.x**
- **MySQL** (puede ser local o en la nube)
- Librerías de Python:
  - `Flask`
  - `Flask-Login`
  - `Flask-Mail`
  - `Flask-MySQLdb`
  - `Flask-WTF`
  - `python-dotenv`
  - `WTForms`
  - `gunicorn`
  - `email_validator`
  - `mysqlclient`
  - `PyJWT`
  - `Unidecode`
---

## Instalación

1. **Clona el repositorio**  
   Ejecuta el siguiente comando en tu terminal:
   ```bash
   git https://github.com/DavidKal29/Proyecto-Final-TFG.git
   cd Proyecto-Final-TFG

2. **Crea un entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv env
   source env/bin/activate    # Linux/Mac
   env\Scripts\activate       # Windows

3. **Instala las dependencias** 
   ```bash
   pip install -r requeriments.txt

4. **Configura las variables de entorno** 
   Crea un archivo .env y pon las siguientes variables, poniendo obviamente tus propios datos:
   ```env
      SECRET_KEY=
      MYSQL_HOST=
      MYSQL_USER=
      MYSQL_PASSWORD=
      MYSQL_DB=
      MYSQL_HOST_CLEVER_CLOUD=
      MYSQL_USER_CLEVER_CLOUD=
      MYSQL_PASSWORD_CLEVER_CLOUD=
      MYSQL_DB_CLEVER_CLOUD=
      CORREO=
      PASSWORD_DEL_CORREO=
      JWT_SECRET_KEY_RESET_PASSWORD=
      JWT_SECRET_KEY_RESET_CART=


5. **Ejectua la aplicacion** 
   ```bash
    python src/app.py 

6. **Abre el navegador** 
   Ve a http://127.0.0.1:5000 para acceder a la aplicación.
