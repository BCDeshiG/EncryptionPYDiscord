import discord, random, json, os
from discord.ext import commands

# Makes new prefix json file
try:
	open("prefixes.json","x")
	open("prefixes.json","w").write("{}")
	print("Prefixes.json created, used to store per server prefixes.\n")
except:
	print("Prefixes.json already exists or was unable to be created.\n")

# Gets bot prefix from file
with open("prefixes.json","r") as f:
	prefixes = json.load(f)
defaultPrefix = "e!"

def prefix(bot, message):
	return str(prefixes.get(str(message.guild.id), defaultPrefix)) if message.guild != None else defaultPrefix

keyLength = 8 # Default Key length
bot = commands.Bot(command_prefix=prefix, description="Encrypts text using a crappy cipher algorithm")
bot.help_message = bot.description
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
	print('---------------------------------------')
	print('Logged in as:')
	print(bot.user.name)
	print(bot.user.id)
	print('---------------------------------------')
	await bot.change_presence(activity=discord.Game(name=games[random.randint(0,len(games)-1)]))

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("Command not found")
		return

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
	# FIXME Remove discord formatting from key
	test = key.replace('```', '\`\`\`')
	if test != key:
		key = test
	key = "```" + key + "```"
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
			# FIXME Test unicode
			while ch >= 127 and ch <= 159: # Make sure it doesn't become a unicode control character
				ch += offsetFactor
			cipher[i] = ch # Adds offset ASCII number to array

	# Build string from array of offset characters
	cipherText = ""
	for i in range(len(cipher)):
		cipherText += chr(cipher[i])
	
	# FIXME Remove discord formatting from encrypted string
	test = cipherText.replace('```', '\`\`\`')
	if test != cipherText:
		cipherText = test
	cipherText = "```" + cipherText + "```"
	await ctx.send(embed=discord.Embed(title="Encryption Complete", description=cipherText))

@bot.command(name="decrypt", description="Decrypts text")
async def decrypt(ctx, *, args): # Decrypts text
	# Parse arguments
	argsArr = args.split(' ', 1)
	if len(argsArr) < 2:
		await ctx.send("Usage: `" + prefixes[str(ctx.guild.id)] + "decrypt <key> <text>` (Make sure there's no new line)")
		return

	nKeyChars = [None] * keyLength
	key = args.split()[0]
	cipher = args.split(' ', 1)[1]
	if len(key) != keyLength:
		await ctx.send("Invalid key length, key must be " + str(keyLength) + " characters long.")
		return

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
			#FIXME Test unicode
			while ch >= 127 and ch <= 159: # Make sure it doesn't become a unicode control character
				ch -= offsetFactor
			plain[i] = ch # Adds offset ASCII number to array

	# Build string from array of offset characters
	plainText = ""
	for i in range(len(plain)):
		plainText += chr(plain[i])
	
	# FIXME Remove discord formatting from encrypted string
	plainText = "```" + plainText + "```"
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

@bot.command(name="setprefix", description="Changes bot prefix for this server")
async def setprefix(ctx, prefixToBeSet):
	prefixes[str(ctx.guild.id)] = prefixToBeSet
	await ctx.send("Prefix for {} set to `{}`".format(ctx.guild.name,prefixToBeSet))
	with open("prefixes.json","w") as f:
		f.write(str(json.dumps(prefixes)))
		f.flush()

@bot.command(name="echo", description="Prints message")
async def echo(ctx, *, message):
	await ctx.send(message)

@bot.command(name="close", description="Stops execution of program")
async def close(ctx):
	await ctx.send("Shutting down...")
	await bot.change_presence(activity=discord.Game(name="Shutting down..."))
	exit()

bot.run(TOKEN)