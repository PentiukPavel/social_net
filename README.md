# Social Net
## Описание
Web приложение для взаимодействия с участниками.

## Для разработчиков:
### Пример файла с переменными среды:
".env.example"

### Линтер:
`black`

### Pre-commit:
Настроен pre-commit для проверки оформления кода.
Для проверки кода перед выполнением операции commit, выполнить команду:

```
pre-commit run --all-files
```

## Как запустить проект:

Клонировать проект
```
git clone git@github.com:PentiukPavel/social_net.git
```

Переименовать файл .env.example и изменить содержимое на актуальные данные.
```
mv .env.example .env
```

### 1) Запуск проекта на локальной машине:

Создать виртуальное окружение:
```
py -3 -m venv venv
```

Активировать виртуальное окружение:
```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

При необходимости установить дополнительные зависимости для разработчиков из файла requirements_dev.txt:
```
pip install -r requirements_dev.txt
```

Запустить проект:
```
uvicorn main:app --reload
```

## Системные требования
### Python==3.12

## Стек
### FastAPI
### FastAPI Users
### geopy
### SQLAlchemy
### PosrgreSQL
