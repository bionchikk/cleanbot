# cleanbot

Telegram бот для клининговой компании. Реализован на 70% . Позьватель заходит в бота , нажиманиет на кнопку /start , вводит все свои данные которые сохранятются в бд. Дальше он может почитать немного информации по поводу уборки в разных комнатах или сразу перейти к заказу.<img width="452" alt="Снимок экрана 2024-05-16 в 21 54 22" src="https://github.com/bionchikk/cleanbot/assets/167641560/fdf5e0f1-8622-444c-8ca7-49de798b7862">

На выбор ему дается два калькулятора : калькулятор после ремонта и простой калькулятор.  
<img width="452" alt="Снимок экрана 2024-05-16 в 21 55 34" src="https://github.com/bionchikk/cleanbot/assets/167641560/a9070113-717b-416d-885d-bb316232b635">
При выборе простого калькулятора пользователь выбирает количество комнат и санузлов 
<img width="452" alt="Снимок экрана 2024-05-16 в 21 56 38" src="https://github.com/bionchikk/cleanbot/assets/167641560/1fe0f88c-c6c4-49<img width="452" alt="Снимок экрана 2024-05-16 в 21 57 03" src="https://github.com/bionchikk/cleanbot/assets/167641560/0f34957a-b40a-414a-bf87-094f4a744bf7">
bf-b3fa-f1efbad78aff">
После выбора этих компанентов можно оформить на данном этапе или перейти к следующему этапу 
<img width="452" alt="Снимок экрана 2024-05-16 в 21 58 14" src="https://github.com/bionchikk/cleanbot/assets/167641560/9f21803a-ae1b-444a-a468-0e86c247e002">
При переходе на следующий этап нужно выбрать частоту уборки 
<img width="452" alt="Снимок экрана 2024-05-16 в 21 59 27" src="https://github.com/bionchikk/cleanbot/assets/167641560/c3b27a6c-4997-4e88-8d12-5347eeb1f5d0">
Далее можно выбрать доп опции для уборки <img width="452" alt="Снимок экрана 2024-05-16 в 21 59 47" src="https://github.com/bionchikk/cleanbot/assets/167641560/557a8955-5114-4fa4-8c3d-1e26aca33839">
После всех выборов можно увидеть состав заказа и те функции что пользователь выбрал
<img width="452" alt="Снимок экрана 2024-05-16 в 22 01 37" src="https://github.com/bionchikk/cleanbot/assets/167641560/150b03c4-65e7-4958-8f53-69cf0398ae99">
После этого нужно выбрать свободную дату и время .Под этим подразумевается дата и время на которую есть свободные клинеры (все дни кроме выходных)<img width="452" alt="Снимок экрана 2024-05-16 в 22 02 06" src="https://github.com/bionchikk/cleanbot/assets/167641560/dd558455-1518-42d7-9871-fc78431b048d"><img width="452" alt="Снимок экрана 2024-05-16 в 22 04 29" src="https://github.com/bionchikk/cleanbot/assets/167641560/16ffc345-f20b-4858-aff3-6983d68d6705">
После того как пользователь заказал он видит информацию о заказе<img width="452" alt="Снимок экрана 2024-05-16 в 22 04 37" src="https://github.com/bionchikk/cleanbot/assets/167641560/72821519-8c2b-4176-802b-483e83e4ee87">
Когда пользователь сделал заказ , в чат с клинерами приходит сообщение с заказом  и кнопка "Принять"
<img width="452" alt="Снимок экрана 2024-05-16 в 22 04 44" src="https://github.com/bionchikk/cleanbot/assets/167641560/59a736d1-3523-4367-9e27-b91c72bdb3e2">
После того как работник принял заказ в гугл таблицу с графиком заполняется время работы ![Снимок экрана 2024-05-16 в 22 05 43](https://github.com/bionchikk/cleanbot/assets/167641560/9549d95f-9c45-45b0-9e28-aab850e56ab9)
После того как работник принял заказ , то есть нажал кнопку сообщение изменяется и появляется кнопка "Заказ выполняется "
<img width="452" alt="Снимок экрана 2024-05-16 в 22 04 57" src="https://github.com/bionchikk/cleanbot/assets/167641560/22ce4cb1-b32c-44ce-a62c-8e38a300629f">
Когда работник выполнил заказ и нажал на кнопку то юзера в чат с ботом приходит сообщение о том что его заказ выполнен 
<img width="452" alt="Снимок экрана 2024-05-16 в 22 05 07" src="https://github.com/bionchikk/cleanbot/assets/167641560/12d908e9-1b48-4abc-8580-c22a44058d5a">
Пользователь может оставить свой отзыв. Все заказы сохраняются в бд . Не реализован алгоритм распределение заказов елси работники не принимают заказ в течении какого то времени. Возможно необходимо сделать еще чат с админами  с функцией добавления новых работников и перенести команды которые показывают выручку , количество инвентаря , в чат с админами.












