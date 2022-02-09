file = open("blacklist.automod", "r")
global blacklist
global OUTCHANNEL
global ROLE
blacklistraw = file.readlines()
blacklist = []
for item in blacklistraw:
    blacklist.append(item)
file.close()
active = "inactive"

import nest_asyncio
nest_asyncio.apply()

import discord

#ENV VARS

TOKEN = 'TOKEN HERE'
GUILD = 'SERVER NAME HERE'
ROLE = "MOD ROLE HERE"

#/ENV VARS

client = discord.Client()

@client.event
async def on_ready():
    
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print ("Bot is READY!")
    
@client.event
async def on_message(message):
    role = discord.utils.find(lambda r: r.name == ROLE, message.guild.roles)
    global active
    file = open("channel.automod", "r")
    channelno = int(file.read())
    file.close()
    OUTCHANNEL = client.get_channel(channelno)
    if message.author == client.user:
        return
    
    if message.content == "automod status" and role in message.author.roles:
        response1 = "Automod is online and " + active
        await OUTCHANNEL.send(response1)
        return
    
    if message.content == "automod start" and role in message.author.roles:
        active = "active"
        response1 = "Automod has been activated"
        await OUTCHANNEL.send(response1)
        return
    
    if message.content == "automod stop" and role in message.author.roles:
        active = "inactive"
        response1 = "Automod has been deactivated"
        await OUTCHANNEL.send(response1)
        return
    
    if message.content == "automod blacklist list" and role in message.author.roles:
        tempstr = "The current word blacklist is as follows: ```"
        for item in blacklist:
            tempstr = tempstr + "\n" + item
        tempstr = tempstr + "```"
        await OUTCHANNEL.send(tempstr)
        return
    
    if "automod blacklist add" in message.content and role in message.author.roles:
        file = open("blacklist.automod", "w")
        file.write("")
        file.close()
        file = open("blacklist.automod", "a")
        blacklist.append(str(message.content)[22:]+"\n")
        for item in blacklist:
            file.write(item)
        file.close()
        await OUTCHANNEL.send("Item ```" + str(message.content)[22:] + "\n" + "``` successfully added to bot blacklist")
        return
    
    if "automod blacklist remove" in message.content and role in message.author.roles:
        testo = str(message.content)[25:]+"\n"
        blacklist.remove(testo)
        file = open("blacklist.automod", "w")
        file.write("")
        file.close()
        file = open("blacklist.automod", "a")
        for item in blacklist:
            file.write(item)
        file.close()
        await OUTCHANNEL.send("Item ```" + str(message.content)[25:] + "``` successfully removed from bot blacklist")
        return
    
    if message.content == "automod set channel" and role in message.author.roles:
        file = open("channel.automod","w")
        file.write(str(message.channel.id))
        file.close()
        file = open("channel.automod", "r")
        channelno = int(file.read())
        file.close()
        OUTCHANNEL = client.get_channel(channelno)
        await OUTCHANNEL.send("Automod channel successfully set to this channel.")
        return
    
    if message.content == "automod help" and role in message.author.roles:
        tempstr = "__**Azriel's Amazing Automod help**__\nAzriel's Amazing Automod bot was created in one sitting of 5 hours. Azriel got hyperfixated on it and forgot to do their homework.\n__Command list:__\n-** automod status**: checks status of the bot\n- **automod start**: starts automod monitoring. Note that this is turned off by default.\n- **automod stop**: the opposite of automod start.\n- **automod blacklist list**: lists all words which are flagged in a message. *WARNING: since there is profanity which is to be flagged, this message will return a list of mostly profanity. If you think you may be triggered by some of these, do not use this command.*\n- **automod blacklist add *word***: adds *word* to the blacklist.\n- **automod blacklist remove *word***: removes *word* from the blacklist.\n- **automod set channel**: sets the output channel of the automod bot to the current channel.\n- **automod help**: returns this menu."
        await OUTCHANNEL.send(tempstr)
        return
                
    for item in blacklist:
        temp = item[0:(len(item)-2)]
        if temp.lower() in str(message.content).lower() and active == "active":
            response1 = "__**#### MESSAGE FLAGGED ####**__" + "\n__User:__" + "\n> " + str(message.author) + "\n__Channel:__" + "\n> " + str(message.channel) + "\n__Message:__" + "\n>>> " + str(message.content)
            await OUTCHANNEL.send(response1)
            return
            

client.run(TOKEN)

