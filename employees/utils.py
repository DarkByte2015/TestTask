import itertools
import collections
from django.db.models import Q, Count
from .models import Employee

MAX_GROUP_COUNT = 7

# сравнивает две одномерные последовательности
def compare(seq1, seq2):
    l1 = len(seq1)
    l2 = len(seq2)

    if l1 != l2:
        return False

    for item1, item2 in zip(seq1, seq2):
        if item1 != item2:
            return False

    return True

# разворачивает многомерную последовательность в одномерную
def flatten(sequence):
    for item in sequence:
        if isinstance(item, collections.Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item)
        else:
            yield item

# ищет элемент последовательности, удовлетворяющий переданному предикату
def get_item(sequence, predicate, default = None):
    for item in sequence:
        if predicate(item):
            return item

    return default

# формирует последовательность символов в дипазоне
def char_range(begin, end):
    for letter in range(ord(begin), ord(end) + 1):
        yield chr(letter)

# рассчитывает информацию о сотрудниках
def compute_letter_info(begin, end):
    # получаем количество сотрудников на каждую букву

    letters = list(Employee.
        objects.
        extra({'letter': 'SUBSTR(UPPER(lastname), 1, 1)'}).
        values('letter').
        annotate(count = Count('pk')).
        order_by('letter'))

    # считаем общее количество сотрудников (так быстрее чем делать запрос к БД)

    all_count = 0

    for l in letters:
        all_count += l['count']

    nonempty_count = len(letters)

    # т.к. из БД были получены не все буквы алфавита,
    # то добавляем недостающие с нулевым количеством

    tmp = [ l['letter'] for l in letters ]

    for l in char_range(begin, end):
        if not l in tmp:
            letter = { 'letter': l, 'count': 0 }
            letters.append(letter)

    # считаем все...

    if nonempty_count:
        avg_count = round(all_count / nonempty_count)
    else:
        avg_count = 0

    required_count = round(all_count / MAX_GROUP_COUNT)

    if avg_count > required_count:
        total_count = avg_count
    else:
        total_count = required_count

    return {
        'letters': letters,
        'letters_count': len(letters),
        'all_count': all_count,
        'nonempty_count': nonempty_count,
        'avg_count': avg_count,
        'required_count': required_count,
        'total_count': total_count
    }

# забирает буквы из списка для группы с индекса
def get_group_letters(info, index):
    employees_count = 0
    j = index

    # забираем буквы пока их количество меньше заданного значения

    while employees_count < info['total_count'] and j < info['letters_count']:
        letter = info['letters'][j]
        employees_count += letter['count']
        j += 1
        yield letter

    # и все пустые буквы, следующие за последней не пустой, тоже

    yield from itertools.takewhile(lambda l: l['count'] == 0, info['letters'][j:])

# формирует группы букв
def compute_groups(begin, end):
    info = compute_letter_info(begin, end)
    i = 0

    while i < info['letters_count']:
        group_letters = list(get_group_letters(info, i))
        i += len(group_letters)
        group = {}
        group['begin'] = group_letters[0]['letter']
        group['end'] = group_letters[-1]['letter']
        group['id'] = ord(group['begin'])
        group['range'] = list(char_range(group['begin'], group['end']))
        group['str'] = '%s-%s' % (group['begin'], group['end'])
        yield group

# формирует запрос
def get_employees(context):
    q1 = Q()
    selected_group = get_item(
        context['groups'],
        lambda g: g['id'] == context['selected_group'],
        context['groups'][0])

    if selected_group['id'] != context['selected_group']:
        context['selected_group'] = selected_group['id']

    for letter in selected_group['range']:
        q1 |= Q(lastname__startswith = letter)

    if context['is_work']:
        q1 &= Q(end_work = None)

    q2 = Q(department_id__in = context['selected_departments'])

    return Employee.objects.filter(q1 & q2)
