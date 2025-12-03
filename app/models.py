"""
FitProof Models - Өгөгдлийн загварууд
US1: QR код уншуулж сесс эхлүүлэх
US2: Гар оролт: жин, sets×reps хадгалах
US12: Хэрэглэгчийн эрхийн түвшин
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Хэрэглэгчийн загвар
    Эрхийн түвшин: member, trainer, admin
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default="member")  # member, trainer, admin
    xp_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Холбоосууд
    workout_sessions = db.relationship("WorkoutSession", backref="user", lazy="dynamic")

    def set_password(self, password):
        """Нууц үг хэш болгож хадгалах"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Нууц үг шалгах"""
        return check_password_hash(self.password_hash, password)

    def add_xp(self, points):
        """XP оноо нэмэх"""
        self.xp_points += points

    def is_admin(self):
        return self.role == "admin"

    def is_trainer(self):
        return self.role == "trainer"

    def __repr__(self):
        return f"<User {self.username}>"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Equipment(db.Model):
    """
    Фитнес төхөөрөмжийн загвар
    QR код нь төхөөрөмж бүрт өвөрмөц байна
    """

    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    qr_code = db.Column(db.String(100), unique=True, nullable=False, index=True)
    equipment_type = db.Column(db.String(50))  # cardio, strength, flexibility
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Холбоосууд
    workout_sessions = db.relationship("WorkoutSession", backref="equipment", lazy="dynamic")

    def __repr__(self):
        return f"<Equipment {self.name}>"


class WorkoutSession(db.Model):
    """
    Дасгалын сессийн загвар
    QR уншуулахад сесс эхэлж, дуусахад бүртгэгдэнэ
    """

    __tablename__ = "workout_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)

    # Сессийн мэдээлэл
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Дасгалын өгөгдөл (US2)
    weight = db.Column(db.Float)  # Жин (кг)
    sets = db.Column(db.Integer)  # Сетийн тоо
    reps = db.Column(db.Integer)  # Давталтын тоо
    duration_minutes = db.Column(db.Integer)  # Cardio-д зориулсан хугацаа
    calories_burned = db.Column(db.Integer)
    notes = db.Column(db.Text)

    # XP оноо
    xp_earned = db.Column(db.Integer, default=0)

    def end_session(self, weight=None, sets=None, reps=None, duration_minutes=None, notes=None):
        """Сессийг дуусгах"""
        self.end_time = datetime.utcnow()
        self.is_active = False
        self.weight = weight
        self.sets = sets
        self.reps = reps
        self.duration_minutes = duration_minutes
        self.notes = notes

        # XP тооцоолох
        self.xp_earned = self.calculate_xp()
        if self.user:
            self.user.add_xp(self.xp_earned)

    def calculate_xp(self):
        """XP оноо тооцоолох"""
        xp = 10  # Суурь оноо
        if self.sets and self.reps:
            xp += (self.sets * self.reps) // 5
        if self.duration_minutes:
            xp += self.duration_minutes // 5
        return xp

    def get_duration(self):
        """Сессийн үргэлжилсэн хугацаа (минут)"""
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() / 60)
        return 0

    def __repr__(self):
        return f"<WorkoutSession {self.id} - User {self.user_id}>"
