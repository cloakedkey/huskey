import re

cast_iron = {'СЧ':'Серый чугун', 'КЧ':'Ковкий чугун',
    'ВЧ': 'Высокопрочный чугун', 'А': 'Антифрикционный'}

steel = {'СТ': 'Конструкционная сталь', 'СТАЛЬ': 'Качественная сталь'}

guarantees = {'А': 'Завод гарантирует заданные механические свойства',
              'Б': 'Завод гарантирует химический состав',
              'В': 'Завод гарантрует химический состав и механические свойства'}

modifiers = {'Х': 'хром', 'Н': 'никель', 'Ф': 'ванадий', 'М': 'молибден',
             'В': 'вольфрам', 'С': 'кремний', 'Г': 'марганец', 'Т': 'титан',
             'Л': 'бериллий', 'Д': 'медь', 'А': 'азот', 'Б': 'ниобий',
             'Ю': 'алюминий', 'Е': 'селен', 'К': 'кобальт', 'Р': 'бор', 'П': 'фосфор',
             'Ц': 'цирконий'}

deoxidation = {'СП': 'Спокойная', 'ПС': 'Полуспокойная', 'КП': 'Кипящая'}

params = {'Р': 'быстрорежущая', 'Ш': 'шарикоподшипниковая',
          'А': 'автоматная', 'Э': 'электротехническая'}

# проверка гарантий стали
def grnt(mark):
    if mark[0] != "С":
        guarantee = mark[0]
        print(f"{guarantees[guarantee]}")
        mark = mark.replace(guarantee, "")
    stl(mark)

# расшифровка имени стали
def stl(mark):
    for i in steel.keys():
        name_pat = re.compile(i)
        matched = name_pat.match(mark)
        if matched != None:
            print(f"{steel[matched.group()]}")
            mark = mark.replace(matched.group(), "")


# расшифровка марки чугуна
def cast_iron_name(mark):
# поиск и удаление имени чугуна из марки
    for i in cast_iron.keys():
        name_pat = re.compile(i)
        matched = name_pat.match(mark)
        if matched != None:
            print(f"{cast_iron[matched.group()]}")
            mark = mark.replace(matched.group(), '')
            if matched.group() == "А":
                cast_iron_name(mark)
    cast_iron_params(mark)

# расшифровка параметров чугуна
def cast_iron_params(mark):
    params_match = re.compile("\d+")
    length_match = re.compile("\-\d")
    matched = params_match.match(mark)
    if matched != None:
        print(f"Предел прочности при растяжении: {matched.group()} кг/мм^2")
        mark = mark.replace(matched.group(), "")
        length = length_match.match(mark)
        if length != None:
            print(f"Относительное удлинение: {length.group().replace('-', '')}%")

grnt("БСТ4СП")
grnt("СТ4ПС")
# doesn't work because it matches СТ in СТАЛЬ
grnt("СТАЛЬУ07")

