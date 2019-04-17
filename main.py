import discord, logging, json
from discord.ext import commands
from profanity import profanity
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment
import asyncio, math
# Requirements: discord.py, tinydb, profanity

# Define all variables to be used around the script
description = '''Bot description here'''
bot = commands.Bot(command_prefix='~',description=description)
db = TinyDB('data.json')
Users = Query()










@bot.event
async def on_ready():
    print('Bot is ready for use')

# Print the starting text
print('By Fbi_ShortMicrobe354_TrickShot (all same person ;>')
print('Better get my dev role fucker')
print('Bot is now ready')
print('prefix ~ Have fun!')

# Setup basic logging for the bot
logging.basicConfig(level=logging.WARNING)


bot.remove_command('help')


@bot.command(pass_context = True, name = 'Help', aliases=['help'])
async def Help(ctx):
  author = ctx.message.author                           	
  embed = discord.Embed(description="MetroPvP's Commands", color=0x157696, inline=True)
  embed.add_field(name="Here", value="Makes sure bot is here!", inline=False)
  embed.add_field(name="Sc", value="Gives Member count and Bot count", inline=False)
  embed.add_field(name="Info", value="Gives info about MetroPvP!", inline=False)
  embed.add_field(name="Vote", value="Gives vote link for MetroPvP!", inline=False)
  embed.add_field(name="Ip", value="Sends server ip!", inline=False)
  embed.add_field(name="Purge", value="Deletes Chat messages!", inline=False)
  embed.add_field(name="Kick", value="Kicks player!", inline=False)
  embed.add_field(name="Ban", value="Bans Player!", inline=False)
  embed.add_field(name="strike", value="Gives player a strike!", inline=False)
  await bot.say(embed=embed) 

@bot.command(pass_context = True, name = 'Ip', aliases=['ip'])
async def Ip(ctx):
  embed = discord.Embed(description="mpvp.nbb.wtf", color=0x157696, inline=True)
  await bot.say(embed=embed)




@bot.command(pass_context=True, name = 'Here', aliases=['here'])
async def Here():
   embed = discord.Embed(description="**I'm here!**", color=0x157696, inline=True)
   await bot.say(embed=embed)


@bot.command(pass_context = True, name = 'Vote', aliases=['vote'])
async def Vote(ctx):
  """Gives server vote link"""
  embed = discord.Embed(description="mcpe.guru/8g6w2r", color=0x157696, inline=True)
  await bot.say(embed=embed)


@bot.command(pass_context = True, name = 'Info', aliases=['info'])
async def Info(ctx):
  embed = discord.Embed(description="**MetroPvP is a Factions based MCPE server. It is Mythologically themed mixed with a futuristic space theme. We strive to be unique and become the #1 server of MCPE. We are aware that we aren't the biggest community, yet that does not mean we won't expand and update all the time. We would like to shout-out all the Support Staff of MetroPvP for helping and making sure the server is successful.**",color=0x157696, inline=True)
  
  await bot.say(embed=embed)

#KICK AND BAN COMMANDS


@bot.command(pass_context = True, name = 'Kick', aliases=['kick'])
async def Kick(ctx, userName: discord.User):
  embed = discord.Embed(description="You've succesfully kicked this user!", color=0x157696, inline=True)
  author = ctx.message.author
  embed.set_thumbnail(url=author.avatar_url)
  if ctx.message.author.server_permissions.administrator:
 	  await bot.kick(userName)
  await bot.say(embed=embed)



@bot.command(pass_context = True, name = 'Ban', aliases=['ban'])
async def Ban(ctx, userName: discord.User):

  embed = discord.Embed(description="You've succesfully Banned this user!", color=0x157696, inline=True)
  author = ctx.message.author
  embed.set_thumbnail(url=author.avatar_url)
  if ctx.message.author.server_permissions.administrator:
 	  await bot.ban(userName)
  await bot.say(embed=embed)


























#chat moderation



@bot.listen()
async def on_message_edit(before, after):
	message = after
	if profanity.contains_profanity(message.content):
		await bot.delete_message(message)
		if db.contains(Users.id == message.author.id):
			if db.contains((Users.id == message.author.id) & (Users.swears == 4)):
				await bot.kick(message.author)
				db.update({'swears': 0}, Users.id == message.author.id)
			else:
				db.update(increment('swears'), Users.id == message.author.id)
		else:
			db.insert({'id': message.author.id, 'swears': 0})
		await bot.send_message(message.author,"You have recived a strike if you recive five strikes you will be kicked")

@bot.listen()
async def on_message(message):
	if profanity.contains_profanity(message.content):
		await bot.delete_message(message)
		if db.contains(Users.id == message.author.id):
			if db.contains((Users.id == message.author.id) & (Users.swears == 4)):
				await bot.kick(message.author)
				db.update({'swears': 0}, Users.id == message.author.id)
			else:
				db.update(increment('swears'), Users.id == message.author.id)
		else:
			db.insert({'id': message.author.id, 'swears': 0})
		await bot.send_message(message.author,"You have recived a strike if you recive five strikes you will be kicked")

@bot.listen()
async def on_member_join(member):
	is_verified = False
	for role in member.roles:
		if role.name == "Verified":
			is_verified = True
			break
	if is_verified == False:
		await bot.send_message(member,"Please message the bot with the command ~verify to get normal permissions")

@bot.command(pass_context=True, hidden=True)
async def strike(context):
  if ctx.message.author.permissions.kick_user:
	  usr = context.message.mentions[0]
	  if db.contains(Users.id ==usr.id):
			  if db.contains((Users.id == usr.id) & (Users.swears == 4)):
				  await bot.kick(usr)
				  db.update({'swears': 0}, Users.id ==usr.id)
			  else:
			  	db.update(increment('swears'), Users.id == usr.id)
	  else:
		  db.insert({'id': usr.id, 'swears': 0})
	  await bot.send_message(usr,"You have recived a strike if you recive three strikes you will be kicked")

@bot.command(pass_context=True)
async def purge(context, number : int):
	"""Clear a specified number of messages in the chat"""
	deleted = await bot.purge_from(context.message.channel, limit=number)
	await bot.send_message(context.message.channel, 'Deleted {} message(s)'.format(len(deleted)))





@bot.command(pass_context=True)
async def roles(context):
	"""Displays all of the roles with their ids"""
	roles = context.message.server.roles
	result = "The roles are "
	for role in roles:
		result += role.name 
	await bot.say(result)

#new addons 



@bot.command(pass_context=True, name = 'Sc', aliases=['sc'])
async def Sc(ctx):
  activeServers = bot.servers
  sum = 0
  for s in activeServers:
    sum += len(s.members)
  author = ctx.message.author
  embed = discord.Embed(description="MetroPvP Server Count", color=0x157696)
  embed.set_thumbnail(url=author.avatar_url)
  embed.add_field(name="Members", value=sum, inline=True)
  embed.add_field(name="Bots", value="5", inline=True)
  await bot.say(embed=embed) 





#new type of member Count






#bot_count = len(([member for member in s.member if not member.bot]))






















#human_count = len([member for member in guild.members if not member.bot])
#bot_count = len(([member for member in guild.members if member.bot]))
























bot.run('NTU4NDI2MjM1MTA2MjMwMzAz.XLdl0w.jndxkZu56AdC2pxAdJtW0JMU1fo')
