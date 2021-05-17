.. role:: shell(code)
   :language: shell

Backend API (CRUD).
==========

Быстрый вариант разворачивания в Docker
-----------------------------------------
С помощью docker-compose:

:shell: docker-compose -f docker-compose-dev.yaml up --build

С помощью make:

:shell: make compose-dev

Это запутсит три контейнера:
- postgres
- application
- alembic (завершит работу после применения миграции)

Чтобы запустить без применения миграции:
-----------------------------------------

С помощью docker-compose:

:shell: docker-compose up --build -d

С помощью make:

:shell: make compose


Это запутсит два контейнера:
- postgres
- application

Чтобы применить миграции нужно выполнить:
---------------

В контейнере:

:shell: docker-compose run app alembic upgrade head

По адресу:

:shell: python3.8 project/db --pg-url postgresql://admin:admin@0.0.0.0:5442/simalend upgrade head

Как очистить базу данных полученную с контейнера?
-----------------------------------------

С помощью make:

:shell: make cleandb

После запуска
==========

Будет открыт доступ по хосту:
---------------
* http://127.0.0.1:3000/

Swagger документация
---------------
* http://127.0.0.1:3000/api/doc


Разработка
==========

Быстрые команды
---------------
.. code-block:: shell
      `make` Отобразить список доступных команд
      `make devenv` Создать и настроить виртуальное окружение для разработки
      `make postgres` Поднять Docker-контейнер с PostgreSQL
      `make clean` Удалить файлы, созданные модулем `distutils`_
      `make sdist` Создать `source distribution`_
      `make docker` Собрать Docker-образ
      `make upload` Загрузить Docker-образ на hub.docker.com
      `make compose` Собрать и запустить проект в Docker
      `make cleanedb` очистить базу данных контейнера


.. _distutils: https://docs.python.org/3/library/distutils.html
.. _source distribution: https://packaging.python.org/glossary/

Как подготовить окружение для разработки?
-----------------------------------------
.. code-block:: shell

    make devenv
    make postgres
    source env/bin/activate
    alembic upgrade head
    python app_run.py

После выполненных команд приложение будет 
доступно по локальному адресу 0.0.0.0:3000


Если хотите снова запустить базу данных в контейнере
и применить миграции

.. code-block:: shell

    make postgres
    alembic upgrade head

Аргументы для запуска приложения
==========

Конфигурирование приложения
-----------------------------------------
* -H --host - На каком адресе приложение будет работать
* -P --port - На каком порту приложение будет работать
* -D --debug - Включает режим дебага. Вывод в консоль и .log файл.

Конфигурирование подключения к базе данных
-----------------------------------------
* --pg-url - Укажите прямой путь подключения к базе данных

Таким образом можно сконфигурировать приложение:
-----------------------------------------
.. code-block:: shell

    python3.8 app_run.py -H 127.0.0.12 -P 2414 -D \
    --pg-url postgresql://admin:admin@0.0.0.0:5442/simalend

Применение миграции через обертку:
-----------------------------------------
.. code-block:: shell

    python3.8 project/db --pg-url postgresql://admin:admin@0.0.0.0:5442/simalend upgrade head

Эту команду не следует запускать по root. Возможна ошибка.

Все эти команды дадут возможность сконфигурировать приложение нужным образом.
