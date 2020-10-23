import discord
import psycopg2
from datetime import datetime


class var:
    token = ''
    sub = 0
    ram = []
    ram_2 = []


con = psycopg2.connect(host='es', database='s7', user='s',
                       password='s')
cur = con.cursor()
client = discord.Client()




@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")

    if client.user.mentioned_in(message):
        msg = message.content
        msg = msg.split(' ', 1)[1]

        if 'newsong' in msg.lower().replace(' ', '') and var.sub == 0:
            await message.channel.send(f'Name your new song {message.author.mention}')
            var.ram.clear() 
            var.sub = 1

        elif var.sub == 1:
            await message.channel.send(f'Name your new lyrics {message.author.mention}')
            var.ram.append(msg.lower())
            var.sub = 2

        elif var.sub == 2:
            await message.channel.send(f'Creating {var.ram[0]} song for {message.author.mention}')
            var.ram.append(msg)
            var.sub = 0
            name = var.ram[1].split(',')
            var.ram_2.clear()
            for no,things in enumerate(name):
                var.ram_2.append(f'{things} VARCHAR(255)')
            final = str(var.ram_2).replace('[', '').replace(']', '').replace("'", "")
            cur.execute(f"DROP TABLE IF EXISTS {var.ram[0]}")
            try:
                cur.execute(f"CREATE TABLE {var.ram[0]}(id SERIAL PRIMARY KEY, {final})")
                await message.channel.send(f'Awesome {message.author.mention} your new {var.ram[0]} song created succesfully')
                con.commit()
            except Exception as sa:
                await message.channel.send(f'''{message.author.mention} an error has occured successfully
        Successfull Error:```{sa}```''')
                con.rollback()

        elif 'showplaylist' in msg.lower().replace(' ', '') and var.sub == 0:
            try:
                cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
                await message.channel.send(f'Hey {message.author.mention} these are the awesome songs in our playlist')
                var.ram.clear()
                for table in cur.fetchall():
                    var.ram.append(table[0])
                await message.channel.send(f'```{var.ram}```')
            except Exception as e:
                await message.channel.send(f'''{message.author.mention} an error has occured successfully
                        Successfull Error:```{e}```''')
                con.rollback()

            
        elif 'deletetable' in msg.lower().replace(' ', '') and var.sub == 0:
            try:
                await message.channel.send(f'Deleting {msg.split()[2]} song')
                cur.execute(f"DROP TABLE {msg.split()[2]}")
                await message.channel.send(f"{message.author.mention} The {msg.split()[2]} song deleted successfully")
            except Exception as ab:
                await message.channel.send(f'''{message.author.mention} an error has occured successfully
                        Successfull Error:```{ab}```''')
                con.rollback()

        elif 'newbeat' in msg.lower().replace(' ', '') and var.sub == 0:
             await message.channel.send(f'Enter the song name {message.author.mention}')
             var.sub=4

        elif var.sub == 4:
            var.ram.clear()
            var.ram.append(msg)
            var.sub = 5
            await message.channel.send(f"Enter the {msg}'s lyrics values {message.author.mention}")

        elif var.sub == 5:
            var.sub=0                        
            cur.execute(f"Select * FROM {var.ram[0]} LIMIT 0")
            colnames = [desc[0] for desc in cur.description]
            colnames = str(colnames[1:]).replace("'",'').replace('[','').replace(']','')
            values = msg.split(',')
            for things in values:
                var.ram.append(things)       
            try:
                res = str(var.ram[1:])[1:-1]
                cur.execute(f"INSERT INTO {var.ram[0]}({colnames}) VALUES({res})")
                con.commit()
                await message.channel.send(f'{message.author.mention} {var.ram[0]} has updated successfully')
            except Exception as e:
                await message.channel.send(f'''{message.author.mention} an error has occured successfully
        Successfull Error:```{e}```''')
                con.rollback()
                
        elif 'showtable' in msg.lower().replace(' ', '') and var.sub == 0:
            try:
                cur.execute(f'''SELECT * from {msg.replace(' ','').replace('show','').replace('table','')}''')
                result = cur.fetchall();
                await message.channel.send(f'''{message.author.mention} These are our lyrics
```{result}```''')
            except Exception as e:
                await message.channel.send(f'''{message.author.mention} an error has occured successfully
                        Successfull Error:```{e}```''')
                con.rollback()


        elif 'rollback' in msg.lower().replace(' ', '') and var.sub == 0:
            con.rollback()
            await message.channel.send(f'{message.author.mention} roll backed')

        elif 'showcolumn' in msg.lower().replace(' ', '') and var.sub == 0:
            cur.execute(f"Select * FROM {msg.replace(' ','').replace('show','').replace('column','')} LIMIT 0")
            colnames = [desc[0] for desc in cur.description]
            await message.channel.send(f'''{message.author.mention} These are the tables from {msg.replace(' ','').replace('show','').replace('column','')}
```{colnames}```''')

        elif 'deletebeat' in msg.lower().replace(' ', '') and var.sub == 0:
            await message.channel.send(f'{message.author.mention} Enter song name')
            var.sub=7
            var.ram.clear()
        elif var.sub == 7:
            await message.channel.send(f'{message.author.mention} Enter the id value')
            var.sub = 8
            var.ram.append(msg)
        elif var.sub == 8:
            var.ram.append(msg)
            var.sub = 0
            try:
                await message.channel.send(f"Deleting {var.ram[0]}'s beat")
                cur.execute(f"DELETE FROM {var.ram[0]} where id = {int(var.ram[1])}")
                con.commit()
                await message.channel.send(f"{message.author.mention} The {var.ram[0]} beat deleted successfully")

            except Exception as e:
                await message.channel.send(f'''{message.author.mention} an error has occured successfully
                        Successfull Error:```{e}```''')
                con.rollback()
        elif 'calculate' in msg.lower().replace(' ', '') and var.sub == 0:
            msg = msg.lower().replace('calculate','').replace(' ','')
            
            try:
                total=0
                var.sub=0
                if '+' in msg:
                    msg = msg.replace('+', ' ')
                    msg = msg.split()
                    for ele in range(0, len(msg)):
                        total = total + int(msg[ele])
                    await message.channel.send(f'{message.author.mention} Answer is : {total}')
                elif '-' in msg:
                    msg = msg.replace('-', ' ')
                    msg = msg.split()
                    total = int(msg[0]) - int(msg[1])
                    await message.channel.send(f'{message.author.mention} Answer is : {total}')
                elif '*' in msg:
                    msg = msg.replace('*', ' ')
                    msg = msg.split()
                    total = int(msg[0]) * int(msg[1])
                    await message.channel.send(f'{message.author.mention} Answer is : {total}')
                elif '/' in msg:
                    msg = msg.replace('/', ' ')
                    msg = msg.split()
                    total = int(msg[0]) / int(msg[1])
                    await message.channel.send(f'{message.author.mention} Answer is : {total}')
               
            except Exception as e:
                await message.channel.send(f'''{message.author.mention} an error has occured successfully
                                        Successfull Error:```{e}```''')
                var.sub=0
        elif 'help' in msg.lower().replace(' ', '') and var.sub == 0:
             await message.channel.send('''```
new song - To create new table
new beat - To insert values to table
show playlist - To show all tables
show table <TABLENAME> - To show particular table values
show column <TABLENAME> - To show column of particular table
delete table <TABLENAME> - To delete particular table
delete beat - To delete particular values with id in table
calculate <PROBLEM> - It finds the answer for it
roll back - To rollback to previous state
```
''')
            

client.run(var.token)
con.close()
