from flask          import Flask, render_template, request, redirect, url_for, session, flash, make_response, send_file
from flask_bcrypt   import bcrypt
from flask_weasyprint import HTML, render_pdf
from werkzeug.utils import secure_filename
from datetime       import datetime
import psycopg2
import os
iam = Flask(__name__)
iam.secret_key = 'udyieyeiyeiey9838y3iyodh$_%'
conn = psycopg2.connect(dbname="iam",
                        user="postgres",
                        password="Ces@rLomeli",
                        host="localhost",
                        port=5433)
iam.config['ESTUDIOS'] = './static/estudios/'
#------------------------------------------------------------ RENDER PAGINA DE LOGIN -----------------------------------------------------------------------------
@iam.route('/')
def index():
    if session.get('IDadmin') or session.get('Nombre'):
        return redirect(url_for('Inicio'))
    else:
        return render_template('login.html')
#------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------- SALIR DE LA SESION ---------------------------------------------------------------------------------
@iam.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect (url_for('index'))
#------------------------------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------- INICIO DE SESION ---------------------------------------------------------------------------------------------
@iam.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo   =  request.form['correo']
        clave    =  request.form['contrasena'].encode('utf-8')
        selAdmin =  conn.cursor()
        selAdmin.execute("SELECT correo, contrasena, id_administrador FROM administrador WHERE correo=%s", (correo,))
        a = selAdmin.fetchone()
        selAdmin.close()
        if a is not None:
            if bcrypt.hashpw(clave, a[1].encode('utf-8')) == a[1].encode('utf-8'):
                session['admin']   =   a[2]
                flash('Se inicio sesion de administrador')
                return redirect( url_for('index'))
            else:
                flash('Tu contrasena es incorrecta')
                return redirect (request.url)
        else:
            selEmpleado = conn.cursor()
            selEmpleado.execute("SELECT id_medico, correo, contrasena FROM medico WHERE correo = %s", (correo,))
            e = selEmpleado.fetchone()
            selEmpleado.close()
            if e is not None:
                if bcrypt.hashpw(clave, e[2].encode('utf-8')) == e[2].encode('utf-8'):
                    session['medico'] = e[0]
                    flash('Se ha iniciado sesion medico')
                    return redirect (url_for('index'))
                else:
                    flash('Contraseña incorrecta')
                    return redirect (request.url)
            flash('El usuario no existe')
            return redirect (request.url)
    else:
        return render_template('login.html')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

#   PACIENTES
@iam.route('/agregarPaciente', methods=['POST'])
def agregarPaciente():
    if session.get('medico'):
        nombre      = request.form[""]
        apellido    = request.form[""]
        edad        = request.form[""]
        sql         = ("""INSERT INTO paciente (nombre, apellido, edad) VALUES (%s,%s,%s)""")
        dat         = (nombre, apellido, edad)
        add         = conn.cursor()
        add.execute(sql, dat)
        flash("Paciente creado exitosamente")
        return redirect(url_for(''))
    else:
        return redirect(url_for(''))
#   ------------------------------------------------------------------------------------------------------   
#   MOD INFO PACIENTE
@iam.route('/modificarPaciente', methods=['POST'])
def modificarPaciente():
    if session.get('medico'):
        paciente    = request.form['']
        nombre      = request.form[""]
        apellido    = request.form[""]
        edad        = request.form[""]
        sql         = ("""UPDATE paciente SET nombre=%s, apellido=%s, edad=%s WHERE id_paciente=%s""")
        dat         = (nombre, apellido, edad, paciente)
        mod         = conn.cursor()
        mod.execute(sql, dat)
        conn.commit()
        mod.close()
        flash('Paciente modificado exitosamente', 'success')
        return redirect(url_for(''))
    else:
        return redirect(url_for('logout'))
