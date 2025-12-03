"""
FitProof Routes - API болон хуудсуудын чиглүүлэлт
US1: QR код уншуулж сесс эхлүүлэх
US2: Гар оролт хадгалах
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Equipment, WorkoutSession

main_bp = Blueprint('main', __name__)


# ==================== PAGES ====================

@main_bp.route('/')
def index():
    """Нүүр хуудас"""
    return render_template('index.html')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Нэвтрэх хуудас"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Амжилттай нэвтэрлээ!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Хэрэглэгчийн нэр эсвэл нууц үг буруу байна.', 'error')

    return render_template('login.html')


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Бүртгүүлэх хуудас"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Шалгах
        if User.query.filter_by(username=username).first():
            flash('Хэрэглэгчийн нэр бүртгэлтэй байна.', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('И-мэйл бүртгэлтэй байна.', 'error')
            return render_template('register.html')

        # Шинэ хэрэглэгч үүсгэх
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Амжилттай бүртгэгдлээ! Нэвтэрнэ үү.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')


@main_bp.route('/logout')
@login_required
def logout():
    """Гарах"""
    logout_user()
    flash('Амжилттай гарлаа.', 'info')
    return redirect(url_for('main.index'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Хэрэглэгчийн dashboard"""
    active_session = WorkoutSession.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).first()

    recent_sessions = WorkoutSession.query.filter_by(
        user_id=current_user.id
    ).order_by(WorkoutSession.start_time.desc()).limit(10).all()

    return render_template('dashboard.html',
                           active_session=active_session,
                           recent_sessions=recent_sessions)


@main_bp.route('/scan')
def scan():
    """QR код уншуулах хуудас"""
    return render_template('scan.html')


@main_bp.route('/equipment')
def equipment_list():
    """Төхөөрөмжийн жагсаалт"""
    equipment = Equipment.query.filter_by(is_active=True).all()
    return render_template('equipment.html', equipment=equipment)


@main_bp.route('/leaderboard')
def leaderboard():
    """Лидерборд хуудас"""
    users = User.query.order_by(User.xp_points.desc()).limit(50).all()
    return render_template('leaderboard.html', users=users)


@main_bp.route('/history')
@login_required
def history():
    """Дасгалын түүх"""
    sessions = WorkoutSession.query.filter_by(
        user_id=current_user.id
    ).order_by(WorkoutSession.start_time.desc()).all()
    return render_template('history.html', sessions=sessions)


# ==================== API ENDPOINTS ====================

@main_bp.route('/api/session/start', methods=['POST'])
def start_session():
    """
    QR кодоор дасгалын сесс эхлүүлэх
    US1: QR код уншуулж сесс эхлүүлэх
    """
    data = request.get_json()
    qr_code = data.get('qr_code')

    if not qr_code:
        return jsonify({'error': 'QR код шаардлагатай'}), 400

    # Төхөөрөмж хайх
    equipment = Equipment.query.filter_by(qr_code=qr_code, is_active=True).first()
    if not equipment:
        return jsonify({'error': 'Төхөөрөмж олдсонгүй эсвэл идэвхгүй байна'}), 404

    # Хэрэглэгч шалгах
    if not current_user.is_authenticated:
        return jsonify({'error': 'Нэвтрэх шаардлагатай'}), 401

    # Идэвхтэй сесс байгаа эсэхийг шалгах
    active_session = WorkoutSession.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).first()

    if active_session:
        return jsonify({
            'error': 'Идэвхтэй сесс байна',
            'session_id': active_session.id,
            'equipment': active_session.equipment.name
        }), 400

    # Шинэ сесс үүсгэх
    session = WorkoutSession(
        user_id=current_user.id,
        equipment_id=equipment.id
    )
    db.session.add(session)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Дасгал эхэллээ!',
        'session_id': session.id,
        'equipment': equipment.name,
        'equipment_type': equipment.equipment_type,
        'start_time': session.start_time.isoformat()
    }), 200


