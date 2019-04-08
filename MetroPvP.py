import discord
import logging, json
from discord.ext import commands
from profanity import profanity
from tinydb import TinyDB, Query
from tinydb.operations import delete,increment
import asyncio
from discord import Member
from discord.ext.commands import has_permissions
import time

# Requirements: discord.py, tinydb, profanity

# Define all variables to be used around the script
description = '''Bot description here'''
bot = commands.Bot(command_prefix='~', case_insensitive=False)
db = TinyDB('data.json')
Users = Query()


case_insensitive=True

@bot.event
async def on_ready():
  print('Bot is ready for use')

# Print the starting text
print('By Fbi_ShortMicrobe354_TrickShot (all same person ;>')
print('Better get my dev role fucker')
print('Bot is now ready')
print('prefix ~ Have fun! ')

# Setup basic logging for the bot
logging.basicConfig(level=logging.WARNING)
bot.remove_command('help')





@bot.command(pass_context = True, name = 'Help', aliases=['help'])
async def Help(ctx):
  author = ctx.message.author                           	
  embed = discord.Embed(description="Metro Help", color=0x157696, inline=True)
  embed.add_field(name="Here", value="Makes sure bot is here!", inline=False)
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

@bot.command(pass_context = True, name = 'Vote', aliases=['vote'])
async def Vote(ctx):
  """Gives server vote link"""
  embed = discord.Embed(description="mcpe.guru/8g6w2r", color=0x157696, inline=True)
  await bot.say(embed=embed)



#metro info


@bot.command(pass_context = True, name = 'Info', aliases=['info'])
async def Info(ctx):
  embed = discord.Embed(description="**MetroPvP is a Factions based MCPE server. It is Mythologically themed mixed with a futuristic space theme. We strive to be unique and become the #1 server of MCPE. We are aware that we aren't the biggest community, yet that does not mean we won't expand and update all the time. We would like to shout-out all the Support Staff of MetroPvP for helping and making sure the server is successful.**",color=0x157696, inline=True)
  
  await bot.say(embed=embed)


#more moderation

@bot.command(pass_context = True, name = 'Kick', aliases=['kick'])
async def Kick(ctx, userName: discord.User):
  embed = discord.Embed(description="You've succesfully kicked this user!", color=0x157696, inline=True)
  if ctx.message.author.server_permissions.administrator:
 	  await bot.kick(userName)
  await bot.say(embed=embed)



@bot.command(pass_context = True, name = 'Ban', aliases=['ban'])
async def Ban(ctx, userName: discord.User):
  embed = discord.Embed(description="You've succesfully Banned this user!", color=0x157696, inline=True)
  if ctx.message.author.server_permissions.administrator:
 	  await bot.ban(userName)
  await bot.say(embed=embed)



















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


#profanity censor
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



#strike
@bot.command(pass_context=True, hidden=True, name = 'Strike', aliases=['strike'])
async def Strike(context):
	usr = context.message.mentions[0]
	if db.contains(Users.id ==usr.id):
		if db.contains((Users.id == usr.id) & (Users.swears == 4)):
				await bot.kick(usr)
				db.update({'swears': 0}, Users.id ==usr.id)
		else:
			db.update(increment('swears'), Users.id == usr.id)
	else:
		db.insert({'id': usr.id, 'swears': 0})
	await bot.send_message(usr,"You have recieved a strike! If you recieve Five strikes you will be kicked")



#clear chat
@bot.command(pass_context=True, name = 'Purge', aliases=['purge'])
async def Purge(context, number : int):
  if ctx.message.author.server_permissions.manage_messages:
	  deleted = await bot.purge_from(context.message.channel,limit=500)
	  await bot.send_message(context.message.channel, '**Deleted {} message(s)**'.format(len(deleted)))





#role 

@bot.command(pass_context=True, name = 'Roles', aliases=['roles'])
async def Roles(context):
	"""Displays all of the roles with their ids"""
	roles = context.message.server.roles
	result = "The roles are "
	for role in roles:
		result += role.name + ","
	await bot.say(result)






@bot.command(pass_context=True, name = 'Here', aliases=['here'])
async def Here():
   embed = discord.Embed(description="**I'm here!**", color=0x157696, inline=True)
   await bot.say(embed=embed)


@bot.command(pass_context=True)
async def GG():
  await bot.say("**After so much time...**")
  time.sleep(2)
  await bot.say("**So much Trial and error...**")
  time.sleep(2)
  await bot.say("**I make my appearance...**")
  time.sleep(1)
  await bot.say("**Ladies and Gentleman!**")
  time.sleep(2)
  await bot.say("**I now bring to you...**")
  time.sleep(4)
  await bot.say("**METROPVPv2!**by tricky :)))")
  time.sleep(3)
  await bot.say("**Can i get a GG in chat??**")
  time.sleep(1)
  await bot.say("**For the Bois!!!**")



bot.run ('NTU4NDI2MjM1MTA2MjMwMzAz.XKkx9w.pFVVyWHy82MTwFJpGV0KOdKmE-I')