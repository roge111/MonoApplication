from django.shortcuts import render, redirect
from datetime import datetime, date
from managers.dataBase import DataBaseManager
# Create your views here.



db = DataBaseManager()


# forms.py
from django import forms

class TransactionForm(forms.Form):
    # Добавляем choices для выпадающих списков
    CURRENCY_CHOICES = [
        ('доллары', 'Доллары'),
        ('рубли', 'Рубли'),
        ('евро', 'Евро'),
        ('юани', 'Юани'),
    ]
    
    STATUS_CHOICES = [
        ('новая', 'Новая'),
        ('в работе', 'В работе'),
        ('завершена', 'Завершена'),
    ]
    
    title = forms.CharField(
        max_length=100,
        label='Название транзакции'
    )
    amount = forms.IntegerField(
        label='Сумма'
    )
    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        label='Валюта'
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label='Статус'
    )

"""
Обрабатывает добавление новой транзакции в базу данных.

Функция принимает HTTP-запрос и обрабатывает данные формы для добавления
новой транзакции. Поддерживает как GET, так и POST запросы.

Args:
    request (HttpRequest): Объект HTTP-запроса, содержащий данные формы
    
Returns:
    HttpResponse: Отрендеренный шаблон 'table.html' с формой TransactionForm
    
Метод POST:
    - Извлекает данные из формы (title, amount, currency, status)
    - Выполняет SQL-запрос INSERT для добавления транзакции в базу данных
    
Метод GET:
    - Отображает пустую форму для ввода данных новой транзакции
"""
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


from django.contrib import messages
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

@main_auth(on_cookies=True)
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            currency = form.cleaned_data['currency']
            status = form.cleaned_data['status']
            current_date = date.today()
            # Безопасный запрос к базе данных
            db.query_database(
                f"INSERT INTO transaction (title, amount, currency, status, created_date) VALUES ('{title}', {amount}, '{currency}', '{status}', '{current_date}');", 
                reg=True
            )
            
            # Сообщение об успехе
            messages.success(request, 'Транзакция успешно добавлена!')
            
            # Перенаправление на страницу таблицы
            return redirect('table_transaction')
    else:
        form = TransactionForm()
    
    return render(request, 'transactions/add_transaction.html', locals())
@main_auth( on_cookies=True)
def table_transaction(request):
    
    information = db.query_database("""
        SELECT * FROM transaction 
        ORDER BY id DESC 
        LIMIT 10
    """)
    
    # Правильный порядок заголовков согласно вашей структуре таблицы
    headers = ['ID', 'Название', 'Сумма', 'Валюта', 'Дата', 'Статус']
    
    # context = {'information': information, 'headers': headers}
    return render(request, 'transactions/table_transaction.html', locals())

    
