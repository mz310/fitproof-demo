# Лабораторийн Ажил 5
## Үндсэн функц хөгжүүлэлт ба код бичих

**Хичээл:** F.CSM316 - Програм хангамж хөгжүүлэлтийн процесс  
**Оюутан:** М.Зоригт B222270035  
**Багш:** Ж.Алимаа  
**Огноо:** 2025-12-03

---

## 1. Оршил

Энэхүү лабораторийн ажлын зорилго нь Sprint backlog-оос эхний User Story-г сонгож, TDD (Test Driven Development) аргаар хөгжүүлэлт хийх явдал юм. FitProof системийн QR код уншуулж дасгалын сесс эхлүүлэх функцийг хэрэгжүүлсэн.

---

## 2. Sprint Backlog-оос ажил сонгох

### 2.1 Эхний Sprint-ийн зорилго
"QR-суурьтай баталгаажуулалт + гар оролт + анхан шатны эрхийн бүтэц"-ийг ажиллагаанд оруулж, бодит өгөгдөл логлох урсгалыг нээх.

### 2.2 Сонгосон User Story-ууд

| ID | User Story | Story Point | Тэргүүлэх чиглэл |
|----|-----------|-------------|------------------|
| US1 | QR код уншуулж сесс эхлүүлэх/баталгаажуулах | 5 | Өндөр |
| US2 | Гар оролт: жин, sets×reps, cardio хадгалах | 3 | Өндөр |
| US12 | Админ: хэрэглэгчийн бүртгэл/эрхийн түвшин | 3 | Дунд |

**Нийт: 11 Story Point** (Багийн хүчин чадал: 15 SP)

### 2.3 Сонгосон шалтгаан
- **Хамгийн их бизнесийн үнэ цэнэ:** QR код уншуулалт нь системийн гол функц
- **Хамгийн бага эрсдэл:** Технологи сайн судлагдсан, баримтжуулалт бүрэн
- **Хамаарал:** Бусад функцууд үүнээс хамаарна

---

## 3. TDD (Test Driven Development) арга

### 3.1 TDD-ийн алхмууд

```
1. Эхлээд нэгж туршилтыг бичих (RED)
2. Туршилтыг амжилтгүй гүйцэтгэхийг шалгах
3. Шаардлагатай кодыг бичих (GREEN)
4. Туршилтыг амжилттай гүйцэтгэхийг баталгаажуулах
5. Кодоо сайжруулах (REFACTOR)
```

### 3.2 Нэгж туршилтын код (test_qr_session.py)

```python
"""
FitProof - US1: QR код уншуулж сесс эхлүүлэх
Нэгж туршилтууд (Unit Tests) - TDD аргаар
"""

import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Equipment, WorkoutSession


class TestQRSession(unittest.TestCase):
    """US1: QR код уншуулж сесс эхлүүлэх туршилт"""

    def setUp(self):
        """Туршилт эхлэхийн өмнө тохиргоо"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Туршилтын хэрэглэгч үүсгэх
        self.user = User(
            username='testuser',
            email='test@fitproof.mn',
            role='member'
        )
        self.user.set_password('password123')
        db.session.add(self.user)

        # Туршилтын төхөөрөмж үүсгэх
        self.equipment = Equipment(
            name='Treadmill 1',
            qr_code='EQ001-TREADMILL',
            equipment_type='cardio',
            description='Гүйлтийн зам 1'
        )
        db.session.add(self.equipment)
        db.session.commit()

    def tearDown(self):
        """Туршилт дууссаны дараа цэвэрлэх"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        """Хэрэглэгч үүсгэх туршилт"""
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@fitproof.mn')
        self.assertEqual(user.role, 'member')

    def test_equipment_creation(self):
        """Төхөөрөмж үүсгэх туршилт"""
        eq = Equipment.query.filter_by(qr_code='EQ001-TREADMILL').first()
        self.assertIsNotNone(eq)
        self.assertEqual(eq.name, 'Treadmill 1')

    def test_workout_session_start(self):
        """Дасгалын сесс эхлүүлэх туршилт"""
        session = WorkoutSession(
            user_id=self.user.id,
            equipment_id=self.equipment.id
        )
        db.session.add(session)
        db.session.commit()

        self.assertIsNotNone(session.id)
        self.assertTrue(session.is_active)
        self.assertIsNotNone(session.start_time)

    def test_workout_session_end(self):
        """Дасгалын сесс дуусгах туршилт"""
        session = WorkoutSession(
            user_id=self.user.id,
            equipment_id=self.equipment.id
        )
        db.session.add(session)
        db.session.commit()

        session.end_session(weight=50, sets=3, reps=12)
        db.session.commit()

        self.assertFalse(session.is_active)
        self.assertIsNotNone(session.end_time)
        self.assertEqual(session.weight, 50)

    def test_xp_calculation(self):
        """XP оноо тооцоолох туршилт"""
        session = WorkoutSession(
            user_id=self.user.id,
            equipment_id=self.equipment.id
        )
        db.session.add(session)
        db.session.commit()

        initial_xp = self.user.xp_points
        session.end_session(sets=3, reps=10)
        db.session.commit()

        self.assertGreater(session.xp_earned, 0)
        self.assertGreater(self.user.xp_points, initial_xp)


if __name__ == '__main__':
    unittest.main()
```

