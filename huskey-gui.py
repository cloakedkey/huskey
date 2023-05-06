import re
import tkinter as tk
import ttkbootstrap as ttk

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
        output_textbox.insert(tk.INSERT, f"{guarantees[guarantee]}\n")
        mark = mark.replace(guarantee, "")
    stl(mark)

# расшифровка имени стали
def stl(mark):
    for i in steel.keys():
        name_pat = re.compile(i)
        matched = name_pat.match(mark)
        if matched != None:
            output_textbox.insert(tk.INSERT, f"{steel[matched.group()]}\n")
            mark = mark.replace(matched.group(), "")
            if matched.group() == "СТ":
                structural_steel(mark)
            else:
                quality_steel(mark)

# расшифровка обыкновенной стали
def structural_steel(mark):
    gost_num = re.findall("[0-9]+", mark[0])
    output_textbox.insert(tk.INSERT, f"Номер стали по ГОСТ-380-2005: {gost_num[0]}\n")
    mark = mark.replace(gost_num[0], "")
    if "Г" in mark:
        output_textbox.insert(tk.INSERT, "Сталь содержит марганец выше 0.8%\n")
        mark = mark.replace("Г", "")
    deox(mark)

# расшифровка качественных сталей
def quality_steel(mark):
    carbon_pat = re.compile("[0-9]+")
    if "У" in mark:
        output_textbox.insert(tk.INSERT, "Сталь инструменатльная\n")
        mark = mark.replace("У", "")
    else:
        output_textbox.insert(tk.INSERT, "Сталь конструкционная\n")
    carbon = carbon_pat.match(mark)
    carbon_value = carbon.group()
    if carbon_value[-1] == "0":
        carbon_value = f"{carbon_value[0]}.{carbon_value[1]}"
        output_textbox.insert(tk.INSERT, f"Содержание углерода: {carbon_value}%\n")
    else:
        carbon_value = f"0.{carbon_value}"
        output_textbox.insert(tk.INSERT, f"Содержание углерода: {carbon_value}%\n")
    mark = mark.replace(carbon.group(), "")
    carbon_check(carbon_value)
    mark = decrypt_params(mark)
    mark = deox(mark)
    output_textbox.insert(tk.INSERT, "\n")
    if len(mark) != 0:
        output_textbox.insert(tk.INSERT, "Сталь содержит легирующие элементы: \n")
    else:
        output_textbox.insert(tk.INSERT, "Сталь не содержит легирующих элементов.\n")
    mod_decrypt(mark)

# расшифровка типа стали
def decrypt_params(mark):
    for i in params.keys():
        param_pat = re.compile(i)
        matched = param_pat.findall(mark)
        if len(matched) != 0:
            mark = mark.replace(matched[0], "", 1)
            output_textbox.insert(tk.INSERT, f"Сталь {params[matched[0]]}\n")
    return mark

# степень раскисления
def deox(mark):
    for i in deoxidation.keys():
        deox = re.compile(i)
        matched = deox.findall(mark)
        if len(matched) != 0:
            output_textbox.insert(tk.INSERT, f"По степени раскисления сталь {deoxidation[matched[0]]}\n")
            mark = mark.replace(matched[0], "", 1)
    return mark

# определение структуры стали и степени содержания углерода
def carbon_check(carbon):
    carbon = float(carbon)
    if carbon < 0.25:
        output_textbox.insert(tk.INSERT, "Сталь низкоуглеродистая\n")
    elif carbon > 0.60:
        output_textbox.insert(tk.INSERT, "Сталь высокоуглеродистая\n")
    else:
        output_textbox.insert(tk.INSERT, "Сталь среднеуглеродистая\n")
    if carbon > 0.8:
        output_textbox.insert(tk.INSERT, "По структуре сталь заэвтектоидная\n")
    elif carbon < 0.8:
        output_textbox.insert(tk.INSERT, "По структуре сталь доэвтектоидная\n")
    else:
        output_textbox.insert(tk.INSERT, "По структуре сталь эвтектоидная\n")

