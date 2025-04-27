# Учебный проект "Сервер картинок"

## Описание

Это учебный сервер для управления и предоставления
доступных изображений через веб-интерфейс. 
Код написан для демонстрации серверной логики 
и обеспечения простого RESTful API для взаимодействия с
изображениями.
Для хранения изображений используется PostgreSQL.

## Функциональные возможности

- Загрузка изображений на сервер.
- Показ списка доступных изображений.
- Удаление изображений с сервера.
- Взаимодействие через удобный API.

## Как запустить

1. Убедитесь, что у вас установлен Python 3.12 или выше.
2. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/project-name.git
   cd project-name
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите сервер:
   ```bash
   python app.py
   ```

Возможен запуск через docker командой docker compose up --build

## API Эндпоинты

- `GET /images/` — Возвращает список всех доступных изображений.
- `POST /upload/` — Загружает новое изображение. 
- `DELETE /api/delete/{image_id}/` — Удаляет изображение по его идентификатору.

## Резервное копирование базы данных

Резервное копирование базы данных выполняется командой `bash backup.sh`.

## Структура проекта

```plaintext
project/
├── /app                # Python-бэкенд
|    ├── app.py             # Основной модуль Python/точка входа
|    ├──Image_Hosting       # HTTP Request Handler
|    |    _HTTP_Handler.py  
|    ├── settings.py        # Настройки приложения  
|    ├── Router.py          # Класс для управления маршрутами
|    ├── DB_Manager.py      # Класс для управления базой данных
|    ├── adv_http_request   #Расширение Base HTTP Request Handler
|    |    _HTTP_handler.py  
|    ├── Dockerfile         # Dockerfile для Python-бэкенда
|    ├── requirements.txt   # Список зависимостей
|    └── init_tables.sqi    # SQL скрипт для инициализации базы данных
├── /backups            # Резервные копии БД
├── /images             # Загруженные изображения
├── /logs               # Логи
├── /static             # Статические файлы
├── backup.sh           # скрипт для создания резервных копий
├── compose.yaml        # Конфигурация Docker Compose
├── nginx.conf          # Конфигурация Nginx
├── .env                # Переменные окружения
└── README.md           # Описание проекта (этот файл)
 
```

## Требования

- Python 3.12 или выше
- loguru~=0.7.3
- psycopg[binary, pool]
- Flask 
(указано в `requirements.txt`)

## Лицензия

none

## Автор 
Alexander Telenkov 
ru3aah@gmail.com

Проект создан в учебных целях.