#---------------------------------------------------------------------------------------------------------
@iam.route('/agregarMedicina', methods=['POST'])
def agregarMedicina():
    if session.get('medico'):
        paciente        = request.form['']
        dosis           = request.form['']
        nombre_medicina = request.form['']
        fecha_inicio    = request.form['']
        fecha_fin       = request.form['']
        sql             = """INSERT INTO medicinas (id_paciente, dosis, nombre_medicina, fecha_inicio, fecha_fin) VALUES (%s,%s,%s,%s,%s)"""
        dat             = (paciente, dosis, nombre_medicina, fecha_inicio, fecha_fin)
        insert          = conn.cursor()
        insert.execute(sql, dat)
        conn.commit()
        insert.close()
        flash('Medicina agregada con exito', 'success')
        return
    else:
        return redirect(url_for('logout'))
#---------------------------------------------------------------------------------------------------------
#   MOD MEDICINA
@iam.route('/modificarMedicina', methods=['POST'])
def modificarMedicina():
    if session.get('medico'):
        paciente            = request.form['']
        dosis               = request.form['']
        nombre_medicina     = request.form['']
        fecha_inicio        = request.form['']
        fecha_fin           = request.form['']
        sql                 = (""" UPDATE medicinas SET dosis=%s, nombre_medicina=%s, fecha_inicio=%s, fecha_fin=%s WHERE id_paciente=%s """)
        dat                 = (paciente, dosis, nombre_medicina, fecha_inicio, fecha_fin)
        update              = conn.cursor()
        update.execute(sql, dat)
        conn.commit()
        update.close()
        flash('Se ha cambiado exitosamente la medicación', 'success')
        return redirect(url_for(''))
    else:
        return redirect(url_for('logout'))
#--------------------------------------------------------------------------------------------------------
@iam.route('/agregarEstudio', methods=['POST'])
def agregarEstudio():
    if session.get('medico'):
        paciente    = request.form['']
        archivo     = request.files['']
        archivo_nvo = secure_filename(archivo.filename)
        try:
            archivo.save(os.path.join(iam.config['ESTUDIOS'], archivo_nvo))
        except FileExistsError:
            os.remove(os.path.join(iam.config['ESTUDIOS'], archivo_nvo))
        sql     = ("""INSERT INTO estudios (id_paciente, nombre_archivo) VALUES (%s,%s)""")
        dat     = (paciente, archivo_nvo)
        insert  = conn.cursor()
        insert.execute(sql,dat)
        conn.commit()
        insert.close()
        flash('Se ha agregado el estudio al paciente existosamente','success')
        return redirect(url_for(''))
    else:
        return redirect(url_for('logout'))
#---------------------------------------------------------------------------------------------------------
@iam.route('/agregarDiagnostico', methods=['POST'])
def agregarDiagnostico():
    if session.get('medico'):
        paciente            = request.form['']
        fecha_diagnosis     = request.form['']
        estatus_paciente    = request.form['']
        notas               = request.form['']
        diagnostico         = request.form['']
        sql                 = (""" INSERT INTO diagnosis (id_medico, id_paciente, fecha_diagnosis, estatus_paciente, notas, diagnositco) VALUES (%s,%s,%s,%s,%s,%s) """)
        dat                 = (session['medico'], paciente, fecha_diagnosis, estatus_paciente, notas, diagnostico, )
        insert              = conn.cursor()
        insert.execute(sql, dat)
        conn.commit()
        insert.close()
        flash('Diagnostico agregado exitosamente', 'success')
        return redirect(url_for(''))
    else:
        return redirect(url_for('logout'))
#----------------------------------------------------------------------------------------------------------
@iam.route('/eliminarPaciente', methods=['POST'])
def eliminarPaciente():
    if session.get('medico'):
        paciente    = request.form['']
        sql         = (""" DELETE FROM paciente WHERE id_paciente=%s""")
        dat         = (paciente,)
        delete      = conn.cursor()
        delete.execute(sql, dat)
        conn.commit()
        delete.close()
        flash('Paciente eliminado exitosamente','success')
        return redirect(url_for(''))
    else:
        return redirect(url_for('logout'))
