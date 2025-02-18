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
    # Lógica de manejo de la sesión y búsqueda...
    if not request.args:
        if 'lastSearch' in session:
            try:
                last_search = datetime.fromisoformat(session.pop('lastSearch'))
            except Exception:
                last_search = None
            if last_search is not None and (datetime.now() - last_search).total_seconds() < 2:
                pass
            else:
                session.pop('rows', None)
        else:
            session.pop('rows', None)

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

    if 'row' in request.args and 'cliente' in request.args:
        try:
            row_num = int(request.args.get('row'))
            cliente_query = request.args.get('cliente', '')

            conn = get_db_connection()
            cursor = conn.cursor()
            sql = """
                SELECT idCliente, nombreCliente, Desarrollo, Financiamiento, idEK, Ubicacion
                FROM clt
                WHERE nombreCliente = ?
            """
            cursor.execute(sql, (cliente_query,))
            result = cursor.fetchone()
            conn.close()

            if result:
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
        
        session['lastSearch'] = datetime.now().isoformat()
        session.modified = True
        return redirect(url_for('index'))

    return render_template('clt/index.html', rows=session['rows'])




@app.route('/addCL.html', methods=['GET'])
def new_clt():
    return render_template('addCL.html')

@app.route('/', methods=['GET'])
def principal():
    return render_template('/')

@app.route('/editMov.html', methods=['GET'])
def edit_Mov():
    return render_template('editMov.html')

@app.route('/addRE.html', methods=['GET'])
def add_RE():
    return render_template('addRE.html')

@app.route('/addIT.html', methods=['GET'])
def add_IT():
    return render_template('addIT.html')

@app.route('/addCR.html', methods=['GET'])
def add_CR():
    return render_template('addCR.html')

@app.route('/addCE.html', methods=['GET'])
def add_CE():
    return render_template('addCE.html')

@app.route('/addAT.html', methods=['GET'])
def add_AT():
    return render_template('addAT.html')


if __name__ == '__main__':
    app.run(debug=True)

