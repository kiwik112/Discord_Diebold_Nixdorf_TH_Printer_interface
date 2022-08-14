from asyncio.windows_events import NULL
import discord
from discord.ext import commands
import serial

sender = ""

connected = False

def tryParse(parsable) :
    try:
        int(parsable)
    except:
        return False
    return True

with open("D:/VS/Python/DiscordPrinterInterface/token.exe") as f :
    token = f.read()
client = commands.Bot(command_prefix = "🖨️ ", Intents = discord.Intents.all())

@client.event
async def on_ready():
    sender = ""
    await client.change_presence(status=discord.Status.idle, activity=discord.Streaming(name='Printa', url='https://www.youtube.com/watch?v=GO5Ch8JDBEo')) #nastavit stav 

@client.event
async def on_message(message) :
 #   if message.author != sender :
 #       await client.process_commands(message)
 #   content = message.content.split(' ')
 #   if content[0] == "🖨️" and content[1] == "print" :
 #       channel = client.get_channel(message.channel.id)
 #       await channel.send(message.content)
    await client.process_commands(message)

#CONNECT
@client.command(aliases = [ "Connect" ])
async def connect(ctx, port, baud):
    global sender
    global ser
    global connected
    if tryParse(baud) :
        if sender != "" :
            await ctx.send(":printer: is already in use.")
            return
        try:    
            ser = serial.Serial(port, baud)
        except:
            await ctx.send(f":printer: not present at { port }.")
        ser.timeout = 1
        ser.write([0x1d, 0x72, 0x01])
        status = ser.read()
        if status :
            sender = ctx.author
            await ctx.send(":printer: Connected.")
            connected = True
            ser.write([ 0x1b, 0x07 ])
            return
        await ctx.send(f":printer: not present at { port }.")
        connected = False
    else :
        await ctx.send(f":printer: { baud } is not a valid number.")

#DISCONNECT
@client.command(aliases = [ "Disconnect" ])
async def disconnect(ctx) :
    ser.close()
    global sender
    global connected
    if (sender == ctx.author or sender.id == 664420407448698881) and connected :
        sender = ""
        connected = False
        await ctx.send(":printer: disconnected.")
    else :
        await ctx.send(":printer: is not in your control.")

#GET STATUS
@client.command(aliases = [ "?" ])
async def getStatus(ctx) :
    if connected :
        ctx.send(":printer: .")
        return
    ctx.send("Not :printer: .")

#MOGUS
@client.command(aliases = [ "Mogus?", "mogus?" ])
async def mogusQuestion(ctx) :
    await ctx.send("Mogus.") #Mogus!

@client.command()
async def print(ctx, *, toPrint) :
    if connected :
        if sender == ctx.author :
            b = bytearray()
            b.extend(map(ord, toPrint))
            b.extend([ 0x0d ])
            ser.write(b)
        else :
            await ctx.send(":printer: is already in use.")
    else :
        await ctx.send(":printer: not connected.")

@client.command(aliases = [ "Cut" ])
async def cut(ctx, type) :
    if connected :
        if sender == ctx.author :
            if type == "full" :
                ser.write([ 0x19 ])
            elif type == "partial" :
                ser.write([ 0x1a ])
            else :
                await ctx.send(f"{ type } is not a valid cut type.")
        else :
            await ctx.send(":printer: is already in use.")
    else :
        await ctx.send(":printer: not connected.")

@client.command(aliases = [ "Feed" ])
async def feed(ctx) :
    if connected :
        if sender == ctx.author :
            #if tryParse(amount) :
            ser.write([ 0x14, 0x10 ])
            #else :
            #    ctx.send(f"{ amount } is not a valid number.")
        else :
            await ctx.send(":printer: is already in use.")
    else :
        await ctx.send(":printer: not connected.")
"""
@client.command(aliases = [ "Rick" ])
async def rick(ctx) :
    if connected :
        if sender == ctx.author :
            with open("D:/VS/Python/DiscordPrinterInterface/rick.bmp") as pic :
                ser.write([ 0x1b ])
                ser.write(pic)
                ser.write([ 0x1d, 0x2f, 0x00 ])
        else :
            await ctx.send(":printer: is already in use.")
    else :
        await ctx.send(":printer: not connected.")
"""



client.run(token)
