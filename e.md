
```bash
git clone https://github.com/gchomg/django_exam.git
cd django_exam
bash setup.sh
```

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
# если всё равно не работает:
sudo apt install python3-dotenv -y
```

### ❌ No module named 'whitenoise'
```bash
pip3 install whitenoise --break-system-packages
```

### ❌ venv не активируется
```bash
python3 -m venv venv
source venv/bin/activate
pip install django python-dotenv whitenoise
```


### ❌ That port is already in use (порт занят)
```bash
python3 manage.py runserver 8080
# открывать http://127.0.0.1:8080/
```

### ❌ Table has no column / OperationalError: no such table
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### ❌ TemplateDoesNotExist
```bash
ls products/templates/products/
# должны быть: base.html, index.html, form.html, confirm_delete.html
```

### ❌ NameError: name 'X' is not defined
Забыла импортировать. Добавь в начало файла нужный импорт.

---

## 📋 ПОЛЕЗНЫЕ КОМАНДЫ

```bash
python3 manage.py migrate                    # применить миграции
python3 manage.py makemigrations             # создать миграции после изменения модели
python3 manage.py createsuperuser            # создать суперпользователя вручную
python3 manage.py test                       # запустить тесты
python3 manage.py showmigrations             # показать все миграции
python3 manage.py runserver                  # запустить сервер
python3 manage.py collectstatic --noinput    # собрать статику
```

---

## 🗂️ СТРУКТУРА ПРОЕКТА — ЧТО ГДЕ ЛЕЖИТ

```
django_exam/
├── manage.py                  ← точка входа, не трогать
├── setup.sh                   ← скрипт запуска на экзамене
├── .env                       ← переменные окружения
│
├── products_project/
│   ├── settings.py            ← настройки (БД, приложения, middleware)
│   ├── urls.py                ← главные маршруты — не трогать
│   └── wsgi.py                ← не трогать
│
└── products/
    ├── models.py              ← ★ МЕНЯТЬ — модель (таблица в БД)
    ├── views.py               ← ★ МЕНЯТЬ — логика обработки запросов
    ├── forms.py               ← ★ МЕНЯТЬ — форма для ввода данных
    ├── urls.py                ← можно не трогать
    ├── admin.py               ← ★ МЕНЯТЬ — настройка админки
    ├── middleware.py          ← не трогать
    ├── tests.py               ← желательно поменять под новую модель
    └── templates/products/
        ├── base.html          ← не трогать
        ├── index.html         ← ★ МЕНЯТЬ — поля в таблице
        ├── form.html          ← не трогать (форма универсальная)
        └── confirm_delete.html← не трогать
```

---

## 📦 ВСЕ ТИПЫ ПОЛЕЙ МОДЕЛИ (Django)

### Текстовые поля
```python
# Короткий текст (до N символов) — VARCHAR в БД
name = models.CharField(max_length=200)

# Длинный текст без ограничений — TEXT в БД
content = models.TextField()

# Email (автоматически проверяет формат email)
email = models.EmailField(max_length=100, unique=True)

# URL (проверяет что это ссылка)
website = models.URLField()
```

### Числовые поля
```python
# Целое число — INTEGER в БД
age = models.IntegerField()
views = models.IntegerField(default=0)  # по умолчанию 0

# Число с дробной частью — DECIMAL в БД (точное, для денег)
price = models.DecimalField(max_digits=10, decimal_places=2)
salary = models.DecimalField(max_digits=10, decimal_places=2)

# Число с дробной частью — FLOAT в БД (менее точное)
rating = models.FloatField()
```

### Дата и время
```python
# Только дата (год-месяц-день) — DATE в БД
hire_date = models.DateField()
published_at = models.DateField(default=datetime.date.today)  # по умолчанию сегодня

# Дата + время — TIMESTAMP в БД
event_date = models.DateTimeField()
created_at = models.DateTimeField(auto_now_add=True)  # заполняется автоматически при создании
updated_at = models.DateTimeField(auto_now=True)       # обновляется при каждом сохранении
```

### Булево поле
```python
# True/False — BOOLEAN в БД
is_published = models.BooleanField(default=False)
is_active = models.BooleanField(default=True)
```

### Дополнительные параметры полей
```python
unique=True          # значение должно быть уникальным
blank=True           # поле необязательно в форме
null=True            # поле может быть NULL в БД
default=0            # значение по умолчанию
verbose_name='Имя'   # название поля в админке
```

---

## ✏️ КАК АДАПТИРОВАТЬ ПОД ДРУГОЙ ВАРИАНТ

### ★ ВАРИАНТ 1 — Сотрудники (employees)

#### models.py
```python
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

