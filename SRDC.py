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


Client = discord.Client()
bot_prefix= "."
client = commands.Bot(command_prefix=bot_prefix)

def convert(t):
	a = int(t/60/60)
	b = int(t/60%60)
	c = t%60
	vt = time(a,b,c)
	return vt

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

boards = ['9d8v46kn','zd36qvdn','xd1mg7d8','zdnlex2q','9kvmn8kg','vdo0w8vd','xk9gvw4d','n2y17z2o','wkpqjvdr','ndxr01dq','wdmw6ro2','wkpo3nw2','02qpyqpd','vdoo1yvd','vdo3wpod','xd1701zd','7dgr6ypk','02qj3jdy','xd1myzd8','jdz5w3dv','824x9wgd','9d8pnr3k','xd1lm8k8','wk6vnxod','9d8p8n7k','824rlogd','zdnprxkq','xk9lv4k0','n2y7op72','7kj103gk','xk98zrx2','7dggn7d4','7dggz8xd','wk6jrxd1','zd3yx82n','7dgjp4d4','5dwp4ekg','q258j8j2','xd17168d','zd3045nd','xk9gp4d0','n2y1yzm2','q25o9r8k','jdrq8jxk','jdrpvg26','9d86l32n','jdz593dv','vdoqv09k','vdo08gvd','xd1e5428','z2761w0d','xk9l84k0','ndxm4nr2','w20w3n5d','xd13zprk','z27l8pgd','zdnqxedq','q2543ydo','n2y3x9ed','rklxy56k','wk61mnxd','zd3yw82n','zdn15xkq','wkpy1gkr','9d8gow3k','ndx895kq','w20zg8dn','wk6vj1qd','n2y71jz2','z27lr5gd','wdmqx52q','mkerv6nd','02qjlqzd','mke5z48k','n2y39y1d','xk9nemg2','7kjq8nzd','wdml1wek','7dg6olk4','mke598k6','z27lryod','xd1l4m8k','jdry0026','jdzx4x2v','n2y1ple2','wk6ownrk','wkpyr1jk','7kjrynn2','ndx86o5k','jdrewgk6','wk6jnqd1','w204ovkn','wk6vrqd1','n2y1oz2o','7kjr3n23','xk9lr4k0','mkez0qnk','w20w5qvd','wdmw75x2','vdoon51d','wkpor502','7dgr7mxk','mkez7xxk','wdmw1j52','7dgrep7k','mkezpm8k','5dw5ezed','7dggjzpd','5dwpw0lk','wkpyx8gk','mke56e6k','xd1mqlzd','5dwpwplk','wk610yxd','rklgzv6d','9kvxv932','zd3yr8e2','ndx807ok','w20z5vjd','wdmq7le2','vdo4n862','9kvxl7e2','n2yo34md']

first = True

@client.event
async def on_ready():
	if first:
		first = False
		channel = client.get_channel(xxxx)
		t2 = dtime.utcnow()-tdel(minutes = 15)
		new_runs = []
		for board in boards:
		    cat = api.get("runs?category="+board+"&max=500")
		    for j in cat:
		        if (j['status']['status']=='verified' and j['status']['verify-date'] is not None):
		            vtime = dtime.strptime(j['status']['verify-date'],'%Y-%m-%dT%H:%M:%SZ')
		            if (vtime>=t2):
		                new_runs.append(j['id'])
		if len(new_runs)>0:
			for i in new_runs:
			    p = 0
			    r = api.get("runs/"+i)
			    n = api.get('users/'+r['players'][0]['id'])['names']['international']
			    g = api.get('games/'+r['game'])['names']['international']
			    c = g+" "+api.get('categories/'+r['category'])['name']
			    t = convert(int(r['times']['primary_t'])).strftime('%H:%M:%S')
			    if r['level'] is None:
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
			        await channel.send(embed = em)
		await client.close()
def sr_handler(event, context):
	client.run("xxxx")
