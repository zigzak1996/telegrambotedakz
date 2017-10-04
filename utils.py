import shelve
from sqll import SQLighter
import config

def set_sub_menu(chat_id,id):
    db = SQLighter(config.db_name)
    sub_menu = db.select_sub_menu(id)
    db.close()
    with shelve.open(config.shelve_name) as storage:
        storage[str(chat_id)+'_'+'sub_menu'] = sub_menu

def get_sub_menu(chat_id):
    with shelve.open(config.shelve_name) as storage:
        sub_menu = storage[str(chat_id)+'_'+'sub_menu']
    return sub_menu

def set_start_eda(chat_id,s):
    with shelve.open(config.shelve_name) as storage:
        storage[str(chat_id)+'_'+'start_eda'] = s

def get_start_eda(chat_id):
    with shelve.open(config.shelve_name) as storage:
        s = storage[str(chat_id)+'_'+'start_eda']
    return s

def set_eda(chat_id,id):
    s = get_start_eda(chat_id)
    db = SQLighter(config.db_name)
    eda = db.select_eda(id,s,3)
    db.close()
    with shelve.open(config.shelve_name) as storage:
        storage[str(chat_id)+'_'+'eda'] = eda

def get_eda(chat_id):
    with shelve.open(config.shelve_name) as storage:
        eda = storage[str(chat_id)+'_'+'eda']
    return eda

def set_order(chat_id,order):
    with shelve.open(config.shelve_name) as storage:
        storage[str(chat_id)+'_'+'order'] = order

def get_order(chat_id):
    with shelve.open(config.shelve_name) as storage:
        if ((str(chat_id)+'_'+'order') not in storage):
            storage[str(chat_id)+'_'+'order'] = None
        order = storage[str(chat_id)+'_'+'order']
    return order

def set_search_eda(chat_id,order):
    with shelve.open(config.shelve_name) as storage:
        storage[str(chat_id)+'_'+'searh_eda'] = order

def get_search_eda(chat_id):
    with shelve.open(config.shelve_name) as storage:
        order = storage[str(chat_id)+'_'+'searh_eda']
    return order

def init_order(chat_id):
    db = SQLighter(config.db_name)
    count = db.all_eda()[0][0]
    db.close()
    order = []
    for i in range(count):
        order.append(0)
    set_order(chat_id,order)
