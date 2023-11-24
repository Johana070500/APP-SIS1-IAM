from flask          import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt   import bcrypt
from werkzeug.utils import secure_filename
from datetime       import datetime
import psycopg2
import os
iam = Flask(__name__)
iam.secret_key = 'udyieyeiyeiey9838y3iyodh$_%'
conn = psycopg2.connect(dbname="iam",
                        user="postgres",
                        password="1316160727Pg",
                        host="localhost",
                        port=5432)
iam.config['ESTUDIOS'] = './static/estudios/'
#------------------------------------------------------------ RENDER PAGINA DE LOGIN -----------------------------------------------------------------------------
@iam.route('/')
def index():
    if session.get('admin'):
        return redirect(url_for('iniAdmin'))
    elif session.get('medico'):
        return redirect(url_for('pacientes'))
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
        correo   =  request.form['email']
        clave    =  request.form['password'].encode('utf-8')
        selAdmin =  conn.cursor()
        selAdmin.execute("SELECT correo, contrasena, id_administrador FROM administrador WHERE correo=%s", (correo,))
        a = selAdmin.fetchone()
        selAdmin.close()
        if a is not None:
            if bcrypt.hashpw(clave, a[1].encode('utf-8')) == a[1].encode('utf-8'):
                session['admin']   =   a[2]
                return redirect( url_for('index'))
            else:
                flash('Tu contrasena es incorrecta','warning')
                return redirect (request.url)
        else:
            selEmpleado = conn.cursor()
            selEmpleado.execute("SELECT id_medico, correo, contrasena FROM medico WHERE correo = %s", (correo,))
            e = selEmpleado.fetchone()
            selEmpleado.close()
            if e is not None:
                if bcrypt.hashpw(clave, e[2].encode('utf-8')) == e[2].encode('utf-8'):
                    session['medico'] = e[0]
                    return redirect (url_for('index'))
                else:
                    flash('Contraseña incorrecta','warning')
                    return redirect (request.url)
            flash('El usuario no existe')
            return redirect (request.url)
    else:
        return render_template('login.html')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
    

#   PACIENTES
@iam.route('/pacientes', methods=['GET'])
def pacientes():
    if session.get('medico'):
        sql = ("""SELECT id_paciente, nombre, apellido, edad FROM paciente ORDER BY apellido""")
        sel = conn.cursor()
        sel.execute(sql,)
        paciente = sel.fetchall()
        sel.close()
        return render_template("pacientes.html", pacientes=paciente)
    else:
        return redirect(url_for('logout'))

#   AGREGAR PACIENTE
@iam.route('/agregarPaciente', methods=['POST'])
def agregarPaciente():
    if session.get('medico'):
        nombre      = request.form["nombre"]
        apellido    = request.form["apellido"]
        edad        = request.form["edad"]
        sql         = ("""INSERT INTO paciente (nombre, apellido, edad) VALUES (%s,%s,%s)""")
        dat         = (nombre, apellido, edad)
        add         = conn.cursor()
        add.execute(sql, dat)
        flash("Paciente creado exitosamente",'success')
        return redirect(url_for('pacientes'))
    else:
        return redirect(url_for(''))
#   ------------------------------------------------------------------------------------------------------   
#   MOD INFO PACIENTE
@iam.route('/modificarPaciente', methods=['POST'])
def modificarPaciente():
    if session.get('medico'):
        paciente    = request.form["id"]
        nombre      = request.form["nombre"]
        apellido    = request.form["apellido"]
        edad        = request.form["edad"]
        sql         = ("""UPDATE paciente SET nombre=%s, apellido=%s, edad=%s WHERE id_paciente=%s""")
        dat         = (nombre, apellido, edad, paciente)
        mod         = conn.cursor()
        mod.execute(sql, dat)
        conn.commit()
        mod.close()
        flash('Paciente modificado exitosamente', 'success')
        return redirect(url_for('pacientes'))
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
        paciente    = request.form['id']
        sql         = (""" DELETE FROM paciente WHERE id_paciente=%s""")
        dat         = (paciente,)
        delete      = conn.cursor()
        delete.execute(sql, dat)
        conn.commit()
        delete.close()
        flash('Paciente eliminado exitosamente','success')
        return redirect(url_for('pacientes'))
    else:
        return redirect(url_for('logout'))
