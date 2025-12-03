"""
FitProof Statistics Module
Дасгалын статистик тооцоолох модуль

Pair Programming:
- Driver: М.Зоригт (код бичих)
- Navigator: [Багийн гишүүн] (шалгах, санал өгөх)

Энэ модуль нь хэрэглэгчийн дасгалын статистикийг тооцоолно:
- Нийт дасгалын тоо
- Нийт XP оноо
- Долоо хоногийн идэвхи
- Хамгийн их хийсэн дасгал
"""

from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from app.models import User, WorkoutSession, Equipment


class WorkoutStatistics:
    """Дасгалын статистик тооцоолох класс"""

    def __init__(self, user_id: int):
        """
        Args:
            user_id: Хэрэглэгчийн ID
        """
        self.user_id = user_id
        self.user = User.query.get(user_id)

    def get_total_sessions(self) -> int:
        """Нийт дасгалын тоо"""
        return WorkoutSession.query.filter_by(user_id=self.user_id, is_active=False).count()

    def get_total_xp(self) -> int:
        """Нийт XP оноо"""
        if self.user:
            return self.user.xp_points
        return 0

    def get_total_duration(self) -> int:
        """Нийт дасгалын хугацаа (минут)"""
        result = (
            db.session.query(func.sum(WorkoutSession.duration_minutes))
            .filter_by(user_id=self.user_id, is_active=False)
            .scalar()
        )
        return result or 0

    def get_total_weight_lifted(self) -> float:
        """Нийт өргөсөн жин (кг)"""
        sessions = WorkoutSession.query.filter_by(user_id=self.user_id, is_active=False).all()

        total = 0.0
        for session in sessions:
            if session.weight and session.sets and session.reps:
                total += session.weight * session.sets * session.reps
        return total

    def get_weekly_activity(self) -> dict:
        """Долоо хоногийн идэвхи"""
        today = datetime.utcnow()
        week_ago = today - timedelta(days=7)

        sessions = WorkoutSession.query.filter(
            WorkoutSession.user_id == self.user_id,
            WorkoutSession.start_time >= week_ago,
            WorkoutSession.is_active.is_(False),
        ).all()

        # Өдөр бүрийн тоо
        daily_counts = {}
        for i in range(7):
            date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_counts[date] = 0

        for session in sessions:
            date = session.start_time.strftime("%Y-%m-%d")
            if date in daily_counts:
                daily_counts[date] += 1

        return daily_counts

    def get_favorite_equipment(self) -> str:
        """Хамгийн их хийсэн төхөөрөмж"""
        result = (
            db.session.query(Equipment.name, func.count(WorkoutSession.id).label("count"))
            .join(WorkoutSession, Equipment.id == WorkoutSession.equipment_id)
            .filter(WorkoutSession.user_id == self.user_id, WorkoutSession.is_active.is_(False))
            .group_by(Equipment.name)
            .order_by(func.count(WorkoutSession.id).desc())
            .first()
        )

        if result:
            return result[0]
        return "Мэдээлэл байхгүй"

    def get_streak_days(self) -> int:
        """Дараалсан өдрийн тоо"""
        sessions = (
            WorkoutSession.query.filter_by(user_id=self.user_id, is_active=False)
            .order_by(WorkoutSession.start_time.desc())
            .all()
        )

        if not sessions:
            return 0

        streak = 0
        current_date = datetime.utcnow().date()

        session_dates = set()
        for session in sessions:
            session_dates.add(session.start_time.date())

        while current_date in session_dates:
            streak += 1
            current_date -= timedelta(days=1)

        return streak

    def get_summary(self) -> dict:
        """Бүх статистикийн товчлол"""
        return {
            "total_sessions": self.get_total_sessions(),
            "total_xp": self.get_total_xp(),
            "total_duration": self.get_total_duration(),
            "total_weight_lifted": self.get_total_weight_lifted(),
            "weekly_activity": self.get_weekly_activity(),
            "favorite_equipment": self.get_favorite_equipment(),
            "streak_days": self.get_streak_days(),
        }


def get_leaderboard_stats(limit: int = 10) -> list:
    """
    Лидерборд статистик

    Args:
        limit: Хамгийн их хэдэн хэрэглэгч харуулах

    Returns:
        Хэрэглэгчдийн жагсаалт XP-ээр эрэмбэлсэн
    """
    users = User.query.order_by(User.xp_points.desc()).limit(limit).all()

    result = []
    for i, user in enumerate(users, 1):
        stats = WorkoutStatistics(user.id)
        result.append(
            {
                "rank": i,
                "username": user.username,
                "xp_points": user.xp_points,
                "total_sessions": stats.get_total_sessions(),
                "streak_days": stats.get_streak_days(),
            }
        )

    return result


def calculate_level(xp_points: int) -> dict:
    """
    XP оноогоор түвшин тооцоолох

    Args:
        xp_points: XP оноо

    Returns:
        Түвшин мэдээлэл
    """
    levels = [
        (0, "Эхлэгч", 100),
        (100, "Идэвхтэн", 250),
        (250, "Тогтмол", 500),
        (500, "Мэргэжилтэн", 1000),
        (1000, "Мастер", 2000),
        (2000, "Аварга", float("inf")),
    ]

    current_level = levels[0]
    next_level = levels[1] if len(levels) > 1 else None

    for i, (min_xp, name, max_xp) in enumerate(levels):
        if xp_points >= min_xp:
            current_level = (min_xp, name, max_xp)
            if i + 1 < len(levels):
                next_level = levels[i + 1]
            else:
                next_level = None

    progress = 0
    if next_level:
        range_xp = current_level[2] - current_level[0]
        current_xp = xp_points - current_level[0]
        progress = min(100, int((current_xp / range_xp) * 100))

    return {
        "level_name": current_level[1],
        "min_xp": current_level[0],
        "max_xp": current_level[2],
        "progress": progress,
        "next_level": next_level[1] if next_level else None,
        "xp_to_next": (current_level[2] - xp_points) if next_level else 0,
    }
