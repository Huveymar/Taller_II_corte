from flask import render_template, request, url_for, redirect, session
from src import app
from src.models.usuarios import usuario
from src.configs.email import mail
from flask_mail import Mail, Message

@app.route('/registrar-usuario', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'GET':
        return render_template('registro_usuario.html')
    
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')

    with app.app_context():
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[email], # replace with your email for testing
                      body="This is a test email I sent with Gmail and Python!",
                      html="<p>Para registrarte has click <a href='http://localhost:5000/confirmar-usuario/"+email+"'>Aqui</a></p>")
        mail.send(msg)

    model_usuario = usuario()
    model_usuario.guardar_usuario(nombre, email, password)

    return redirect(url_for('iniciar_sesion'))

@app.route('/confirmar-usuario/<email>', methods=['GET', 'POST'])
def confirmar_usuario(email):
    model_usuario = usuario()
    model_usuario.fecha_confirmacion(email)

    return redirect(url_for('iniciar_sesion'))

@app.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'GET':
        return render_template('iniciar_sesion.html')
    
    email = request.form.get('email')
    password = request.form.get('password')

    model_usuario = usuario()
    registros = model_usuario.validar_fecha(email)

    if registros == None:
        return render_template('iniciar_sesion.html', error='el correo aun no se registra o digitaste mal los datos')

    if registros[0] == None:
        return render_template('iniciar_sesion.html', error='no se ha confirmado el correo')
    
    registros = model_usuario.validar_usuario(email, password)

    if registros == None:
        return render_template('iniciar_sesion.html', error='contraseña incorrecta')

    session['usuario'] = {
        'id':registros[0],
        'nombre':registros[1],
        'email':email
    }

    print(session['usuario'])

    return redirect(url_for('index'))

@app.route('/cerrar-sesion', methods=['GET', 'POST'])
def cerrar_sesion():
    session.pop('usuario', None)

    return redirect(url_for('index'))

@app.route('/links-usarios', methods=['GET', 'POST'])
def links_usarios():
    model_usuario = usuario()
    links = model_usuario.links_guardados(session['usuario']['id'])

    return render_template('links.html', links=links)

@app.route('/eliminar-link/<id_registro>', methods=['GET', 'POST'])
def eliminar_link(id_registro):
    model_usuario = usuario()
    model_usuario.eliminar_link(id_registro)

    return redirect(url_for('links_usarios'))

@app.route('/editar-link/<id_registro>', methods=['GET', 'POST'])
def editar_link(id_registro):
    model_usuario = usuario()
    links = model_usuario.links_guardados(session['usuario']['id'])
    link_original = ''

    for link in links:
        if link[0] == int(id_registro):
            link_original = link[2]

    if request.method == 'GET':
        return render_template('editar_registro.html', link=link_original, id_registro=id_registro)
    
    link_nuevo = request.form.get('link')

    if link_nuevo == '':
        return render_template('editar_registro.html', link=link_original, id_registro=id_registro, error='el campo no puede estar vacio')

    model_usuario.editar_link(id_registro, link_nuevo)

    return redirect(url_for('links_usarios'))