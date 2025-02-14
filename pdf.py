# pdf.py
import os
import io
import pyodbc
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
import locale

#DICT1
MAPA_CNV = {
    'ALOJ': {
        'Convivencia': 'CONVIVENCIA ALOJA AC',
        'Correo': 'aloja@convivencia.mx',
        'Telefono': '9981509598',
        'RFC': 'CAL170707ND2',
        'Clabe': '012694001235674002',
        'Cta': '0123567400',
        'Banco': 'BBVA'
    },
    'CENT': {
        'Convivencia': 'ASOCIACION CONVIVENCIA QUINTANA ROO AC',
        'Correo': 'ialva@convivencia.mx',
        'Telefono': '9831131937',
        'RFC': 'ACQ110615BJ3',
        'Clabe': '012691001153123023',
        'Cta': '0115312302',
        'Banco': 'BBVA'
    },
    'ECOZ': {
        'Convivencia': 'CONVIVENCIA EL ENCANTO AC',
        'Correo': 'encantocozumel@convivencia.mx',
        'Telefono': '9871034926',
        'RFC': 'CCA1205151Z0',
        'Clabe': '012694001235673540',
        'Cta': '0123567354',
        'Banco': 'BBVA'
    },
    'PAMA': {
        'Convivencia': 'CONVIVENCIA CANCUN AC',
        'Correo': 'puscanga@convivencia.mx',
        'Telefono': '9984100884',
        'RFC': 'CCA1205151Z0',
        'Clabe': '012691001153121834',
        'Cta': '0115312183',
        'Banco': 'BBVA'
    },
    'PUMA': {
        'Convivencia': 'CONVIVENCIA PLAYA DEL CARMEN AC',
        'Correo': 'convivenciapuma@convivencia.mx',
        'Telefono': '9841833488',
        'RFC': 'CPC130530FE6',
        'Clabe': '012691001154133892',
        'Cta': '0115413389',
        'Banco': 'BBVA'
    },
    'SMAR': {
        'Convivencia': 'CONVIVENCIA MERIDA AC',
        'Correo': 'sanmarcos@convivencia.mx',
        'Telefono': '9997389818',
        'RFC': 'CME120601A5A',
        'Clabe': '012691001153117990',
        'Cta': '0115311799',
        'Banco': 'BBVA'
    },
    'VECL': {
        'Convivencia': 'ASOCIACION CONVIVENCIA TABASCO AC',
        'Correo': 'ghernandez@convivencia.mx',
        'Telefono': '9932001303',
        'RFC': 'ACT110704DLA',
        'Clabe': '012694001235666764',
        'Cta': '0123566676',
        'Banco': 'BBVA'
    },
    'VMAY': {
        'Convivencia': 'CONVIVENCIA YUCATAN AC',
        'Correo': 'vegadelmayab@convivencia.mx',
        'Telefono': '9997389816',
        'RFC': 'CYU120515DA4',
        'Clabe': '012694001235669512',
        'Cta': '0123566951',
        'Banco': 'BBVA'
    },
    'VITA': {
        'Convivencia': 'CONVIVENCIA YUCATAN AC',
        'Correo': 'vegadelmayab@convivencia.mx',
        'Telefono': '9997389816',
        'RFC': 'CYU120515DA4',
        'Clabe': '012694001235669512',
        'Cta': '0123566951',
        'Banco': 'BBVA'
    }
}
#DICT2
MAPA_PRY = {
    'ALOJ': 'ALOJA',
    'CENT': 'CENTENARIO',
    'ECOZ': 'EL ENCANTO COZUMEL',
    'PAMA': 'PARAISO MAYA',
    'PUMA': 'PUERTO MAYA',
    'SMAR': 'SAN MARCOS',
    'VECL': 'EL CIELO',
    'VMAY': 'VEGA DEL MAYAB',
 
}

#QUERY
#VISUAL FUNCTION_SHOW DF

def get_sql_server_connection():
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=34.45.59.38,1433;"
        "DATABASE=convivencia;" 
        "UID=SA;"
        "PWD=Belen117"
    )
    return connection

def obtener_datos_cliente(nombre_cliente: str) -> pd.DataFrame:
    query = """
    SELECT Año, Bimestre, CE, CR
    FROM cnv
    WHERE Cliente = ?
    """
    try:
        with get_sql_server_connection() as conn:
            df = pd.read_sql_query(query, conn, params=(nombre_cliente,))
            return df
    except Exception as e:
        print(f"Error en obtener_datos_cliente: {e}")
        return pd.DataFrame()

