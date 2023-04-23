import discord
import os
import random
import rsiDocRe
from datetime import datetime, timedelta 

intents = discord.Intents.all()
#intents.message_content = True

client = discord.Client(intents=intents)
file = open("quotes.txt","r")
file1 = file.readlines()


@client.event
async def on_ready():
    print('Fired up and ready to serve as {0.user}'.format(client))
   

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')

    if message.content.startswith("$commands"):
        await message.channel.send("rsi: acronym")
        await message.channel.send("quote: return random motivational quote")
    if message.content.startswith('$rsi'):
        params = str(message.content).split(" ")
        rsiNum = rsiDocRe.rsi(params[1],(datetime.now() - timedelta(365)).strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d"))
        file = discord.File("rsiPlot.png", filename="rsiPlot.png")
        await message.channel.send(file=file)
        await message.channel.send(f"Current RSI: {rsiNum}")
      
    if message.content.startswith("$quote"):
        await message.channel.send(file1[random.randint(0,100)])

try:
    client.run(os.environ['TOKEN'])
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system("python restarter.py")
    os.system('kill 1')