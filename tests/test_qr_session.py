"""
FitProof - US1: QR код уншуулж сесс эхлүүлэх
Нэгж туршилтууд (Unit Tests) - TDD аргаар

Test Driven Development:
1. Эхлээд туршилтыг бичих
2. Туршилтыг амжилтгүй гүйцэтгэхийг шалгах
3. Шаардлагатай кодыг бичих
4. Туршилтыг амжилттай гүйцэтгэх
5. Кодоо сайжруулах (refactor)
"""

import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Equipment, WorkoutSession


class TestQRSession(unittest.TestCase):
    """US1: QR код уншуулж сесс эхлүүлэх туршилт"""

    def setUp(self):
        """Туршилт эхлэхийн өмнө тохиргоо"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Туршилтын хэрэглэгч үүсгэх
        self.user = User(username="testuser", email="test@fitproof.mn", role="member")
        self.user.set_password("password123")
        db.session.add(self.user)

        # Туршилтын төхөөрөмж үүсгэх
        self.equipment = Equipment(
            name="Treadmill 1",
            qr_code="EQ001-TREADMILL",
            equipment_type="cardio",
            description="Гүйлтийн зам 1",
        )
        db.session.add(self.equipment)
        db.session.commit()

    def tearDown(self):
        """Туршилт дууссаны дараа цэвэрлэх"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # ==================== MODEL TESTS ====================

    def test_user_creation(self):
        """Хэрэглэгч үүсгэх туршилт"""
        user = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@fitproof.mn")
        self.assertEqual(user.role, "member")
        self.assertEqual(user.xp_points, 0)

    def test_user_password(self):
        """Нууц үг шалгах туршилт"""
        user = User.query.filter_by(username="testuser").first()
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.check_password("wrongpassword"))

    def test_equipment_creation(self):
        """Төхөөрөмж үүсгэх туршилт"""
        eq = Equipment.query.filter_by(qr_code="EQ001-TREADMILL").first()
        self.assertIsNotNone(eq)
        self.assertEqual(eq.name, "Treadmill 1")
        self.assertEqual(eq.equipment_type, "cardio")

    def test_workout_session_start(self):
        """Дасгалын сесс эхлүүлэх туршилт"""
        session = WorkoutSession(user_id=self.user.id, equipment_id=self.equipment.id)
        db.session.add(session)
        db.session.commit()

        self.assertIsNotNone(session.id)
        self.assertTrue(session.is_active)
        self.assertIsNotNone(session.start_time)
        self.assertIsNone(session.end_time)

    def test_workout_session_end(self):
        """Дасгалын сесс дуусгах туршилт"""
        session = WorkoutSession(user_id=self.user.id, equipment_id=self.equipment.id)
        db.session.add(session)
        db.session.commit()

        # Сесс дуусгах
        session.end_session(weight=50, sets=3, reps=12, notes="Сайн дасгал боллоо")
        db.session.commit()

        self.assertFalse(session.is_active)
        self.assertIsNotNone(session.end_time)
        self.assertEqual(session.weight, 50)
        self.assertEqual(session.sets, 3)
        self.assertEqual(session.reps, 12)

    def test_xp_calculation(self):
        """XP оноо тооцоолох туршилт"""
        session = WorkoutSession(user_id=self.user.id, equipment_id=self.equipment.id)
        db.session.add(session)
        db.session.commit()

        initial_xp = self.user.xp_points
        session.end_session(sets=3, reps=10)
        db.session.commit()

        self.assertGreater(session.xp_earned, 0)
        self.assertGreater(self.user.xp_points, initial_xp)

    # ==================== API TESTS ====================

    def test_scan_qr_page_loads(self):
        """QR уншуулах хуудас ачаалагдах туршилт"""
        response = self.client.get("/scan")
        self.assertEqual(response.status_code, 200)

    def test_equipment_list(self):
        """Төхөөрөмжийн жагсаалт харуулах туршилт"""
        response = self.client.get("/equipment")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Treadmill 1", response.get_data(as_text=True))

    def test_start_session_via_qr(self):
        """QR кодоор сесс эхлүүлэх API туршилт"""
        # Нэвтрэх
        with self.client.session_transaction() as sess:
            sess["_user_id"] = str(self.user.id)

        response = self.client.post("/api/session/start", json={"qr_code": "EQ001-TREADMILL"})

        self.assertIn(response.status_code, [200, 302])

    def test_invalid_qr_code(self):
        """Буруу QR код туршилт"""
        with self.client.session_transaction() as sess:
            sess["_user_id"] = str(self.user.id)

        response = self.client.post("/api/session/start", json={"qr_code": "INVALID-CODE"})

        data = response.get_json()
        if data:
            self.assertIn("error", data)

    def test_end_session_api(self):
        """Сесс дуусгах API туршилт"""
        # Сесс үүсгэх
        session = WorkoutSession(user_id=self.user.id, equipment_id=self.equipment.id)
        db.session.add(session)
        db.session.commit()

        with self.client.session_transaction() as sess:
            sess["_user_id"] = str(self.user.id)

        response = self.client.post(
            f"/api/session/{session.id}/end", json={"weight": 60, "sets": 4, "reps": 10}
        )

        self.assertIn(response.status_code, [200, 302])

    # ==================== USER ROLE TESTS ====================

    def test_member_role(self):
        """Member эрхийн туршилт"""
        user = User.query.filter_by(username="testuser").first()
        self.assertEqual(user.role, "member")
        self.assertFalse(user.is_admin())
        self.assertFalse(user.is_trainer())

    def test_admin_role(self):
        """Admin эрхийн туршилт"""
        admin = User(username="admin", email="admin@fitproof.mn", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

        self.assertTrue(admin.is_admin())
        self.assertFalse(admin.is_trainer())

    def test_trainer_role(self):
        """Trainer эрхийн туршилт"""
        trainer = User(username="trainer", email="trainer@fitproof.mn", role="trainer")
        trainer.set_password("trainer123")
        db.session.add(trainer)
        db.session.commit()

        self.assertTrue(trainer.is_trainer())
        self.assertFalse(trainer.is_admin())


class TestLeaderboard(unittest.TestCase):
    """Лидерборд туршилтууд"""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Олон хэрэглэгч үүсгэх
        for i in range(5):
            user = User(username=f"user{i}", email=f"user{i}@fitproof.mn", xp_points=i * 100)
            user.set_password("password")
            db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_leaderboard_page(self):
        """Лидерборд хуудас туршилт"""
        response = self.client.get("/leaderboard")
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_order(self):
        """Лидерборд эрэмбэ туршилт"""
        users = User.query.order_by(User.xp_points.desc()).all()
        self.assertEqual(users[0].xp_points, 400)
        self.assertEqual(users[-1].xp_points, 0)


if __name__ == "__main__":
    unittest.main()
