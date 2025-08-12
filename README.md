## Как пользоваться ботом:
### 1. Клонируй репозиторий 

- git clone git@github.com:Molloko/telegram-translit-bot.git


### 2.Установите токен 

- Откройте Dockerfile и замените строку: dockerfile ENV TOKEN='Your token from GodFather'на ENV TOKEN='ВАШ_ТОКЕН_БОТА'
- Ваш токен можно получить в боте GodFather

### 3. Соберите Docker-образ
- docker build -t translit-bot .

### 5. Запустите контейнер
- docker run -d --name translit-bot \
  -v $(pwd)/logs:/logs \
  translit-bot


  ### 6. Проверьте логи 
  - docker logs -f translit-bot