### 3.3 Туршилтын үр дүн

```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-7.4.3
collected 16 items

tests/test_qr_session.py::TestQRSession::test_admin_role PASSED          [  6%]
tests/test_qr_session.py::TestQRSession::test_end_session_api PASSED     [ 12%]
tests/test_qr_session.py::TestQRSession::test_equipment_creation PASSED  [ 18%]
tests/test_qr_session.py::TestQRSession::test_equipment_list PASSED      [ 25%]
tests/test_qr_session.py::TestQRSession::test_invalid_qr_code PASSED     [ 31%]
tests/test_qr_session.py::TestQRSession::test_member_role PASSED         [ 37%]
tests/test_qr_session.py::TestQRSession::test_scan_qr_page_loads PASSED  [ 43%]
tests/test_qr_session.py::TestQRSession::test_start_session_via_qr PASSED [ 50%]
tests/test_qr_session.py::TestQRSession::test_trainer_role PASSED        [ 56%]
tests/test_qr_session.py::TestQRSession::test_user_creation PASSED       [ 62%]
tests/test_qr_session.py::TestQRSession::test_user_password PASSED       [ 68%]
tests/test_qr_session.py::TestQRSession::test_workout_session_end PASSED [ 75%]
tests/test_qr_session.py::TestQRSession::test_workout_session_start PASSED [ 81%]
tests/test_qr_session.py::TestQRSession::test_xp_calculation PASSED      [ 87%]
tests/test_qr_session.py::TestLeaderboard::test_leaderboard_order PASSED [ 93%]
tests/test_qr_session.py::TestLeaderboard::test_leaderboard_page PASSED  [100%]

======================= 16 passed in 5.82s =======================
```

**Бүх 16 туршилт амжилттай!**

---

## 4. Хөгжүүлсэн код

### 4.1 Өгөгдлийн загварууд (models.py)

```python
class User(UserMixin, db.Model):
    """Хэрэглэгчийн загвар"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='member')
    xp_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    workout_sessions = db.relationship('WorkoutSession', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_xp(self, points):
        self.xp_points += points


class Equipment(db.Model):
    """Фитнес төхөөрөмжийн загвар"""
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    qr_code = db.Column(db.String(100), unique=True, nullable=False)
    equipment_type = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)


class WorkoutSession(db.Model):
    """Дасгалын сессийн загвар"""
    __tablename__ = 'workout_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    weight = db.Column(db.Float)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    xp_earned = db.Column(db.Integer, default=0)

    def end_session(self, weight=None, sets=None, reps=None):
        self.end_time = datetime.utcnow()
        self.is_active = False
        self.weight = weight
        self.sets = sets
        self.reps = reps
        self.xp_earned = self.calculate_xp()
        self.user.add_xp(self.xp_earned)

    def calculate_xp(self):
        xp = 10
        if self.sets and self.reps:
            xp += (self.sets * self.reps) // 5
        return xp
```

### 4.2 API Endpoints (routes.py)

```python
@main_bp.route('/api/session/start', methods=['POST'])
def start_session():
    """QR кодоор дасгалын сесс эхлүүлэх"""
    data = request.get_json()
    qr_code = data.get('qr_code')

    if not qr_code:
        return jsonify({'error': 'QR код шаардлагатай'}), 400

    equipment = Equipment.query.filter_by(qr_code=qr_code, is_active=True).first()
    if not equipment:
        return jsonify({'error': 'Төхөөрөмж олдсонгүй'}), 404

    if not current_user.is_authenticated:
        return jsonify({'error': 'Нэвтрэх шаардлагатай'}), 401

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
        'equipment': equipment.name
    }), 200


@main_bp.route('/api/session/<int:session_id>/end', methods=['POST'])
def end_session(session_id):
    """Дасгалын сесс дуусгах"""
    session = WorkoutSession.query.get_or_404(session_id)
    data = request.get_json() or {}

    session.end_session(
        weight=data.get('weight'),
        sets=data.get('sets'),
        reps=data.get('reps')
    )
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Дасгал дууслаа!',
        'xp_earned': session.xp_earned,
        'total_xp': session.user.xp_points
    }), 200
```

---

## 5. Daily Stand-up уулзалт

### 5.1 Stand-up уулзалтын бүтэц

Өдөр бүр 15 минутын турш дараах асуултуудыг хэлэлцнэ:
1. Өчигдөр юу хийсэн бэ?
2. Өнөөдөр юу хийх вэ?
3. Ямар саад тотгор тулгарсан бэ?

### 5.2 Жишээ Stand-up (2025-12-03)

| Гишүүн | Өчигдөр | Өнөөдөр | Саад тотгор |
|--------|---------|---------|-------------|
| М.Зоригт | User, Equipment, WorkoutSession model-уудыг бичсэн. Нэгж туршилтуудыг үүсгэсэн. | API endpoint-уудыг дуусгах, UI template-уудыг хийх | Pillow library суулгахад хувилбарын асуудал гарсан - шийдсэн |

