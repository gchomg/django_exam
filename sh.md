python3 -m venv venv
source venv/bin/activate
pip install django python-dotenv whitenoise
python3 manage.py runserver

После запуска открыть в браузере:
- http://127.0.0.1:8000/ — сайт
- http://127.0.0.1:8000/admin/ — админка (login: admin, password: admin)
- http://127.0.0.1:8000/ping/ — тест (должен вернуть OK)

---

## 🔧 ЧАСТЫЕ ОШИБКИ И КАК ИСПРАВИТЬ

### ❌ No module named 'django'
```bash
pip install django python-dotenv whitenoise
# если не работает:
pip3 install django python-dotenv whitenoise --break-system-packages
# если всё равно не работает:
sudo apt install python3-django -y
pip3 install python-dotenv whitenoise --break-system-packages
```

### ❌ No module named 'dotenv'
```bash
pip3 install python-dotenv --break-system-packages
# если не работает:
sudo pip3 install python-dotenv
```

### ❌ venv не активируется (source venv/bin/activate — нет файла)
```bash
python3 -m venv venv
source venv/bin/activate
pip install django python-dotenv whitenoise
```

### ❌ Authentication failed (git push не работает)
Нужен новый токен:
1. github.com → аватарка → Settings → Developer settings → Tokens (classic) → Generate new token
2. Поставить галочку repo → Generate
3. Скопировать токен
```bash
git remote set-url origin https://gchomg:ВАШ_ТОКЕН@github.com/gchomg/django_exam.git
git push
```

### ❌ That port is already in use (порт занят)
```bash
python3 manage.py runserver 8080
# открывать http://127.0.0.1:8080/
```

### ❌ Table has no column (ошибка после изменения модели)
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### ❌ OperationalError: no such table
```bash
python3 manage.py migrate
```

### ❌ django.db.utils.IntegrityError (дубликат уникального поля)
Это нормально — валидация работает правильно.

### ❌ TemplateDoesNotExist
Проверить что папка templates существует:
```bash
ls products/templates/products/
# должны быть: base.html, index.html, form.html, confirm_delete.html
```

---

## 📋 ПОЛЕЗНЫЕ КОМАНДЫ

```bash
# Применить миграции
python3 manage.py migrate

# Создать миграции после изменения модели
python3 manage.py makemigrations

# Создать суперпользователя вручную
python3 manage.py createsuperuser

# Запустить тесты
python3 manage.py test

# Показать все миграции
python3 manage.py showmigrations

# Запустить сервер
python3 manage.py runserver

# Собрать статику
python3 manage.py collectstatic --noinput
```

---

## 🗂️ СТРУКТУРА ПРОЕКТА — ЧТО ГДЕ ЛЕЖИТ

```
django_exam/
├── manage.py                  ← точка входа, не трогать
├── setup.sh                   ← скрипт запуска
├── .env                       ← переменные окружения
├── requirements.txt           ← список библиотек
│
├── products_project/          ← папка настроек проекта
│   ├── settings.py            ← ВСЕ НАСТРОЙКИ (БД, приложения, middleware)
│   ├── urls.py                ← главные маршруты
│   └── wsgi.py                ← не трогать
│
└── products/                  ← само приложение
    ├── models.py              ← МОДЕЛЬ (таблица в БД) ← МЕНЯТЬ ПОД ВАРИАНТ
    ├── views.py               ← ЛОГИКА (что делать с запросами) ← МЕНЯТЬ
    ├── forms.py               ← ФОРМА (поля для ввода) ← МЕНЯТЬ
    ├── urls.py                ← МАРШРУТЫ приложения ← МЕНЯТЬ НАЗВАНИЯ
    ├── admin.py               ← настройка админки ← МЕНЯТЬ
    ├── middleware.py          ← счётчик запросов, не трогать
    ├── tests.py               ← тесты ← МЕНЯТЬ под новую модель
    └── templates/products/
        ├── base.html          ← шапка сайта, можно не трогать
        ├── index.html         ← список записей ← МЕНЯТЬ поля
        ├── form.html          ← форма создания/редактирования, можно не трогать
        └── confirm_delete.html← подтверждение удаления, можно не трогать
```

---

## ✏️ КАК АДАПТИРОВАТЬ ПОД ДРУГОЙ ВАРИАНТ

### Вариант 2 — Мероприятия (events): пример адаптации

### ШАГ 1 — models.py
Меняешь поля под свою задачу:
```python
# БЫЛО (товары):
class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    category = models.CharField(max_length=100, blank=True, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    sku = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

# СТАЛО (мероприятия):
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    location = models.CharField(max_length=150, verbose_name='Место')
    event_date = models.DateTimeField(verbose_name='Дата проведения')
    max_guests = models.IntegerField(verbose_name='Макс. гостей')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.title or not self.title.strip():
            raise ValidationError({'title': 'Название не может быть пустым.'})
        if self.event_date and self.event_date <= timezone.now():
            raise ValidationError({'event_date': 'Дата должна быть в будущем.'})
        if self.max_guests is not None and self.max_guests <= 0:
            raise ValidationError({'max_guests': 'Количество гостей должно быть больше 0.'})
```

