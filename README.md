# CFTaskManager

CFTaskManager — проект для автоматизации работы с задачами Codeforces. Он облегчает процесс выбора и отслеживания задач с помощью тематических подборок и предоставляет простой интерфейс в виде Telegram-бота.

## О проекте

CFTaskManager парсит задачи с сайта Codeforces, сохраняет их в базе данных, разделяет по контестам и позволяет пользователям Telegram-бота выбирать задачи по сложности и теме.

## Требования

- Python 3.11
- PostgreSQL

## Сборка и настройка проекта

1. **Клонирование репозитория**:

    ```sh
    git clone https://github.com/OrdinSI/CFTaskManager.git
    cd CFTaskManager
    ```

2. **Создание директории для хранения данных базы данных**:

    ```sh
    mkdir -p /mnt/postgres/postgres-data
    ```

3. **Создание файла .env на основе .env.example**:

    Скопируйте файл `.env.example` в `.env` и отредактируйте его в соответствии с вашими настройками:

    ```sh
    cp .env.example .env
    ```

4. **Сборка и запуск Docker контейнеров**:

    ```sh
    docker-compose up -d --build
    ```

5. **Инициализация базы данных**:

    Выполните следующие команды:

    ```sh
    docker exec -it app sh -c "PYTHONPATH=/app aerich init -t src.settings.TORTOISE_ORM --location src/db/migrations"
    docker exec -it app sh -c "PYTHONPATH=/app aerich init-db"
    ```

6. **Заполнение базы данных первичными данными**:

    Выполните команду:

    ```sh
    docker exec -it app sh -c "PYTHONPATH=/app python /app/src/db/utils/init_subjects.py"
    ```
   
## Дополнительная информация

Более подробно о проекте и его архитектуре можно узнать в [документации](./docs/README.md).