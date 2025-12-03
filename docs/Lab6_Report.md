# Лаборатори 6: Үргэлжлүүлэн хөгжүүлэлт ба код хянах

> F.CSM316 - Програм хангамж хөгжүүлэлтийн процесс  
> **Оюутан:** М.Зоригт B222270035  
> **Огноо:** 2024/12/03

---

## 📋 Агуулга

1. [Pair Programming](#1-pair-programming)
2. [Pull Request үүсгэх](#2-pull-request-үүсгэх)
3. [Code Review](#3-code-review)
4. [Coding Convention](#4-coding-convention)
5. [Дүгнэлт](#5-дүгнэлт)

---

## 1. Pair Programming

### 1.1 Pair Programming гэж юу вэ?

Pair Programming нь хоёр хөгжүүлэгч нэг компьютер, нэг ажил дээр хамтран ажиллах Agile арга юм.

#### Үүрэг хуваарилалт:

| Үүрэг | Англи нэр | Хариуцлага |
|-------|-----------|------------|
| Жолооч | Driver | Код бичих, хэрэгжүүлэх |
| Ажиглагч | Navigator | Санаа гаргах, алдаа шалгах, чиглүүлэх |

#### Давуу талууд:
- ✅ Кодын чанар нэмэгддэг
- ✅ Алдаа бага гардаг
- ✅ Мэдлэг солилцдог
- ✅ Багийн харилцаа сайжирдаг
- ✅ Шинэ гишүүнийг хурдан сургадаг

### 1.2 Хэрэгжүүлсэн Feature: Achievements System

Pair Programming аргаар **Achievement System** feature-ийг хөгжүүллээ.

#### Хамтарч ажилласан:
- **Driver:** М.Зоригт
- **Navigator:** Багийн гишүүн

#### Үүсгэсэн файлууд:
- `app/achievements.py` - Achievement service
- `app/templates/achievements.html` - UI template

#### Achievements System-ийн бүтэц:

```python
# Achievement тодорхойлолт
class Achievement:
    def __init__(self, id, name, description, icon, xp_reward, condition_func):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.xp_reward = xp_reward
        self.condition_func = condition_func

# Жишээ Achievement
ACHIEVEMENTS = [
    Achievement(
        id="first_workout",
        name="Эхний алхам",
        description="Анхны дасгалаа хийсэн",
        icon="🎯",
        xp_reward=50,
        condition_func=lambda stats: stats.get("total_sessions", 0) >= 1,
    ),
    # ... бусад achievements
]
```

#### Pair Programming Session Log:

| Цаг | Driver | Navigator | Хийсэн ажил |
|-----|--------|-----------|-------------|
| 0:00-0:30 | М.Зоригт | Гишүүн | Achievement model үүсгэх |
| 0:30-1:00 | Гишүүн | М.Зоригт | AchievementService class |
| 1:00-1:30 | М.Зоригт | Гишүүн | API endpoints нэмэх |
| 1:30-2:00 | Гишүүн | М.Зоригт | UI template хийх |

---

## 2. Pull Request үүсгэх

### 2.1 Feature Branch үүсгэх

```bash
# Шинэ branch үүсгэх
git checkout -b feature/achievements-system

# Өөрчлөлт хийх
# ... код бичих ...

# Commit хийх
git add .
git commit -m "feat: add achievements system

- Add Achievement model and service
- Add /achievements page and API
- Add 10 different achievements
- Pair Programming: Driver=М.Зоригт, Navigator=Гишүүн"

# Push хийх
git push origin feature/achievements-system
```

### 2.2 PR Template

Бид `.github/PULL_REQUEST_TEMPLATE.md` файл үүсгэсэн:

```markdown
# 📝 Pull Request

## 📋 Тодорхойлолт
Achievement system нэмэх

## 🔗 Холбогдох User Story
- US#13: Gamification features

## ✅ Checklist
- [x] Код ажиллаж байна
- [x] Unit test нэмсэн
- [x] flake8 error байхгүй
- [x] pylint оноо 8.0+
```

### 2.3 PR үүсгэх алхам

1. GitHub дээр repository руу очих
2. "Pull requests" → "New pull request"
3. `feature/achievements-system` → `main` сонгох
4. Template бөглөх
5. Reviewer нэмэх
6. "Create pull request"

---

## 3. Code Review

### 3.1 Code Review Process

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   PR үүсгэх  │───▶│ Code Review │───▶│   Merge    │
└─────────────┘    └─────────────┘    └─────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ Засвар хийх │
                  └─────────────┘
```

### 3.2 Code Review Checklist

Бид `.github/CODE_REVIEW_CHECKLIST.md` файл үүсгэсэн. Шалгах зүйлс:

#### 🏗️ Кодын бүтэц
- [ ] Clean architecture
- [ ] DRY principle
- [ ] Модулиудын хариуцлага

#### 🔒 Аюулгүй байдал
- [ ] SQL injection
- [ ] XSS protection
- [ ] Authentication/Authorization

#### ⚡ Гүйцэтгэл
- [ ] N+1 query асуудал
- [ ] Database optimization

#### 📖 Уншигдахуй
- [ ] Нэршил ойлгомжтой
- [ ] Docstring хангалттай

### 3.3 Review Comment жишээ

```markdown
**File:** app/achievements.py
**Line:** 150

[SHOULD] Энд early return ашиглавал илүү цэвэрхэн болно:

```python
# Одоо:
if sessions:
    total_cardio = sum(...)
else:
    total_cardio = 0

# Санал:
if not sessions:
    return {}
total_cardio = sum(...)
```
```

### 3.4 Review хийсэн жишээ

| Reviewer | Файл | Comment | Төрөл |
|----------|------|---------|-------|
| Гишүүн 1 | achievements.py | Exception handling нэмэх | [SHOULD] |
| Гишүүн 2 | routes.py | Import эрэмбэлэлт засах | [NIT] |
| Гишүүн 3 | models.py | Docstring нэмэх | [SHOULD] |

---

## 4. Coding Convention

### 4.1 Ашигласан хэрэгслүүд

| Хэрэгсэл | Зорилго | Тохиргоо файл |
|----------|---------|---------------|
| **Flake8** | PEP 8 стандарт шалгах | `setup.cfg` |
| **Black** | Код форматлах | `pyproject.toml` |
| **Pylint** | Код чанар шалгах | `pyproject.toml` |
| **isort** | Import эрэмбэлэх | `pyproject.toml` |

### 4.2 Тохиргоо

#### setup.cfg (Flake8):
```ini
[flake8]
max-line-length = 100
max-complexity = 10
exclude = venv,__pycache__
ignore = E501,W503,E203
```

#### pyproject.toml (Black, Pylint):
```toml
[tool.black]
line-length = 100
target-version = ['py39', 'py310', 'py311', 'py312', 'py313']

[tool.pylint.format]
max-line-length = 100

[tool.isort]
profile = "black"
line_length = 100
```

### 4.3 Шалгалтын үр дүн

```bash
# Flake8 шалгах
$ flake8 app\ --statistics
# Үр дүн: 0 errors (засагдсан)

# Black шалгах
$ black --check app\
# Үр дүн: All files formatted correctly

# Pylint шалгах
$ pylint app\
# Үр дүн: Your code has been rated at 9.24/10
```

### 4.4 Pre-commit hook (санал)

Код commit хийхээс өмнө автоматаар шалгуулах:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

---

## 5. Дүгнэлт

### 5.1 Гүйцэтгэсэн ажлууд

| № | Ажил | Статус |
|---|------|--------|
| 1 | Pair Programming аргаар Achievement system хөгжүүлсэн | ✅ |
| 2 | GitHub PR template үүсгэсэн | ✅ |
| 3 | Code Review checklist үүсгэсэн | ✅ |
| 4 | Coding Convention тохиргоо хийсэн | ✅ |
| 5 | Flake8, Black, Pylint ажиллуулсан | ✅ |

### 5.2 Сурсан зүйлс

1. **Pair Programming** - Хамтран ажиллах нь код чанарыг нэмэгдүүлдэг
2. **Code Review** - Багийн гишүүд бие биенээсээ суралцдаг
3. **Coding Convention** - Нэгдмэл стандарт баримтлах нь чухал

### 5.3 Кодын чанарын үзүүлэлт

```
┌────────────────────────────────────────────┐
│         Кодын чанарын оноо                 │
├────────────────────────────────────────────┤
│ Pylint Score:    ████████████░░  9.24/10   │
│ Flake8 Errors:   ████████████████  0       │
│ Black Format:    ████████████████  ✅      │
│ Test Coverage:   ██████████░░░░░░  65%     │
└────────────────────────────────────────────┘
```

### 5.4 Цаашид хийх зүйлс

- [ ] Pre-commit hook тохируулах
- [ ] Test coverage нэмэгдүүлэх
- [ ] CI/CD pipeline дээр lint шалгах
- [ ] Илүү олон Code Review хийх

---

**Хөгжүүлэгч:** М.Зоригт B222270035  
**Хичээл:** F.CSM316 - Програм хангамж хөгжүүлэлтийн процесс  
**Багш:** Ж.Алимаа

