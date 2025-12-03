"""
FitProof Achievements System
Лаборатори 6: Pair Programming-д зориулсан шинэ feature

Pair Programming Roles:
- Driver (Жолооч): Код бичих
- Navigator (Ажиглагч): Санаа гаргах, алдаа шалгах

Хамтарч хийсэн: М.Зоригт (Driver) ба Багийн гишүүн (Navigator)
"""

from datetime import datetime
from typing import Optional

from app import db
from app.models import User, WorkoutSession


class Achievement:
    """Амжилтын тодорхойлолт"""

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        icon: str,
        xp_reward: int,
        condition_func: callable,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.xp_reward = xp_reward
        self.condition_func = condition_func


# Амжилтуудын жагсаалт
ACHIEVEMENTS = [
    Achievement(
        id="first_workout",
        name="Эхний алхам",
        description="Анхны дасгалаа хийсэн",
        icon="🎯",
        xp_reward=50,
        condition_func=lambda stats: stats.get("total_sessions", 0) >= 1,
    ),
    Achievement(
        id="workout_streak_3",
        name="3 өдрийн цуваа",
        description="3 өдөр дараалан дасгал хийсэн",
        icon="🔥",
        xp_reward=100,
        condition_func=lambda stats: stats.get("current_streak", 0) >= 3,
    ),
    Achievement(
        id="workout_streak_7",
        name="Долоо хоногийн баатар",
        description="7 өдөр дараалан дасгал хийсэн",
        icon="💪",
        xp_reward=250,
        condition_func=lambda stats: stats.get("current_streak", 0) >= 7,
    ),
    Achievement(
        id="sessions_10",
        name="10 сесс",
        description="10 удаа дасгал хийсэн",
        icon="⭐",
        xp_reward=100,
        condition_func=lambda stats: stats.get("total_sessions", 0) >= 10,
    ),
    Achievement(
        id="sessions_50",
        name="50 сесс",
        description="50 удаа дасгал хийсэн",
        icon="🌟",
        xp_reward=300,
        condition_func=lambda stats: stats.get("total_sessions", 0) >= 50,
    ),
    Achievement(
        id="sessions_100",
        name="100 сесс",
        description="100 удаа дасгал хийсэн",
        icon="🏆",
        xp_reward=500,
        condition_func=lambda stats: stats.get("total_sessions", 0) >= 100,
    ),
    Achievement(
        id="heavy_lifter",
        name="Хүнд өргөгч",
        description="100кг-аас дээш жин өргөсөн",
        icon="🏋️",
        xp_reward=200,
        condition_func=lambda stats: stats.get("max_weight", 0) >= 100,
    ),
    Achievement(
        id="cardio_master",
        name="Кардио мастер",
        description="Нийт 500 минут кардио хийсэн",
        icon="🏃",
        xp_reward=300,
        condition_func=lambda stats: stats.get("total_cardio_minutes", 0) >= 500,
    ),
    Achievement(
        id="xp_1000",
        name="1000 XP",
        description="1000 XP цуглуулсан",
        icon="💎",
        xp_reward=0,  # XP шагналгүй (давхардахаас сэргийлэх)
        condition_func=lambda stats: stats.get("total_xp", 0) >= 1000,
    ),
    Achievement(
        id="early_bird",
        name="Эрт босогч",
        description="Өглөөний 6 цагаас өмнө дасгал хийсэн",
        icon="🌅",
        xp_reward=75,
        condition_func=lambda stats: stats.get("early_workouts", 0) >= 1,
    ),
]


