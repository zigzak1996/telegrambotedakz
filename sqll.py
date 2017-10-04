import sqlite3

# ДБ eda
# Таблицы eda, kitchen, subkitchen
class SQLighter:
    # Инициализация дб
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    # Список кухни с дб
    def select_menu(self):
        with self.connection:
            return self.cursor.execute('Select * from kitchen').fetchall()
    # Список под кухни выбранной кухни
    def select_sub_menu(self,id): # id - кухни
        with self.connection:
            return self.cursor.execute('Select * from subkitchen where kitchen_id='+str(id)).fetchall()
    # Список еды выбранной под кухни
    def select_eda(self,id,s,f): # id - под кухни, s - позиция начала, f - сколько вытащить
        with self.connection:
            return self.cursor.execute('Select * from eda where '+str(id)+'=subkitchen_id limit '+str(s)+','+str(f)).fetchall()

    def select_only_one_eda(self,id):
        with self.connection:
            return self.cursor.execute('Select * from eda where '+str(id)+'=id').fetchall()

    def select_all_eda(self):
        with self.connection:
            return self.cursor.execute('Select * from eda').fetchall()

    def all_eda(self):
        with self.connection:
            return self.cursor.execute('Select count(*) from eda').fetchall()

    def get_search_eda(self,q):
        with self.connection:
            return self.cursor.execute('select * from eda where '+q).fetchall()
    # Выключаем конект к ДБ
    def close(self):
        self.connection.close()
