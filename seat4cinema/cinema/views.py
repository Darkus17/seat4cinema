from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.db.models import Prefetch
from .models import Movie, Showtime, Ticket, Review
from .forms import TicketForm, ReviewForm
from .auth_forms import RegisterForm
from datetime import timedelta
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator

# Регистрация
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

# Главная страница - ОПТИМИЗИРОВАННАЯ
def home(request):
    # Оптимизированные запросы с ограничением количества
    now_showing = Movie.objects.filter(
        release_date__lte=timezone.now()
    ).select_related().order_by('-release_date')[:8]  # Увеличили лимит для сетки
    
    coming_soon = Movie.objects.filter(
        release_date__gt=timezone.now()
    ).select_related().order_by('release_date')[:6]  # 6 для карусели
    
    context = {
        'now_showing': now_showing,
        'coming_soon': coming_soon
    }
    
    # Для отладки производительности
    if request.GET.get('debug') and request.user.is_superuser:
        from django.db import connection
        context['queries'] = connection.queries
        context['queries_count'] = len(connection.queries)
    
    return render(request, 'cinema/home.html', context)

# Список фильмов - ОПТИМИЗИРОВАННЫЙ
def movie_list(request):
    movies = Movie.objects.all().select_related().order_by('-release_date')
    
    # Пагинация для больших списков
    from django.core.paginator import Paginator
    paginator = Paginator(movies, 12)  # 12 фильмов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'cinema/movie_list.html', {
        'page_obj': page_obj,
        'movies': page_obj.object_list  # для обратной совместимости
    })

# Детали фильма (с отзывами) - ОПТИМИЗИРОВАННЫЙ
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie.objects.select_related(), id=movie_id)
    
    # Оптимизированные запросы для связанных данных
    showtimes = Showtime.objects.filter(
        movie=movie, 
        start_time__gte=timezone.now()
    ).select_related('movie').order_by('start_time')
    
    reviews = Review.objects.filter(movie=movie).select_related('user').order_by('-created_at')[:10]  # лимит отзывов
    
    review_form = None
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв добавлен!')
            return redirect('movie_detail', movie_id=movie_id)
    else:
        if request.user.is_authenticated:
            review_form = ReviewForm()
    
    return render(request, 'cinema/movie_detail.html', {
        'movie': movie,
        'showtimes': showtimes,
        'reviews': reviews,
        'review_form': review_form
    })

# Бронирование билетов - ОПТИМИЗИРОВАННОЕ
@login_required
def book_ticket(request, showtime_id):
    showtime = get_object_or_404(
        Showtime.objects.select_related('movie'), 
        id=showtime_id
    )
    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.showtime = showtime
            
            # Проверка доступности мест
            if ticket.quantity > showtime.available_seats:
                messages.error(request, f'Недостаточно свободных мест! Доступно: {showtime.available_seats}')
                return render(request, 'cinema/book_ticket.html', {
                    'showtime': showtime,
                    'form': form
                })
            
            # Бронирование
            try:
                with transaction.atomic():
                    ticket.save()
                    showtime.available_seats -= ticket.quantity
                    showtime.save()
                    
                    messages.success(request, f'✅ Билеты успешно забронированы! Сумма: {ticket.total_price} руб.')
                    return redirect('my_tickets')
                    
            except Exception as e:
                messages.error(request, f'Ошибка при бронировании: {str(e)}')
    else:
        form = TicketForm(initial={'quantity': 1})
    
    return render(request, 'cinema/book_ticket.html', {
        'showtime': showtime,
        'form': form
    })

# Мои билеты - ОПТИМИЗИРОВАННЫЕ
@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(
        user=request.user
    ).select_related(
        'showtime', 
        'showtime__movie'
    ).order_by('-created_at')[:20]  # лимит билетов
    
    # Добавляем текущее время + 1 час для проверки в шаблоне
    now_plus_1h = timezone.now() + timedelta(hours=1)
    
    return render(request, 'cinema/my_tickets.html', {
        'tickets': tickets,
        'now_plus_1h': now_plus_1h
    })

# Отмена бронирования - ОПТИМИЗИРОВАННАЯ
@login_required
def cancel_booking(request, ticket_id):
    ticket = get_object_or_404(
        Ticket.objects.select_related('showtime'), 
        id=ticket_id, 
        user=request.user
    )
    
    # Проверяем можно ли отменить (не менее чем за 1 час до сеанса)
    can_cancel = timezone.now() + timedelta(hours=1) < ticket.showtime.start_time
    
    if request.method == 'POST':
        if not can_cancel:
            messages.error(request, '❌ Нельзя отменить бронь менее чем за 1 час до сеанса')
            return redirect('my_tickets')
        
        # Отменяем бронь и возвращаем места
        if ticket.status != 'cancelled':
            try:
                with transaction.atomic():
                    # Возвращаем места обратно
                    ticket.showtime.available_seats += ticket.quantity
                    ticket.showtime.save()
                    
                    # Меняем статус на отменен
                    ticket.status = 'cancelled'
                    ticket.save()
                    
                    messages.success(request, f'✅ Бронирование #{ticket.id} успешно отменено!')
                    messages.info(request, f'🔄 Возвращено {ticket.quantity} мест')
                    
            except Exception as e:
                messages.error(request, f'Ошибка при отмене брони: {str(e)}')
        else:
            messages.error(request, 'Бронь уже отменена')
        
        return redirect('my_tickets')
    
    # Показываем страницу подтверждения отмены
    context = {
        'ticket': ticket,
        'can_cancel': can_cancel
    }
    return render(request, 'cinema/cancel_booking.html', context)

# Новый метод для API карусели (опционально)
def coming_soon_api(request):
    """API для получения фильмов 'скоро в прокате' (для AJAX)"""
    coming_soon = Movie.objects.filter(
        release_date__gt=timezone.now()
    ).values('id', 'title', 'poster_url', 'release_date', 'price')[:6]
    
    import json
    from django.http import JsonResponse
    return JsonResponse(list(coming_soon), safe=False)

def search(request):
    q = request.GET.get('q', '').strip()
    page_number = request.GET.get('page')

    # пустой запрос — можно перенаправить на список или показать пустой результат
    if not q:
        movies = Movie.objects.none()
        total = 0
    else:
        # простое текстовое совпадение по нескольким полям
        movies_qs = Movie.objects.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(genre__icontains=q) |
            Q(director__icontains=q)
        ).order_by('-release_date')

        # можно заранее ограничить поля/количество загрузки для скорости
        movies = movies_qs
        total = movies_qs.count()

    paginator = Paginator(movies, 12)  # 12 результатов на страницу
    page_obj = paginator.get_page(page_number)

    return render(request, 'cinema/movie_list.html', {
        'page_obj': page_obj,
        'movies': page_obj.object_list,
        'q': q,
        'total': total,
        'is_search': True,  # флаг в шаблоне чтобы показать заголовок
    })