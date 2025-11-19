from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, TelField, SelectField, DateField, TimeField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional
from datetime import datetime, timedelta

class ContactoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    asunto = StringField('Asunto', validators=[DataRequired(), Length(min=5, max=200)])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired(), Length(min=10, max=1000)])

class CitaForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    telefono = TelField('Teléfono', validators=[DataRequired(), Length(min=9, max=20)])
    direccion = TextAreaField('Dirección completa', validators=[DataRequired(), Length(min=10, max=500)])
    localidad = StringField('Localidad', validators=[DataRequired(), Length(min=2, max=100)])
    cp = StringField('Código Postal', validators=[DataRequired(), Length(min=5, max=10)])
    
    mascota_tipo = SelectField('Tipo de mascota', choices=[
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('ave', 'Ave'),
        ('roedor', 'Roedor'),
        ('reptil', 'Reptil'),
        ('otro', 'Otro')
    ], validators=[DataRequired()])
    
    mascota_edad = StringField('Edad de la mascota', validators=[Optional(), Length(max=50)])
    motivo = TextAreaField('Motivo de la consulta', validators=[DataRequired(), Length(min=10, max=1000)])
    
    zona = SelectField('Zona de cobertura', choices=[
        ('centro', 'Centro - Sin recargo'),
        ('norte', 'Zona Norte - Recargo 5€'),
        ('sur', 'Zona Sur - Recargo 5€'),
        ('este', 'Zona Este - Recargo 10€'),
        ('oeste', 'Zona Oeste - Recargo 10€'),
        ('extrarradio', 'Extrarradio - Recargo 15€')
    ], validators=[DataRequired()])
    
    fecha_pref = DateField('Fecha preferida', validators=[DataRequired()])
    hora_pref = TimeField('Hora preferida', validators=[DataRequired()])
    
    privacidad = BooleanField('Acepto la política de privacidad', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])

class PostForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(min=5, max=200)])
    slug = StringField('Slug (URL)', validators=[DataRequired(), Length(min=5, max=200)])
    extracto = TextAreaField('Extracto', validators=[Optional(), Length(max=500)])
    contenido = TextAreaField('Contenido', validators=[DataRequired()])
    visible = BooleanField('Visible', default=True)