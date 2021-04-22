from flask import render_template, request, url_for, redirect, session
from src import app
from src.models.links import link

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('inicio.html')
    
    link_enviado=request.form.get('link')
    model_link=link()

    # renviamos el link y recibimos un codigo
    if 'usuario' in session:
        link_acortado=model_link.guardar_link(link_enviado, session['usuario']['id'])
    else: 
        link_acortado=model_link.guardar_link(link_enviado)

    # con el codigo recibido le añadimos la ruta principal
    link_acortado = "http://localhost:5000/" + link_acortado

        
    return render_template('inicio.html', link_acortado=link_acortado)

@app.route('/<codigo>')
def shortLink(codigo):
    model_link=link()
    link_guardado = model_link.link_guardado(codigo)

    # como se retorna una tupla solo necesitamos el valor de la posicion 0
    link_guardado = link_guardado[0]

    return redirect(link_guardado)