class Employee(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='Полное имя')
    position = models.CharField(max_length=100, verbose_name='Должность')
    hire_date = models.DateField(verbose_name='Дата приёма')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Зарплата')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.full_name} ({self.position})'

    def clean(self):
        if not self.full_name or not self.full_name.strip():
            raise ValidationError({'full_name': 'Имя не может быть пустым.'})
        if not self.position or not self.position.strip():
            raise ValidationError({'position': 'Должность не может быть пустой.'})
        if self.hire_date and self.hire_date > datetime.date.today():
            raise ValidationError({'hire_date': 'Дата приёма не может быть в будущем.'})
        if self.salary is not None and self.salary <= 0:
            raise ValidationError({'salary': 'Зарплата должна быть больше 0.'})
        if self.email and '@' not in self.email:
            raise ValidationError({'email': 'Email должен содержать символ @.'})
        qs = Employee.objects.filter(email=self.email)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError({'email': 'Сотрудник с таким email уже существует.'})
```

#### forms.py
```python
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'hire_date', 'salary', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'full_name': 'Полное имя',
            'position': 'Должность',
            'hire_date': 'Дата приёма',
            'salary': 'Зарплата',
            'email': 'Email',
        }
```

#### views.py — меняешь только импорты и названия
```python
from .models import Employee      # вместо Product
from .forms import EmployeeForm   # вместо ProductForm

def product_list(request):
    items = Employee.objects.all().order_by('-created_at')
    return render(request, 'products/index.html', {'object_list': items})

def product_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)   # вместо ProductForm
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.full_clean()
                obj.save()
                messages.success(request, 'Сотрудник добавлен.')
                return redirect('index')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = EmployeeForm()
    return render(request, 'products/form.html', {'form': form})

def product_update(request, pk):
    obj = get_object_or_404(Employee, pk=pk)   # вместо Product
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                updated = form.save(commit=False)
                updated.full_clean()
                updated.save()
                messages.success(request, 'Сотрудник обновлён.')
                return redirect('index')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = EmployeeForm(instance=obj)
    return render(request, 'products/form.html', {'form': form, 'object': obj})

def product_delete(request, pk):
    obj = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Сотрудник удалён.')
        return redirect('index')
    return render(request, 'products/confirm_delete.html', {'object': obj})
```

#### admin.py
```python
from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'position', 'salary', 'email', 'hire_date')
    search_fields = ('full_name', 'email')
    ordering = ('-created_at',)
```

#### index.html — меняешь колонки таблицы
```html
<thead class="table-dark">
    <tr>
        <th>ID</th><th>Имя</th><th>Должность</th><th>Зарплата</th><th>Email</th><th>Дата приёма</th><th>Действия</th>
    </tr>
</thead>
<tbody>
    {% for obj in object_list %}
    <tr>
        <td>{{ obj.id }}</td>
        <td>{{ obj.full_name }}</td>
        <td>{{ obj.position }}</td>
        <td>{{ obj.salary }} руб.</td>
        <td>{{ obj.email }}</td>
        <td>{{ obj.hire_date|date:"d.m.Y" }}</td>
        <td>
            <a href="{% url 'update' obj.id %}" class="btn btn-sm btn-warning">Изменить</a>
            <a href="{% url 'delete' obj.id %}" class="btn btn-sm btn-danger">Удалить</a>
        </td>
    </tr>
    {% empty %}
    <tr><td colspan="7" class="text-center">Нет записей</td></tr>
    {% endfor %}