#----------------------------------------------------------------------------------------------------------

# MEDICOS 
@iam.route('/iniAdmin', methods=["GET"])
def iniAdmin():
    if session.get('admin'):
        sql = ("""SELECT id_medico, nombre, apellido, cedula, correo FROM medico""")
        sel = conn.cursor()
        sel.execute(sql,)
        medicos = sel.fetchall()
        sel.close()
        return render_template("iniadmin.html", medicos=medicos)
    else:
        return redirect(url_for('logout'))
#-----------------------------------------------------------------------------------------------------------
@iam.route('/agregarMedico', methods=['POST'])
def agregarMedico():
    if session.get('admin'):
        nombre      = request.form['nombre']
        apellido    = request.form['apellido']   
        cedula      = request.form['cedula']
        correo      = request.form['correo']
        contrasena  = request.form['contrasena'].encode('utf-8')
        cifrar      = bcrypt.hashpw(contrasena,bcrypt.gensalt())
        sql         = """INSERT INTO medico (nombre, apellido, cedula, correo, contrasena) VALUES (%s,%s,%s,%s,%s)"""
        dat         = (nombre, apellido, cedula, correo, cifrar)
        insert      = conn.cursor()
        insert.execute(sql, dat)
        conn.commit()
        insert.close()
        flash('Medico agregado con exito','success')
        return redirect(url_for('iniAdmin'))
    else:
        return redirect(url_for('logout'))
#-----------------------------------------------------------------------------------------------------------
#   MOD INFO MEDICO
@iam.route('/modificarMedico', methods=['POST'])
def modificarMedico():
    if session.get('admin'):
        medico      = request.form['id']
        nombre      = request.form['nombre']
        apellido    = request.form['apellido']   
        cedula      = request.form['cedula']
        correo      = request.form['correo']
        sql         = (""" UPDATE medico SET nombre=%s, apellido=%s, cedula=%s, correo=%s WHERE id_medico=%s""")
        dat         = (nombre, apellido, cedula, correo, medico)
        update      = conn.cursor()
        update.execute(sql, dat)
        conn.commit()
        update.close()
        flash('Información de medico actualizada con exito', 'success')
        return redirect(url_for('iniAdmin'))
    else:
        return redirect(url_for('logout'))
#-----------------------------------------------------------------------------------------------------------
#   MOD CONTRASENA
@iam.route('/modificarContrasena', methods=['POST'])
def modificarContrasena():
    if session.get('admin') or session.get('medico'):
        medico      = request.form['id']
        contrasena  = request.form['password'].encode('utf-8')
        cifrar      = bcrypt.hashpw(contrasena, bcrypt.gensalt())
        sql         = (""" UPDATE medico SET contrasena=%s WHERE id_medico=%s""")
        dat         = (cifrar, medico)
        update      = conn.cursor()
        update.execute(sql, dat)
        conn.commit()
        update.close()
        flash('Se ha actualizado exitosamente la contrasena','success')
        return redirect(url_for('iniAdmin'))
    else:
        return redirect(url_for('logout'))
#-----------------------------------------------------------------------------------------------------------
@iam.route('/eliminarMedico', methods=['POST'])
def eliminarMedico():
    if session.get('admin'):
        medico  = request.form['id']
        sql     = (""" DELETE FROM medico WHERE id_medico=%s """)
        dat     = (medico)
        delete  = conn.cursor()
        delete.execute(sql, dat)
        conn.commit()
        delete.close()
        flash('Medico eliminado exitosamente','success')
        return redirect(url_for('iniAdmin'))
    else:
        return redirect(url_for('logout'))
#-----------------------------------------------------------------------------------------------------------

