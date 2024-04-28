import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение для внесения данных")

        self.conn = mysql.connector.connect(
            host="31.31.196.161",
            user="u2363403_u2main",
            password="oT8kX3fL8jkG4nO4",
            database="u2363403_Port"
        )
        self.cursor = self.conn.cursor()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Выберите таблицу:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.table_var = tk.StringVar()
        self.table_combobox = ttk.Combobox(self.root, textvariable=self.table_var, values=["очередь_кукуруза", "очередь_пшеница", "очередь_ячмень"])
        self.table_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.table_combobox.set("очередь_кукуруза")
        self.table_combobox.bind("<<ComboboxSelected>>", self.update_table)

        ttk.Label(self.root, text="Номер телефона:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.phone_entry = ttk.Entry(self.root)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="ФИО:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Номер авто:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.car_entry = ttk.Entry(self.root)
        self.car_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Номер прицепа:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.trailer_entry = ttk.Entry(self.root)
        self.trailer_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Груз:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.cargo_var = tk.StringVar()
        self.cargo_combobox = ttk.Combobox(self.root, textvariable=self.cargo_var, values=["Кукуруза", "Пшеница", "Ячмень"])
        self.cargo_combobox.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Поставщик:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.supplier_entry = ttk.Entry(self.root)
        self.supplier_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self.root, text="Вес по накладной:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.grid(row=7, column=1, padx=5, pady=5)

        ttk.Button(self.root, text="Добавить запись", command=self.add_record).grid(row=8, column=0, columnspan=2, pady=10)
        ttk.Button(self.root, text="Выгрузить и удалить", command=self.copy_and_delete_records).grid(row=9, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Дата", "Время", "Номер телефона", "ФИО", "Номер авто", "Номер прицепа", "Груз", "Поставщик", "Вес по накладной"))
        self.tree.grid(row=1, column=2, rowspan=8, padx=10, pady=10, sticky="nsew")

        self.tree.heading("#1", text="Дата")
        self.tree.heading("#2", text="Время")
        self.tree.heading("#3", text="Номер телефона")
        self.tree.heading("#4", text="ФИО")
        self.tree.heading("#5", text="Номер авто")
        self.tree.heading("#6", text="Номер прицепа")
        self.tree.heading("#7", text="Груз")
        self.tree.heading("#8", text="Поставщик")
        self.tree.heading("#9", text="Вес по накладной")

        self.tree.bind("<ButtonRelease-1>", self.show_selected_record)

        vscroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        vscroll.grid(row=1, column=3, rowspan=8, sticky="ns")
        hscroll = ttk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)
        hscroll.grid(row=9, column=2, sticky="ew")

        self.tree.configure(yscrollcommand=vscroll.set, xscrollcommand=hscroll.set)

        self.tree.column("#1", width=80, minwidth=80, anchor="center")
        self.tree.column("#2", width=80, minwidth=80, anchor="center")
        self.tree.column("#3", width=100, minwidth=100, anchor="center")
        self.tree.column("#4", width=150, minwidth=150, anchor="center")
        self.tree.column("#5", width=120, minwidth=120, anchor="center")
        self.tree.column("#6", width=80, minwidth=80, anchor="center")
        self.tree.column("#7", width=80, minwidth=80, anchor="center")
        self.tree.column("#8", width=100, minwidth=100, anchor="center")
        self.tree.column("#9", width=150, minwidth=150, anchor="center")

        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.show_records()

    def add_record(self):
        номер_телефона = self.phone_entry.get()
        ФИО = self.name_entry.get()
        номер_авто = self.car_entry.get()
        номер_прицепа = self.trailer_entry.get()
        груз = self.cargo_var.get()
        поставщик = self.supplier_entry.get()

        вес_по_накладной_str = self.weight_entry.get()

        try:
            вес_по_накладной = float(вес_по_накладной_str)
        except ValueError:
            print("Ошибка: Вес по накладной должен быть числом.")
            return

        текущая_дата = datetime.now().date()
        текущее_время = datetime.now().time()

        table_name = self.table_var.get()
        self.cursor.execute(f'''
        INSERT INTO {table_name} (
            дата, время, `Номер_телефона`, `ФИО`, `Номер_авто`, `Номер_прицепа`, `Груз`, `Поставщик`,
            `Вес_по_накладной`
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        ''', (текущая_дата, текущее_время, номер_телефона, ФИО, номер_авто, номер_прицепа,
              груз, поставщик, вес_по_накладной))

        self.conn.commit()

        # Получите данные только что вставленной записи
        new_record = (текущая_дата, текущее_время, номер_телефона, ФИО, номер_авто, номер_прицепа,
                      груз, поставщик, вес_по_накладной)

        # Вставьте новую запись в Treeview
        self.tree.insert("", "end", values=new_record)

        # Очистите поля ввода
        self.phone_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.car_entry.delete(0, tk.END)
        self.trailer_entry.delete(0, tk.END)
        self.cargo_combobox.set("")
        self.supplier_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)

    def copy_and_delete_records(self):
        selected_items = self.tree.selection()
        if not selected_items:
            print("Выберите записи для выгрузки и удаления.")
            return

        table_name = self.table_var.get()

        for item in selected_items:
            values = self.tree.item(item, "values")
            if values:
                try:
                    unique_columns = values[2], values[4], values[6]  # Номер телефона, Номер авто, Груз
                    self.cursor.execute(
                        f"INSERT INTO выгрузка_{values[6].lower()} (Дата, Время, `Номер_телефона`, `ФИО`, `Номер_авто`, `Номер_прицепа`, `Груз`, `Поставщик`, `Вес_по_накладной`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        values)
                    self.conn.commit()

                    self.cursor.execute(f"DELETE FROM {table_name} WHERE `Номер_телефона` = %s AND `Номер_авто` = %s AND `Груз` = %s", unique_columns)
                    self.conn.commit()
                except Exception as e:
                    print(f"Ошибка при копировании и удалении записи: {e}")

                # Удаляем удаленную запись из Treeview
                self.tree.delete(item)

        # Очищаем поля ввода после удаления
        self.clear_entries()

    def clear_entries(self):
        self.phone_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.car_entry.delete(0, tk.END)
        self.trailer_entry.delete(0, tk.END)
        self.cargo_combobox.set("")
        self.supplier_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)

    def show_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        table_name = self.table_var.get()
        self.cursor.execute(f"SELECT * FROM {table_name}")
        records = self.cursor.fetchall()

        for record in records:
            self.tree.insert("", "end", values=record)

    def show_selected_record(self, event):
        self.clear_entries()

        item = self.tree.selection()
        if item:
            values = self.tree.item(item, "values")
            if values:
                if len(values) > 0:
                    self.phone_entry.insert(0, values[0])
                if len(values) > 1:
                    self.name_entry.insert(0, values[1])
                if len(values) > 2:
                    self.car_entry.insert(0, values[2])
                if len(values) > 3:
                    self.trailer_entry.insert(0, values[3])
                if len(values) > 4:
                    self.cargo_combobox.set(values[4])
                if len(values) > 5:
                    self.supplier_entry.insert(0, values[5])
                if len(values) > 6:
                    self.weight_entry.insert(0, values[6])

    def update_table(self, event):
        self.show_records()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()