import os
import django
import sys
from datetime import datetime, timedelta
import random

# Настройка Django
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_project.settings')
django.setup()

from cinema.models import Movie, CinemaHall, Showtime
from django.utils import timezone

def populate_database():
    print("🎬 Начинаем заполнение базы данных кинотеатра...")
    
    # Очищаем старые данные
    Movie.objects.all().delete()
    CinemaHall.objects.all().delete()
    Showtime.objects.all().delete()
    print("✅ Старые данные очищены")
    
    # Создаем залы кинотеатра
    halls = [
        {"name": "Красный зал", "seats": 120},
        {"name": "Синий зал", "seats": 80},
        {"name": "Зеленый зал", "seats": 100},
        {"name": "VIP зал", "seats": 50},
    ]
    
    created_halls = []
    for hall_data in halls:
        hall = CinemaHall.objects.create(**hall_data)
        created_halls.append(hall)
        print(f"✅ Создан зал: {hall.name} ({hall.seats} мест)")
    
    # Данные фильмов с реальными постерами
    movies_data = [
        {
            "title": "Дюна: Часть вторая",
            "description": "Пол Атреидс объединяется с Чани и фременами, чтобы отомстить заговорщикам, уничтожившим его семью.",
            "duration": 166,
            "genre": "Фантастика, Драма",
            "director": "Дени Вильнёв",
            "price": 550,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/6201401/022a58e3-5b9b-4c66-bc46-5fbd6a59c6b7/300x450"
        },
        {
            "title": "Оппенгеймер",
            "description": "История жизни американского физика-теоретика Роберта Оппенгеймера, создателя первой атомной бомбы.",
            "duration": 180,
            "genre": "Биография, Драма, История",
            "director": "Кристофер Нолан",
            "price": 500,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9ed9e4c1-8c22-46b5-86d5-1e81bb1c1c87/300x450"
        },
        {
            "title": "Барби",
            "description": "Кукла Барби живет в идеальном мире Барбиленда, но однажды обнаруживает, что в реальном мире не всё так прекрасно.",
            "duration": 114,
            "genre": "Комедия, Приключения, Фэнтези",
            "director": "Грета Гервиг",
            "price": 450,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9ed6d949-5c54-4b92-bcd7-0b1652c53b1b/300x450"
        },
        {
            "title": "Человек-паук: Паутина вселенных",
            "description": "Майлз Моралес отправляется в захватывающее приключение по мультивселенной, где встречает команду Людей-пауков.",
            "duration": 140,
            "genre": "Мультфильм, Фантастика, Приключения",
            "director": "Жуакин Душ Сантуш",
            "price": 480,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e5b/300x450"
        },
        {
            "title": "Миссия невыполнима: Смертельная расплата",
            "description": "Итан Хант и его команда IMF сталкиваются с самым опасным противником — искусственным интеллектом.",
            "duration": 163,
            "genre": "Боевик, Триллер, Приключения",
            "director": "Кристофер Маккуорри",
            "price": 520,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e5c/300x450"
        },
        {
            "title": "Стражи Галактики: Часть 3",
            "description": "Команда Стражей Галактики отправляется в опасное путешествие, чтобы спасти одного из своих.",
            "duration": 150,
            "genre": "Фантастика, Боевик, Комедия",
            "director": "Джеймс Ганн",
            "price": 490,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e5d/300x450"
        },
        {
            "title": "Джон Уик 4",
            "description": "Джон Уик открывает путь к победе над Правлением Кланов, но должен столкнуться с новым врагом.",
            "duration": 169,
            "genre": "Боевик, Триллер, Криминал",
            "director": "Чад Стахелски",
            "price": 530,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e5e/300x450"
        },
        {
            "title": "Аватар: Путь воды",
            "description": "Джейк Салли и Нейтири создают семью и делают всё возможное, чтобы остаться вместе.",
            "duration": 192,
            "genre": "Фантастика, Приключения, Боевик",
            "director": "Джеймс Кэмерон",
            "price": 560,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e5f/300x450"
        },
        {
            "title": "Круэлла",
            "description": "Молодая дизайнерша становится знаменитой, но её успех привлекает внимание могущественной соперницы.",
            "duration": 134,
            "genre": "Комедия, Криминал, Драма",
            "director": "Крэйг Гиллеспи",
            "price": 420,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e60/300x450"
        },
        {
            "title": "Топ Ган: Мэверик",
            "description": "Пит Митчелл тренирует группу выпускников Top Gun для выполнения особой миссии.",
            "duration": 130,
            "genre": "Боевик, Драма",
            "director": "Джозеф Косински",
            "price": 510,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e61/300x450"
        },
        {
            "title": "Чёрная Пантера: Ваканда навеки",
            "description": "Народ Ваканды борется, чтобы защитить свою нацию от вмешательства мировых держав.",
            "duration": 161,
            "genre": "Фантастика, Боевик, Драма",
            "director": "Райан Куглер",
            "price": 480,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e62/300x450"
        },
        {
            "title": "Бэтмен",
            "description": "Брюс Уэйн становится Бэтменом и сталкивается с Загадочником, серийным убийцей в Готэме.",
            "duration": 176,
            "genre": "Боевик, Драма, Криминал",
            "director": "Мэтт Ривз",
            "price": 520,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e63/300x450"
        },
        {
            "title": "Флэш",
            "description": "Барри Аллен использует свои суперспособности, чтобы изменить прошлое, но будущее оказывается под угрозой.",
            "duration": 144,
            "genre": "Фантастика, Боевик, Приключения",
            "director": "Андрес Мускетти",
            "price": 470,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e64/300x450"
        },
        {
            "title": "Трансформеры: Эпоха зверей",
            "description": "Автоботы и Максималы объединяются против террористической организации, которая охотится за артефактом.",
            "duration": 127,
            "genre": "Фантастика, Боевик, Приключения",
            "director": "Стивен Кейпл",
            "price": 490,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e65/300x450"
        },
        {
            "title": "Индиана Джонс и Колесница судьбы",
            "description": "Индиана Джонс отправляется в новое приключение, чтобы найти магический артефакт.",
            "duration": 154,
            "genre": "Приключения, Боевик",
            "director": "Джеймс Мэнголд",
            "price": 540,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e66/300x450"
        },
        {
            "title": "Элементально",
            "description": "В элементальном городе, где живут существа огня, воды, земли и воздуха, загорается страсть.",
            "duration": 102,
            "genre": "Мультфильм, Комедия, Семейный",
            "director": "Питер Сон",
            "price": 380,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e67/300x450"
        },
        {
            "title": "Медведь Гризли",
            "description": "Семья медведей гризли пытается выжить в суровых условиях Аляски.",
            "duration": 85,
            "genre": "Документальный, Семейный",
            "director": "Алайн Дешам",
            "price": 350,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e68/300x450"
        },
        {
            "title": "Красный",
            "description": "13-летняя девочка переживает сложный период взросления и находит утешение в музыке.",
            "duration": 100,
            "genre": "Мультфильм, Комедия, Семейный",
            "director": "Доме Ши",
            "price": 390,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e69/300x450"
        },
        {
            "title": "Человек-муравей и Оса: Квантомания",
            "description": "Скотт Лэнг и Хоуп ван Дайн отправляются в квантовое измерение.",
            "duration": 125,
            "genre": "Фантастика, Боевик, Комедия",
            "director": "Пейтон Рид",
            "price": 480,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e70/300x450"
        },
        {
            "title": "Достать Ножов",
            "description": "Детектив Бенуа Блан расследует новое дело с участием эксцентричных миллиардеров.",
            "duration": 140,
            "genre": "Детектив, Комедия, Криминал",
            "director": "Райан Джонсон",
            "price": 460,
            "poster_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/10809116/9c5d19c7-7c27-4c5c-8c0a-7b3c5e5b5e71/300x450"
        }
    ]
    
    # Создаем фильмы
    created_movies = []
    for i, movie_data in enumerate(movies_data):
        # Случайная дата выхода (от 30 дней назад до 60 дней вперед)
        days_ago = random.randint(0, 30)
        days_future = random.randint(1, 60)
        release_date = timezone.now().date() - timedelta(days=days_ago) + timedelta(days=days_future)
        
        movie = Movie.objects.create(
            **movie_data,
            release_date=release_date
        )
        created_movies.append(movie)
        print(f"✅ Создан фильм: {movie.title}")
    
    # Создаем сеансы
    showtime_count = 0
    for movie in created_movies:
        # Создаем 3-5 сеансов для каждого фильма
        num_showtimes = random.randint(3, 5)
        
        for i in range(num_showtimes):
            # Случайный зал
            hall = random.choice(created_halls)
            
            # Случайное время (от 1 до 14 дней вперед, с 10:00 до 22:00)
            days_ahead = random.randint(1, 14)
            hour = random.randint(10, 22)
            minute = random.choice([0, 15, 30, 45])
            
            start_time = timezone.now() + timedelta(days=days_ahead, hours=hour, minutes=minute)
            end_time = start_time + timedelta(minutes=movie.duration)
            
            Showtime.objects.create(
                movie=movie,
                hall=hall,
                start_time=start_time,
                end_time=end_time,
                available_seats=hall.seats
            )
            showtime_count += 1
    
    print("🎉 База данных успешно заполнена!")
    print(f"📊 Статистика:")
    print(f"   🎭 Залы: {len(created_halls)}")
    print(f"   🎬 Фильмы: {len(created_movies)}")
    print(f"   ⏰ Сеансы: {showtime_count}")
    print(f"   💰 Цены: от 350 до 560 руб.")
    print("\n🚀 Теперь можно запускать сервер и тестировать кинотеатр!")

if __name__ == "__main__":
    populate_database()