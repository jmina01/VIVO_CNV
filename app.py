from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import pyodbc
from datetime import datetime
import pdf
app = Flask(__name__)
app.secret_key = "m2Prazlbo$"


@app.route('/pdf/<nombre_cliente>', methods=['GET'])
def generar_pdf(nombre_cliente):
    pdf_buffer = pdf.exportar_pdf_cliente_memoria(nombre_cliente)
    if pdf_buffer:
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"{nombre_cliente}.pdf",
            mimetype='application/pdf'
        )
    else:
        flash("No se pudo generar el PDF para el cliente " + nombre_cliente, "error")
        return redirect(url_for('index'))
    
def get_db_connection():
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=34.45.59.38,1433;"
        "DATABASE=convivencia;"
        "UID=SA;"
        "PWD=Belen117"
    )
    return connection

@app.route('/', methods=['GET'])
def index():
   
    # Si la peticion NO tiene parámetros (URL limpia)
    if not request.args:
        if 'lastSearch' in session:
            try:
                # ultima marca de tiempo de busqueda
                last_search = datetime.fromisoformat(session.pop('lastSearch'))
            except Exception:
                last_search = None
            # Si <2s, se asume que es el redirect
            if last_search is not None and (datetime.now() - last_search).total_seconds() < 2:
                pass  # NO limpiamos
            else:
                # Refresh manual
                session.pop('rows', None)
        else:
            # No hay registro de busqueda reciente → se limpia (si existiera)
            session.pop('rows', None)

    # START SESSION
    if 'rows' not in session:
        session['rows'] = [
            {
                'idCliente': '',
                'nombreCliente': '',
                'Desarrollo': '',
                'Financiamiento': '',
                'idEK': '',
                'Ubicacion': ''
            }
            for _ in range(5)
        ]

    # Si se row y cliente  se procesa la busqueda
    if 'row' in request.args and 'cliente' in request.args:
        try:
            row_num = int(request.args.get('row'))  # 1 or 5
            cliente_query = request.args.get('cliente', '')

            conn = get_db_connection()
            cursor = conn.cursor()
            # Busqueda EXACTA
            sql = """
                SELECT idCliente, nombreCliente, Desarrollo, Financiamiento, idEK, Ubicacion
                FROM clt
                WHERE nombreCliente = ?
            """
            cursor.execute(sql, (cliente_query,))
            result = cursor.fetchone()
            conn.close()

            if result:
                # fila por fila
                session['rows'][row_num - 1] = {
                    'idCliente': result[0],
                    'nombreCliente': result[1],
                    'Desarrollo': result[2],
                    'Financiamiento': result[3],
                    'idEK': result[4],
                    'Ubicacion': result[5]
                }
            else:
                flash("Cliente no encontrado", "error")
        except Exception as e:
            flash("Error en la búsqueda: " + str(e), "error")
        
        # time saver para distinguir redirect vs. refresh manual.
        session['lastSearch'] = datetime.now().isoformat()
        session.modified = True
        #  redirect para limpiar la URL de los parametros.
        return redirect(url_for('index'))

    return render_template('clt/index.html', rows=session['rows'])

if __name__ == '__main__':
    app.run(debug=True)
