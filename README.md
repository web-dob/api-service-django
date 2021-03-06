### WEB Сервис

**Стек технологий:**

    1. Python 3.10
    2. Django 4.0
    3. PostgreeSQL
    4. Pandas
    4. Docker


**Установка проекта на сервере**
    - Копируем репозиторий
    - Устанавливаем docker
    - Устанавливаем docker-compose

    - Находясьв дирректории, где лежит docker-compose.yml выполнить команду:
          - sudo docker-compose build
          - Проект достаточно долго собирается, из-за того, что pandas собирается из исходников.

    - После того, как проект соберется, необходимо запустить контейнеры:
          - sudo docker-compose up -d

    - Далее необходимо выполнить миграции
          - sudo docker-compose exec web python manage.py flush --no-input
          - sudo docker-compose exec web python manage.py migrate

    - Coздадим суперпользователя для проекта
          - sudo docker-compose exec web python manage.py createsuperuser
          - далее в предлагаемых полях введите необходимые данные, например
                - Логин: admin (Enter)
                - E-mail: можно оставить пустым (Enter)
                - Пароль: ***  (Enter)
                - Пароль еще раз: ***  (Enter)
    
    - Теперь можем при необходимости перейти на страницу проекта:
          - 127.0.0.1:8050
    
    - Зайти в админку проекта, используя введенные ранее данные администратора:
          - 127.0.0.1:8050/admin

    - Или сразу же воспользоваться API


**Авторизация**

    - Для отправки запросов можно воспользоваться сторонним приложением, например POSTMAN
          - http://127.0.0.1:8050/auth/token/login
          - В body form-data вводим данные администратора, которые ввели выше или пользователя, 
          которого создали через админку приложения:
              - username
              - password
          - В ответе должны получить токен авторизации, например:
          {
              "auth_token": "375c3c5b5858b94ad02d54c3b10346f0eabcf912"
          }


**Выполнение запросов**

    - Для выполнения запроса потребуется полученный ранне токен авторизации
          - В HEADERS необходимо добавить параметр:
                - Authorization
          - В качестве значения выбрать полученный ранее токен с префиксом Token, например:
                - Token 375c3c5b5858b94ad02d54c3b10346f0eabcf912
                
    - API пополнения данных: POST /calculate
    
        {
            "user_id": int,
            "data": {
                "x_data_type": str,
                "y_data_type": str,
                "x": [
                    {
                        "date": YYYY-MM-DD,
                        "value": float,
                    },
                    ...
                ],
                "y": [
                    {
                        "date": YYYY-MM-DD,
                        "value": float,
                    },
                    ...
                ]
            }
        }

    - API получения результата: GET /correlation?x_data_type=str&y_data_type=str&user_id=int

**PS**

    - Значение "value", указанное 0 по умолчанию.