#HEADER CREATE DATA
def obtener_encabezado_cliente(nombre_cliente: str) -> dict:
    query = """
    SELECT nombreCliente, Desarrollo, idEK, Ubicacion
    FROM clt
    WHERE nombreCliente = ?
    """
    try:
        with get_sql_server_connection() as conn:
            df = pd.read_sql_query(query, conn, params=(nombre_cliente,))
            if not df.empty:
                row = df.iloc[0]
                return {
                    "nombreCliente": row["nombreCliente"],
                    "Desarrollo": row["Desarrollo"],
                    "idEK": row["idEK"],
                    "Ubicacion": row["Ubicacion"]
                }
            else:
                return None
    except Exception as e:
        print(f"Error en obtener_encabezado_cliente: {e}")
        return None
#FECHA AUTOMATICA
def formatear_fecha_espanol(fecha):
    """
    Formatea una fecha datetime al estilo español (México) sin usar locale.
    Ejemplo de salida: "miércoles, 29 de enero de 2025".
    
    :param fecha: Objeto datetime.
    :return: String con día, número de día, mes y año en español.
    """
  
    dias = ['lunes','martes','miércoles','jueves','viernes','sábado','domingo']
    
    
    meses = [
        'enero','febrero','marzo','abril','mayo','junio',
        'julio','agosto','septiembre','octubre','noviembre','diciembre'
    ]
    
    
    dia_semana = dias[fecha.weekday()]
    
    mes = meses[fecha.month - 1]
    
    
    return f"{dia_semana}, {fecha.day} de {mes} de {fecha.year}"

