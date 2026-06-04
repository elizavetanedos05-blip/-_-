from django.db import models


class Worker(models.Model):
    """Работник (доярка, тракторист и т.д.)"""
    full_name = models.CharField(max_length=100, verbose_name="ФИО")
    position = models.CharField(max_length=100, verbose_name="Должность")
    def __str__(self):
        return f"{self.full_name} ({self.position})"
    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

class SpecOdejda(models.Model):
    """Номенклатура спецодежды на складе"""
    TYPES = [
        ('upper', 'Верхняя одежда'),
        ('shoes', 'Обувь'),
        ('gloves', 'Перчатки'),
        ('head', 'Головной убор'),
        ('other', 'Прочее'),
    ]

    name = models.CharField(max_length=150, verbose_name="Наименование")
    type = models.CharField(max_length=20, choices=TYPES, verbose_name="Тип")
    size = models.CharField(max_length=10, verbose_name="Размер")
    norm_days = models.IntegerField(verbose_name="Срок носки по нормативу (дней)")
    quantity_in_stock = models.IntegerField(default=0, verbose_name="Количество на складе")

    def __str__(self):
        return f"{self.name} (разм. {self.size})"

    class Meta:
        verbose_name = "Единица спецодежды"
        verbose_name_plural = "Спецодежда"


class IssuedItem(models.Model):
    """Журнал выдачи: какая вещь кому выдана и её текущее состояние"""
    STATUSES = [
        ('issued', 'Выдана'),
        ('worn_out', 'Изношена'),
        ('written_off', 'Списана'),
    ]

    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name="Работник")
    spec_odejda = models.ForeignKey(SpecOdejda, on_delete=models.CASCADE, verbose_name="Спецодежда")
    issue_date = models.DateField(auto_now_add=True, verbose_name="Дата выдачи")
    wear_level = models.IntegerField(default=0, verbose_name="Износ (%)")
    status = models.CharField(max_length=20, choices=STATUSES, default='issued', verbose_name="Статус")

    def __str__(self):
        return f"{self.spec_odejda.name} → {self.worker.full_name}"

    class Meta:
        verbose_name = "Запись о выдаче"
        verbose_name_plural = "Журнал выдачи"