#----------------------------------------------------------------------------------------------------------

# MEDICOS 
@iam.route('/agregarMedico', methods=['POST'])
def agregarMedico():
    if session.get('admin'):
        nombre      = request.form['']
        apellido    = request.form['']   
        cedula      = request.form['']
        correo      = request.form['']
        contrasena  = request.form[''].encode('utf-8')
        cifrar      = bcrypt.hashpw(contrasena,bcrypt.gensalt())
        sql         = """INSERT INTO medico (nombre, apellido, cedula, correo, contrasena) VALUES (%s,%s,%s,%s)"""
        dat         = (nombre, apellido, cedula, correo, cifrar)
        insert      = conn.cursor()
        insert.execute(sql, dat)
        conn.commit()
        insert.close()
        flash('Medico agregado con exito','success')
        return redirect(url_for('medicos'))
    else:
        return redirect(url_for('logout'))
#-----------------------------------------------------------------------------------------------------------
#   MOD INFO MEDICO
@iam.route('/modificarMedico', methods=['POST'])
def modificarMedico():
    if session.get('admin'):
        medico      = request.form['']
        nombre      = request.form['']
        apellido    = request.form['']   
        cedula      = request.form['']
        correo      = request.form['']
        sql         = (""" UPDATE medico SET nombre=%s, apellido=%s, cedula=%s, correo=%s WHERE id_medico=%s""")
        dat         = (nombre, apellido, cedula, correo, medico)
        update      = conn.cursor()
        update.execute(sql, dat)
        conn.commit()
        update.close()
        flash('Información de medico actualizada con exito', 'success')
        return redirect(url_for(''))
    else:
        return redirect(url_for('logout'))
#-----------------------------------------------------------------------------------------------------------
#   MOD CONTRASENA
@iam.route('/modificarContrasena', methods=['POST'])
def modificarContrasena():
    if session.get('admin') or session.get('medico'):
        medico      = request.form['']
        contrasena  = request.form[''].encode('utf-8')
        cifrar      = bcrypt.hashpw(contrasena, bcrypt.gensalt())
        sql         = (""" UPDATE medico SET contrasena=%s WHERE id_medico=%s""")
        dat         = (medico, cifrar)
        update      = conn.cursor()
        update.execute(sql, dat)
        conn.commit()
        update.close()
        flash('Se ha actualizado exitosamente la contrasena','success')
        return redirect(url_for(''))
    else:
        return redirect(url_for('logout'))
#-----------------------------------------------------------------------------------------------------------
@iam.rouet('/eliminarMedico', methods=['POST'])
def eliminarMedico():
    if session.get('admin'):
        medico  = request.form['']
        sql     = (""" DELETE FROM medicos WHERE id_medico=%s """)
        dat     = (medico)
        delete  = conn.cursor()
        delete.execute(sql, dat)
        conn.commit()
        delete.close()
        flash('Medico eliminado exitosamente','success')
        return redirect(url_for(''))
    else:
        return redirect(url_for('logout'))
#-----------------------------------------------------------------------------------------------------------

# ADMINISTRADOR
@iam.route('/agregarAdministrador', methods=['POST'])
def agregarAdministrador():
    if session.get('admin'):
        correo      = request.form['']
        contrasena  = request.form[''].encode('urf-8')
        cifrar      = bcrypt.hashpw(contrasena, bcrypt.gensalt())
        sql         = (""" INSERT INTO administrado (correo, contrasena) VALUES (%s,%s)""")
        dat         = (correo, cifrar)
        insert      = conn.cursor()
        insert.execute(sql, dat)
        conn.commit()
        insert.close()
        flash('Administrador agregado exitosamente','success')
        return redirect(url_for(''))
    else:
        return redirect(url_for('logout'))

if __name__ == '__main__':
    iam.run(port=3000,debug=True)