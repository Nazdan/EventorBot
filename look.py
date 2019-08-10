snd = ''
command = 'SELECT * FROM all'
cursor.execute(command)
data = cursor.fetchall()
for event in data:
    snd += event[2] + " " + event[3] + ' ' + event[4] + '\n' + event[5] + '\n' + event[7] + '\n'*2
bot.send.message(message.chat.id, snd)

