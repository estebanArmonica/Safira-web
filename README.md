## Página Web Safira Energía Chile 🌱

Este es un proyecto de una página web empresarial de energía donde los potenciales clientes podran realizar cotizaciones por KwH.

## Tecnologías

- Python 3.12.6
- Django 5.2.4
- HTML5
- CSS3
- Bootstrap 5.0.2
- PostgreSQL 17

## Entorno Local

Lo primero que tienes que hacer para poder ejecutar el proyecto es clonar el repositorio en tu computadora:

```bash
git clone https://github.com/estebanArmonica/Safira-web.git
cd ./backend
```

Ahora que clonamos el repositorio, tenemos que crear un entorno virtual de Python para la instalación de dependencias del proyecto:

```bash
python -m virtualenv venv

# Windows
venv\Scripts\activate

# Linux o Mac
source venv/bin/activate
```

> [!NOTE]
> Si quieres utilizar virtualenv, tienes que instalarlo con pip `pip install virtualenv`.

### Instalación de Dependencias

Con el entorno virtual de Python activado y configurado, instalamos las dependencias del proyecto:

    pip install -r requirements.txt

### Variables de Entorno

Ahora tenemos que configurar las variables de entorno, en la carpeta del proyecto debera crear un `.env` para utilizar y llamar a esas variables de entorno en python:

> [!NOTE]
> Para la variable de entorno `SECRET_KEY` tienes que ingresar una clave secreta válida para que el proyecto pueda ejecutarse. Puedes conseguir una clave en la siguiente página **[Djecrety](https://djecrety.ir/)**.

### Migraciones

Con las variables de entorno configuradas, tenemos que realizar las migraciones de los modelos para que se creen las tablas en la base de datos:

```bash
python manage.py makemigrations
python manage.py migrate
```

Con esto se migrarán los modelos a la base de datos y se crearán las tablas correspondientes para el funcionamiento de la aplicación.

### Ejecución

Con todo listo y configurado, ejecutemos el proyecto con el siguiente comando:

    python manage.py runserver

Listo!!, si todo salio bien ya tienes el proyecto corriento en tu computadora de manera local

## Entorno Docker

Lo primero que tienes que hacer para poder ejecutar el proyecto es clonar el repositorio en tu computadora:

```bash
git clone https://github.com/estebanArmonica/Safira-web.git
cd ./backend
```

Ahora espero que tengas instalado en tu computadora el software de contenedores Docker

### Variables de Entorno

de la forma anterior debemos crear las variables de entorno.

> [!NOTE]
> Para la variable de entorno `SECRET_KEY` tienes que ingresar una clave secreta válida para que el proyecto pueda ejecutarse. Puedes conseguir una clave en la siguiente página **[Djecrety](https://djecrety.ir/)**.

### Creación de la Imagen

Ahora que tenemos las variables de entorno configuradas, creemos la imagen de Docker del proyecto:

```bash
docker compose build
```

### Ejecución

Con la imagen de Docker ya creada ejecutaremos el proyecto a traves de Docker:

```bash
docker compose up
```

Si todo salio bien, ya tienes el proyecto corriendo con Docker, igualmente asegúrate de revisar cualquier detalle o error específico que haya ocurrido en el proyecto.
