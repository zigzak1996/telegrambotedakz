from sqll import SQLighter
import config
import telebot
import os
import utils
import re


bot = telebot.TeleBot(config.token)

print(bot.get_me())
db = SQLighter(config.db_name)
menu = db.select_menu()

sub_menu = []
eda = []
eda_id = 0
db.close()
def log(message):
    print('\n-------')
    print('Text: {0}'.format(message.text))

# Стартовое меню
@bot.message_handler(commands=['start'])
def handle_start(message):
    if utils.get_order(message.from_user.id) is None or len(utils.get_order(message.from_user.id))<4:
        utils.init_order(message.from_user.id)
    print (utils.get_order(message.from_user.id))
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row(u'Меню \U0001f374', u'Корзина \U0001f4e6')
    user_markup.row(u'Поиск \U0001f50d', u'Обратная связь \U00002709')
    bot.send_message(message.from_user.id, 'Добро пожаловать',reply_markup=user_markup)

@bot.message_handler(commands=['search'])
def handle_search(message):
#try:
    text = message.text.split("/search ")
    text = text[1].split(", ")
    query=""
    z=0
    for i in range(len(text)):
        if(text[i]=="" or text[i] is None):
            continue
        if(z==0):
            query+="name='"+text[i]+"' or description='"+text[i]+"' "
        else :
            query+="or name='"+text[i]+"' or description='"+text[i]+"' "
    db = SQLighter(config.db_name)
    eda = db.get_search_eda(query)
    db.close()
    print(eda)
    if eda==[]:
        bot.send_message(message.from_user.id,"poshlo vse k chertyam")
        return
    utils.set_search_eda(message.from_user.id,eda)
    id = 0
    n = min(3,len(eda)-id)
    directory='sets/'
    for file,i in zip(eda[id:id+n],range(n)):
        keyboard = telebot.types.InlineKeyboardMarkup()
        cost_button = telebot.types.InlineKeyboardButton(text="Цена: " + str(file[3]), callback_data="addToBuscket"+str(file[0]))
        img = open(directory + '/' + file[-1], 'rb')
        bot.send_chat_action(message.from_user.id, 'upload_photo')
        keyboard.add(cost_button)
        # под конец добавляю кнопку 'еще'
        if i == n-1:
            more_button = telebot.types.InlineKeyboardButton(text=u"Еще", callback_data="moreSearchBuscket"+str(id))
            keyboard.add(more_button)
        bot.send_photo(message.from_user.id, img, caption=file[1]+'\n'+ file[-2]+'\n',reply_markup=keyboard)
        img.close()


#except:
#    bot.send_message(message.from_user.id,"Правильно пиши через запятую с пробелом и впереди /search")


