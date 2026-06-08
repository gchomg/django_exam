pip3 install django python-dotenv whitenoise --break-system-packages
python3 manage.py migrate
python3 manage.py shell -c "
from django.contrib.auth import get_user_model
U = get_user_model()
if not U.objects.filter(username='admin').exists():
    U.objects.create_superuser('admin', 'a@a.com', 'admin')
    print('Админ создан: admin / admin')
"
python3 manage.py runserver
