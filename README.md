DevOpsTest

### Для запуска контейнера выполнить команду:

```bash

docker build -t timurhisamov/devmts:latest .
docker run -d -v ~/{относительный путь до склонированного репо}/app/:/usr/src/app timurhisamov/devmts

```

#### Сервер принимает POST запросы на 127.0.0.1:5000/post. В ответ прилетает ОК.

Доступ по ssh реализован:

```bash

ssh root@localhost -p 2222 -i ../devkey

```

 Мое мнение заключается в том, что использовать ssh в контейнере не целесообразно. Докер по дефолту следит только за одним процессом. Доступ в контейнер можно осуществить зайдя по ssh на сервер, а от туда через 

```bash

docker exec -it {{container_id}} /bin/bash

```
