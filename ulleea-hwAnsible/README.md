# Домашнее задание №3. Ansible

* **Мягкий deadline:** 27.11, 23:59.
* **Жёсткий deadline:** 04.12, 23:59.

## Задание

### Базовый поток

Необходимо с помощью Ansible реализовать следующую автоматизацию на одном из дистрибутивов Linux (*укажите название и версию выбранного дистро в `README.md`*):
1. Установить `nginx`
2. Изменить конфигурацию nginx таким образом, чтобы по запросу `GET /service_data` отдавалось содержимое файла `/opt/service_state`
3. Поместить файл `/opt/service_state` состоящий из 2 строк:
    ```
    Seems work
    Service uptime is 0 minutes
    ```
4. Обеспечить запуск `nginx`
5. Добавить в cron выполнение раз в минуту команды:
   ```
   sed -i "s/is .*$/is $(($(ps -o etimes= -p $(cat /var/run/nginx.pid)) / 60)) minutes/" /opt/service_state
   ```

   **Замечание:** для автоматизации работы с cron можно пользоваться `python-crontab`.

6. Выполнить проверку того, что значение `uptime` в файле `/opt/service_state` начало изменяться.

**Внимание** - конфигурация ansible должна быть идемпотентной, т.е. соответствовать следующим требованиям:

- Повторный запуск ansible с той же конфигурацией **не должен сбрасывать** значение `uptime` в файле `/opt/service_state` и **не должен рестартовать** nginx.
- После изменения первой строки файла `service_state` (например, на "Seems work ok") должно происходить обновление файла `/opt/service_state` и рестарт сервиса `nginx`.

### Продвинутый поток

То же, что и базовый, но дополнительно:
1. Ваша конфигурация для Ansible должна быть выполнена в виде роли (role), а не обычного playbook
2. Ваша конфигурация должна работать на нескольких операционных системах:
   - Ubuntu 22.04
   - Centos 7
   - Arch Linux

## Формат проверки

Запускается чистая виртуалка на Vagrant и на ней запускается ваша конфигурация ansible.

**Для базового потока** - не забудьте указать название и версию выбранного дистро в `README.md`.

Проверки:
1. `GET /service_data` с помощью curl на порт 80 должен отдать:
    ```
    Seems work
    Service uptime is 0 minutes
    ```
2. Делается пауза X минут. Затем снова `GET /service_data` с помощью curl на порт 80:
    ```
   Seems work
   Service uptime is Х minutes
   ```
3. Повторный запуск ansible. `GET /service_data` с помощью curl на порт 80 возвращает:
    ```
   Seems work
   Service uptime is Х minutes
   ```
4. Изменяем первую строку в файле `service_state` и еще раз запускаем ansible. 
`GET /service_data` с помощью curl на порт 80 возвращает:
    ```
    [Измененная первая строка]
    Service uptime is 0 minutes
    ```
5. Делается пауза X минут. Затем снова `GET /service_data` с помощью curl на порт 80:
    ```
   [Измененная первая строка]
    Service uptime is Х minutes
   ```

**Невыполнение каждого из пунктов - штраф 20% от оценки за ДЗ.**

Дополнительно, штрафы для продвинутого потока ():
- сделан playbook вместо role - **штраф 50%**
- конфигурация не работает на указанной в задании ОС - **штраф 30%** за ОС 

## Формат сдачи

Сдача происходит точно также, как и в предыдущем ДЗ. Вы заливаете код в ветку `hwansibletask1` (не мастер!) репозитория `***-hwansible` в `gitlab.atp-fivt.org` и делаете Merge Request.
Assignee должен быть пустым (Unassigned)!
