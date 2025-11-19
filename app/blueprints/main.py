from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from models import db, MensajeContacto
from forms import ContactoForm
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('main/home.html', now=datetime.now())

@main_bp.route('/servicios')
def servicios():
    return render_template('main/servicios.html', now=datetime.now())

@main_bp.route('/precios')
def precios():
    return render_template('main/precios.html', now=datetime.now())

@main_bp.route('/cobertura')
def cobertura():
    return render_template('main/cobertura.html', now=datetime.now())

@main_bp.route('/sobre')
def sobre():
    return render_template('main/sobre.html', now=datetime.now())

@main_bp.route('/faq')
def faq():
    return render_template('main/faq.html', now=datetime.now())

@main_bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactoForm()
    if form.validate_on_submit():
        # Guardar mensaje en BD
        mensaje = MensajeContacto(
            nombre=form.nombre.data,
            email=form.email.data,
            asunto=form.asunto.data,
            mensaje=form.mensaje.data
        )
        db.session.add(mensaje)
        db.session.commit()
        
        # Enviar email
        try:
            from flask import current_app
            msg = Message(
                subject=f'Nuevo mensaje de contacto: {form.asunto.data}',
                recipients=['info@veterinaria.com'],
                body=f'''
Nuevo mensaje de contacto recibido:

Nombre: {form.nombre.data}
Email: {form.email.data}
Asunto: {form.asunto.data}

Mensaje:
{form.mensaje.data}
'''
            )
            current_app.extensions['mail'].send(msg)
            flash('Tu mensaje ha sido enviado correctamente. Te contactaremos pronto.', 'success')
        except Exception as e:
            print(f'Error enviando email: {e}')
            flash('Tu mensaje ha sido guardado, pero hubo un problema enviando el email. Te contactaremos pronto.', 'warning')
        
        return redirect(url_for('main.contacto'))
    
    return render_template('main/contacto.html', form=form, now=datetime.now())

@main_bp.route('/privacidad')
def privacidad():
    return render_template('main/privacidad.html', now=datetime.now())

@main_bp.route('/cookies')
def cookies():
    return render_template('main/cookies.html', now=datetime.now())

@main_bp.route('/legal')
def legal():
    return render_template('main/legal.html', now=datetime.now())