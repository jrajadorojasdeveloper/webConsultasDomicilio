from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_mail import Message
from models import db, Cita
from forms import CitaForm
from datetime import datetime

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/', methods=['GET', 'POST'])
def nueva_cita():
    form = CitaForm()
    if form.validate_on_submit():
        # Crear nueva cita
        cita = Cita(
            nombre=form.nombre.data,
            email=form.email.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data,
            localidad=form.localidad.data,
            cp=form.cp.data,
            mascota_tipo=form.mascota_tipo.data,
            mascota_edad=form.mascota_edad.data,
            motivo=form.motivo.data,
            zona=form.zona.data,
            fecha_pref=form.fecha_pref.data,
            hora_pref=form.hora_pref.data
        )
        
        db.session.add(cita)
        db.session.commit()
        
        # Enviar emails de confirmación
        try:
            # Email al cliente
            msg_cliente = Message(
                subject='Confirmación de solicitud de cita - Veterinaria a Domicilio',
                recipients=[form.email.data],
                body=f'''
Estimado/a {form.nombre.data},

Hemos recibido tu solicitud de cita veterinaria a domicilio con los siguientes datos:

• Fecha solicitada: {form.fecha_pref.data.strftime('%d/%m/%Y')}
• Hora solicitada: {form.hora_pref.data.strftime('%H:%M')}
• Dirección: {form.direccion.data}, {form.localidad.data} ({form.cp.data})
• Mascota: {form.mascota_tipo.data}
• Motivo: {form.motivo.data}

Te contactaremos en las próximas 24 horas para confirmar la cita y coordinar los detalles.

Gracias por confiar en nosotros para el cuidado de tu mascota.

Saludos cordiales,
Veterinaria a Domicilio
'''
            )
            
            # Email al admin
            msg_admin = Message(
                subject=f'Nueva cita solicitada - {form.nombre.data}',
                recipients=['info@veterinaria.com'],
                body=f'''
Nueva solicitud de cita recibida:

Cliente: {form.nombre.data}
Email: {form.email.data}
Teléfono: {form.telefono.data}
Dirección: {form.direccion.data}, {form.localidad.data} ({form.cp.data})
Zona: {form.zona.data}

Mascota: {form.mascota_tipo.data} - {form.mascota_edad.data}
Motivo: {form.motivo.data}

Fecha solicitada: {form.fecha_pref.data.strftime('%d/%m/%Y')}
Hora solicitada: {form.hora_pref.data.strftime('%H:%M')}

ID de cita: {cita.id}
'''
            )
            
            current_app.extensions['mail'].send(msg_cliente)
            current_app.extensions['mail'].send(msg_admin)
            
            flash('Tu solicitud de cita ha sido enviada correctamente. Te contactaremos pronto para confirmar.', 'success')
        except Exception as e:
            print(f'Error enviando emails: {e}')
            flash('Tu cita ha sido registrada, pero hubo un problema enviando el email de confirmación. Te contactaremos pronto.', 'warning')
        
        return redirect(url_for('booking.confirmacion', cita_id=cita.id))
    
    return render_template('booking/nueva_cita.html', form=form, now=datetime.now())

@booking_bp.route('/confirmacion/<int:cita_id>')
def confirmacion(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    return render_template('booking/confirmacion.html', cita=cita, now=datetime.now())