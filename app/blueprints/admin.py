from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, make_response
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Usuario, Cita, MensajeContacto, Post
from forms import LoginForm, PostForm
import csv
from io import StringIO

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data) and user.is_admin:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        flash('Email o contraseña incorrectos', 'danger')
    
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('main.home'))

@admin_bp.route('/')
@login_required
def dashboard():
    # Estadísticas de citas
    total_citas = Cita.query.count()
    citas_pendientes = Cita.query.filter_by(estado='pendiente').count()
    citas_confirmadas = Cita.query.filter_by(estado='confirmada').count()
    citas_completadas = Cita.query.filter_by(estado='completada').count()
    
    # Próximas citas
    proximas_citas = Cita.query.filter(
        Cita.estado.in_(['pendiente', 'confirmada'])
    ).order_by(Cita.fecha_pref.asc(), Cita.hora_pref.asc()).limit(10).all()
    
    # Mensajes de contacto recientes
    mensajes = MensajeContacto.query.order_by(MensajeContacto.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_citas=total_citas,
                         citas_pendientes=citas_pendientes,
                         citas_confirmadas=citas_confirmadas,
                         citas_completadas=citas_completadas,
                         proximas_citas=proximas_citas,
                         mensajes=mensajes)

@admin_bp.route('/citas')
@login_required
def citas():
    estado = request.args.get('estado', 'todas')
    page = request.args.get('page', 1, type=int)
    
    query = Cita.query
    if estado != 'todas':
        query = query.filter_by(estado=estado)
    
    citas = query.order_by(Cita.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/citas.html', citas=citas, estado_actual=estado)

@admin_bp.route('/citas/<int:cita_id>')
@login_required
def cita_detalle(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    return render_template('admin/cita_detalle.html', cita=cita)

@admin_bp.route('/citas/<int:cita_id>/actualizar', methods=['POST'])
@login_required
def actualizar_cita(cita_id):
    cita = Cita.query.get_or_404(cita_id)
    
    nuevo_estado = request.form.get('estado')
    nota_interna = request.form.get('nota_interna')
    
    if nuevo_estado in ['pendiente', 'confirmada', 'completada', 'cancelada']:
        cita.estado = nuevo_estado
    
    if nota_interna:
        cita.nota_interna = nota_interna
    
    db.session.commit()
    flash('Cita actualizada correctamente', 'success')
    
    return redirect(url_for('admin.cita_detalle', cita_id=cita_id))

@admin_bp.route('/citas/exportar')
@login_required
def exportar_citas():
    # Crear CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Cabeceras
    writer.writerow([
        'ID', 'Nombre', 'Email', 'Teléfono', 'Dirección', 'Localidad', 'CP',
        'Mascota Tipo', 'Mascota Edad', 'Motivo', 'Zona', 'Fecha Pref', 
        'Hora Pref', 'Estado', 'Fecha Creación', 'Nota Interna'
    ])
    
    # Datos
    citas = Cita.query.all()
    for cita in citas:
        writer.writerow([
            cita.id, cita.nombre, cita.email, cita.telefono, cita.direccion,
            cita.localidad, cita.cp, cita.mascota_tipo, cita.mascota_edad,
            cita.motivo, cita.zona, cita.fecha_pref.strftime('%d/%m/%Y'),
            cita.hora_pref.strftime('%H:%M'), cita.estado,
            cita.created_at.strftime('%d/%m/%Y %H:%M'), cita.nota_interna or ''
        ])
    
    # Crear respuesta
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=citas.csv'
    
    return response

@admin_bp.route('/mensajes')
@login_required
def mensajes():
    page = request.args.get('page', 1, type=int)
    mensajes = MensajeContacto.query.order_by(MensajeContacto.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/mensajes.html', mensajes=mensajes)

@admin_bp.route('/blog')
@login_required
def blog_admin():
    posts = Post.query.order_by(Post.fecha_pub.desc()).all()
    return render_template('admin/blog.html', posts=posts)

@admin_bp.route('/blog/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            titulo=form.titulo.data,
            slug=form.slug.data,
            extracto=form.extracto.data,
            contenido=form.contenido.data,
            visible=form.visible.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Post creado correctamente', 'success')
        return redirect(url_for('admin.blog_admin'))
    
    return render_template('admin/post_form.html', form=form, titulo='Nuevo Post')

@admin_bp.route('/blog/<int:post_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.slug = form.slug.data
        post.extracto = form.extracto.data
        post.contenido = form.contenido.data
        post.visible = form.visible.data
        db.session.commit()
        flash('Post actualizado correctamente', 'success')
        return redirect(url_for('admin.blog_admin'))
    
    return render_template('admin/post_form.html', form=form, titulo='Editar Post', post=post)

@admin_bp.route('/blog/<int:post_id>/eliminar', methods=['POST'])
@login_required
def eliminar_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post eliminado correctamente', 'success')
    return redirect(url_for('admin.blog_admin'))