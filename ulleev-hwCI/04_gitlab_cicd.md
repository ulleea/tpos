# Домашнее задание №4. GitLab CI/CD

* **Мягкий deadline:** 04.12, 23:59
* **Жёсткий deadline:** 11.12, 23:59

## Задание

Необходимо создать пайплайн для работы с реальным проектом, содержащий в себе компиляцию (при необходимости), 
тестирование, сборку пакетов (*.deb, *.rpm или wheel) для двух ОС (Ubuntu и CentOS), и продемонстрировать ее работоспособность.

Все задание состоит из нескольких пунктов:

### 1. "Проект"

**Проект** - какой-либо код, для которого вы будете создавать пайплайн. В качестве проекта можно взять любой код, например, часть вашего диплома или лабы по другим предметам, если он удовлетворяет следующим условиям:
1. Проект имеет разумную длину и сложность (не 10-20 строчек, если есть сомнения - пишите в TG @nchestnov)
2. У проекта имеются внешние зависимости (импорт сторонних библиотек / фреймворков)
3. В проекте реализованы хотя бы минимальные тесты.
4. Проект имеет документацию по работе с ним - что делает, как запустить и проверить работоспособность

> **Что делать, если у вас нет своего подходящего проекта?**
> 
> Можете взять в качестве проекта одну из популярных библиотек с открытым исхоным кодом и тестами, например, `pandas`.

### 2. Пайплайн тестирования и сборки

Пайплайн необходимо реализовать с помощью GitLab CI/CD в вашем репозитории `***-hwansible` на https://gitlab.atp-fivt.org/.

Пайплайн состоит из следующих этапов:
1. **компиляция кода** - опционально, если код компилируемый
2. **тестирование** - запуск юнит-тестов, которые написаны для проекта
3. **сборка пакетов** - получение пакетов для Ubuntu и CentOS и их сохранение в виде артефактов

Все этапы пайплайна должны выполняться в контейнерах Docker с заранее подготовленными образами - образ ОС + зависимости проекта.
Чтобы образы можно было использовать при сборке, их нужно загрузить в registry - либо [DockerHub](https://hub.docker.com/), либо Container Registry вашего репозитория в Гитлабе.

В репозитории необходимо создать три ветки (ветку hwansibletask1 игнорируйте):
- **dev** - основная ветка для разработки
- **staging**
- **main**

Пайплайн должен автоматически вызываться на следующие действия:
- **Push в dev** - запускается частичный пайплайн (пп. 1-2, компиляция и тесты)
- **Merge Request из dev в staging** - запускается полный пайплайн (1-3)
- **Merge Request из staging в main** - запускается полный пайплайн (1-3)

> **Примечание**
> 
> Для запуска ваших job используйте тег tpos, на него настроен специально отведенный раннер.

### 3. "Развертывание" в проде

Поскольку выделенных продовых машин у нас нет, то придется их эмулировать. Для этого вам необходимо воспользоваться связкой Vagrant и Ansible:
- написать Ansible Playbook (или роль, если хотите), который будет устанавливать зависимости, 
а также [скачивать ваш пакет из артефактов](https://docs.gitlab.com/ee/api/job_artifacts.html#download-a-single-artifact-file-from-specific-tag-or-branch) из ветки `main` и устанавливать его
- написать Vagrant, который будет поднимать 2 машины с ОС Ubuntu и CentOS и применять к ним ваш Ansible Playbook в качестве provisioning

В результате должны создаваться две виртуальные машины с установленным пакетом вашего приложения.

## Формат сдачи

Для сдачи задания нужно:
1. Собрать докер-образы с Ubuntu и CentOS и необходимыми зависимостями и поместить их в registry
2. Загрузить код вашего проекта и все файлы задания (.gitlab-ci.yml пайплайна, Dockerfile образов, Vagrantfile виртуалок, playbook.yml) в репозиторий
3. Выполнить несколько коммитов в ветку dev:
   - с некорректными тестами - пайплайн падает
   - с корректными тестами - пайплайн выполняется корректно
4. Выполнить MR и merge из ветки dev в staging - пайплайн должен выполниться, собрать пакеты и сохранить их в артефактах
5. Сделать MR из staging в main - пайплайн также, должен корректно выполниться

## Критерии оценивания

| Описание                                            | Баллы | 
|-----------------------------------------------------|-------|
| **Проект.** Качество, внешние зависимости           | 1     |
| **Проект.** Тесты проекта                           | 1     |
| **Docker.** Образы                                  | 2     |
| **GitLab CI/CD.** Компиляция, запуск тестов, сборка | 2     |
| **GitLab CI/CD.** Сохранение артефактов             | 2     |
| **Vagrant.** "Продовые" виртуалки                   | 2     |
| **ИТОГО**                                           | 10    |