class UserAchievement(db.Model):
    """Хэрэглэгчийн авсан амжилтуудын бүртгэл"""

    __tablename__ = "user_achievements"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    achievement_id = db.Column(db.String(50), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Давхардахаас сэргийлэх
    __table_args__ = (
        db.UniqueConstraint("user_id", "achievement_id", name="unique_user_achievement"),
    )


class AchievementService:
    """Амжилт шалгах ба олгох сервис"""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user = User.query.get(user_id)

    def get_user_stats(self) -> dict:
        """Хэрэглэгчийн статистик авах"""
        sessions = WorkoutSession.query.filter_by(user_id=self.user_id, is_active=False).all()

        # Кардио нийт минут
        total_cardio = sum(
            s.duration_minutes or 0 for s in sessions if s.equipment.equipment_type == "cardio"
        )

        # Хамгийн их жин
        max_weight = max((s.weight or 0 for s in sessions), default=0)

        # Эрт босогч шалгах
        early_workouts = sum(1 for s in sessions if s.start_time.hour < 6)

        # Streak тооцоолох (энгийн хувилбар)
        streak = self._calculate_streak(sessions)

        return {
            "total_sessions": len(sessions),
            "total_xp": self.user.xp_points if self.user else 0,
            "max_weight": max_weight,
            "total_cardio_minutes": total_cardio,
            "early_workouts": early_workouts,
            "current_streak": streak,
        }

    def _calculate_streak(self, sessions: list) -> int:
        """Дасгалын цуваа (streak) тооцоолох"""
        if not sessions:
            return 0

        # Өдрүүдийг ялгаж авах
        workout_dates = sorted(set(s.start_time.date() for s in sessions), reverse=True)

        if not workout_dates:
            return 0

        streak = 1
        for i in range(len(workout_dates) - 1):
            diff = (workout_dates[i] - workout_dates[i + 1]).days
            if diff == 1:
                streak += 1
            else:
                break

        return streak

    def get_earned_achievements(self) -> list:
        """Авсан амжилтуудыг авах"""
        earned = UserAchievement.query.filter_by(user_id=self.user_id).all()
        earned_ids = [e.achievement_id for e in earned]

        result = []
        for achievement in ACHIEVEMENTS:
            if achievement.id in earned_ids:
                earned_record = next(e for e in earned if e.achievement_id == achievement.id)
                result.append(
                    {
                        "id": achievement.id,
                        "name": achievement.name,
                        "description": achievement.description,
                        "icon": achievement.icon,
                        "xp_reward": achievement.xp_reward,
                        "earned": True,
                        "earned_at": earned_record.earned_at.isoformat(),
                    }
                )
        return result

    def get_available_achievements(self) -> list:
        """Боломжит (авч болох) амжилтуудыг авах"""
        earned = UserAchievement.query.filter_by(user_id=self.user_id).all()
        earned_ids = [e.achievement_id for e in earned]

        stats = self.get_user_stats()
        result = []

        for achievement in ACHIEVEMENTS:
            if achievement.id not in earned_ids:
                progress = self._get_progress(achievement, stats)
                result.append(
                    {
                        "id": achievement.id,
                        "name": achievement.name,
                        "description": achievement.description,
                        "icon": achievement.icon,
                        "xp_reward": achievement.xp_reward,
                        "earned": False,
                        "progress": progress,
                    }
                )
        return result

    def _get_progress(self, achievement: Achievement, stats: dict) -> Optional[dict]:
        """Амжилтын явцыг авах"""
        progress_map = {
            "first_workout": ("total_sessions", 1),
            "workout_streak_3": ("current_streak", 3),
            "workout_streak_7": ("current_streak", 7),
            "sessions_10": ("total_sessions", 10),
            "sessions_50": ("total_sessions", 50),
            "sessions_100": ("total_sessions", 100),
            "heavy_lifter": ("max_weight", 100),
            "cardio_master": ("total_cardio_minutes", 500),
            "xp_1000": ("total_xp", 1000),
            "early_bird": ("early_workouts", 1),
        }

        if achievement.id in progress_map:
            stat_key, target = progress_map[achievement.id]
            current = stats.get(stat_key, 0)
            return {
                "current": current,
                "target": target,
                "percentage": min(100, int((current / target) * 100)),
            }
        return None

    def check_and_award_achievements(self) -> list:
        """Шинэ амжилт авсан эсэхийг шалгаж, олгох"""
        stats = self.get_user_stats()
        earned = UserAchievement.query.filter_by(user_id=self.user_id).all()
        earned_ids = [e.achievement_id for e in earned]

        new_achievements = []

        for achievement in ACHIEVEMENTS:
            if achievement.id not in earned_ids:
                if achievement.condition_func(stats):
                    # Амжилт олгох
                    user_achievement = UserAchievement(
                        user_id=self.user_id, achievement_id=achievement.id
                    )
                    db.session.add(user_achievement)

                    # XP олгох
                    if achievement.xp_reward > 0 and self.user:
                        self.user.add_xp(achievement.xp_reward)

                    new_achievements.append(
                        {
                            "id": achievement.id,
                            "name": achievement.name,
                            "description": achievement.description,
                            "icon": achievement.icon,
                            "xp_reward": achievement.xp_reward,
                        }
                    )

        if new_achievements:
            db.session.commit()

        return new_achievements