# Работа иннлайн клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        # кнопка 'еще' добавление еды
        if u'moreSearchBuscket' in call.data:
            id = 0
            res = 1
            i = -1
            # вытаскиваю id с сообщения какую еду смотрю
            while call.data[i]!='t':
                id += int(call.data[i]) * res
                res*=10
                i -= 1
            print(id)
            id+=3
            utils.set_start_eda(call.from_user.id,id)
            eda = utils.get_search_eda(call.from_user.id)
            n = min(3,len(eda)-id)
            directory='sets/'
            if eda == []: # Если еды нету
                bot.send_message(call.from_user.id,'Oblomis edy netu')
                return
            if n == 0: # Если еды нету
                bot.send_message(call.from_user.id,'Oblomis edy netu')
                return
            print(eda)
            for file,i in zip(eda[id:id+n],range(n)):
                keyboard = telebot.types.InlineKeyboardMarkup()
                cost_button = telebot.types.InlineKeyboardButton(text="Цена: " + str(file[3]), callback_data="addToBuscket"+str(file[0]))
                img = open(directory + '/' + file[-1], 'rb')
                bot.send_chat_action(call.from_user.id, 'upload_photo')
                keyboard.add(cost_button)
                # под конец добавляю кнопку 'еще'
                if i == n-1:
                    more_button = telebot.types.InlineKeyboardButton(text=u"Еще", callback_data="moreSearchBuscket"+str(id))
                    keyboard.add(more_button)
                bot.send_photo(call.from_user.id, img, caption=file[1]+'\n'+ file[-2]+'\n',reply_markup=keyboard)
                img.close()

        elif u'moreToBuscket' in call.data:
            id = 0
            res = 1
            i = -1
            # вытаскиваю id с сообщения какую еду смотрю
            while call.data[i]!='t':
                id += int(call.data[i]) * res
                res*=10
                i -= 1
            print(id)
            eda_id = utils.get_start_eda(call.from_user.id)
            utils.set_eda(call.from_user.id,id)
            eda = utils.get_eda(call.from_user.id)
            if eda == []: # Если еды нету
                bot.send_message(call.from_user.id,'Oblomis edy netu')
                return
            eda_id += 3
            utils.set_start_eda(call.from_user.id,eda_id)
            directory = 'sets/'
            # Передаем клиенту
            keyboard = telebot.types.InlineKeyboardMarkup()
            for file,i in zip(eda,range(len(eda))):
                keyboard = telebot.types.InlineKeyboardMarkup()
                cost_button = telebot.types.InlineKeyboardButton(text="Цена: " + str(file[3]), callback_data="addToBuscket"+str(file[0]))
                img = open(directory + '/' + file[-1], 'rb')
                bot.send_chat_action(call.from_user.id, 'upload_photo')
                keyboard.add(cost_button)
                # под конец добавляю кнопку 'еще'
                if i == len(eda)-1:
                    more_button = telebot.types.InlineKeyboardButton(text=u"Еще", callback_data="moreToBuscket"+str(id))
                    keyboard.add(more_button)
                bot.send_photo(call.from_user.id, img, caption=file[1]+'\n'+ file[-2]+'\n',reply_markup=keyboard)
                img.close()
        elif "addToBuscket" in call.data:
            id = 0
            res = 1
            i = -1

            while call.data[i]!='t':
                id += int(call.data[i])*res
                res *= 10
                i -= 1
            order = utils.get_order(call.from_user.id)
            order[id-1] +=1
            utils.set_order(call.from_user.id,order)
            print(id)
            print(order)
        elif "orderInBuscket" in call.data:
            id = 0
            res = 1
            i = -1

            while call.data[i]!='+' and call.data[i]!='-':
                id += int(call.data[i])*res
                res *= 10
                i -= 1
            order = utils.get_order(call.from_user.id)
            if ('+' in call.data) :
                order[id-1] += 1
                i = len(call.message.caption) - 1
                res = 1
                idd = 0
                while call.message.caption[i]>='0' and call.message.caption[i]<='9':
                    idd += int(call.message.caption[i]) * res
                    res*=10
                    i -= 1

                keyboard = telebot.types.InlineKeyboardMarkup()

                plus = telebot.types.InlineKeyboardButton(text="+", callback_data="orderInBuscket+"+str(id))
                minus = telebot.types.InlineKeyboardButton(text="-", callback_data="orderInBuscket-"+str(id))
                keyboard.add(plus)
                keyboard.add(minus)

                bot.edit_message_caption(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            caption=call.message.caption[:i+1]+str(idd+1),
                                            reply_markup=keyboard)
            elif ('-' in call.data) and (order[id-1]>0) :
                order[id-1] -= 1

                i = len(call.message.caption) - 1
                res = 1
                idd = 0
                while call.message.caption[i]>='0' and call.message.caption[i]<='9':
                    idd += int(call.message.caption[i]) * res
                    res*=10
                    i -= 1
                print(call.message.caption)
                print(call.message.chat)
                keyboard = telebot.types.InlineKeyboardMarkup()

                plus = telebot.types.InlineKeyboardButton(text="+", callback_data="orderInBuscket+"+str(id))
                minus = telebot.types.InlineKeyboardButton(text="-", callback_data="orderInBuscket-"+str(id))
                keyboard.add(plus)
                keyboard.add(minus)

                bot.edit_message_caption(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            caption=call.message.caption[:i+1]+str(idd-1),
                                            reply_markup=keyboard)
                print(call.message.caption)


            print(order)
            utils.set_order(call.from_user.id,order)




