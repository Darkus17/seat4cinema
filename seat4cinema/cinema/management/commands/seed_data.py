from django.core.management.base import BaseCommand
from cinema.models import Movie, CinemaHall, Showtime
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('🎬 Начинаем заполнение базы данных...')
        
        # Очищаем старые данные
        Movie.objects.all().delete()
        CinemaHall.objects.all().delete()
        Showtime.objects.all().delete()
        self.stdout.write('✅ Старые данные очищены')

        # Создаем залы
        hall1 = CinemaHall.objects.create(name="Зал 1", seats=100)
        hall2 = CinemaHall.objects.create(name="Зал 2", seats=80)
        self.stdout.write('✅ Кинотеатры созданы')

        # Создаем фильмы (БЕЗ poster_url)
        movies_data = [
            {
                'title': "Интерстеллар", 
                'description': "Фантастический эпос о путешествии через червоточину",
                'duration': 169,
                'genre': "Фантастика",
                'director': "Кристофер Нолан",
                'price': 450
            },
            {
                'title': "Начало",
                'description': "Проникновение в сны с целью кражи идей", 
                'duration': 148,
                'genre': "Триллер",
                'director': "Кристофер Нолan",
                'price': 400
            }
        ]
        
        created_movies = []
        for movie_info in movies_data:
            movie = Movie.objects.create(
                **movie_info,
                release_date=timezone.now().date() - timedelta(days=10)
                # Убрали poster_url - его нет в вашей модели
            )
            created_movies.append(movie)
            self.stdout.write(f'✅ Создан фильм: {movie.title}')
        
        # Создаем сеансы
        for i in range(2):  # Создаем 2 сеанса для каждого фильма
            Showtime.objects.create(
                movie=created_movies[0],  # Интерстеллар
                hall=hall1,
                start_time=timezone.now() + timedelta(days=i, hours=14),
                end_time=timezone.now() + timedelta(days=i, hours=16, minutes=49),
                available_seats=hall1.seats
            )
            
            Showtime.objects.create(
                movie=created_movies[1],  # Начало
                hall=hall2,
                start_time=timezone.now() + timedelta(days=i, hours=16),
                end_time=timezone.now() + timedelta(days=i, hours=18, minutes=28),
                available_seats=hall2.seats
            )
        
        self.stdout.write('✅ Сеансы созданы')
        self.stdout.write('🎉 ВСЁ ГОТОВО! База заполнена тестовыми данными!')
        self.stdout.write(f'📊 Создано: {len(created_movies)} фильма, 2 зала, 4 сеанса')