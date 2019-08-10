snd = ''
command = 'SELECT * FROM `all` WHERE 1'
cursor.execute(command)
data = cursor.fetchall()
for event in data:
    snd += event[2] + " " + event[3] + ' ' + event[4] + '\n' + event[5] + '\n' + event[7] + '\n' * 2
bot.send_message(message.chat.id, snd + 'Воть!!!')
start(message, False)

thsor = message.text
if thsor == 'Спорт':
    command = 'SELECT * FROM `theme` WHERE Спорт'
    cursor.execute(command)
    data = cursor.fetchall()
    for event in data:
        snd += event[2] + " " + event[3] + ' ' + event[4] + '\n' + event[5] + '\n' + event[7] + '\n' * 2
    bot.send_message(message.chat.id, snd)
    start(message, False)