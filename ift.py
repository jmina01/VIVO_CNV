import paramiko
from pathlib import Path
from datetime import datetime, timedelta
import os

def get_bimestre_start_date(date):

    month = date.month
    year = date.year
    if 1 <= month <= 2:
        return datetime(year, 1, 1)
    elif 3 <= month <= 4:
        return datetime(year, 3, 1)
    elif 5 <= month <= 6:
        return datetime(year, 5, 1)
    elif 7 <= month <= 8:
        return datetime(year, 7, 1)
    elif 9 <= month <= 10:
        return datetime(year, 9, 1)
    elif 11 <= month <= 12:
        return datetime(year, 11, 1)

def process_connection(connection_params, fecha_corte):
    """
   SFTP conexion.
    """
    desarrollo = connection_params['Desarrollo']
    usuario = connection_params['user']
    password = connection_params['pass']
    host = connection_params['host']
    puerto = connection_params['port']
    ruta = connection_params['ruta']
    rutaG = connection_params['rutaG']

    print(f'\n=== Procesando: {desarrollo} ===')

    LOCAL_DIR = Path(rutaG)
    try:
        LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f'Error al crear el directorio local {rutaG}: {e}')
        return

    bimestre_counters = {}

    try:
        # Conectar
        transport = paramiko.Transport((host, puerto))
        transport.connect(username=usuario, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.chdir(ruta)
        print(f'Conectado a {host} y navegado al directorio {ruta}')

        # Obtener lista de archivos
        archivos = sftp.listdir_attr()
        print(f'Se encontraron {len(archivos)} archivos en el directorio {ruta}.')

        archivos_descargados = 0  # Contador

        for archivo in archivos:
            # Obtener la fecha del archivo
            fecha_modificacion = datetime.fromtimestamp(archivo.st_mtime)
            nombre_archivo = archivo.filename

            # >fecha corte?
            if fecha_modificacion > fecha_corte:
                # bimestre pertenece
                bimestre_inicio = get_bimestre_start_date(fecha_modificacion)
                bimestre_inicio_str = bimestre_inicio.strftime('%d-%m-%Y')

                # iniciar contador si bimestre no existe
                if bimestre_inicio_str not in bimestre_counters:
                    bimestre_counters[bimestre_inicio_str] = 1  

                # Asignar el dia
                dia_asignado = bimestre_counters[bimestre_inicio_str]
                fecha_asignada = bimestre_inicio + timedelta(days=dia_asignado - 1)
                fecha_asignada_str = fecha_asignada.strftime('%d-%m-%Y')

                # incremento del contador
                bimestre_counters[bimestre_inicio_str] += 1

                # extension
                extension = Path(nombre_archivo).suffix  

                # nombrar 
                nuevo_nombre = f'{fecha_asignada_str}{extension}'
                ruta_local = LOCAL_DIR / nuevo_nombre

                # descargar
                try:
                    sftp.get(nombre_archivo, str(ruta_local))
                    print(f'Descargado y guardado como: {ruta_local}')
                    archivos_descargados += 1
                except Exception as descarga_error:
                    print(f'Error al descargar {nombre_archivo}: {descarga_error}')

        if archivos_descargados == 0:
            print('No se descargaron archivos. Ninguno cumplió con el criterio de fecha.')
        else:
            print(f'Total de archivos descargados: {archivos_descargados}')

    except paramiko.AuthenticationException:
        print('Error de autenticacion.')
    except paramiko.SSHException as ssh_error:
        print(f'Error en la conexión SSH/SFTP: {ssh_error}')
    except Exception as e:
        print(f'Error SFTP: {e}')

    finally:
        # Cerrar sftp
        try:
            if 'sftp' in locals():
                sftp.close()
            if 'transport' in locals():
                transport.close()
            print('Conexion SFTP cerrada')
        except Exception as cierre_error:
            print(f'Error al cerrar SFTP: {cierre_error}')

# onexiones sftp 
connections = [
    {
        'Desarrollo': 'ALOJ',
        'user': 'IECAL101',
        'pass': 'LCALc1I2',
        'host': '201.134.132.136',
        'port': 22,
        'ruta': '/Salida',
        'rutaG': r'\\10.10.10.122\Administracion_AV\01 CONVIVENCIAS\CONVIVENCIAS\00.CNV\Reporte de convivencias\Database\ALOJ'
    },
    {
        'Desarrollo': 'CENT',
        'user': 'IEACQ101',
        'pass': 'x+%8/WWj',
        'host': '201.134.132.136',
        'port': 22,
        'ruta': '/Salida',
        'rutaG': r'\\10.10.10.122\Administracion_AV\01 CONVIVENCIAS\CONVIVENCIAS\00.CNV\Reporte de convivencias\Database\CENT'
    },
    {
        'Desarrollo': 'ECOZ',
        'user': 'IECEN101',
        'pass': 'D3*c3Nis',
        'host': '201.134.132.136',
        'port': 22,
        'ruta': '/Salida',
        'rutaG': r'\\10.10.10.122\Administracion_AV\01 CONVIVENCIAS\CONVIVENCIAS\00.CNV\Reporte de convivencias\Database\ECOZ'
    },
    {
        'Desarrollo': 'PAMA',
        'user': 'IECOC101',
        'pass': 'J-Wl4qMq',
        'host': '201.134.132.136',
        'port': 22,
        'ruta': '/Salida',
        'rutaG': r'\\10.10.10.122\Administracion_AV\01 CONVIVENCIAS\CONVIVENCIAS\00.CNV\Reporte de convivencias\Database\PAMA'
    },
    {
        'Desarrollo': 'PUMA',
        'user': 'IECPC101',
        'pass': 'G5Sy){j3',
        'host': '201.134.132.136',
        'port': 22,
        'ruta': '/Salida',
        'rutaG': r'\\10.10.10.122\Administracion_AV\01 CONVIVENCIAS\CONVIVENCIAS\00.CNV\Reporte de convivencias\Database\PUMA'
    },
    {
        'Desarrollo': 'SMAR',
        'user': 'IECME101',
        'pass': '0-3cDf3a',
        'host': '201.134.132.136',
        'port': 22,
        'ruta': '/Salida',
        'rutaG': r'\\10.10.10.122\Administracion_AV\01 CONVIVENCIAS\CONVIVENCIAS\00.CNV\Reporte de convivencias\Database\SMAR'
    },
    {
        'Desarrollo': 'VECL',
        'user': 'IEACT101',
        'pass': 'cF~73V!_',
        'host': '201.134.132.136',
        'port': 22,
        'ruta': '/Salida',
        'rutaG': r'\\10.10.10.122\Administracion_AV\01 CONVIVENCIAS\CONVIVENCIAS\00.CNV\Reporte de convivencias\Database\VECL'
    },
    {
        'Desarrollo': 'VMAY',
        'user': 'IECYU101',
        'pass': '3E$b#-fD',
        'host': '201.134.132.136',
        'port': 22,
        'ruta': '/Salida',
        'rutaG': r'\\10.10.10.122\Administracion_AV\01 CONVIVENCIAS\CONVIVENCIAS\00.CNV\Reporte de convivencias\Database\VMAY'
    }
]

# start in
FECHA_CORTE_STR = '01/01/2025'
FECHA_CORTE = datetime.strptime(FECHA_CORTE_STR, '%d/%m/%Y')
print(f'Fecha de corte establecida en: {FECHA_CORTE.strftime("%d-%m-%Y")}')

# bucle connection
for conn in connections:
    process_connection(conn, FECHA_CORTE)
