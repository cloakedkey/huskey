import re

cast_iron = {'СЧ':'Серый чугун', 'КЧ':'Ковкий чугун',
    'ВЧ': 'Высокопрочный чугун', 'А': 'Антифрикционный'}

steel = {'СТАЛЬ': 'Качественная сталь', 'СТ': 'Сталь обыкновенного качества'}

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
            if matched.group() == "СТ":
                structural_steel(mark)
            else:
                quality_steel(mark)

# расшифровка качественной стали
# Теперь необходимо избавиться от доп марок таких как А так как из-за этого будут проблемы
# ведь такая марка будет иметь вид СтальАУ10Н5 что А в этом случае забьёт match метод regex.
# Сталь без аргумента У не будет выводить углерод, что верно.
def quality_steel(mark):
    if "У" in mark:
        print("Сталь инструменатльная")
        mark = mark.replace("У", "")
        carbon_pat = re.compile("[0-9]+")
        carbon = carbon_pat.match(mark)
        carbon = carbon.group()
        if carbon[0] == "0":
            print(f"Содержание углерода: {carbon[0]}.{carbon[1]}%")
        else:
            print(f"Содержание углерода: 0.{carbon}%")

    else:
        print("Сталь конструкционная")


# расшифровка обыкновенной стали
def structural_steel(mark):
    gost_num = re.findall("[0-9]+", mark[0])
    print("Сталь конструкционная")
    print("Номер стали по ГОСТ-380-2005: ", gost_num[0])
    mark = mark.replace(gost_num[0], "")
    if "Г" in mark:
        print("Сталь содержит марганец выше 0.8%")
        mark = mark.replace("Г", "")
    for i in deoxidation.keys():
        deox = re.compile(i)
        matched = deox.match(mark)
        if matched != None:
            print(f"По окислению сталь {deoxidation[matched.group()]}")

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
print("\n")
grnt("СТ4ПС")
print("\n")
grnt("СТАЛЬУ07Н5")
print("\n")
grnt("СТАЛЬУ10Н4")
