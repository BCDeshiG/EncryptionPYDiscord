import discord
import random
import os
from discord.ext import commands

keyLength = 8 # Default Key length
bot = commands.Bot(command_prefix='!', description="Encrypts text using a crappy cipher algorithm")
games = ["dont", "Phentom Pen", "Ledder clemb", "Maghrib Salah", "pleg pleg", "MoinCraph"]

# Gets bot token from file or input
if os.path.isfile("token.txt"):
    tokenFile = open("token.txt", "r")
    TOKEN = tokenFile.readline()
    tokenFile.close()
else:
    TOKEN = input("Token plez\n")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name=games[random.randint(0,len(games)-1)]))

@bot.command(name="bekfast", description="Prints something stupid")
async def bekfast(ctx):
    await ctx.send("https://www.youtube.com/watch?v=O3sndzGmfX4")

async def offset(nKeyChars, keyLength: int): # Calculates offset factor
    charSum=sum(nKeyChars) # Gets sum of ASCII values
    offsetFactor = round(charSum/keyLength) - 32
    return offsetFactor

@bot.command(name="encrypt", description="Encrypts text")
async def encrypt(ctx, *, plain): # Encrypts text
    key = ""
    nKeyChars = [None] * keyLength

    for i in range(keyLength):
        nKeyChars[i]=random.randint(33,126) # Generates a random number within ASCII range
        key += chr(nKeyChars[i]) # Casts to char then adds to end of 'key' String
    await ctx.send(embed=discord.Embed(title="Keep this key safe for decryption:", description=key))

    offsetFactor = await offset(nKeyChars, keyLength)
    cipher = [None] * len(plain) # Make cipher same length as message
    
    for i in range(len(cipher)):
        if plain[i] == ' ': # Checks for space
            cipher[i] = 32 # Adds ASCII number for space
        elif plain[i] == '\n': # Checks for new line
            cipher[i] = 10 # Adds ASCII number for new line
        else:
            ch = ord(plain[i]) + offsetFactor # Offset ASCII number
            if ch >= 127:
                ch -= 94 # Puts number within ASCII range
            cipher[i] = ch # Adds offset ASCII number to array

    # Build string from array of offset characters
    cipherText = ""
    for i in range(len(cipher)):
        cipherText += chr(cipher[i])
    await ctx.send(embed=discord.Embed(title="Encryption Complete", description=cipherText))

@bot.command(name="decrypt", description="Decrypts text")
async def decrypt(ctx, key, *, cipher): # Decrypts text
    nKeyChars = [None] * keyLength
    if len(key) != keyLength:
        # FIXME report error
        await ctx.send("Bro taht wrong key.")

    for i in range(keyLength):
        nKeyChars[i] = ord(key[i])

    offsetFactor = await offset(nKeyChars, keyLength)
    plain = [None] * len(cipher) # Make plain length same as cipher
    
    for i in range(len(plain)):
        if cipher[i] == ' ': # Checks for space
            plain[i] = 32 # Adds ASCII number for space
        elif cipher[i] == '\n': # Checks for new line
            plain[i] = 10 # Adds ASCII number for new line
        else:
            ch = ord(cipher[i]) - offsetFactor # Offset ASCII number
            if ch < 32:
                ch += 94 # Puts number within ASCII range
            plain[i] = ch # Adds offset ASCII number to array

    # Build string from array of offset characters
    plainText = ""
    for i in range(len(plain)):
        plainText += chr(plain[i])
    await ctx.send(embed=discord.Embed(title="Decryption Complete", description=plainText))

@bot.command(name="chunk", description="Chunks text")
async def chunk(ctx, *, message): # Chunks text
    alteredMessage = ""
    count = 0
    for i in range(len(message)):
        if message[i] != " ": # Checks for space
            alteredMessage += message[i] # Add character to alteredMessage
            count += 1
            if count%5==0: # If a multiple of 5
             alteredMessage += " " # Add a space
    await ctx.send(embed=discord.Embed(title="Chunking Complete", description=alteredMessage))

@bot.command(name="reroll", description="Changes random status")
async def reroll(ctx):
    await ctx.send("Rerolling Status...")
    await bot.change_presence(activity=discord.Game(name=games[random.randint(0,len(games)-1)]))

@bot.command(name="status", description="Sets bot status to whatever")
async def status(ctx, *, status):
    await ctx.send("Changing Status...")
    await bot.change_presence(activity=discord.Game(name=status))

@bot.command(name="close", description="Stops execution of program")
async def close(ctx):
    await ctx.send("Shutting down...")
    await bot.change_presence(activity=discord.Game(name="Shutting down..."))
    exit()

bot.run(TOKEN)