### ШАГ 2 — forms.py
Меняешь название класса и поля:
```python
# БЫЛО:
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'sku']

# СТАЛО:
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'location', 'event_date', 'max_guests']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'max_guests': forms.NumberInput(attrs={'class': 'form-control'}),
        }
```

### ШАГ 3 — views.py
Меняешь импорты и названия:
```python
# БЫЛО:
from .models import Product
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/index.html', {'object_list': products})

def product_create(request):
    ...
    form = ProductForm(request.POST)

# СТАЛО:
from .models import Event
from .forms import EventForm

def product_list(request):  # название функции можно оставить
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'products/index.html', {'object_list': events})

def product_create(request):
    ...
    form = EventForm(request.POST)
```

### ШАГ 4 — admin.py
```python
# БЫЛО:
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'sku', 'created_at')

# СТАЛО:
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'event_date', 'max_guests', 'created_at')
```

### ШАГ 5 — migrations (после изменения модели!)
```bash
# Удалить старую миграцию и создать новую:
rm products/migrations/0001_initial.py
python3 manage.py makemigrations
python3 manage.py migrate
```

### ШАГ 6 — index.html (поменять названия колонок)
Открыть `products/templates/products/index.html` и поменять:
```html
<!-- БЫЛО: -->
<th>Название</th><th>Категория</th><th>Цена</th><th>Артикул</th>
...
<td>{{ obj.name }}</td>
<td>{{ obj.category }}</td>
<td>{{ obj.price }}</td>
<td>{{ obj.sku }}</td>

<!-- СТАЛО: -->
<th>Название</th><th>Место</th><th>Дата</th><th>Гостей</th>
...
<td>{{ obj.title }}</td>
<td>{{ obj.location }}</td>
<td>{{ obj.event_date|date:"d.m.Y H:i" }}</td>
<td>{{ obj.max_guests }}</td>
```

---

## 🧠 ОБЪЯСНЕНИЕ КОДА — ЧТО ДЕЛАЕТ КАЖДЫЙ ФАЙЛ

### models.py — модель = таблица в базе данных
```python
class Product(models.Model):        # один класс = одна таблица в БД
    name = models.CharField(...)    # CharField = текстовое поле (VARCHAR)
    price = models.DecimalField(...)# DecimalField = число с запятой
    sku = models.CharField(unique=True) # unique=True = значение уникальное
    created_at = models.DateTimeField(auto_now_add=True) # заполняется автоматически

    def clean(self):                # валидация — проверка данных перед сохранением
        if self.price <= 0:
            raise ValidationError(...)  # если цена <= 0, выбросить ошибку
```

### views.py — логика обработки запросов
```python
def product_list(request):          # GET / → показать список
    products = Product.objects.all()# взять все записи из БД
    return render(request, 'products/index.html', {'object_list': products})
    # передать данные в шаблон

def product_create(request):
    if request.method == 'POST':    # если форма отправлена
        form = ProductForm(request.POST)
        if form.is_valid():         # если данные валидны
            form.save()             # сохранить в БД
            return redirect('index')# перенаправить на список
    else:                           # если просто открыли страницу
        form = ProductForm()        # показать пустую форму
    return render(request, 'products/form.html', {'form': form})
```

### urls.py — маршруты (какой URL → какая функция)
```python
urlpatterns = [
    path('ping/', views.ping, name='ping'),           # /ping/
    path('', views.product_list, name='index'),        # /
    path('create/', views.product_create, name='create'), # /create/
    path('<int:pk>/update/', views.product_update, name='update'), # /1/update/
    path('<int:pk>/delete/', views.product_delete, name='delete'), # /1/delete/
]
```

### middleware.py — считает запросы
Автоматически считает сколько было запросов и выводит в консоль. Не трогать!

### settings.py — главные настройки
- `INSTALLED_APPS` — список приложений (туда добавляется 'products')
- `MIDDLEWARE` — список middleware (туда добавляется MetricsMiddleware)
- `DATABASES` — настройки базы данных
- `TEMPLATES` — настройки шаблонов

---

## ✅ ЧЕКЛИСТ ПЕРЕД СДАЧЕЙ

- [ ] Сайт открывается: http://127.0.0.1:8000/
- [ ] Можно добавить запись
- [ ] Можно редактировать запись
- [ ] Можно удалить запись (с подтверждением)
- [ ] Валидация работает (попробовать сохранить пустое поле или неверные данные)
- [ ] 404 при несуществующем ID: http://127.0.0.1:8000/9999/update/
- [ ] Админка работает: http://127.0.0.1:8000/admin/
- [ ] Тесты проходят: `python3 manage.py test`
- [ ] Метрики видны в терминале при запросах
- [ ] /ping/ возвращает OK: http://127.0.0.1:8000/ping/