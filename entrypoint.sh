#!/bin/bash

# Apply database migrations

./wait-for-it.sh db:5432 -- echo "Creating config file"

if [ ! -f manage.py ]; then
  cd libra
fi

if [ ! -f libra/config.py ]; then
    cp libra/config.py.example libra/config.py
fi

echo "Apply database migrations"
python manage.py makemigrations && python manage.py migrate

# echo "Create users"
# python manage.py shell -c "from django.contrib.auth.models import User; \
#   User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"

#Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8004
