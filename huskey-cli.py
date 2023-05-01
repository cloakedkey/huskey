import re
import sys

cast_iron = {'СЧ':'Серый чугун', 'КЧ':'Ковкий чугун',
    'ВЧ': 'Высокопрочный чугун', 'А': 'Антифрикционный'}

steel = {'СТАЛЬ': 'Качественная сталь', 'СТ': 'Сталь обыкновенного качества(конструкционная)'}

guarantees = {'А': 'Завод гарантирует заданные механические свойства',
              'Б': 'Завод гарантирует химический состав',
              'В': 'Завод гарантрует химический состав и механические свойства'}

modifiers = {'Х': 'Хром', 'Н': 'Никель', 'Ф': 'Ванадий', 'М': 'Молибден',
             'В': 'Вольфрам', 'С': 'Кремний', 'Г': 'Марганец', 'Т': 'Титан',
             'Л': 'Бериллий', 'Д': 'Медь', 'Б': 'Ниобий',
             'Ю': 'Алюминий', 'Е': 'Селен', 'К': 'Кобальт', 'П': 'Фосфор',
             'Ц': 'Цирконий'}

deoxidation = {'СП': 'спокойная', 'ПС': 'полуспокойная', 'КП': 'кипящая'}

params = {'Р': 'быстрорежущая', 'Ш': 'шарикоподшипниковая',
          'А': 'высококачественая', 'Э': 'электротехническая'}

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

# расшифровка обыкновенной стали
def structural_steel(mark):
    gost_num = re.findall("[0-9]+", mark[0])
    print("Номер стали по ГОСТ-380-2005: ", gost_num[0])
    mark = mark.replace(gost_num[0], "")
    if "Г" in mark:
        print("Сталь содержит марганец выше 0.8%")
        mark = mark.replace("Г", "")
    deox(mark)

# расшифровка качественных сталей
def quality_steel(mark):
    carbon_pat = re.compile("[0-9]+")
    if "У" in mark:
        print("Сталь инструменатльная\n")
        mark = mark.replace("У", "")
    else:
        print("Сталь конструкционная\n")
    carbon = carbon_pat.match(mark)
    carbon_value = carbon.group()
    if carbon_value[-1] == "0":
        carbon_value = f"{carbon_value[0]}.{carbon_value[1]}"
        print(f"Содержание углерода: {carbon_value}%")
    else:
        carbon_value = f"0.{carbon_value}"
        print(f"Содержание углерода: {carbon_value}%")
    mark = mark.replace(carbon.group(), "")
    carbon_check(carbon_value)
    mark = decrypt_params(mark)
    mark = deox(mark)
    print("\n")
    if len(mark) != 0:
        print("Сталь содержит легирующие элементы: ")
    else:
        print("Сталь не содержит легирующих элементов.")
    mod_decrypt(mark)

# расшифровка типа стали
def decrypt_params(mark):
    for i in params.keys():
        param_pat = re.compile(i)
        matched = param_pat.findall(mark)
        if len(matched) != 0:
            mark = mark.replace(matched[0], "", 1)
            print(f"Сталь {params[matched[0]]}")
    return mark

# степень раскисления
def deox(mark):
    for i in deoxidation.keys():
        deox = re.compile(i)
        matched = deox.findall(mark)
        if len(matched) != 0:
            print(f"По степени раскисления сталь {deoxidation[matched[0]]}")
            mark = mark.replace(matched[0], "", 1)
    return mark

# определение структуры стали и степени содержания углерода
def carbon_check(carbon):
    carbon = float(carbon)
    if carbon < 0.25:
        print("Сталь низкоуглеродистая")
    elif carbon > 0.60:
        print("Сталь высокоуглеродистая")
    else:
        print("Сталь среднеуглеродистая")
    if carbon > 0.8:
        print("По структуре сталь заэвтектоидная")
    elif carbon < 0.8:
        print("По структуре сталь доэвтектоидная")
    else:
        print("По структуре сталь эвтектоидная")

# расшифровка добавок и процента их содержания
def mod_decrypt(mark):
    while len(mark) != 0:
        try:
            print(modifiers[mark[0]])
            mark = mark.replace(mark[0], "")

            if len(mark) == 0 or mark[0].isalpha():
                print("1%")
        except KeyError:
            if len(mark) > 1 and mark[1].isdecimal():
                value = mark[0] + mark[1]
                print(f"{value}%")
                mark = mark.replace(value, "", 1)
            else:
                print(f"{mark[0]}%")
                mark = mark.replace(mark[0], "", 1)

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
    print("\n")
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

if sys.argv[1] == "-steel":
    mark = sys.argv[2]
    mark = mark.upper()
    grnt(mark)
elif sys.argv[1] == "-castiron":
    mark = sys.argv[2]
    mark = mark.upper()
    cast_iron_name(mark)
else:
    print("Руководство по использованию: \n")
    print("\tдля того чтобы расшифровать марку чугуна используйте -castiron [марка]")
    print("\tдля марки стали используйте: -steel [марка]\n")
    print("**МАРКУ НЕОБХОДИМО ВВОДИТЬ БЕЗ []**")


