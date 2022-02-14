import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import srcomapi, srcomapi.datatypes as dt
api = srcomapi.SpeedrunCom(); api.debug = 1
from datetime import datetime as dtime
from datetime import timedelta as tdel
from datetime import time
import math

global perm 
perm = True
Client = discord.Client()
bot_prefix= "."
client = commands.Bot(command_prefix=bot_prefix)

def check():
	return perm

def change():
	global perm
	perm = False

def convert(t):
	a = int(t/60/60)
	b = int(t/60%60)
	c = t%60
	vt = time(a,b,c)
	return vt

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

boards = []
boardlist = open("boards.txt", "r")
boardtemp = boardlist.readlines()
for i in boardtemp:
	boards.append(i[:8])
	
@client.event
async def on_ready():
	print("Bot Online!")
	print("Name: {}".format(client.user.name))
	print("ID: {}".format(client.user.id))
	p = check()
	if p:
		change()
		await post()	

multiruns = ['n2y39y1d', 'xk9nemg2', '7kjq8nzd', 'wdml1wek', 'vdo8g8ok','jdz9xeg2','zd3wzryk','7dg6n97k','mke49r82']
HP4 = ['zd3yx82n', '7dgjp4d4']
HP5 = ['q25o9r8k', 'jdrq8jxk']
sixth = ['824x9wgd','9d8pnr3k']
lego = ['wk6jnqd1', 'n2y1oz2o', '7kjr3n23', 'xk9lr4k0', 'ndx807ok', 'w20z5vjd', 'wdmq7le2', 'vdo4n862']
subcat = ['n2y39y1d', 'xk9nemg2', '7kjq8nzd', 'wdml1wek', 'vdo8g8ok', 'zd3yx82n', '7dgjp4d4', 'q25o9r8k', 'jdrq8jxk', 'wk6jnqd1', 'n2y1oz2o', '7kjr3n23', 'xk9lr4k0', 'ndx807ok', 'w20z5vjd', 'wdmq7le2', 'vdo4n862']

# find categories at https://www.speedrun.com/api/v1/categories/

async def post():
	channel = client.get_channel(597203792055894016)
	channel2 = client.get_channel(679222589796646912)
	t2 = dtime.utcnow()-tdel(minutes = 60)
	print(t2)
	new_runs = []
	for board in boards:
		try:
			lb = api.get("categories/"+board)
			cat = api.get(lb["links"][-1]["uri"][32:])['runs']
			for j in cat:
				if (j['run']['status']['status']=='verified' and j['run']['status']['verify-date'] is not None):
					vtime = dtime.strptime(j['run']['status']['verify-date'],'%Y-%m-%dT%H:%M:%SZ')
					#if (board == "9d8gow3k"):
					#	print(j['weblink'])
					if (vtime>=t2):
						new_runs.append(j['run']['id'])
					#	print(j['run']['weblink'])
		except:
			print("<@217757826414673920> category " + board + "has been deleted")
	if len(new_runs)>0:
		for i in new_runs:
			p = 0
			r = api.get("runs/"+i)
			n = api.get('users/'+r['players'][0]['id'])['names']['international']
			g = api.get('games/'+r['game'])['names']['international']
			c = g+" "+api.get('categories/'+r['category'])['name']
			if r['category'] in subcat:
				try:
					if r['category'] in multiruns:
						c = c + " "+api.get("variables/789k439l")['values']['values'][r['values']['789k439l']]['label']
					if r['category'] in HP4:
						c = c + " "+api.get("variables/j84k0x2n")['values']['values'][r['values']['j84k0x2n']]['label']
					if r['category'] in HP5:
						c = c + " "+api.get("variables/0nw7gk8q")['values']['values'][r['values']['0nw7gk8q']]['label']
					if r['category'] in sixth:
						c = c + " "+api.get("variables/p85rp0ng")['values']['values'][r['values']['p85rp0ng']]['label']
					if r['category'] in lego:
						c = c + " "+api.get("variables/"+str(list(r['values'].keys())[0]))['values']['values'][r['values'][str(list(r['values'].keys())[0])]]['label']
				except:
					await channel2.send("<@217757826414673920> run " + i + " has broken subcategories")
			t = convert(int(r['times']['primary_t'])).strftime('%H:%M:%S')
			if r['level'] is None:
				print("3")
				b = api.get('leaderboards/'+r['game']+'/category/'+r['category'])
				for j in range(len(b['runs'])):
					if b['runs'][j]['run']['id']==i:
						p = b['runs'][j]['place']
				if p ==1:
					m = "<:GoldScar:619662499381379072> ["+n+"]("+api.get('users/'+r['players'][0]['id'])['weblink']+") got a new WR in ["+c+"]("+api.get('categories/'+r['category'])['weblink']+") with a time of ["+t+"]("+api.get("runs/"+i)['weblink']+")"
				elif p ==0:
					m = "["+n+"]("+api.get('users/'+r['players'][0]['id'])['weblink']+") got a new PB in ["+c+"]("+api.get('categories/'+r['category'])['weblink']+") with a time of ["+t+"]("+api.get("runs/"+i)['weblink']+")"
				else:
					m = "["+n+"]("+api.get('users/'+r['players'][0]['id'])['weblink']+") got a new PB in ["+c+"]("+api.get('categories/'+r['category'])['weblink']+") with a time of ["+t+"]("+api.get("runs/"+i)['weblink']+") ["+ordinal(p)+"]"
				em = discord.Embed(colour=discord.Colour(0xffd700), url="https://discordapp.com", description=m)
				print("4")
				await channel.send(embed = em)
			else:
				print(r['level'])
	await client.close()
def sr_handler(event, context):
	client.run("XXXX")
