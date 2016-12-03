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

    for c in char_range(begin, end):
        char_count = Employee.objects.filter(lastname__startswith = c).count()
        all_count += char_count
        letter = { 'letter': c, 'count': char_count }
        letters.append(letter)

        if char_count:
            nonempty_count += 1

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

def get_group_letters(info, index):
    employees_count = 0
    j = index

    while employees_count < info['avg_count'] and j < info['letters_count']:
        letter = info['letters'][j]
        employees_count += letter['count']
        j += 1
        yield letter

    yield from itertools.takewhile(lambda l: l['count'] == 0, info['letters'][j:])

# формирует группы букв
def compute_groups(begin, end):
    info = compute_letter_info(begin, end)
    i = 0

    while i < info['letters_count']:
        group_letters = list(get_group_letters(info, i))
        i += len(group_letters)
        group_begin = group_letters[0]['letter']
        group_end = group_letters[-1]['letter']
        group = LetterGroup.objects.create(begin = group_begin, end = group_end)
        group.save()
        yield group

# распределяет работников по буквам
def distribute_by_letters(employees):
    letters = []
    count = 0

    # получаем работников начинающихся с каждой буквы
    # и считаем количество не пустых букв

    for c in char_range('А', 'Я'):
        c_employees = [e for e in employees if e[0].upper() == c]
        letter = (c, c_employees)
        letters.append(letter)

        if len(c_employees) != 0:
            count += 1

    # вычисляем среднее количество работников на группу

    avg = 0 if count == 0 else len(employees) / count
    return (letters, round(avg))

# распределяет работников по группам
def distribute_by_groups(letters, avg):
    i = 0

    while i < len(letters):
        group_letters = []
        j = i
        count = 0

        # забираем работников пока их количество меньше среднего значения

        while count < avg and j < len(letters):
            group_letters.append(letters[j])
            count += len(letters[j][1])
            j += 1

        # и все пустые буквы, следующие за последней не пустой, тоже

        empty_letters = itertools.takewhile(lambda l: len(l[1]) == 0, letters[j:])
        group_letters.extend(empty_letters)
        group_letters = list(group_letters)

        # формируем имя группы

        begin_letter = letters[i][0]
        end_letter = group_letters[-1][0]
        group_name = '%s-%s' % (begin_letter, end_letter)

        # формируем группу

        i += len(group_letters)
        group_employees = [l[1] for l in group_letters]
        group_employees = list(flatten(group_employees))
        group = (group_name, group_employees)
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