### 5.3 Stand-up тэмдэглэл

**Өдөр 1:**
- Model-ууд бичигдсэн
- Database schema үүссэн
- Туршилтын өгөгдөл нэмэгдсэн

**Өдөр 2:**
- Нэгж туршилтууд бичигдсэн (16 тест)
- Бүх туршилт амжилттай болсон
- API endpoints хийгдсэн

**Өдөр 3:**
- UI templates үүссэн
- QR скан хуудас ажилласан
- Лидерборд хэрэгжсэн

---

## 6. Git Workflow ба Merge

### 6.1 Git командууд

```bash
# 1. Feature branch үүсгэх
git checkout -b feature/qr-session-start

# 2. Код бичих, туршилтуудыг бичих...
# ... development work ...

# 3. Өөрчлөлтүүдийг stage хийх
git add .

# 4. Commit хийх
git commit -m "US1: QR код уншуулж сесс эхлүүлэх функц нэмэв

- User, Equipment, WorkoutSession models үүсгэсэн
- 16 нэгж туршилт бичсэн, бүгд passed
- /api/session/start, /api/session/end endpoints
- QR скан хуудас, Dashboard, Leaderboard UI"

# 5. Remote руу push хийх
git push origin feature/qr-session-start

# 6. Pull Request үүсгэх (GitHub дээр)
# 7. Code Review хийлгэх
# 8. CI/CD pipeline ажиллуулах
# 9. Main branch руу merge хийх
```

### 6.2 Commit түүх

```
feat: US1 - QR код уншуулж сесс эхлүүлэх
├── models.py - User, Equipment, WorkoutSession
├── routes.py - API endpoints
├── test_qr_session.py - 16 unit tests
├── templates/ - UI хуудсууд
└── requirements.txt - dependencies

feat: US2 - Гар оролт хадгалах
├── WorkoutSession.end_session() method
├── weight, sets, reps fields
└── XP calculation logic

feat: US12 - Эрхийн түвшин
├── User.role field (member/trainer/admin)
├── Admin dashboard
└── Role-based access control
```

---

## 7. Төслийн бүтэц

```
fitproof/
├── app/
│   ├── __init__.py          # App Factory Pattern
│   ├── models.py            # ORM Models
│   ├── routes.py            # API & Views
│   ├── qr_generator.py      # QR код үүсгэгч
│   └── templates/
│       ├── base.html        # Үндсэн template
│       ├── index.html       # Нүүр хуудас
│       ├── scan.html        # QR скан
│       ├── login.html       # Нэвтрэх
│       ├── register.html    # Бүртгүүлэх
│       ├── dashboard.html   # Dashboard
│       ├── equipment.html   # Төхөөрөмжүүд
│       ├── leaderboard.html # Лидерборд
│       ├── history.html     # Түүх
│       └── admin/
│           ├── dashboard.html
│           └── users.html
├── tests/
│   ├── __init__.py
│   └── test_qr_session.py   # 16 Unit Tests
├── config.py                # Тохиргоо
├── run.py                   # App эхлүүлэгч
├── requirements.txt
└── README.md
```

---

## 8. Дүгнэлт

### 8.1 Хэрэгжүүлсэн функцууд

| Функц | Тайлбар | Статус |
|-------|---------|--------|
| QR код скан | Төхөөрөмжийн QR уншуулж сесс эхлүүлэх | ✅ |
| Гар оролт | Жин, сет, давталт хадгалах | ✅ |
| XP систем | Дасгал бүрт XP оноо олгох | ✅ |
| Лидерборд | XP-ээр эрэмбэлсэн жагсаалт | ✅ |
| Эрхийн түвшин | Member/Trainer/Admin | ✅ |
| Нэгж туршилт | 16 тест, 100% passed | ✅ |

### 8.2 TDD-ийн давуу тал

1. **Кодын чанар сайжирсан** - Туршилт эхлээд бичснээр кодын бүтэц сайн болсон
2. **Regression илэрч** - Шинэ өөрчлөлт хийхэд хуучин функц эвдэхгүй
3. **Баримтжуулалт** - Туршилтууд кодын ажиллагааг баримтжуулсан
4. **Итгэлтэй refactor** - Туршилт байгаа тул код сайжруулахад итгэлтэй

### 8.3 Сурсан зүйлс

- Flask application factory pattern
- SQLAlchemy ORM ашиглах
- TDD арга зүй
- Git branching strategy
- Daily stand-up уулзалт зохион байгуулах

---

## 9. Эх сурвалж

1. Flask Documentation - https://flask.palletsprojects.com/
2. SQLAlchemy Documentation - https://docs.sqlalchemy.org/
3. Test Driven Development by Example - Kent Beck
4. Agile Software Development - Scrum methodology

---

**Тайлан бэлтгэсэн:** М.Зоригт B222270035  
**Огноо:** 2025-12-03

