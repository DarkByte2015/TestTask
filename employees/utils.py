import itertools
import collections
from django.db.models import Q
from .models import Employee, LetterGroup

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
    all_count = 0
    nonempty_count = 0
    letters = []

    # получаем количество работников, начинающихся
    # с каждой буквы и считаем количество не пустых букв

    for c in char_range(begin, end):
        char_count = Employee.objects.filter(lastname__startswith = c).count()
        all_count += char_count
        letter = { 'letter': c, 'count': char_count }
        letters.append(letter)

        if char_count:
            nonempty_count += 1

    # вычисляем среднее количество работников на группу

    if nonempty_count:
        avg_count = all_count / nonempty_count
    else:
        avg_count = 0

    return {
        'letters': letters,
        'letters_count': len(letters),
        'all_count': all_count,
        'nonempty_count': nonempty_count,
        'avg_count': round(avg_count)
    }

# забирает буквы из списка для группы с индекса
def get_group_letters(info, index):
    employees_count = 0
    j = index

    # забираем буквы пока их количество меньше среднего значения

    while employees_count < info['avg_count'] and j < info['letters_count']:
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
        group = LetterGroup.objects.create()
        group.begin = group_letters[0]['letter']
        group.end = group_letters[-1]['letter']
        group.save()
        yield group

# формирует запрос
def get_employees(context):
    q1 = Q()
    selected_group = get_item(context['groups'], lambda g: g['id'] == context['selected_group'])

    for letter in selected_group['range']:
        q1 |= Q(lastname__startswith = letter)

    if context['is_work']:
        q1 &= Q(end_work = None)

    q2 = Q()

    for department_id in context['selected_departments']:
        q2 |= Q(department_id = department_id)

    return Employee.objects.filter(q1 & q2)

def get_groups():
    groups = LetterGroup.objects.all()

    if len(groups) == 0:
        groups = compute_groups('А', 'Я')

    for group in groups:
        yield {
            'id': group.id,
            'range': char_range(group.begin, group.end),
            'begin': group.begin,
            'end': group.end,
            'str': str(group)
        }
