.. role:: shell(code)
   :language: shell

Backend API (CRUD).

Более быстрый вариант разворачивания в Docker:
==========

.. code-block:: shell

    make compose

Будут совершены команды:

.. code-block:: shell

    	docker-compose build
	docker-compose run app alembic upgrade head
	docker-compose run app alembic upgrade head
	docker-compose up

Будет открыт доступ по хосту:

* http://127.0.0.1:3000/

Разработка
==========

Быстрые команды
---------------
* :shell:`make` Отобразить список доступных команд
* :shell:`make devenv` Создать и настроить виртуальное окружение для разработки
* :shell:`make postgres` Поднять Docker-контейнер с PostgreSQL
* :shell:`make clean` Удалить файлы, созданные модулем `distutils`_
* :shell:`make sdist` Создать `source distribution`_
* :shell:`make docker` Собрать Docker-образ
* :shell:`make upload` Загрузить Docker-образ на hub.docker.com
* :shell:`make compose` Собрать и запустить проект в Docker
* :shell:`make cleanedb` очистить базу данных контейнера


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


Как очистить базу данных полученную с контейнера?
-----------------------------------------
.. code-block:: shell

    make cleandb

Если хотите снова запустить базу данных в контейнере
и применить миграции

.. code-block:: shell

    make postgres
    alembic upgrade head