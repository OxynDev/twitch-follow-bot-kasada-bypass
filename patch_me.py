import traceback, time, discord, threading, httpx, random, json, tracemalloc, asyncio

from dotenv import load_dotenv
from discord.ext import commands
  

tracemalloc.start()



config = json.loads(open("config.json","r", encoding="utf8").read())
tokens = open('tokens.txt',"r").read().splitlines()
proxy = open("proxy.txt","r").read().splitlines()

prefix = config['bot_config']["prefix"]
token = config['bot_config']["token"]

tokens_proxy = []
followed_users = []

for i in tokens:
    tokens_proxy.append([i,"http://"+random.choice(proxy),'Dalvik/2.1.0 (Linux; U; Android '+str(random.randint(8,11))+'; SM-G'+str(random.randint(1111,9999))+' Build/QP1A.190711.020) tv.twitch.android.app/13.8.0/'+ str(random.randint(1,99999))])


dt = {}


load_dotenv()
intents = discord.Intents().all()
bot = commands.AutoShardedBot(command_prefix=prefix, help_command=None, intents=intents)



def init():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.run(token))
    threading.Thread(target=loop.run_forever).start()

def get_id(user):
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept-Language': 'en-US',
        'sec-ch-ua-mobile': '?0',
        'Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Client-Session-Id': '51789c1a5bf92c65',
        'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        'X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.twitch.tv',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.twitch.tv/',
    }
    data = '[{"operationName": "WatchTrackQuery","variables": {"channelLogin": "'+user+'","videoID": null,"hasVideoID": false},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "38bbbbd9ae2e0150f335e208b05cf09978e542b464a78c2d4952673cd02ea42b"}}}]'
    try:
        response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)
        id = response.json()[0]['data']['user']['id']
        return id
    except:
        return None




@bot.command()
async def tfollow(ctx, arg):
    genchannel =config['bot_config']["twitch_channel"]
    if ctx.channel.id == int(genchannel):
        for role_name in config['tfollow']:

            follow_count = config['tfollow'][role_name]
            
            if discord.utils.get(ctx.guild.roles, name=role_name) in ctx.author.roles:

                target_id = get_id(arg)
                
                if target_id == None:
                    embed=discord.Embed(color=0x3498db, description=f"**ERROR** Invalid **username** {arg}")
                    await ctx.send(embed=embed, delete_after=5); return  
                
                if arg in followed_users:
                    embed=discord.Embed(color=0x3498db, description=f"➣ CANT FOLLOW 2 TIMES SAME ACCOUNT `Wait for restock`")
                    await ctx.send(embed=embed); return

                num_lines = len(tokens)
                
                if num_lines < follow_count:
                    embed=discord.Embed(color=0x3498db, description=f"➣ Adding **{num_lines}** follows to **{arg}**")
                    await ctx.send(embed=embed)
                    caunt_to_follow = num_lines
                else:
                    embed=discord.Embed(color=0x3498db, description=f"➣ Adding **{follow_count}** Twitch Follows to **{arg}**")
                    await ctx.send(embed=embed)                
                    caunt_to_follow = follow_count
                

                class Threads1():
                    tha = 0
                
                def follow(token,proxy,useragent):
                    Threads1.tha = Threads1.tha + 1
                    try:
                        payload = '[{"operationName":"FollowUserMutation","variables":{"targetId":"'+target_id+'","disableNotifications":false},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"cd112d9483ede85fa0da514a5657141c24396efbc7bac0ea3623e839206573b8"}}}]'
                        headers = {'accept':'application/vnd.twitchtv.v3+json',
                            'accept-encoding':'gzip',
                            'api-consumer-type':'mobile; Android/1308000',
                            'authorization':'OAuth ' + token,
                            'client-id':'kd1unb4b3q4t58fwlpcbzcbnm76a8fp',
                            'client-session-id':'97f9101e-8ec1-40e7-9bae-aff8c93ce051',
                            'connection':'Keep-Alive',
                            'content-type':'application/json',
                            'host':'gql.twitch.tv',
                            'transfer-encoding':'chunked',
                            'user-agent':useragent,
                            'x-apollo-operation-name':'FollowUserMutation',
                            'x-app-version':'13.8.0',
                            'x-device-id':'3085330b917e4aeb8a47415d9dad814c'}
                        res = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers,proxies=proxy,timeout=40)
                        print(res.text)
                    except:
                        traceback.print_exc()
                    Threads1.tha = Threads1.tha - 1

                def start():
                    for i in range(caunt_to_follow):
                        while True:
                            time.sleep(0.01)
                            if Threads1.tha < 20:
                                t_p_u = tokens_proxy[i]
                                token = t_p_u[0]
                                proxy = t_p_u[1]
                                useragents = t_p_u[2]
                                threading.Thread(
                                    target=follow, args=(token,proxy,useragents)).start()
                                break
                            else:
                                time.sleep(1)

                followed_users.append(arg)
                threading.Thread(target=start).start()
                break




init()
