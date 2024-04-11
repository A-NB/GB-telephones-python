# ТЕЛЕФОННЫЙ СПРАВОЧНИК
## Консольное приложение с GUI

Контакты хранятся на диске в файле `contacts.json`, расположенном в одной директории с программой.

Посредством графического интерфейса реализована возможность просматривать все контакты в телефонном справочнике, создавать новые, изменять и удалять существующие.

Приложение позволяет:
* просматривать все контакты в одном окне в виде пронумерованного списка;
* осуществлять поиск контакта по любым данным (фамилия, имя, отчество, номер телефона, адрес электронной почты, дополнительная информация), по вхождению символов из поискового запроса в любое из полей либо в ключевое поле;
* избежать случайной перезаписи контактов при попытке добавления в книгу записи с уже имеющимися ФИО. Поскольку ключом в словаре с информацией о контактах является именно ФИО контакта, при подтверждении пользователем намерения создать контакт, к ключу добавляется специальный символ, по которому можно определить, что в словаре есть контакт с такими же фамилией, именем и отчеством;
* редактировать выбранный контакт (включая фамилию, имя и отчество).

Ниже представлено несколько скриншотов.
1. Главное окно программы:
<p align="center"><image src="/src/Главное окно.jpg" alt="Главное окно программы"></p>

2. Список всех контактов:
<p align="center"><image src="/src/Список всех контактов.jpg" alt="Список всех контактов"></p>

3. Окно поиска:
<p align="center"><image src="/src/Окно поиска.jpg" alt="Окно поиска"></p>

4. Результаты поиска:
<p align="center"><image src="/src/Результаты поиска.jpg" alt="Результаты поиска"></p>

5. Редактирование (создание нового) контакта:
<p align="center"><image src="/src/Редактирование (создание нового) контакта.jpg" alt="Редактирование (создание нового) контакта"></p>

6. Редактирование (изменение) контакта:
<p align="center"><image src="/src/Редактирование (изменение) контакта.jpg" alt="Редактирование (изменение) контакта"></p>

7. Предупреждение:
<p align="center"><image src="/src/Предупреждение.jpg" alt="Предупреждение"></p>