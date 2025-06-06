# Финальный проект в курсе информационного поиска

В этом проекте вам предстоит:
- Побить бейзлайн (и ваших коллег) в контесте на платформе Kaggle
- Предоставить код, который подтверждает выбитые скоры

Ссылка на контест на Kaggle: https://www.kaggle.com/competitions/final-project-vk-ir-spring-2025

По этой ссылке доступны данные контеста, а также подробно описаны:
- формат датасета
- какие модели можно использовать
- приемочная метрика
- как засабмитить предсказания модели
и т.п.

В этой же доке мы сфокусируемся на том, как подтвердить выбитые скоры.

Ожидается, что, после того как завершится контест, вы:
- приджойнитесь к заданию "HW5 Final Project" в классруме. Для этого надо будет зайти туда по инвайт-ссылке, которую вам пришлют в чате курса, найти себя в списке студентов и подключить свой аккаунт на гитхабе.
- после этого автоматически создастся ваш личный приватный форк репы курса, в который вы будете коммитить код вашего решения. Этот форк будет "жить" в гитхаб-аккаунте организации https://github.com/vk-ir-course-org/ которую мы создали специально для проведения этого курса. Ваш форк будет доступен только вам и преподавателям/менторам курса.
- создадите в своем форке новую ветку для своего решения, можете назвать ее например _hw5-final-project_ (но подойдет и любое другое название на ваш вкус)
- оформите свое решение в виде скрипта _solution.py_ в этой ветке
- запушите ветку на github
- сигнализируете менторам о том, что ваше решение готово к проверке. Это можно сделать через т.н. feedback pull request. Обратите внимание, что при создании вашего форка в нем автоматически создался специальный pull request с названием Feedback (его можно найти на вкладке "Pull requests"). В этот PR автоматически попадают все ваши коммиты, а также через него можно общаться с менторами. Ожидаем, что когда вы все докоммитите и код будет готов к проверке, то вы просто напишите в этот PR что "можно проверять ДЗ", и тэгните менторов. Про все это еще подробно напишем в чате курса.
- обратите внимание, что самостоятельно ставить pull request'ы к официальной репе курса не надо! Вся сдача происходит в вашей приватной репе через автоматически созданный feedback pull request.

После этого мы, т.е. преподаватели, которые будут проверять ваше решение:
- счекаутим вашу ветку
- проверим что ваш _solution.py_ действительно генерит сабмишн, который действительно выбивает те скоры, которые вы выбили на Kaggle

Теперь распишем все это немного детальнее.

## Виртуальное окружение

В своем скрипте вы скорее всего будете использовать какие-то фреймворки или библиотеки для обучения моделей, такие как, например, _pytorch_ или _transformers_.
У преподавателя, который будет проверять ваш код, должна быть возможность воспроизвести точно такое же окружение (т.е. тот же набор сторонних библиотек), какое было у вас, когда вы обучали модель.

Для этого предлагается воспользоваться механизмом виртуальных окружений (т.н. virtualenv).

В "главном" README в корне репы курса подробно расписано, как создать и активировать виртуальное окружение.
Ожидается, что вы:
- Создадите виртуальное окружение, например в папке _.venvs/hw5-final-project_ в корне счекаученного на вашу локальную машину вашего форка репы курса
- Поставите в него все необходимые библиотеки, напр. `pip install torch`
- Сохраните итоговое окружение в файлик _requirements.txt_: `pip freeze > requirements.txt`

Сейчас в репе в качестве примера уже лежит файлик _requirements.txt_ с несколькими библиотеками (такими как _pandas_), но вы в своей ветке можете спокойно его перезаписать.

Ожидается, что преподаватель:
- Тоже создаст у себя новое виртуальное окружение
- Поставит в него сохраненные вами библиотеки с помощью команды: `pip install -r requirements.txt`, где _requirements.txt_ будет взят уже из вашей ветки

и дальше будет запускать ваше решение _solution.py_ уже в этом восстановленном виртуальном окружении.

## Скрипт решения solution.py

Ожидается, что в этом скрипте лежит код, воспроизводящий ваши модель и сабмишн, который вы засабмитили на Kaggle.

Скрипт будет запускаться вот так: `./solution.py --submission_file=submission.csv PATH-TO-CONTEST-DATA`

Т.е. преподаватель:
- перейдет в папку со скриптом в счекаученной ветке с вашим решением
- запустит скрипт из-под созданного ранее виртуального окружения, и передаст вашему скрипту несколько параметров командной строки

Подробнее про параметры:
- _PATH-TO-CONTEST-DATA_ -- это путь к папке с данными контеста (т.е. это те самые данные, которые можно скачать с Kaggle командой `kaggle competitions download -c CONTEST-NAME`)
- _--submission_file_ -- это как раз путь до сабмишна, который и должен сгенерить ваш скрипт

Ожидаем, что ваш скрипт сгенерит точно такой же _submission.csv_, как тот, который вы залили на Kaggle в качестве решения.
Но, если по каким-то причинам (напр. если не получилось зафиксировать генератор случайных чисел) этот сабмишн будет отличаться, то ожидаем что он выбьет плюс-минус точно такие же скоры, которые вы выбили на Kaggle.

Тем не менее, постарайтесь, пожалуйста, зафиксировать в своем скрипте генераторы случайных чисел.

Еще несколько важных для воспроизводимости моментов:
- проверять решение будем на Linux-машинах, поэтому избегайте в своем решении каких-то конструкций, которые могут не заработать под Linux
- проверять будем на машине с GPU, т.е. в своем решении можете смело использовать GPU (но только одну карту)
- будьте готовы что проверяющий придет к вам с уточняющими вопросами если у него что-то не будет запускаться, или воспроизводиться и т.п. Ожидается, что все общение с проверяющим будет происходить в комментариях к вашему pull request'у.
- если вы пойдете путем обучения своей модели, то будет полезно если вы приложите к решению ссылку, по которой можно скачать веса обученной вами модели. Сами веса можете выложить куда-нибудь в облако (но не коммитьте их, пожалуйста, в свою ветку, т.к. они скорее всего будут довольно большие)

На этом все, надеемся что вам понравится решать этот контест!