@bot.message_handler(content_types=['text'])
def handle_keybord(message):
    if message.text == 'Назад':
        handle_start(message)

    if message.text == u'Поиск \U0001f50d':
        bot.send_message(message.from_user.id,u"ведите команду /search и через запятую")

    if message.text == u'Обратная связь \U00002709':
        bot.send_message(message.from_user.id,"Главный повар - Асанали: +77022618888\nРазРаб - Анатолий: +77781669223\nUX/UI - Ербол: +77021113438\nПосыльник- Райымбек: +77080666001\nPudge - Диас: +77470344368\nВо всем виноват Камалхан: +77022148010\nБухгалтер Бекжан: +77751422212")

    if message.text == u'Меню \U0001f374':
        # Выдаю список кухни
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        for i in range(1,len(menu),2):
            user_markup.row(u''+menu[i-1][1],u''+menu[i][1])

        # если менюшка нечетной длины добавляю последний в списке
        if len(menu)%2==1:
            user_markup.row(menu[-1][1],'Назад')
        # иначе просто 'назад'
        else :
            user_markup.row('Назад')
        bot.send_message(message.from_user.id, 'Меню', reply_markup=user_markup)
        return
    # из кухни вытаскиваю подкухни
    for i in range(len(menu)):
        # нашли что хотели из меню и теперь выдаем список из подкухни
        print(menu[i][1],message.text)
        if menu[i][1] == message.text:
            utils.set_sub_menu(message.from_user.id,menu[i][0])
            sub_menu = utils.get_sub_menu(message.from_user.id)

            user_markup = telebot.types.ReplyKeyboardMarkup(True)
            for j in range(1,len(sub_menu),2):
                user_markup.row(u''+sub_menu[j-1][1],u''+sub_menu[j][1])
            # если менюшка нечетной длины добавляю последний в списке
            if len(menu)%2==1:
                user_markup.row(menu[-1][1],'Назад')
            # иначе просто 'назад'
            else :
                user_markup.row('Назад')
            bot.send_message(message.from_user.id, menu[i][1], reply_markup=user_markup)
            return
    sub_menu = utils.get_sub_menu(message.from_user.id)
    # print(sub_menu)
    for i in range(len(sub_menu)):
        # нашли из под кухни выдаем список еды
        if sub_menu[i][1] == message.text:
            utils.set_start_eda(message.from_user.id, 0)
            eda_id = utils.get_start_eda(message.from_user.id)
            utils.set_eda(message.from_user.id, sub_menu[i][0])
            eda = utils.get_eda(message.from_user.id) # Запрос на еду
            if eda == []: # Если еды нету
                bot.send_message(call.from_user.id,'Oblomis edy netu')
                return
            eda_id += 3
            utils.set_start_eda(message.from_user.id,eda_id)
            directory = 'sets/'
            # Передаем клиенту
            for file,j in zip(eda,range(len(eda))):
                keyboard = telebot.types.InlineKeyboardMarkup()
                cost_button = telebot.types.InlineKeyboardButton(text="Цена: " + str(file[3]), callback_data="addToBuscket"+str(file[0]))
                img = open(directory + '/' + file[-1], 'rb')
                bot.send_chat_action(message.from_user.id, 'upload_photo')
                keyboard.add(cost_button)
                # под конец добавляем кнопку `еще`
                if j == len(eda)-1:
                    more_button = telebot.types.InlineKeyboardButton(text=u"Еще", callback_data="moreToBuscket"+str(sub_menu[i][0]))
                    keyboard.add(more_button)
                bot.send_photo(message.from_user.id, img, caption=file[1]+'\n'+ file[-2]+'\n',reply_markup=keyboard)
                img.close()


    if message.text == u'Корзина \U0001f4e6':
        user_markup = telebot.types.ReplyKeyboardMarkup(True)
        user_markup.row(u'Оформить заказ \U0001F4CC')
        user_markup.row('Назад')
        order = utils.get_order(message.from_user.id)
        directory = 'sets'
        for i in range(len(order)):
            if order[i]>0:
                db = SQLighter(config.db_name)
                file = list(db.select_only_one_eda(i+1)[0])
                db.close()
                keyboard = telebot.types.InlineKeyboardMarkup()

                plus = telebot.types.InlineKeyboardButton(text="+", callback_data="orderInBuscket+"+str(i+1))
                minus = telebot.types.InlineKeyboardButton(text="-", callback_data="orderInBuscket-"+str(i+1))

                img = open(directory + '/' + file[-1], 'rb')
                bot.send_chat_action(message.from_user.id, 'upload_photo')
                keyboard.add(plus)
                keyboard.add(minus)
                # под конец добавляем кнопку `еще`
                bot.send_photo(message.from_user.id, img, caption=file[1]+'\n'+ file[-2]+'\n'+str(order[i]),reply_markup=keyboard)
                img.close()
        bot.send_message(message.from_user.id, 'Ваш заказ', reply_markup=user_markup)



    if message.text == u'Оформить заказ \U0001F4CC':
        hide_markup = telebot.types.ReplyKeyboardRemove()
        order = utils.get_order(message.from_user.id)
        db = SQLighter(config.db_name)
        eda = db.select_all_eda()
        db.close()
        summ = 0
        for i in range(len(order)):
            summ += order[i] * eda[i][3]

        bot.send_message(message.from_user.id,'Общая сумма: '+str(summ), reply_markup=hide_markup)
        bot.send_message(message.from_user.id,'Введите ваше (имя, Адрес доставки, Телефон). Если самовывоз так и напишите', reply_markup=hide_markup)


    if ',' in message.text:
        order = utils.get_order(message.from_user.id)
        s = ''
        summ = 0
        for i in range(len(order)):
            if order[i] > 0:
                db = SQLighter(config.db_name)
                a = list(db.select_only_one_eda(i+1)[0])
                db.close()
                s += a[1] + ' x'+str(order[i])+', '
                summ += a[3] * order[i]
        bot.send_message(message.from_user.id,'Ваш Заказ Оформлен. Скора вам перезвонят')
        bot.send_message(206708384,'Заказ: '+s[:len(s)-1]+str(summ)+'\n'+ message.text)
        bot.send_message(101041293,'Заказ: '+s[:len(s)-1]+str(summ)+'\n'+ message.text)
        utils.set_order(message.from_user.id,None)





@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "pizza":
            directory = '/Users/Assanali/Desktop/telegramBot/pizza'
            all_files = os.listdir(directory)
            for file in all_files:
                img = open(directory+'/'+file,'rb')






bot.polling(none_stop=True)
