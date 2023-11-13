# weather_task

1) Откуда и каким образом будете получать информацию о погоде по конкретному городу? какие библиотеки будете для этого использовать? 

Информацию о погоде буду получать через API openweathermap. Для этого понадобится библиотека requests. Пока вроде все.
__________________________
2) Как будете определять текущее месторасположение и как будете получать информацию о погоде по текущему расположению? какие библиотеки будете для этого использовать

Информацию о текущем местоположении буду получать с помощью библиотеки geocoder. geocoder.ip('me') - вернет данные о геолокации, а именно ip адресс и широту с долготой. По широте и долготе уже можно определить погоду через  API openweathermap.
__________________________
3) Как планируете хранить историю результатов запросов и как планируете выводить ее пользователю?

Пока что думаю записывать в текстовый файл, каким-то таким образом: file = open("data.txt", "w"), file.write(f"{data}"), file.close().
Вывод пользователю по его команде в консоли. Допустим, История будет под пунктом 3. После того, как пользователь ввел цифру "3", его спросят, какое количество записей из истории он хочет просмотреть. На этот экран также можно добавить количество записей, чтобы пользователь понимал свои возможности. Ну и после введения пользователем числа, выводится история просмотра погоды.
__________________________

4) Какой интерфейс для программы вы собираетесь использовать и как он будет работать? (предлагаю сделать простую консольную реализацию с выбором действия по пунктам). 

Думаю сделать простую консольную реализацию с выбором действия по пунктам)
Что-то вроде:
1. Узнать погоду в городе (по названию/широте-долготе)
2. Узнать погоду по моему местоположению
3. Посмотреть историю запросов

"0". Закрыть программу

Во время открытия одной из вкладок, будут соответствующие просьбы по введению какого-либо текста от полльзователя. Также будет пункт, а-ля "Введите 0, чтобы вернуться назад". А после выведения необходимой ему информации, выведения в консоли, будет также выводиться пункт "Введите 0, чтобы вернуться в меню"
__________________________

<url>weqwq

5) Не забудте учесть тот факт, что пользователь может вводить невалидные значения, API может отвалиться, вы сами можете неверно сформировать запрос в API. Все это надо обрабатывать с помощью try...except и как-то на это реагировать. Программа не должна от этого ломаться.

Да, это сделаю. Валидацию хочу сделать в отдельном файле, ну или как минимум в отдельной функции.
__________________________