# расшифровка добавок и процента их содержания
def mod_decrypt(mark):
    while len(mark) != 0:
        try:
            output_textbox.insert(tk.INSERT, f"{modifiers[mark[0]]}")
            mark = mark.replace(mark[0], "")

            if len(mark) == 0 or mark[0].isalpha():
                output_textbox.insert(tk.INSERT, " 1%\n")
        except KeyError:
            if len(mark) > 1 and mark[1].isdecimal():
                value = mark[0] + mark[1]
                output_textbox.insert(tk.INSERT, f" {value}%\n")
                mark = mark.replace(value, "", 1)
            else:
                output_textbox.insert(tk.INSERT, f" {mark[0]}%\n")
                mark = mark.replace(mark[0], "", 1)

# расшифровка марки чугуна
def cast_iron_name(mark):
# поиск и удаление имени чугуна из марки
    for i in cast_iron.keys():
        name_pat = re.compile(i)
        matched = name_pat.match(mark)
        if matched != None:
            output_textbox.insert(tk.INSERT, f"{cast_iron[matched.group()]}\n")
            mark = mark.replace(matched.group(), '')
            if matched.group() == "А":
                cast_iron_name(mark)
    output_textbox.insert(tk.INSERT, "\n")
    cast_iron_params(mark)
# расшифровка параметров чугуна
def cast_iron_params(mark):
    params_match = re.compile("\d+")
    length_match = re.compile("\-\d")
    matched = params_match.match(mark)
    if matched != None:
        output_textbox.insert(tk.INSERT, f"Предел прочности при растяжении: {matched.group()} кг/мм^2\n")
        mark = mark.replace(matched.group(), "")
        length = length_match.match(mark)
        if length != None:
            output_textbox.insert(tk.INSERT, f"Относительное удлинение: {length.group().replace('-', '')}%\n")

def branch(material, mark):
    mark = mark.upper()
    if material == "Сталь":
        output_textbox.configure(state="normal")
        output_textbox.delete(1.0, 50.0)
        grnt(mark)
        output_textbox.configure(state="disabled")
    elif material == "Чугун":
        output_textbox.configure(state="normal")
        output_textbox.delete(1.0, 50.0)
        cast_iron_name(mark)
        output_textbox.configure(state="disabled")


# --- GUI ---

# window setup
window = ttk.Window(themename="minty")
window.title("Huskey - mark decryptor")
window.geometry("550x650")

# material combo box setup
material_list = ["Сталь", "Чугун", "Бронза"]
material = tk.StringVar(value=material_list[0])
material_combobox = ttk.Combobox(master=window, values=material_list,
                                 textvariable=material, font=("Arial", 14))

combobox_label = ttk.Label(master=window, text="Материал",
                           font=("Arial bold", 20))

# mark input entry setup

mark = tk.StringVar()
mark_entry = ttk.Entry(master=window, textvariable=mark, width=21,
                       font=("Arial", 14))

mark_entry_label = ttk.Label(master=window, text="Марка",
                             font=("Arial bold", 20))

# decrypt button

decrypt_button = ttk.Button(master=window, text="Расшифровать",
                            width=25, command= lambda: branch(material.get(), mark.get()))

# output textbox

output_textbox = ttk.ScrolledText(master=window, width=44, height=16,
                              font=("Arial", 14))

output_textbox_label = ttk.Label(master=window, text="Информация",
                                 font=("Arial bold", 14))


# placing the widgets
combobox_label.place(x=50, y=50)
material_combobox.place(x=250, y=55)
mark_entry.place(x=250, y=150)
mark_entry_label.place(x=50, y=145)
decrypt_button.place(x=250, y=190)
output_textbox.place(x=50, y=280)
output_textbox_label.place(x=50, y=250)

window.mainloop()

