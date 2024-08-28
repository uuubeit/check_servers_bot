
import telebot
from telebot import types
from writer_reader import fileManager
from checker import sshManager 
import time


bot=telebot.TeleBot('BOT_API')
chatId= 000000
fileMn=fileManager()
sshMn=sshManager(bot)

mainMessage=None
secondMessages=[]
errorMessage=None


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id ==chatId:
        delMessages('second')
        sshMn.setEditer(showGoodHosts,showBadHosts,polligMessages)
        try:
            sshMn.start()
            setMessages('main',bot.send_message(chatId,text= '<code>'+'Server polling...'+'</code>',parse_mode='html'))
        except Exception:
            setMessages('main',bot.send_message(chatId,text= '<code>'+'Server polling...'+'</code>',parse_mode='html'))
            sshMn.checkAllHost()

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call): 
    if getMessages('main') != None:
        if call.data == 'addHost':        
            msg=setMessages('second',bot.send_message(call.message.chat.id,'Enter the data in the format: name/ip/user/password'))
            bot.register_next_step_handler(msg,addHost)

        elif call.data == 'showHost':
            sshMn.checkAllHost()
    else:
        msg=setMessages('second',bot.send_message(call.message.chat.id,'Please enter /start'))


#   FUNCTIONS
def polligMessages():
    main=getMessages('main')
    if  main != None and main.text!='Server polling...':
        setMessages('main',bot.edit_message_text(chat_id= chatId,message_id= main.id,text= '<code>'+'Server polling...'+'</code>',parse_mode='html'))
    if getMessages('error')!=None:
        bot.delete_message(chatId,getMessages('error').id)
        setMessages('error',None)

def showGoodHosts(availHosts=[]):
    line='✅ Available hosts:\n'
    for host in availHosts:
        line+=host[0]+' '*(15-len(host[0]))+host[1]+'\n'
    line+=f'Number of available hosts: {len(availHosts)}'
    
    markup=types.InlineKeyboardMarkup()
    showButton=types.InlineKeyboardButton(text='Update hosts',callback_data='showHost')
    addButton=types.InlineKeyboardButton(text='Add hosts',callback_data='addHost')
    markup.add(addButton,showButton)
    try:
        setMessages('main',bot.edit_message_text(chat_id= chatId,message_id= getMessages('main').id,text= '<code>'+line+'</code>',parse_mode='html', reply_markup=markup))
    except Exception:
        setMessages('main',bot.send_message(chatId,text= '<code>'+line+'</code>',parse_mode='html', reply_markup=markup))


def showBadHosts(unavailHosts=[]):
    errorMessage=getMessages('error')
    if len(unavailHosts) != 0:
        line='❌ Unavailable hosts:\n'
        for host in unavailHosts:
            line+=host[0]+' '*(15-len(host[0]))+host[1]+'\n'
        if errorMessage == None:
            setMessages('error', bot.send_message(chat_id=chatId, text="<code>" + line + "</code>", parse_mode="html"))
        else:
            setMessages('error',bot.edit_message_text(chat_id=chatId, message_id=getMessages('error').id, text="<code>" + line + "</code>", parse_mode="html"))
    else:
        if errorMessage !=None:
            bot.delete_message(chatId,errorMessage.id)
            setMessages('error',None)



#   UTILITY
def getMessages(name=str):
    global mainMessage,secondMessages,errorMessage
    if name == 'main':
        return mainMessage
    elif name=='second':
        return secondMessages
    elif name=='error':
        return errorMessage
    
def setMessages(name=str,msg=types.Message):
    global mainMessage,secondMessages,errorMessage
    if name == 'main':
        mainMessage = msg
    elif name=='second':
        secondMessages.append(msg)
    elif name=='error':
        errorMessage = msg
    return msg
    
def addHost(message):
    if fileMn.addHost(message.text):
        setMessages('second',bot.send_message(chatId,'Complete'))
        time.sleep(1)
    else: 
        setMessages('second',bot.send_message(chatId,'Error'))
        time.sleep(1)
    delMessages('second')

def delMessages(name=str):  
    if name == 'main':
        bot.delete_message(chatId,getMessages('main').id)

    elif name == 'second':
        listMsg=getMessages('second')
        for message in listMsg:
            bot.delete_message(chatId,message.id)
        global secondMessages
        secondMessages=[]

    elif name ==' error':
        bot.delete_message(chatId,getMessages('error').id)
        global errorMessages
        errorMessages=None  


bot.infinity_polling()
   

