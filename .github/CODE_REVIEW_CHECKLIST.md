# 🔍 Code Review Checklist

> FitProof төслийн Code Review хийхдээ анхаарах зүйлс
> Лаборатори 6: Code Review ба Coding Convention

## 📋 Шалгах ёстой зүйлс

### 1. 🏗️ Кодын бүтэц (Architecture)
- [ ] Clean architecture дагасан эсэх
- [ ] MVC/Blueprint бүтцийг зөв ашигласан эсэх
- [ ] Модулиудын хариуцлага тодорхой эсэх
- [ ] Хэт их code duplication байхгүй эсэх (DRY principle)

### 2. 🔒 Аюулгүй байдал (Security)
- [ ] SQL injection-оос хамгаалагдсан эсэх (ORM ашиглалт)
- [ ] XSS халдлагаас хамгаалагдсан эсэх
- [ ] Нууц мэдээлэл (password, API key) хардкод хийгдээгүй эсэх
- [ ] Authentication/Authorization зөв хэрэгжсэн эсэх
- [ ] Input validation хийгдсэн эсэх

### 3. ⚠️ Алдааны менежмент (Error Handling)
- [ ] Exception handling зөв хийгдсэн эсэх
- [ ] Хэрэглэгчид ойлгомжтой алдааны мессеж харуулсан эсэх
- [ ] Error log хийгдсэн эсэх
- [ ] Edge case-үүдийг анхаарсан эсэх

### 4. ⚡ Гүйцэтгэл (Performance)
- [ ] N+1 query асуудал байхгүй эсэх
- [ ] Давтамжтай ашиглагдах код оновчтой эсэх
- [ ] Database index зөв тавигдсан эсэх
- [ ] Их хэмжээний өгөгдөл pagination ашигладаг эсэх

### 5. 📖 Уншигдахуй (Readability)
- [ ] Хувьсагч, функцын нэршил ойлгомжтой эсэх
- [ ] Docstring/comment хангалттай эсэх
- [ ] Төвөгтэй logic тайлбарлагдсан эсэх
- [ ] Код formatting стандартыг дагасан эсэх

### 6. 🧪 Туршилт (Testing)
- [ ] Unit test нэмэгдсэн эсэх
- [ ] Test coverage хангалттай эсэх
- [ ] Edge case-үүд туршигдсан эсэх
- [ ] Test нэршил тодорхой эсэх

### 7. 📝 Coding Convention
- [ ] PEP 8 стандарт дагасан эсэх
- [ ] Flake8 error байхгүй эсэх
- [ ] Black format дагасан эсэх
- [ ] Import эрэмбэлэлт зөв эсэх (isort)

---

## 🛠️ Code Review хийх заавар

### Reviewer-ийн үүрэг:
1. **Эелдэг байх** - Санал шүүмжлэл бус, сургамжтай байх
2. **Тодорхой байх** - Яагаад өөрчлөх ёстойг тайлбарлах
3. **Жишээ өгөх** - Шаардлагатай үед код жишээ оруулах
4. **Асуулт асуух** - Ойлгохгүй зүйлээ асуух

### Comment төрлүүд:
- `[MUST]` - Заавал засах ёстой
- `[SHOULD]` - Засвал сайн болно
- `[NIT]` - Жижиг санал (optional)
- `[QUESTION]` - Асуулт

### Жишээ Review Comment:
```
[MUST] SQL injection эмзэг байдал:
Raw SQL query биш, ORM method ашигла.

Одоо:
db.execute(f"SELECT * FROM users WHERE id = {user_id}")

Засвар:
User.query.filter_by(id=user_id).first()
```

---

## 📊 Code Review-ийн үр дүн

### Approve хийх нөхцөл:
- [ ] Бүх `[MUST]` санал засагдсан
- [ ] Аюулгүй байдлын асуудал байхгүй
- [ ] Код компайл/ажиллаж байгаа
- [ ] Туршилт амжилттай

### Request Changes хийх нөхцөл:
- `[MUST]` санал байгаа
- Аюулгүй байдлын асуудал илэрсэн
- Код ажиллахгүй

---

## 📚 Ашигтай холбоосууд

- [PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Flask Best Practices](https://flask.palletsprojects.com/en/2.0.x/patterns/)

