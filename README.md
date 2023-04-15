# Проект «YaMDb»

## Описание:
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Технологии:
- Python
- Django
- DRF
- JWT

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Galichskyeyu/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать виртуальное окружение:

```
# Команда для Windows:
python -m venv venv
```

```
# Команда для Linux и macOS:
python3 -m venv venv
```

Активировать виртуальное окружение:

```
# Команда для Windows:
source venv/Scripts/activate
```

```
# Команда для Linux и macOS:
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

```
python -m pip install --upgrade pip
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Примеры работы с API:

### Получение списка всех категорий.
Получить список всех категорий. Права доступа: Доступно без токена.

METHOD/URL:
```
GET http://127.0.0.1:8000/api/v1/categories/
```
Пример ответа:
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```
### Добавление новой категории.
Создать категорию. Права доступа: Администратор. Поле slug каждой категории должно быть уникальным.

METHOD/URL:
```
POST http://127.0.0.1:8000/api/v1/categories/
```
Пример запроса:
```
{
  "name": "string",
  "slug": "string"
}
```
Пример ответа:
```
{
    "name": "string",
    "slug": "string"
}
```
Примеры других запросов к API и документацию можно посмотреть [здесь](http://127.0.0.1:8000/redoc/ "здесь") (проект должен быть запущен).

## Авторы: 
### [Эмин Галичский](https://github.com/Galichskyeyu "Эмин Галичский")

### [Данила Мандрейкин](https://github.com/Danila-19 "Данила Мандрейкин")

### [Кристина Шунькина](https://github.com/krispushka "Кристина Шунькина")