</tbody>
```

#### migrations — после изменения модели обязательно!
```bash
rm products/migrations/0001_initial.py
python3 manage.py makemigrations
python3 manage.py migrate
```

---

### ★ ВАРИАНТ 2 — Посты в блоге (posts)

#### models.py
```python
from django.db import models
from django.core.exceptions import ValidationError
import datetime

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    published_at = models.DateField(default=datetime.date.today, verbose_name='Дата публикации')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def clean(self):
        if not self.title or not self.title.strip():
            raise ValidationError({'title': 'Заголовок не может быть пустым.'})
        if not self.content or not self.content.strip():
            raise ValidationError({'content': 'Содержание не может быть пустым.'})
        if self.published_at and self.published_at > datetime.date.today():
            raise ValidationError({'published_at': 'Дата публикации не может быть в будущем.'})
        if self.views is not None and self.views < 0:
            raise ValidationError({'views': 'Количество просмотров не может быть отрицательным.'})
```

#### forms.py
```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'published_at', 'views', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'published_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'views': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'published_at': 'Дата публикации',
            'views': 'Просмотры',
            'is_published': 'Опубликован',
        }
```

#### admin.py
```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_at', 'views', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title',)
    ordering = ('-created_at',)
```

#### index.html — колонки для постов
```html
<thead class="table-dark">
    <tr>
        <th>ID</th><th>Заголовок</th><th>Дата</th><th>Просмотры</th><th>Статус</th><th>Действия</th>
    </tr>
</thead>
<tbody>
    {% for obj in object_list %}
    <tr>
        <td>{{ obj.id }}</td>
        <td>{{ obj.title }}</td>
        <td>{{ obj.published_at|date:"d.m.Y" }}</td>
        <td>{{ obj.views }}</td>
        <td>{% if obj.is_published %}✅ Опубликован{% else %}📝 Черновик{% endif %}</td>
        <td>
            <a href="{% url 'update' obj.id %}" class="btn btn-sm btn-warning">Изменить</a>
            <a href="{% url 'delete' obj.id %}" class="btn btn-sm btn-danger">Удалить</a>
        </td>
    </tr>
    {% empty %}
    <tr><td colspan="6" class="text-center">Нет записей</td></tr>
    {% endfor %}
</tbody>
```

---

## 🧠 ТЕОРИЯ — ЧТО ЭТО ТАКОЕ И ЗАЧЕМ

### Модель (models.py)
Это класс Python который описывает таблицу в базе данных. Каждое поле класса = колонка в таблице. Django сам создаёт SQL-таблицу по этому классу.

### Миграции
Это файлы которые Django генерирует на основе модели и применяет к базе данных. Без миграций таблица не создастся.
- `makemigrations` — создать файл миграции
- `migrate` — применить миграцию к БД

### CRUD
Четыре основных операции с данными:
- **C**reate — создание (POST /create/)
- **R**ead — чтение (GET /)
- **U**pdate — редактирование (POST /1/update/)
- **D**elete — удаление (POST /1/delete/)

### Валидация (метод clean)
Проверка данных перед сохранением в БД. Если данные неверные — выбрасывается `ValidationError` и пользователь видит сообщение об ошибке. Валидация находится в методе `clean()` модели.

### Middleware (middleware.py)
Код который выполняется при каждом запросе и ответе. Наш middleware считает количество запросов и пишет статистику в консоль и файл `metrics.log`. Работает автоматически, не надо ничего делать.

### .env файл
Файл с секретными настройками которые не хранятся в коде:
- `DEBUG` — режим отладки (True/False)
- `SECRET_KEY` — секретный ключ Django
- `DB_NAME` — имя базы данных

### Статические файлы (static)
CSS, JS, картинки. При `DEBUG=True` Django сам их отдаёт. При `DEBUG=False` нужен WhiteNoise — он уже подключён в проекте.

### WhiteNoise
Библиотека которая отдаёт статические файлы (CSS Bootstrap) даже при `DEBUG=False`. Уже настроена в проекте.

### Интеграционный тест (tests.py)
Тест который проверяет что сервер отвечает. Наш тест делает GET запрос на `/ping/` и проверяет что ответ 200. Запускается командой `python3 manage.py test`.

### HTTP статусы
- **200** — OK, всё хорошо
- **302** — редирект (переход на другую страницу после сохранения)
- **400** — неверные данные
- **404** — запись не найдена
- **500** — ошибка сервера

### get_object_or_404
Функция Django — ищет запись по id, если не найдена — автоматически возвращает страницу 404. Используется во views.py.

### {% csrf_token %}
Защита от атак в формах. Обязательно должен быть в каждой HTML форме с `method="post"`. Уже есть в шаблонах.

---

## ✅ ЧЕКЛИСТ ПЕРЕД СДАЧЕЙ

- [ ] Сайт открывается: http://127.0.0.1:8000/
- [ ] Можно добавить запись
- [ ] Можно редактировать запись
- [ ] Можно удалить запись (с подтверждением)
- [ ] Валидация работает (попробовать сохранить пустое поле или неверные данные — должна быть ошибка)
- [ ] 404 при несуществующем ID: http://127.0.0.1:8000/9999/update/
- [ ] Админка работает: http://127.0.0.1:8000/admin/
- [ ] Тесты проходят: `python3 manage.py test`
- [ ] Метрики видны в терминале при запросах
- [ ] /ping/ возвращает OK: http://127.0.0.1:8000/ping/

### валидация
Смотри, валидация вся находится в методе `clean()` в `models.py`. Это просто набор условий `if` — каждое условие проверяет одно правило.

**Структура всегда одинаковая:**
```python
def clean(self):
    if УСЛОВИЕ:
        raise ValidationError({'ИМЯ_ПОЛЯ': 'Текст ошибки'})
