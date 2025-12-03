"""
FitProof - Апп эхлүүлэх
Лабораторийн ажил 5: US1 хэрэгжүүлэлт
"""

from app import create_app, db
from app.models import User, Equipment, WorkoutSession

app = create_app('development')


@app.shell_context_processor
def make_shell_context():
    """Flask shell-д ашиглах объектууд"""
    return {
        'db': db,
        'User': User,
        'Equipment': Equipment,
        'WorkoutSession': WorkoutSession
    }


def init_sample_data():
    """Туршилтын өгөгдөл оруулах"""
    with app.app_context():
        # Хэрэв өгөгдөл байвал алгасах
        if User.query.first():
            print("Өгөгдөл аль хэдийн байна.")
            return

        print("Туршилтын өгөгдөл оруулж байна...")

        # Админ хэрэглэгч
        admin = User(
            username='admin',
            email='admin@fitproof.mn',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Дасгалжуулагч
        trainer = User(
            username='trainer',
            email='trainer@fitproof.mn',
            role='trainer',
            xp_points=500
        )
        trainer.set_password('trainer123')
        db.session.add(trainer)

        # Гишүүд
        members = [
            ('bataa', 'bataa@fitproof.mn', 250),
            ('sarnai', 'sarnai@fitproof.mn', 180),
            ('bold', 'bold@fitproof.mn', 320),
            ('oyuka', 'oyuka@fitproof.mn', 150),
        ]

        for username, email, xp in members:
            user = User(
                username=username,
                email=email,
                role='member',
                xp_points=xp
            )
            user.set_password('password123')
            db.session.add(user)

        # Төхөөрөмжүүд
        equipment_list = [
            ('Treadmill 1', 'EQ001-TREADMILL', 'cardio', 'Гүйлтийн зам 1'),
            ('Treadmill 2', 'EQ002-TREADMILL', 'cardio', 'Гүйлтийн зам 2'),
            ('Bench Press', 'EQ003-BENCH', 'strength', 'Өргөлтийн ширээ'),
            ('Squat Rack', 'EQ004-SQUAT', 'strength', 'Сквот рэк'),
            ('Leg Press', 'EQ005-LEGPRESS', 'strength', 'Хөлний машин'),
            ('Lat Pulldown', 'EQ006-LAT', 'strength', 'Латын татах машин'),
            ('Rowing Machine', 'EQ007-ROW', 'cardio', 'Сэлэлтийн машин'),
            ('Exercise Bike', 'EQ008-BIKE', 'cardio', 'Дугуйн машин'),
            ('Dumbbell Rack', 'EQ009-DUMBBELL', 'strength', 'Гантелийн тавиур'),
            ('Yoga Mat Area', 'EQ010-YOGA', 'flexibility', 'Йогийн талбай'),
        ]

        for name, qr_code, eq_type, desc in equipment_list:
            eq = Equipment(
                name=name,
                qr_code=qr_code,
                equipment_type=eq_type,
                description=desc
            )
            db.session.add(eq)

        db.session.commit()
        print("✅ Туршилтын өгөгдөл амжилттай нэмэгдлээ!")
        print("\nНэвтрэх мэдээлэл:")
        print("  Admin: admin / admin123")
        print("  Trainer: trainer / trainer123")
        print("  Member: bataa / password123")


if __name__ == '__main__':
    # Туршилтын өгөгдөл оруулах
    init_sample_data()

    # Апп эхлүүлэх
    print("\n🚀 FitProof сервер эхэллээ!")
    print("📍 http://127.0.0.1:5000")
    print("\nЗогсоох: Ctrl+C\n")

    app.run(debug=True, host='127.0.0.1', port=5000)

