from django.contrib import admin
from .models import Movie, CinemaHall, Showtime, Ticket, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'director', 'release_date', 'price']
    list_filter = ['genre', 'release_date']
    search_fields = ['title', 'director']
    
    readonly_fields = ['poster_preview']
    
    def poster_preview(self, obj):
        if obj.poster:
            return f'<img src="{obj.poster.url}" style="max-height: 200px;" />'
        elif obj.poster_url:
            return f'<img src="{obj.poster_url}" style="max-height: 200px;" />'
        return "Нет изображения"

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'hall', 'start_time', 'available_seats']
    list_filter = ['start_time', 'hall']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'showtime', 'quantity', 'total_price', 'status']
    list_filter = ['status', 'created_at']

admin.site.register(CinemaHall)
admin.site.register(Review)
