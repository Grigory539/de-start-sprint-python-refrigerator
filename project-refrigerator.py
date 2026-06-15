/// 11.03.2025 ///

from datetime import datetime, timedelta, date
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'


goods = {}



def add(items, title, amount, expiration_date=None):
    if expiration_date is not None:
        expiration_date = datetime.strptime(expiration_date, DATE_FORMAT).date()
    if title not in items:
        items[title] = []   
    items[title].append({'amount': amount, 'expiration_date': expiration_date})

    
add(goods, 'Вода', Decimal('2.5'))

add(goods, 'Яйца', Decimal('10'), '2023-10-28')

add(goods, 'Яйца', Decimal('3'), '2023-10-15')


def add_by_note(items, note):
    note_parts = str.split(note)
    last_element = note_parts[-1]
    last_element_list = str.split(last_element, '-')

    date_new = None
    amount = None
    name = ''
    if len(last_element_list) == 3:
        date_new = last_element
        amount = Decimal(note_parts[-2])
        name = str.join(' ', note_parts[0:-2])
    else:
        amount = Decimal(note_parts[-1])
        name = str.join(' ', note_parts[0:-1])

    add(items, name, amount, date_new)


add_by_note(goods, 'Яйца гусиные 4 2023-07-15')

add_by_note(goods, 'Яйца гусиные 5')




def find(items, needle):
    result = []
    for item in items:
        search = str.find(str.lower(item), str.lower(needle))
        if search >= 0:
            result.append(item)
    return result




def amount(items, needle):
    amount_total = Decimal('0')
    for title in find(items, needle):
        amount_total += sum(amounts['amount'] for amounts in items[title])
    return amount_total


print(amount(goods, 'яйца'))

print(amount(goods, 'морковь'))



def expire(items, in_advance_days=0):
    today = date.today()
    expiration_items = []
    advance_date = today + timedelta(days=in_advance_days)
    for title in items:
        expired_amount = 0
        for item in items[title]:
            if item['expiration_date'] and item['expiration_date'] <= advance_date:
                expired_amount += item['amount']
        if expired_amount:
            expiration_items.append((title, expired_amount))
    return expiration_items



# Вызов функции 10 декабря 2023 года
print(expire(goods))
# Вывод: [('Хлеб', Decimal('1'))]
print(expire(goods, 1))
# Вывод: [('Хлеб', Decimal('1')), ('Яйца', Decimal('3'))]
print(expire(goods, 2))
# Вывод: [('Хлеб', Decimal('1')), ('Яйца', Decimal('5'))]
