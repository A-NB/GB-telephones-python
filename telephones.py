import json
import easygui

CONTACTS_FILE = "contacts.json"

def load_contacts():
    """ Загрузка контактов из файла """
    try:
        with open(CONTACTS_FILE, 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_contacts(contacts):
    """ Запись контакта в файл """
    with open(CONTACTS_FILE, 'w', encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)


def display_contact_info(name, contact):
    """ Вывод информации об одиночном контакте """
    message = f"Имя: {name}\n"
    
    phones = contact.get('phones', [])
    phones_str = ', '.join(phones) if phones else "Нет телефонов"
    message += f"Телефоны: {phones_str}\n"
    
    emails = contact.get('emails', [])
    emails_str = ', '.join(emails) if emails else "Нет адресов эл. почты"
    message += f"Emails: {emails_str}\n"
    
    message += f"День рождения: {contact.get('birthday', 'Не указан')}\n"
    message += f"Доп. информация: {contact.get('additional_info', 'Отсутствует')}\n"
    
    easygui.codebox("Информация о контакте", "Контакт", message)


def search_contact(contacts, edit = False, delete = False):
    """ Поиск и вывод на экран найденных контактов, выбор действий """
    query = easygui.enterbox("Введите поисковый запрос:")
    if not query:  # Проверяем, что пользователь ввел запрос
        easygui.msgbox("Поисковый запрос не может быть пустым.")
        return
    results = find_contacts(contacts, query)
    if results:
        choices = []
        for name, contact in results:
            contact_info = f"{name} (телефоны: {', '.join(contact.get('phones', ['Нет']))}, " \
                        f"emails: {', '.join(contact.get('emails', ['Нет']))}, " \
                        f"день рождения: {contact.get('birthday', 'Не указан')}, " \
                        f"доп. информация: {contact.get('additional_info', 'Отсутствует')})"
            choices.append(contact_info)        
        if len(choices) > 1:
            choice = easygui.choicebox(edit * "Выберите контакт для редактирования:" +
                                       delete * "Выберите контакт для удаления:",
                                       "Результаты поиска",
                                       choices=choices)
        elif len(choices) == 1: # Если найдено более одного контакта
            display_contact_info(results[0][0], results[0][1])
            choice = choices[0] # Если найден единственный контакт
        if choice:
            selected_contact_info = next((info for info in choices if choice in info), None)
            if selected_contact_info:
                # Извлекаем имя контакта из строки выбора
                selected_name = selected_contact_info.split(" (")[0]
                # Получаем выбранный контакт из словаря
                selected_contact = next((contact for name, contact in results if name == selected_name), None)
                if selected_contact:
                    if delete:
                        if easygui.ynbox("Вы уверены, что хотите удалить этот контакт?", "Подтверждение удаления", choices=("[<F1>]Да", "[<F2>]Нет"), image=None, default_choice='[<F2>]Нет', cancel_choice='[<F1>]Да'):
                            del contacts[selected_name] # Удаляем контакт из словаря
                            save_contacts(contacts)     # Сохраняем обновленный список контактов
                            easygui.msgbox(f"Контакт {selected_name} успешно удалён.") 
                        else:
                            easygui.msgbox(f"Удаление контакта {selected_name} отменено пользователем.")
                    else:                   
                        create_new_or_edit_selected_contact(contacts, selected_name, selected_contact)
                else:
                    easygui.msgbox("Контакт не найден.")
        else:
            easygui.msgbox("Действие отменено пользователем.")
    else:
        easygui.msgbox("Контакт не найден.")


def find_contacts(contacts, query):
    """ Поиск контакта по ключу и всем полям, включая частичные совпадения """    
    results = []
    for name, contact in contacts.items():
        if query.lower() in name.lower():  # Поиск по имени
            results.append((name, contact))
        elif any(query.lower() in phone.lower() for phone in contact['phones']):
            results.append((name, contact))  # Поиск по телефонам
        elif any(query.lower() in email.lower() for email in contact['emails']):
            results.append((name, contact))
        elif query.lower() in contact['birthday'].lower():
            results.append((name, contact))  # Поиск по дате рождения
        elif query.lower() in contact['additional_info'].lower():
            results.append((name, contact))  # Поиск по дополнительной информации
    return results


def create_new_or_edit_selected_contact(contacts, selected_name="", selected_contact=None):
    """ Создание, редактирование контакта """
    if selected_contact is None:
        selected_contact = {}  # Создаем новый контакт, если он не указан
    if contacts is None:
        contacts = {}  # Создаем новый словарь контактов, если он не указан
    contact = selected_contact.copy() # Извлекаем данные выбранного контакта
    # Разбиваем строку имени контакта по запятой и пробелу
    name_parts = selected_name.split(" ")
    last_name = name_parts[0] if len(name_parts) >= 1 else ""
    first_name = name_parts[1] if len(name_parts) >= 2 else ""
    middle_name = name_parts[2] if len(name_parts) >= 3 else ""
    # Вводим данные для редактирования
    field_values = [
        last_name,
        first_name,
        middle_name if middle_name else "",  # Проверяем, содержит ли отчество значение
        ', '.join(contact.get('phones', [])),  # Номера телефонов
        ', '.join(contact.get('emails', [])),  # Email адреса
        contact.get('birthday', ''),  # День рождения
        contact.get('additional_info', '')  # Доп. информация
    ]
    field_names = ["Фамилия", "Имя", "Отчество", "Телефоны", "Emails", "День рождения", "Доп. информация"]
    new_values = easygui.multenterbox("Редактирование контакта", "Редактировать контакт", field_names, field_values)
    if new_values:
        # Обновляем данные контакта
        last_name, first_name, middle_name, phones, emails, birthday, additional_info = new_values
        new_name = f"{last_name} {first_name} {middle_name}"
        new_phones = [phone.strip() for phone in phones.split(',')]
        new_emails = [email.strip() for email in emails.split(',')]
        contact.update(
                        {
                        "phones": new_phones,
                        "emails": new_emails,
                        "birthday": birthday,
                        "additional_info": additional_info
                        }
                      )
        if new_name != selected_name:
            if selected_name != "":
                del contacts[selected_name]  # Удаляем старый ключ
            selected_name = new_name  # Обновляем имя

        while True:
            if selected_name in contacts:
                if easygui.ynbox("Контакт с таким именем существует! Презаписать существующий контакт?\nПри нажатии 'Нет' будет создан новый контакт.", "Внимание!", choices=("[<F1>]Да", "[<F2>]Нет"), image=None, default_choice='[<F2>]Нет', cancel_choice='[<F1>]Да'):
                    contacts[selected_name] = contact # Обновляем данные контакта
                    break
                else:
                    selected_name = "~" + selected_name # Добавляем тильду перед фамилией. Это значит,
                                                        # что контакт с такими же ФИО уже есть в телефонной книге
                                                        # (полный тёзка)
            else:
                contacts[selected_name] = contact # Создаём контакт с видоизменённым именем
                break
        # Сохраняем обновленные данные
        save_contacts(contacts)
        easygui.msgbox("Контакт успешно обновлён или добавлен.")
    else:
        if selected_name == "":
            easygui.msgbox("Контакт не создан.")
        else:
            easygui.msgbox("Изменения не были внесены.")


def view_all_contacts(contacts):
    """ Просмотр всех контактов """
    counter = 1
    message = f"Всего контактов: {len(contacts)}\n\n"
    for name, contact in contacts.items():
        message += f"{counter}. {name}\n"
       
        phones = contact.get('phones', [])  # Получаем список номеров телефонов или пустой список, если ключ отсутствует
        phones_str = ', '.join(phones) if phones else "Нет телефонов"
        
        emails = contact.get('emails', [])  # Получаем список email'ов или пустой список, если ключ отсутствует
        emails_str = ', '.join(emails) if emails else "Нет адресов эл. почты"

        message += f"Телефоны: {phones_str}\n"
        message += f"Emails: {emails_str}\n"
        message += f"День рождения: {contact.get('birthday', 'Не указан')}\n"
        message += f"Доп. информация: {contact.get('additional_info', 'Отсутствует')}\n\n"

        counter += 1
    easygui.codebox("Все контакты", "Контакты", message)


def main():
    contacts = load_contacts()
    while True:
        choices = ["Просмотреть все контакты",
                   "Добавить контакт",
                   "Найти контакт",
                   "Редактировать контакт",
                   "Удалить контакт",
                   "Выход"]
        choice = easygui.choicebox("Выберите действие:", "Телефонная книга", choices)
        if not choice or choice == "Выход":
            easygui.msgbox("Программа завершена.")
            break
        elif choice == "Просмотреть все контакты":
            view_all_contacts(contacts)
        elif choice == "Добавить контакт":
            create_new_or_edit_selected_contact(contacts) #add_contact(contacts)
        elif choice == "Найти контакт":
            search_contact(contacts)
        elif choice == "Редактировать контакт":
            search_contact(contacts, edit = True) #edit_contact(contacts)
        elif choice == "Удалить контакт":
            search_contact(contacts, delete = True) #delete_contact(contacts)

if __name__ == "__main__":
    main()
