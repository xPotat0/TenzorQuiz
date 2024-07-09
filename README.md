Сборка проекта
Подготовление
УСТАНОВКА POSTGRESQL
1. Скачать PostgreSQL.
2. Установить постгрес. Не забудьте пароль, который вводите.
3. Перейти в "Настройка системных переменных среды". Для этого используйте поиск.
4. Нажмите "Изменение переменных среды".
5. Добавьте переменную. Укажите ей папку, в которой хранится файл psql.exe. Обычно место хранения "ваше_место_установки/PostgreSQL/bin". Назовите переменную и запомните её. (Я назвал postgres).
6. Добавим созданую в прошлом шаге переменную в путь. Для этого отредактируем переменную "Path". Добавим новую запись "%название_вашей_переменной%".(У меня это было "%postgres%").
![image](https://github.com/xPotat0/TenzorQuiz/assets/106258306/bf69d68a-a9db-4873-9b98-5e2dc7516d80)
7. Сохраните изменения. Проверить успешность установки PostgreSQL можно перейдя в коносль(пересоздайте коносль, если открыли до того, как установили переменные среды) и воспользовавшись командой psql. Если команда была распознана, то вы поймете это.
СОЗДАНИЕ БАЗЫ ДАННЫХ
1. Скачайте данный репозиторий. В нём есть папка "data". В ней мы будем хранить базу данных. Если хотите использовать другую папку на вашем компьютере, то не забудье изменить переменные в папке ".env".
2. Откройте консоль. Введите команду "psql -U postgres;". После вам будет нужно ввести пароль, который вы вводили при установке PostgreSQL. Эта команда переведёт вас в режим суперюзера. Здесь мы будем создавать базу данных.
3. Введите команду "CREATE TABLESPACE имя_пространства_таблиц OWNER CURRENT_USER LOCATION '.../TenzorQuiz/data';
4. Введите команду ""
