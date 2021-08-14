# arentex-backend

### Локальный запуск 

1. Запульнуть контейнеры
```
$ docker-compose up -d --build
```

2. Заполнить базу
```
$ docker-compose exec web python scripts/fill_db.py
```

3. Документация тут http://127.0.0.1:8000/docs
