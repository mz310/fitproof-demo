# FitProof - Фитнес дасгалын бүртгэл

> Лабораторийн ажил 5: Эхний User Story хэрэгжүүлэх  
> F.CSM316 - Програм хангамж хөгжүүлэлтийн процесс

## Хэрэгжүүлсэн User Story-ууд

### Sprint 1 Backlog (11 Story Point)

| ID | User Story | SP | Статус |
|----|-----------|-----|--------|
| US1 | QR код уншуулж сесс эхлүүлэх/баталгаажуулах | 5 | ✅ |
| US2 | Гар оролт: жин, sets×reps, cardio хадгалах | 3 | ✅ |
| US12 | Админ: хэрэглэгчийн бүртгэл/эрхийн түвшин | 3 | ✅ |

## Эхлүүлэх

### 1. Virtual Environment үүсгэх

```bash
cd fitproof
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

### 2. Сангуудыг суулгах

```bash
pip install -r requirements.txt
```

### 3. Апп эхлүүлэх

```bash
python run.py
```

Хөтөч дээр http://127.0.0.1:5000 нээнэ үү.

### 4. Туршилтын хэрэглэгчид

| Эрх | Нэвтрэх нэр | Нууц үг |
|-----|-------------|---------|
| Admin | admin | admin123 |
| Trainer | trainer | trainer123 |
| Member | bataa | password123 |

## Нэгж туршилт ажиллуулах (TDD)

```bash
cd fitproof
python -m pytest tests/ -v
# Эсвэл:
python -m unittest tests.test_qr_session -v
```

## Төслийн бүтэц

```
fitproof/
├── app/
│   ├── __init__.py         # App factory
│   ├── models.py           # User, Equipment, WorkoutSession
│   ├── routes.py           # API болон хуудсууд
│   ├── qr_generator.py     # QR код үүсгэгч
│   └── templates/
│       ├── base.html       # Үндсэн template
│       ├── index.html      # Нүүр хуудас
│       ├── scan.html       # QR скан хуудас
│       ├── login.html      # Нэвтрэх
│       ├── register.html   # Бүртгүүлэх
│       ├── dashboard.html  # Dashboard
│       ├── equipment.html  # Төхөөрөмжүүд
│       ├── leaderboard.html # Лидерборд
│       ├── history.html    # Дасгалын түүх
│       └── admin/
│           ├── dashboard.html
│           └── users.html
├── tests/
│   ├── __init__.py
│   └── test_qr_session.py  # US1 нэгж туршилтууд
├── config.py               # Тохиргоо
├── run.py                  # App эхлүүлэгч
├── requirements.txt        # Сангуудын жагсаалт
└── README.md
```

## Git Workflow

### Feature branch үүсгэх

```bash
git checkout -b feature/qr-session-start
```

### Commit хийх

```bash
git add .
git commit -m "US1: QR код уншуулж сесс эхлүүлэх функц нэмэв"
```

### Push хийх

```bash
git push origin feature/qr-session-start
```

### Pull Request үүсгэх

GitHub дээр Pull Request үүсгэж, code review хийлгээд main branch руу merge хийнэ.

## Daily Stand-up жишээ

### Өчигдөр юу хийсэн бэ?
- User, Equipment, WorkoutSession model-уудыг бичсэн
- QR сканнерийн UI хийсэн

### Өнөөдөр юу хийх вэ?
- Нэгж туршилтуудыг бичих
- API endpoint-уудыг дуусгах

### Саад тотгор?
- QR camera API ажиллуулахад HTTPS шаардлагатай

## Definition of Done (DoD)

- [x] Код GitHub дээр version control-д оруулсан
- [x] Unit test-үүд бичигдсэн
- [x] Code review хийгдсэн
- [x] UI энгийн, ойлгомжтой
- [x] Эрхийн түвшин зөв ажиллаж байгаа

##  API Endpoints

| Method | Endpoint | Тайлбар |
|--------|----------|---------|
| POST | `/api/session/start` | QR кодоор сесс эхлүүлэх |
| POST | `/api/session/{id}/end` | Сесс дуусгах, өгөгдөл хадгалах |
| GET | `/api/session/active` | Идэвхтэй сесс авах |
| GET | `/api/user/stats` | Хэрэглэгчийн статистик |
| GET | `/api/leaderboard` | Лидерборд |

---

**Хөгжүүлэгч:** М.Зоригт B222270035  
**Хичээл:** F.CSM316 - Програм хангамж хөгжүүлэлтийн процесс  
**Багш:** Ж.Алимаа