#CREATE PDF
def exportar_pdf_cliente_memoria(nombre_cliente: str) -> io.BytesIO:
   
    encabezado = obtener_encabezado_cliente(nombre_cliente)
    if not encabezado:
        print(f"No se encontró encabezado para cliente '{nombre_cliente}' en clt.")
        return None
    df = obtener_datos_cliente(nombre_cliente)
    if df.empty:
        print(f"No hay datos en cnv_consult para '{nombre_cliente}'. No se genera PDF.")
        return None

    # check
    for col in ['Año', 'Bimestre', 'CE', 'CR']:
        if col not in df.columns:
            print(f"Falta la columna '{col}' para '{nombre_cliente}'. PDF cancelado.")
            return None

    # MAP
    desarrollo_abreviado = str(encabezado.get('Desarrollo', '')).strip()
    desarrollo_abreviado_upper = desarrollo_abreviado.upper()
    desarrollo_completo = MAPA_PRY.get(
        desarrollo_abreviado_upper,
        desarrollo_abreviado_upper 
    )

    convivencia_info = MAPA_CNV.get(desarrollo_abreviado_upper, {})
    convivencia = convivencia_info.get('Convivencia', desarrollo_completo)
    correo = convivencia_info.get('Correo', '')
    telefono = convivencia_info.get('Telefono', '')
    rfc = convivencia_info.get('RFC', '')
    clabe = convivencia_info.get('Clabe', '')
    cta = convivencia_info.get('Cta', '')
    banco = convivencia_info.get('Banco', '')

    ubicacion = str(encabezado.get('Ubicacion', '')).strip()
    id_ek = str(encabezado.get('idEK', '')).strip()

    # GROUP
    df_grouped = df.groupby(['Año', 'Bimestre']).agg({
        'CE': 'sum',
        'CR': 'sum'
    }).reset_index()
    df_grouped['Diferencia CE-CR'] = df_grouped['CE'] - df_grouped['CR']
    df_grouped = df_grouped.sort_values(['Año', 'Bimestre'])

    total_ce = df_grouped['CE'].sum()
    total_cr = df_grouped['CR'].sum()
    total_diferencia = df_grouped['Diferencia CE-CR'].sum()

    # DF
    data = []
    data.append(['Año', 'Bimestre', 'Cobranza esperada', 'Cobranza real', 'Diferencia cobranza'])
    for _, row in df_grouped.iterrows():
        data.append([
            int(row['Año']),
            int(row['Bimestre']),
            f"${row['CE']:,.2f}",
            f"${row['CR']:,.2f}",
            f"${row['Diferencia CE-CR']:,.2f}"
        ])
    data.append([
        'Total', '',
        f"${total_ce:,.2f}",
        f"${total_cr:,.2f}",
        f"${total_diferencia:,.2f}"
    ])

    #  GUARDADO EN MEMORIA
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=30, leftMargin=30,
        topMargin=30, bottomMargin=18
    )
    elements = []
    styles = getSampleStyleSheet()

    # CUSTOM PDF
    estilo_fecha = ParagraphStyle(
        name='Fecha',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=12,
        leading=14,
        alignment=TA_RIGHT,
        spaceAfter=6
    )
    estilo_encabezado_propietario = ParagraphStyle(
        name='EncabezadoPropietario',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=6
    )
    estilo_encabezado_general = ParagraphStyle(
        name='EncabezadoGeneral',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=6
    )
    estilo_introduccion = ParagraphStyle(
        name='Introduccion',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        spaceAfter=12
    )
    estilo_pie_pagina = ParagraphStyle(
        name='PiePagina',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        spaceBefore=12
    )

    # FECHA 
    fecha_formateada = formatear_fecha_espanol(datetime.now()).capitalize()

    # IMAGENES
    base_imagen_path = os.path.join(os.path.dirname(__file__), 'static', 'img')
    ruta_logo_fijo = os.path.join(base_imagen_path, 'CONVIVENCIA.png')
    ruta_imagen_variable = os.path.join(base_imagen_path, f"{desarrollo_completo}.png")

    try:
        img_logo_fijo = Image(ruta_logo_fijo)
        img_logo_fijo.drawHeight = 1.0 * inch
        img_logo_fijo.drawWidth = 1.0 * inch
    except Exception as ex:
        print(f"Error cargando logo fijo: {ex}")
        img_logo_fijo = Spacer(1, 0.5 * inch)

    try:
        img_variable = Image(ruta_imagen_variable)
        img_variable.drawHeight = 1.0 * inch
        img_variable.drawWidth = 1.6 * inch
    except Exception as ex:
        print(f"Error cargando imagen variable: {ex}")
        img_variable = Spacer(1, 0.5 * inch)

    img_spacer = Spacer(0.2 * inch, 1.0 * inch)

    header_table = Table(
        [
            [img_logo_fijo, img_spacer, img_variable, Paragraph(fecha_formateada, estilo_fecha)]
        ],
        colWidths=[1 * inch, 0.2 * inch, 1 * inch, 4.5 * inch]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (3, 0), (3, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 12))

    # ENCABEZADO
    datos_generales = [
        [Paragraph(f"<b>Propietario:</b> {nombre_cliente}", estilo_encabezado_propietario), ""],
        [Paragraph(f"<b>Ubicación:</b> {ubicacion}", estilo_encabezado_general), ""],
        [Paragraph(f"<b>Desarrollo:</b> {desarrollo_completo}", estilo_encabezado_general), ""],
        [Paragraph(f"<b>ID EK:</b> {id_ek}", estilo_encabezado_general), ""],
    ]
    datos_generales_table = Table(datos_generales, colWidths=[5 * inch, 1.5 * inch])
    datos_generales_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(datos_generales_table)
    elements.append(Spacer(1, 12))

    # INTRO
    introduccion_texto = f"""
    La asociación administradora de las cuotas de sustentabilidad: <b>{convivencia}</b> 
    le informa que la vivienda actualmente presenta un adeudo de: 
    <b><font color='red'>${total_diferencia:,.2f}</font></b>.<br/><br/>

    El cual es necesario cubrir para que la asociación pueda continuar con su labor de 
    mantenimiento de las Áreas Públicas del desarrollo habitacional, 
    que incluyen, entre otros aspectos:<br/><br/>

    1. Barrer las calles.<br/>
    2. Podar las áreas públicas.<br/>
    3. Mantener los jardines de las áreas públicas.<br/>
    4. Promoción de la Cultura Vecinal y Gestión Comunitaria.<br/><br/>

    A continuación, se detalla la tabla de pagos sobre la cobranza esperada 
    y la cobranza real, así como los datos bancarios a los cuales 
    deberá hacer el depósito correspondiente:
    """
    introduccion_paragraph = Paragraph(introduccion_texto, estilo_introduccion)
    elements.append(introduccion_paragraph)
    elements.append(Spacer(1, 24))

    # DF
    table = Table(data, hAlign='LEFT')
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 1), (-1, -2), 'Courier'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 1), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Courier-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 10),
    ])
    table.setStyle(table_style)
    table._argW = [1.1 * inch, 1.1 * inch, 1.7 * inch, 1.7 * inch, 1.7 * inch]
    elements.append(table)
    elements.append(Spacer(1, 24))

    # FOOT
    pie_pagina_texto = f"""
    <b>El pago deberá hacerse a nombre de:</b> {convivencia}<br/><br/>
    <b>Banco:</b> {banco}<br/><br/>
    <b>Cta:</b> {cta}<br/><br/>
    <b>Clabe interbancaria:</b> {clabe}<br/><br/>
    <b>R.F.C:</b> {rfc}<br/><br/>
    Es necesario compartir el comprobante de pago a Convivencia 
    vía WhatsApp o correo electrónico. 
    Por este medio se le enviará su comprobante oficial del pago.<br/><br/>
    <b>Número de teléfono:</b> {telefono}<br/><br/>
    <b>Correo electrónico:</b> {correo}<br/><br/>
    """
    pie_pagina_paragraph = Paragraph(pie_pagina_texto, estilo_pie_pagina)
    elements.append(pie_pagina_paragraph)

    # BUFFER
    try:
        doc.build(elements)
        buffer.seek(0)
        print(f"PDF generado para '{nombre_cliente}' en memoria")
        return buffer
    except Exception as e:
        print(f"Error al generar el PDF para '{nombre_cliente}': {e}")
        return None

