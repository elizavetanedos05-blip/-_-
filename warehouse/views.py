from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Worker, SpecOdejda, IssuedItem


def dashboard(request):
    """Главная страница с общей статистикой"""
    workers_count = Worker.objects.count()
    items_count = SpecOdejda.objects.count()
    issued_count = IssuedItem.objects.filter(status='issued').count()
    worn_count = IssuedItem.objects.filter(status='worn_out').count()
    # Предметы с износом больше 70% (требуют внимания)
    worn_items = IssuedItem.objects.filter(wear_level__gte=50, status='issued')

    context = {
        'workers_count': workers_count,
        'items_count': items_count,
        'issued_count': issued_count,
        'worn_count': worn_count,
        'worn_items': worn_items,
    }
    return render(request, 'warehouse/dashboard.html', context)


def worker_list(request):
    """Список всех работников"""
    workers = Worker.objects.all()
    return render(request, 'warehouse/worker_list.html', {'workers': workers})


def stock_list(request):
    """Остатки на складе"""
    stock = SpecOdejda.objects.all()
    return render(request, 'warehouse/stock_list.html', {'stock': stock})


def issue_form(request):
    """Форма выдачи одежды работнику"""
    if request.method == 'POST':
        worker_id = request.POST.get('worker_id')
        item_id = request.POST.get('item_id')
        worker = Worker.objects.get(id=worker_id)
        item = SpecOdejda.objects.get(id=item_id)
        # Проверяем, есть ли на складе
        if item.quantity_in_stock > 0:
            # Создаём запись о выдаче
            IssuedItem.objects.create(
                worker=worker,
                spec_odejda=item,
                wear_level=0,  # Новая вещь — износ 0%
            )
            # Уменьшаем количество на складе
            item.quantity_in_stock -= 1
            item.save()
            messages.success(request, f' {item.name} выдано работнику {worker.full_name}')
        else:
            messages.error(request, f' {item.name} отсутствует на складе!')

        return redirect('issue_form')
    # GET-запрос — показываем форму
    workers = Worker.objects.all()
    # Показываем только то, что есть в наличии
    items = SpecOdejda.objects.filter(quantity_in_stock__gt=0)
    recent_issues = IssuedItem.objects.all().order_by('-issue_date')[:10]
    context = {
        'workers': workers,
        'items': items,
        'recent_issues': recent_issues,
    }
    return render(request, 'warehouse/issue_form.html', context)


def run_simulation(request):
    """
    Имитация одного месяца работы.
    Каждая выданная вещь изнашивается на случайную величину (20-40%).
    """
    issued_items = IssuedItem.objects.filter(status='issued')

    for item in issued_items:
        # Имитируем износ: добавляем случайные 20-40%
        import random
        wear_increase = random.randint(20, 40)
        item.wear_level += wear_increase

        # Если износ достиг или превысил 100% — вещь изношена
        if item.wear_level >= 100:
            item.wear_level = 100
            item.status = 'worn_out'

        item.save()

    messages.info(request, f'⚙ Имитация завершена! Обработано {issued_items.count()} записей.')
    return redirect('dashboard')

def worn_items_list(request):
    """Список всей изношенной одежды"""
    worn_items = IssuedItem.objects.filter(status='worn_out').order_by('-issue_date')
    return render(request, 'warehouse/worn_items.html', {'worn_items': worn_items})