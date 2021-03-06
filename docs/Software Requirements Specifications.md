# Software Requirements Specification

* * *

## Введение

Цель документа — собрать и проанализировать все идеи, возникшие для определения системы, ее требования по отношению к потребителям. В спецификации будет представлен подробный обзор программного обеспечения, его параметры и задачи. Будет описана целевая аудитория проекта, требования к аппаратному и программному обеспечению. Также будет осуществляться прогнозирование того, как продукт будет использоваться, изложение концепций, которые могут быть разработаны позже и  документирование идей, находящихся в рассмотрении, но могут быть выброшены по мере развития проекта.

Данный продукт нацелен на разумный способ разделения задолженности между друзьями. По итогу, будет рассчитана потраченная сумма каждого, сумма долга каждого члена группы. Подразумевается, что данное приложение будет использовано во время совместного времяпрепровождения группы людей. В веб-приложении можно создавать поездки, для каждой из них можно добавлять разных людей, по каждой будет вестись отдельная статистика. Продукт не включает в себя настройку сервера.

## Требования пользователя

### Программные интерфейсы

Проект будет написан с использованием языка программирования Python. Также будет использоваться микрофреймворк Flask для создания backend части приложения.

## Интерфейс пользователя

Взаимодействие с пользователем будет происходит при помощи веб-интерфейса. В интерфейсе будут присутствовать необходимые формы для ввода информации, будут отображаться поездки, созданные пользователем, таймлайн расходов, чарт со статистикой расходов.

Пример интерфейса представлен по [ссылке](https://www.figma.com/file/NZQD8A5JyyxLQQRoDINif2/DivideXp-prototype?node-id=0%3A1).

## Характеристики пользователей

Данное приложение будет интересно пользователям, которые хотят контролировать и отслеживать свои расходы во время путешествий. Также благодаря возможности добавлять нескольких людей к своей поездке, оно будет интересно пользователям, которые во время поездки с друзьями хотят автоматизировать распределение расходов каждого.

## Документация для пользователя

Для комфортного использования приложения пользователем требуется сделать видео, в котором кратко продемонстрировать весь функционал, для дополнительной информации организовать поддержку, к которой пользователь может обратиться в случае вопросов и/или предложений.

## Системные требования

### Функциональные требования

-   Внесение информации о расходах.

    По умолчанию, все расходы, внесенные пользователем, делятся поровну между всеми участниками команды, но можно снять соответствующую галочку в чекбоксе и расход будет учтен только для одного пользователя.

    ![img](https://github.com/veronika-suprunovich/dividexp/blob/main/docs/img/add_expense_form.PNG)

-   Добавление участников в поездку.

    Для добавления нового участника нужно ввести его имя пользователя, в команду могут быть добавлены только пользователи, зарегистрированные в приложении.

    ![img](https://github.com/veronika-suprunovich/dividexp/blob/main/docs/img/add_new_member_form.PNG)

-   Наличие всплывающих форм для быстрого внесения новой информации.
-   Защита паролем.

    Для защиты данных используется хеширование с солями.

-   Полное управление категориями расходов.

    Пользователь может использовать как предложенные категории, так и добавлять свои.

-   Бюджетирование.

## Нефункциональные требования

### **Атрибуты качества**

-   Простой и удобный интерфейс взаимодействия (соответствует мак-апам).
-   Обработка ошибок.
-   Защита данных пользователя (соответствует функциональным требованиям).