@main_bp.route('/api/session/<int:session_id>/end', methods=['POST'])
def end_session(session_id):
    """
    Дасгалын сесс дуусгах
    US2: Гар оролт хадгалах
    """
    session = WorkoutSession.query.get_or_404(session_id)

    # Эзэмшигч мөн эсэхийг шалгах
    if current_user.is_authenticated and session.user_id != current_user.id:
        return jsonify({'error': 'Зөвшөөрөлгүй'}), 403

    if not session.is_active:
        return jsonify({'error': 'Сесс аль хэдийн дууссан'}), 400

    data = request.get_json() or {}

    # Сесс дуусгах
    session.end_session(
        weight=data.get('weight'),
        sets=data.get('sets'),
        reps=data.get('reps'),
        duration_minutes=data.get('duration_minutes'),
        notes=data.get('notes')
    )
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Дасгал амжилттай дууслаа!',
        'session_id': session.id,
        'xp_earned': session.xp_earned,
        'total_xp': session.user.xp_points,
        'duration': session.get_duration()
    }), 200


@main_bp.route('/api/session/active')
@login_required
def get_active_session():
    """Идэвхтэй сесс авах"""
    session = WorkoutSession.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).first()

    if not session:
        return jsonify({'active': False}), 200

    return jsonify({
        'active': True,
        'session_id': session.id,
        'equipment': session.equipment.name,
        'equipment_type': session.equipment.equipment_type,
        'start_time': session.start_time.isoformat()
    }), 200


@main_bp.route('/api/user/stats')
@login_required
def user_stats():
    """Хэрэглэгчийн статистик"""
    total_sessions = WorkoutSession.query.filter_by(
        user_id=current_user.id,
        is_active=False
    ).count()

    total_duration = db.session.query(
        db.func.sum(WorkoutSession.duration_minutes)
    ).filter_by(user_id=current_user.id, is_active=False).scalar() or 0

    return jsonify({
        'username': current_user.username,
        'xp_points': current_user.xp_points,
        'total_sessions': total_sessions,
        'total_duration_minutes': total_duration,
        'role': current_user.role
    }), 200


@main_bp.route('/api/leaderboard')
def api_leaderboard():
    """Лидерборд API"""
    users = User.query.order_by(User.xp_points.desc()).limit(50).all()
    return jsonify({
        'leaderboard': [
            {
                'rank': i + 1,
                'username': u.username,
                'xp_points': u.xp_points
            } for i, u in enumerate(users)
        ]
    }), 200


# ==================== ADMIN ENDPOINTS (US12) ====================

@main_bp.route('/admin')
@login_required
def admin_dashboard():
    """Админ dashboard"""
    if not current_user.is_admin():
        flash('Админ эрх шаардлагатай', 'error')
        return redirect(url_for('main.dashboard'))

    users = User.query.all()
    equipment = Equipment.query.all()
    return render_template('admin/dashboard.html', users=users, equipment=equipment)


@main_bp.route('/admin/users')
@login_required
def admin_users():
    """Хэрэглэгчдийн жагсаалт"""
    if not current_user.is_admin():
        return redirect(url_for('main.dashboard'))

    users = User.query.all()
    return render_template('admin/users.html', users=users)


@main_bp.route('/admin/user/<int:user_id>/role', methods=['POST'])
@login_required
def change_user_role(user_id):
    """Хэрэглэгчийн эрх өөрчлөх"""
    if not current_user.is_admin():
        return jsonify({'error': 'Админ эрх шаардлагатай'}), 403

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    new_role = data.get('role')

    if new_role not in ['member', 'trainer', 'admin']:
        return jsonify({'error': 'Буруу эрхийн түвшин'}), 400

    user.role = new_role
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'{user.username} хэрэглэгчийн эрх {new_role} болгож өөрчлөгдлөө'
    }), 200


@main_bp.route('/admin/equipment/add', methods=['POST'])
@login_required
def add_equipment():
    """Төхөөрөмж нэмэх"""
    if not current_user.is_admin():
        return jsonify({'error': 'Админ эрх шаардлагатай'}), 403

    data = request.get_json()

    equipment = Equipment(
        name=data.get('name'),
        qr_code=data.get('qr_code'),
        equipment_type=data.get('equipment_type'),
        description=data.get('description')
    )
    db.session.add(equipment)
    db.session.commit()

    return jsonify({
        'success': True,
        'equipment_id': equipment.id,
        'message': f'{equipment.name} амжилттай нэмэгдлээ'
    }), 201