```

**Готовые шаблоны под любые задания:** валидация

```python
# Поле не может быть пустым
if not self.full_name or not self.full_name.strip():
    raise ValidationError({'full_name': 'Поле не может быть пустым.'})

# Число должно быть больше 0
if self.salary is not None and self.salary <= 0:
    raise ValidationError({'salary': 'Должно быть больше 0.'})

# Число не может быть отрицательным
if self.views is not None and self.views < 0:
    raise ValidationError({'views': 'Не может быть отрицательным.'})

# Дата не может быть в будущем (hire_date — дата приёма)
if self.hire_date and self.hire_date > datetime.date.today():
    raise ValidationError({'hire_date': 'Дата не может быть в будущем.'})

# Дата должна быть в будущем (event_date — дата мероприятия)
if self.event_date and self.event_date <= timezone.now():
    raise ValidationError({'event_date': 'Дата должна быть в будущем.'})

# Email должен содержать @
if self.email and '@' not in self.email:
    raise ValidationError({'email': 'Введите корректный email.'})

# Поле должно быть уникальным
qs = MyModel.objects.filter(email=self.email)
if self.pk:
    qs = qs.exclude(pk=self.pk)
if qs.exists():
    raise ValidationError({'email': 'Такой email уже существует.'})
```

Просто смотришь на задание, читаешь правила валидации и берёшь нужный шаблон!

## что где менять
Смотри, всё просто. Везде где в коде написано `Product` или `product` — меняешь на название своей модели.

**Пример: тебе попался вариант "Сотрудники"**

| Что было (товары) | Что ставишь (сотрудники) |
|---|---|
| `class Product` | `class Employee` |
| `ProductForm` | `EmployeeForm` |
| `from .models import Product` | `from .models import Employee` |
| `Product.objects.all()` | `Employee.objects.all()` |
| `get_object_or_404(Product` | `get_object_or_404(Employee` |
| `verbose_name = 'Товар'` | `verbose_name = 'Сотрудник'` |
| `@admin.register(Product)` | `@admin.register(Employee)` |

**Поля** — меняешь в `models.py` под свою таблицу:
```python
# Было:
name = models.CharField(max_length=150)
price = models.DecimalField(max_digits=10, decimal_places=2)
sku = models.CharField(max_length=50, unique=True)

# Стало (сотрудники):
full_name = models.CharField(max_length=200)
salary = models.DecimalField(max_digits=10, decimal_places=2)
email = models.EmailField(unique=True)
```

**В `forms.py`** меняешь только список `fields` — пишешь туда названия своих полей:
```python
fields = ['full_name', 'position', 'hire_date', 'salary', 'email']
```

**В `index.html`** меняешь только названия колонок и `obj.поле`:
```python
# Было:
{{ obj.name }} {{ obj.price }}

# Стало:
{{ obj.full_name }} {{ obj.salary }}
```

Вот и всё! Названия полей везде должны совпадать с тем что написано в `models.py`.

Да, всё верно! Папка `products` остаётся как есть, и в `urls.py` ничего не трогаешь. 

Меняешь только **внутри файлов**:
- `models.py` — класс и поля
- `forms.py` — импорт и fields
- `views.py` — импорт и название класса
- `admin.py` — импорт и register
- `index.html` — названия колонок и `obj.поле`

Всё остальное не трогаешь!

#### фронт

Смотри, открой файл `index.html` — там две части:

**Часть 1 — шапка таблицы (`<thead>`)** — это названия колонок которые видит пользователь:
```html
<th>ID</th>
<th>Название</th>   ← просто текст, пиши что хочешь
<th>Категория</th>
<th>Цена</th>
<th>Артикул</th>
<th>Дата</th>
<th>Действия</th>   ← эту не трогай
```

**Часть 2 — строки таблицы (`<tbody>`)** — это реальные данные из БД:
```html
<td>{{ obj.id }}</td>           ← id не трогай
<td>{{ obj.name }}</td>         ← тут меняешь на своё поле
<td>{{ obj.category }}</td>     ← тут меняешь на своё поле
<td>{{ obj.price }}</td>        ← тут меняешь на своё поле
<td>{{ obj.sku }}</td>          ← тут меняешь на своё поле
```


**Правило простое:** что написано в `models.py` — то же самое пишешь после `obj.`

Например для сотрудников:
```python
# в models.py написано:
full_name = ...
salary = ...
email = ...

# значит в index.html пишешь:
<td>{{ obj.full_name }}</td>
<td>{{ obj.salary }}</td>
<td>{{ obj.email }}</td>
```

И количество `<th>` в шапке должно совпадать с количеством `<td>` в строке! Плюс всегда +1 для кнопок "Действия".

## миграции
Да, это правильно! Это происходит потому что старые миграции от товаров конфликтуют с новой моделью.

**Поэтому на экзамене после того как поменяла модель — сразу делай:**

```bash
rm products/migrations/0001_initial.py
python3 manage.py makemigrations
python3 manage.py migrate
```

##

1. `git clone` + `cd django_exam`
2. Меняешь `models.py`, `forms.py`, `views.py`, `admin.py`, `index.html`
3. Удаляешь старую миграцию: `rm products/migrations/0001_initial.py`
4. `bash setup.sh`


### 404

Окей! Нужно сделать два шага:

**Шаг 1** — создать файл `404.html`. В папке `products/templates/` создай файл `404.html` и вставь туда:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Страница не найдена</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-5 text-center">
    <h1 class="display-1">404</h1>
    <p class="lead">Запрашиваемая страница не найдена.</p>
    <a href="/" class="btn btn-primary">На главную</a>
</div>
</body>
</html>
```

**Шаг 2** — в `products_project/settings.py` поменять:
```python
DEBUG = True
```
на:
```python
DEBUG = False
```

И после этого залить на GitHub:
```bash
git add .
git commit -m "add 404 page"
git push
```

На экзамене после клона — не забудь что `DEBUG=False` значит обязательно нужно сначала собрать статику:
```bash
python3 manage.py collectstatic --noinput
```

Иначе админка будет без стилей!

### .env

Объясняю каждую строчку:

```
DEBUG=True
```
Режим отладки. `True` = включён (для разработки, показывает подробные ошибки). `False` = выключен (для продакшена, нужна страница 404 и collectstatic).

```
SECRET_KEY=your-secret-key-exam123456789abcdef
```
Секретный ключ Django — нужен для безопасности (шифрование паролей, сессий). Может быть любой длинной строкой. На экзамене не важно какой он.

```
DB_NAME=db.sqlite3
```
Имя файла базы данных. SQLite хранит всю БД в одном файле `db.sqlite3`. На экзамене не трогаешь.

```
DB_ENGINE=django.db.backends.sqlite3
```
Тип базы данных. SQLite — самая простая, не требует установки отдельного сервера. На экзамене не трогаешь.

---

**Короче говоря** — на экзамене в `.env` трогаешь только одну строчку:

- Если нужна страница 404 со стилями → меняешь `DEBUG=True` на `DEBUG=False`
- Во всех остальных случаях → вообще не открываешь этот файл!


#### если меня попросят показать 404 страницу
Да! Но после того как поменяешь на `False` — обязательно ещё одна команда, иначе админка будет без стилей (без CSS):

```bash
python3 manage.py collectstatic --noinput
```

И потом перезапусти сервер:
```bash
python3 manage.py runserver
```

Потом просто зайди на http://127.0.0.1:8000/9999/update/ — покажется твоя страница 404!