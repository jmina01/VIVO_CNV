Intro
1. Access to SQL Server
Para la transferencia de la base de datos a SQL Server se utilizó la herramienta SQL Server Migration Assistant

2. Py scripts
  Librerias:
    app.py
      1. Flask, comunicacion de archivos y creacion de host web
      2. Pyodbc, llamado al script 'pdf' y guardar en memoria el estado de cuenta
    pdf.py
      1.  pandas, cracion de df
      2. reportlab, customizacion del pdf

3. VM (Google cloud)
  Caracteristicas:
  location, us-central1-c
  Host físico ,Ninguna
  Protección contra la eliminación Inhabilitado
  Servicio Confidential VM,Inhabilitado
  Tamaño de estado preservado,0 GB
  
  Configuración de la máquina
  e2-highcpu-2,2 vCPUs, 2 GB Memory (requerimiento minimo para SQL Server)
  Plataforma de CPU,Intel Broadwell
  Plataforma de CPU mínima, x86‑64
  CPU virtuales para proporción de núcleos —
  Núcleos visibles personalizados —
  Modo turbo exclusivo para todos los núcleos —
  Dispositivo de visualización, Inhabilitado
  GPU,Ninguna
  
  Redes
  Registro PTR del DNS público, Ninguno
  Nivel total de ancho de banda de salida —
  Tipo de NIC —
  Firewalls, crear 2 reglas, una para SQL Server y la otra para el alojamiento web
    Regla 1, Rangos de IP: 0.0.0.0/0, port: tcp 1433, Direccion de entrada, todas las instancias de la red, rangos de IPV4, filtros (ninguno)
    Regla 2, Rangos de IP: 0.0.0.0/0, port: tcp 8000, Direccion de entrada, todas las instancias de la red, rangos de IPV4, filtros (ninguno)
  Tráfico HTTP, Activo
  Tráfico HTTPS, Activo
  Permitir las verificaciones de estado del balanceador de cargas, Inactivo
  
  Almacenamiento
  Tamaño (GB), 30
  Tipo, Disco persistente estándar
  Arquitectura,x86‑64
  Inicio, lectura/escritura
  Discos locales, Ninguna
  Discos adicionales, Ninguna
  Plan de creación de copias de seguridad, Administrado por el servicio Backup and DR
  Estado de programación de copias de seguridad,No configurada
  Plan de creación de copias de seguridad


4. Ubuntu
  a. Instalación de Dependencias del Sistema
  Actualiza el sistema e instala Apache, Python y las librerías necesarias:
  "sudo apt update"
  "sudo apt install apache2 python3 python3-pip python3-venv libapache2-mod-wsgi-py3"
  
  Si tu aplicación utiliza pyodbc y necesitas el controlador ODBC para SQL Server, instala:
  "sudo apt install unixodbc-dev"
  
  Y, para instalar el driver de Microsoft (si aún no lo tienes):
  sudo su
  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
  curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
  exit
  sudo apt update
  sudo ACCEPT_EULA=Y apt install msodbcsql17
  
  Clonar repo
  "git clone https://github.com/tu_usuario/tu_repositorio.git"
  cd tu_repositorio
  python3 -m venv venv
  source venv/bin/activate
  
  b. instalar dependencias py
  
  c. Configuración del Archivo WSGI
  Crea o edita el archivo run.wsgi en la raíz del proyecto (/home/jmina/VIVO_CNV/run.wsgi) con el siguiente contenido
  #!/usr/bin/python3
  "import sys
  import logging
  logging.basicConfig(stream=sys.stderr)
  sys.path.insert(0, "/home/jmina/VIVO_CNV")
  from app import app as application"
  
  Nota:Asegúrate de que el módulo app corresponda al archivo que contiene la instancia de tu aplicación Flask y que la variable expuesta se llame application.
  "app = Flask(__name__)"
  

Apache

Configuración de Apache con mod_wsgi
Edita el archivo default de apache con el siguiente comando:
"sudo nano /etc/apache2/sites-available/000-default.conf"

Nuevo contenido:
"<VirtualHost *:80>
    ServerName 34.45.59.38
    WSGIDaemonProcess VIVO_CNV user=jmina group=www-data threads=2
    WSGIScriptAlias / /home/jmina/VIVO_CNV/run.wsgi
    <Directory /home/jmina/VIVO_CNV/>
        WSGIProcessGroup VIVO_CNV
        WSGIApplicationGroup %{GLOBAL}
        Require all granted
    </Directory>
    Alias /static/ /home/jmina/VIVO_CNV/static/
    <Directory /home/jmina/VIVO_CNV/static/>
        Require all granted
    </Directory>
    ErrorLog /home/jmina/VIVO_CNV/error.log
    CustomLog /home/jmina/VIVO_CNV/access.log combined
</VirtualHost>"

Recargar para el nuevo contenido
sudo systemctl reload apache2

Permisos en el Sistema de Archivos
Asegúrate de que Apache (usuario www-data) tenga permisos de lectura y ejecución en el directorio del proyecto:

bash 
sudo chown -R jmina:www-data /home/jmina/VIVO_CNV
sudo chmod -R 755 /home/jmina/VIVO_CNV


Actualización del Repositorio Local (Sobrescribiendo Archivos)
Si necesitas actualizar tu repositorio local sobrescribiendo todos los cambios (¡Atención: se perderán los cambios locales!), utiliza:
git fetch --all
git reset --hard origin/main  # Cambia 'main' por 'master' si ese es el nombre de tu rama principal
git clean -fd








Notas adicionales: el script ift.py no se utiliza en ningun momento por ahora, sin embargo se piensa implementar para descargar la data del infonavit
editar el archivo apache default.conf= sudo nano /etc/apache2/sites-available/000-default.conf
restart apache: sudo systemctl restart apache2
actualizar repo ubuntu: git pull
leer archivos: cat /home/jmina/VIVO_CNV/run.wsgi   /home/jmina/VIVO_CNV/run.wsgi
actualizar y sobreescribir repo: git reset --hard origin/main