# ADMINISTRADOR
@iam.route('/Administradores', methods=['GET'])
def Administradores():
    if session.get('admin'):
        sql = ( """ SELECT id_administrador, correo, contrasena FROM administrador """ )
        sel = conn.cursor()
        sel.execute(sql,)
        admins = sel.fetchall()
        sel.close()
        return render_template('administradores.html', admins=admins)
    else:
        return redirect(url_for('logout'))
#   AGREGAR
@iam.route('/agregarAdministrador', methods=['POST'])
def agregarAdministrador():
    if session.get('admin'):
        correo      = request.form['correo']
        contrasena  = request.form['contrasena'].encode('utf-8')
        cifrar      = bcrypt.hashpw(contrasena, bcrypt.gensalt())
        sql         = (""" INSERT INTO administrador (correo, contrasena) VALUES (%s,%s)""")
        dat         = (correo, cifrar)
        insert      = conn.cursor()
        insert.execute(sql, dat)
        conn.commit()
        insert.close()
        flash('Administrador agregado exitosamente','success')
        return redirect(url_for('Administradores'))
    else:
        return redirect(url_for('logout'))
#---------
#   EDITAR ADMIN
@iam.route('/modificarAdmin', methods=['POST'])
def modificarAdmin():
    if session.get('admin'):
        admin   = request.form['id']
        correo  = request.form['correo']
        sql     = (""" UPDATE administrador SET correo=%s WHERE id_administrador=%s """)
        dat     = (correo,admin)
        update  = conn.cursor()
        update.execute(sql,dat)
        conn.commit()
        update.close()
        flash('Cambios en administrador realizado exitosamente','success')
        return redirect(url_for('Administradores'))
    else:
        return redirect(url_for('logout'))
#   EDITAR CONTRASEÑA ADMIN
@iam.route('/modificarContrasenaAdmin', methods=['POST'])
def modificarContrasenaAdmin():
    if session.get('admin'):
        admin       = request.form['id']
        password    = request.form['contrasena'].encode('utf-8')
        cifrar      = bcrypt.hashpw(password, bcrypt.gensalt())
        sql         = ( """UPDATE administrador SET contrasena=%s WHERE id_administrador=%s""" )
        dat         = (cifrar, admin)
        update      = conn.cursor()
        update.execute(sql,dat)
        conn.commit()
        update.close()
        flash('Constaseña modificada exitosamente','success')
        return redirect(url_for('Administradores'))
    else:
        return redirect(url_for('logout'))
#   ELIMINAR ADMIN
@iam.route('/eliminarAdmin', methods=['POST'])
def eliminarAdmin():
    if session.get('admin'):
        admin   = request.form['id']
        sql     = (""" DELETE FROM administrador WHERE id_administrador=%s """)
        dat     = (admin)
        delete  = conn.cursor()
        delete.execute(sql, dat)
        conn.commit()
        delete.close()
        flash('Administrador eliminado exitosamente','success')
        return redirect(url_for('Administradores'))
    else:
        return redirect(url_for('logout'))
#   Vista paciente
@iam.route('/paciente/<string:id_paciente>',methods=['GET'])
def paciente(id_paciente):
    if session.get('medico'):
        sql_paciente    = (""" SELECT nombre, apellido, edad FROM paciente WHERE id_paciente=%s""")
        select_db       = conn.cursor()
        select_dat      = (id_paciente)
        select_db.execute(sql_paciente, select_dat)
        info_p  = select_db.fetchone()
        sql_paciente    = (""" SELECT id_medicina, dosis, nombre_medicina, fecha_inicio, fecha_fin FROM medicinas WHERE id_paciente=%s """)
        select_db.execute(sql_paciente, select_dat)
        medicinas       = select_db.fetchall()
        sql_paciente    = (""" SELECT id_estudio, nombre_archivo, descripcion FROM estudios WHERE id_paciente=%s """)
        select_db.execute(sql_paciente, select_dat)
        estudios = select_db.fetchall()
        select_db.close()
        return render_template("paciente.html", info_p=info_p, m=medicinas, e=estudios, id=id_paciente)
    else:
        return redirect(url_for('logout'))
