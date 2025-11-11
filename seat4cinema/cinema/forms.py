from django import forms
from .models import Ticket, Review

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                # УБИРАЕМ 'max': 10 - чтобы можно было брать все билеты!
                'value': 1
            })
        }
    
    def __init__(self, *args, **kwargs):
        # Получаем максимальное количество из контекста (если передано)
        self.max_tickets = kwargs.pop('max_tickets', None)
        super().__init__(*args, **kwargs)
        
        # Если знаем максимум, устанавливаем его в поле
        if self.max_tickets:
            self.fields['quantity'].widget.attrs['max'] = self.max_tickets

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 5,
                'value': 5
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Оставьте ваш отзыв...'
            })
        }