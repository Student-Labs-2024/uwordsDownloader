# UWORDS DOWNLOADER API
API-микросервис для загрузки контента с зарубежных сервисов

![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)
![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)
![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)
![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)
![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)
![](https://cultofthepartyparrot.com/parrots/hd/congaparrot.gif)

## Stack
Python 3.11, FastAPI, gunicorn, Docker

## Packages
yt-dlp, aiohhtp, aiofiles

## Запуск проекта
Чтобы сделать миграцию к БД, нужно прописать в контейнере docker следующую команду

Запуск проекта на локальной машине
```shell
docker-compose -f "docker-compose.dev.yml" up --build
```

Настройка локального окружения pre-commit:
```shell
pre-commit install
pre-commit run --all-files
pre-commit install --hook-type commit-msg
```

Перед коммитом проверять код линтером Black
```shell
python -m black ./src --check
```

В случае замечаний линтера выполнить команду
```shell
python -m black ./src
```

Пример .env можно увидеть в следующих файлах:
- env.dev.example

## Authors
Daniil Kolevatykh - CTO, python software developer

Azamat Aubakirov - python software developer

Dmitry Prasolov - python software developer