#   Agregar medicina
@iam.route('/addMedicina', methods=['POST'])
def addMedicina():
    if session.get('medico'):
        id_paciente = request.form['id_paciente']
        nombre_m    = request.form['nombre_m']
        dosis_m     = request.form['dosis_m']
        inicio_m    = request.form['inicio_m']
        fin_m       = request.form['fin_m']
        sql         = (""" INSERT INTO medicinas (id_paciente, dosis, nombre_medicina, fecha_inicio, fecha_fin) VALUES (%s,%s,%s,%s,%s) """)
        dat         = (id_paciente, dosis_m, nombre_m, inicio_m, fin_m)
        db          = conn.cursor()
        db.execute(sql, dat)
        conn.commit()
        db.close()
        flash('Medicina agregada al historial','success')
        return redirect(url_for('paciente', id_paciente=id_paciente ))
    else:
        return redirect(url_for('logout'))
#   Editar medicina
@iam.route('/editM',methods=['POST'])
def edit():
    if session.get('medico'):
        id_paciente = request.form['id_paciente']
        id_medicina = request.form['id_medicina']
        nombre_m    = request.form['nombre_m']
        dosis_m     = request.form['dosis_m']
        inicio_m    = request.form['inicio_m']
        fin_m       = request.form['fin_m']
        sql = (""" UPDATE medicinas SET dosis=%s,nombre_medicina=%s,fecha_inicio=%s,fecha_fin=%s WHERE id_medicina=%s """)
        dat = (dosis_m, nombre_m, inicio_m, fin_m, id_medicina)
        db  = conn.cursor()
        db.execute(sql,dat)
        conn.commit()
        db.close()
        flash('Medicina actualizada exitosamente','success')
        return redirect(url_for('paciente',id_paciente=id_paciente))
    else:
        return redirect(url_for('logout'))
#   Agregar archivo
@iam.route('/addE',methods=['POST'])
def addE():
    if session.get('medico'):
        id_paciente = request.form['id_paciente']
        archivo     = request.files['archivo']
        descripcion = request.form['descripcion']
        new_file    = secure_filename(archivo.filename)
        #   GUARDAMOS ARCHIVO
        archivo.save(os.path.join(iam.config['ESTUDIOS'], new_file))
        #   GENERAMOS NUEVO NOMBRE DE ARCHIVO
        nombre = ""
        parte1 = datetime.now()
        extension = new_file.split(".")
        nombre += parte1.strftime('%d-%m-%Y_%H_%M_%S')
        nombre += '.'
        nombre += extension[1]
        #   renombramos archivo
        os.rename(os.path.join(iam.config['ESTUDIOS'], new_file), os.path.join(iam.config['ESTUDIOS'],nombre))
        sql = (""" INSERT INTO estudios (id_paciente, nombre_archivo, descripcion) VALUES (%s,%s,%s) """)
        dat = (id_paciente, nombre, descripcion)
        db  = conn.cursor()
        db.execute(sql, dat)
        conn.commit()
        db.close()
        flash('Estudio agregado con exito','success')
        return redirect(url_for('paciente', id_paciente=id_paciente))
    else:
        return redirect(url_for('logout'))
#   Eliminar estudio
@iam.route('/deleteE',methods=['POST'])
def deleteE():
    if session.get('medico'):
        id_paciente = request.form['id_paciente']
        id_estudio  = request.form['id_estudio']
        nombre      = request.form['nombre_e']
        sql = (""" DELETE FROM estudios WHERE id_estudio=%s """)
        dat = (id_estudio,)
        db  = conn.cursor()
        db.execute(sql, dat)
        conn.commit()
        db.close()
        #   Eliminar archivo fisico
        os.remove(os.path.join(iam.config['ESTUDIOS'], nombre))
        flash('Se elimino con exito el estudio','success')
        return redirect(url_for('paciente',id_paciente=id_paciente))
    else:
        return redirect(url_for('logout'))
if __name__ == '__main__':
    iam.run(port=3000,debug=True)