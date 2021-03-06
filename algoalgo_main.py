import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import algoalgo_member
import algoalgo_shop
import algoalgo_item
import algoalgo_map
import algoalgo_error
import algoalgo_step
import algoalgo_boss

client = discord.Client()
admin = 742625793276116992

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    print("디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + client.user.name)
    print("디스코드봇 ID:" + str(client.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('------')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("GM on Board, w/ 알고리즘"))

@client.event
async def db_refresh():
    print(datetime.now())
    algoalgo_member.refresh()

@client.event
async def on_message(message):
    # if this message is sent by bot itself, do nothing.
    if message.author == client.user:
        return
    
    # adduser function
    if message.content.startswith('!adduser'):
        result = algoalgo_member.adduser(str(message.author), message.content)
        await message.channel.send(result)
    
    # adduser function - admin
    if message.content.startswith('!admin_adduser'):
        result = algoalgo_member.adduser("admin", message.content)
        await message.channel.send(result)
    
    # show user info
    if message.content.startswith('!showuserinfo'):
        result, userinfo = algoalgo_member.showuserinfo(message.author)
        embed = discord.Embed(title = f"USERINFO_{message.author}", description=userinfo, color = 0xffffff)
        await message.channel.send(result)
        await message.channel.send(embed=embed)

    if message.content.startswith('!refresh'):
        result = f"[!] Admin Permission Required."
        if message.author.top_role.id == admin:
            result = algoalgo_member.refresh()
        await message.channel.send(result)

    if message.content.startswith('!addpoint'):
        result = f"[!] Admin Permission Required."
        if message.author.top_role.id == admin:
            result = algoalgo_member.addpoint(message.content)
        await message.channel.send(result)

    if message.content.startswith('!list_achievement'):
        result = algoalgo_member.list_achievement()
        if result.split()[0] != '[!]':
            embed = discord.Embed(title="Achievement List", description=result, color=0xffffff)
            await message.channel.send(f"[*] Successfully Inquired Achievement List")
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(result)

    if message.content.startswith('!random_bj'):
        result = algoalgo_member.random_bj(str(message.author), message.content)
        if result.split()[0] != '[!]':
            embed = discord.Embed(title="Try This!", description=result, color=0xffffff)
            await message.channel.send(f"[*] Successfully Found A Random Baekjoon Problem")
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(result)

    if message.content.startswith('!daily_baekjoon'):
        result = algoalgo_member.daily_baekjoon(str(message.author), message.content)
        await message.channel.send(result)

    if message.content.startswith('!unlock'):
        result = algoalgo_member.unlock(str(message.author))
        await message.channel.send(result)


    # show items detail info
    if message.content.startswith('!showshopinfo'):
        embed = discord.Embed(title="ALGOALGO SHOP BOT",description="SHOP 아이템 목록", color=0x00aaaa, inline=True)
        embed.add_field(name="STEP🦶", value="저희 게임 일반 모드에서의 전진 아이템입니다. 보드 판 위의 문제(백준 알고리즘 문제)를 해결 했을 때, 앞으로 1칸 전진할 수 있는 기회를 제공해주는 아이템입니다. 하루 최대 2개 까지 구매가능 합니다. 다만, 두 번째 구매시엔 가격이 두 배로(10pt로) 상승합니다. 즉, 하루에 STEP을 사용하여 2칸까지 전진할 수 있습니다.", inline=False)
        embed.add_field(name="THE ALGOALGO REDEMPTION🛡", value="저희 게임 일반 모드에서의 방어 아이템입니다. 보드 판 위의 문제(백준 알고리즘 문제)를 해결하지 못했을 때의 상황을 모면하는 아이템 입니다. REDEMPTION을 사용하면, 문제를 해결하지 못해도 STEP을 사용하여 전진할 수 있게 됩니다. 하루 최대 1개 까지 구매가능 합니다.", inline=False)
        embed.add_field(name="SNAKE HUNTER🐍", value="저희 게임 일반 모드에서의 방어 아이템입니다. 저희 게임 맵은 뱀사다리 게임의 보드판을 표방합니다. 게임 진행 시 뱀으로 인한 후퇴 상황을 막아줍니다. 게임이 진행될 수록, 가격이 하락합니다.", inline=False)
        embed.add_field(name="ASSASSIN ALGOALGO🗡", value="저희 게임 일반 모드에서의 타 플레이어 방해 아이템입니다. N개의 아이템 사용으로, 유저 한 명을 N칸 후퇴시킬 수 있습니다.", inline=False)
        embed.add_field(name="STUN⚔️", value="저희 게임 일반 모드에서의 타 플레이어 방해 아이템입니다. 유저 한명의 아이템 STEP 사용을 막아 전진을 못하게 합니다.", inline=False)
        embed.add_field(name="CAFFEINE🍺", value="저희 게임 보스레이드 모드에서의 버프 아이템입니다. 본인의 공격을 2배로 늘릴 수 있습니다.", inline=False)
        embed.add_field(name="REDBULL💊", value="저희 게임 보스레이드 모드에서의 버프 아이템입니다. 본인의 공격을 3배로 늘릴 수 있습니다.", inline=False)
        embed.add_field(name="BOMB💣", value="저희 게임 보스레이드 모드에서의 보스 공격 아이템입니다. 구매 즉시 보스에게 100 데미지를 주게됩니다. 다만 각 개인들은 해당 아이템을 5개 까지만 구매 가능합니다.", inline=False)
        await message.channel.send(embed=embed)
        await message.channel.send("Please enter the item you want\nSTEP🦶, REDEMPTION🛡, SNAKE🐍, ASSASSIN🗡, STUN⚔️\nUsage: Usage: !buyitem <item name> <number>")

    # show shop items info
    if message.content.startswith('!shop'):
        embed = discord.Embed(title="유후! 여름 빅 세일입니다\nSTEP과 STUN, 제가 직접 만든 SNAKE도 반값 할인 중입니다")
        embed.set_image(url="https://blog.kakaocdn.net/dn/b4numP/btqIrvqfcvg/Hm88ead0XHCjQnyKjoSO91/img.png")
        embed.add_field(name="STEP🦶", value="3pt", inline=True)
        embed.add_field(name="REDEMPTION🛡", value="5pt", inline=True)
        embed.add_field(name="SNAKE🐍", value="10pt", inline=True)
        embed.add_field(name="ASSASSIN🗡", value="6pt", inline=True)
        embed.add_field(name="STUN⚔️", value="6pt", inline=True)
        await message.channel.send(embed=embed)
        await message.channel.send("**지금 당장 구매하세요!** -->> !buyitem <item name> <number>")

    # buy items 
    if message.content.startswith('!buyitem'):
        result, pointinfo = algoalgo_shop.point_check(message.author)
        await message.channel.send("현재 보유 포인트: "+pointinfo)
        if int(pointinfo)>0:
            result = algoalgo_shop.buy_item(str(message.author), message.content)
            await message.channel.send(result)
        else:
            await message.channel.send("포인트가 부족합니다. 구매를 종료합니다")

    # show boss shop items detail info
    if message.content.startswith('!boss_shop'):
        embed = discord.Embed(title="ALGOALGO BOSS SHOP BOT",description="BOSS SHOP 아이템 목록", color=0x00aaaa, inline=True)
        embed.add_field(name="CAFFEINE🍺", value="3포인트. 본인의 다음 공격 데미지가 2배가 됩니다", inline=False)
        embed.add_field(name="REDBULL💊", value="5포인트. 본인의 다음 공격 데미지가 3배가 됩니다", inline=False)
        embed.add_field(name="BOMB💣", value="6포인트. 구매 즉시 자동 사용으로, 보스에게 100 데미지 공격을 합니다", inline=False)
        await message.channel.send(embed=embed)
        #await message.channel.send("Please enter the item you want\CAFFEINE🍺, REDBULL💊, BOMB💣\nUsage: !buybossitem <item name> <number>")
        msg = await message.channel.send("원하는 아이템 이모지를 클릭하세요")
        await msg.add_reaction("🍺") #caffeine
        await msg.add_reaction("💊") #red bull
        await msg.add_reaction("💣") #bomb
        
        def check(reaction, user):
            return user == message.author and (str(reaction.emoji) == '🍺' or str(reaction.emoji) == '💊' or str(reaction.emoji) == '💣')
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send('👎')
        else:
            #await message.channel.send('👍')
            whatemoji=""
            if str(reaction.emoji) == '🍺':
                whatemoji="CAFFEINE"
            elif str(reaction.emoji) == '💊':
                whatemoji="REDBULL"
            elif str(reaction.emoji) == '💣':
                whatemoji="BOMB"
            
            result, pointinfo = algoalgo_shop.point_check(message.author)
            await message.channel.send("현재 보유 포인트: "+pointinfo)
            if int(pointinfo)>0:
                gogo = "!buyitem "+whatemoji+" 1"
                result = algoalgo_shop.buy_item(str(message.author), gogo)
                await message.channel.send(result)
            else:
                await message.channel.send("포인트가 부족합니다. 구매를 종료합니다")

    
    #################################
    # boss 관련 명령어               #
    # 담당자 : 2018111339 신유림     #
    #################################
    if message.content.startswith('!atk_boss'):
        atk_result = algoalgo_boss.attackBoss(str(message.author), message.content)
        embed = discord.Embed(title = f"""== 보스 공격 여부 ==""", description=atk_result, color = 0x6b9560)
        await message.channel.send(embed=embed)


    if message.content.startswith('!boss'):
        curr_life = algoalgo_boss.getBossLife()
        embed = discord.Embed(title = f"""== 보스 남은 체력 ==""", description=curr_life, color = 0x6b9560)
        
        await message.channel.send(embed=embed)
    
    

    
    ################################
    # map 관련 명령어
    # 담당자 : 20181113nn 박세란 
    # 보조 : 2018111339 신유림
    #################################

    #player's location
    if message.content.startswith('!show_map'):
        await message.channel.send('Loading...Map..')
        result, Locinfo, bj_no = algoalgo_map.showmap(message.author)
        bj_url = f"https://www.acmicpc.net/problem/{bj_no}"
        embed = discord.Embed(title = f"""== **{message.author}** 's location ==""", description=Locinfo, color = 0x6b9560)
        embed.add_field(name='**풀어야 할 문제**', value = bj_url, inline=False)
        
        await message.channel.send(result)
        await message.channel.send(embed=embed)
    
    #admin :: set map feature
    if message.content.startswith('!set_map'):
        result = f"[*] the admin permission required."
        if message.author.top_role.id == admin:
            result = algoalgo_map.setmap(message.content)
        await message.channel.send(result)

    #admin :: getLocType
    if message.content.startswith('!getLocType'):
        result = f"""[*] the admin permission required."""
        embed = discord.Embed(title = f"""[*] the admin permission required.""", description=f"""your role :: {message.author.top_role.name}""", color = 0x00aaaa)
        if message.author.top_role.id == admin:
            result, LocFeatureInfo, nowLoc = algoalgo_map.getLocType(message.content)
            embed = discord.Embed(title = f"""== the feature of the **{nowLoc}** location ==""", description=LocFeatureInfo, color = 0x6b9560)
        await message.channel.send(result)
        await message.channel.send(embed=embed)

    #admin :: getPlayers
    if message.content.startswith('!getPlayers'):
        result = f"""[*] the admin permission required."""
        embed = discord.Embed(title = f"""[*] the admin permission required.""", description=f"""your role :: {message.author.top_role.name}""", color = 0x00aaaa)
        if message.author.top_role.id == admin:
            result , Locinfo, nowLoc = algoalgo_map.getPlayers(message.content)
            embed = discord.Embed(title = f"""== the player list in the **{nowLoc}** location ==""", description=Locinfo, color = 0x6b9560)
        await message.channel.send(result)
        await message.channel.send(embed=embed)
        
    #admin ::  printing the highest role 
    if message.content.startswith('!role_id'):
        await message.channel.send(embed=discord.Embed(title=f"""== {message.author}'s the highest role INFO ==""", description = f""" the highest role :: {message.author.top_role.name}\n the highest role id :: {message.author.top_role.id} """, color = 0x6b9560))


    #admin ::  printing all_role id 
    if message.content.startswith('!all_roles_id'):
        for i in range(len(message.author.roles)):
            await message.channel.send(embed=discord.Embed(title=f"""== {message.author}'s the roles INFO ==""", description = f""" the role #{i} :: {message.author.roles[i].name}\n the role #{i}'s' id :: {message.author.roles[i].id} """, color = 0x6b9560))
    
    #################################
    # step 관련 명령어               #
    #################################
    #!step
    if message.content.startswith('!step'):
        try:
            user_location = algoalgo_step.get_location(message.author)

            # check step value. have to be > 0
            step_value = algoalgo_step.check_items(message.author, "STEP")       
            if step_value <= 0:
                e_msg = "You have No STEP item. Please buy and try again."
                raise algoalgo_error.UserDefinedException(e_msg)
            
            # check user status. status == 1
            user_status = algoalgo_step.check_status(message.author)
            if user_status != 1:
                e_msg = ""
                if user_status == 0:                    
                    e_msg = "You are now LOCKED. Please solve problem to unlock your status.\nSTEP으로 진행을 하기 위해서는 알고리즘 문제를 풀어주세요."
                elif user_status == -1:
                    e_msg = "You are now STUNNED. Please wait.\n스턴은 하루가 지나면 풀립니다. 내일 다시 찾아와서 STEP 진행을 해주세요."
                else:
                    e_msg = "Your status is now unidentified. Please contact to staff.\n현재 status 값에 오류가 발생했습니다. 스탭에게 연락해주세요."
                raise algoalgo_error.UserDefinedException(e_msg)

            # check user's daily_step
            daily_step = algoalgo_step.check_dailystep(message.author)
            if daily_step >= 1:
                e_msg = "You already use STEP twice per day. Please use later.\n이미 하루에 사용하실 수 있는 STEP을 모두 사용하셨습니다. 내일 다시 진행해주세요."
                raise algoalgo_error.UserDefinedException(e_msg)

            # check user location
            if not 1 <= user_location <= 49:
                e_msg = f"You can't use step anymore.\n이제 STEP을 사용하실 수 없습니다.\n현재 위치:{user_location}"
                raise algoalgo_error.UserDefinedException(e_msg)


            # update map location
            update_result = algoalgo_step.update_location(message.author)
            if update_result != 0:
                e_msg = "Something went wrong while updating location...\n업데이트 중 오류가 발생했습니다. 다시 시도해주세요."
                raise algoalgo_error.UserDefinedException(e_msg)

            # check feature
            # slider - 6->11
            # snake  - 21->8
            map_feature = algoalgo_step.check_feature(message.author)
            
            # split into features
            # 0: normal
            # 1: ladder
            # 2: snake

            info1 = "" #info about map_feature
            info2 = "" #info about location 

            if map_feature == 0:
                info1 = "You stepped into NORMAL block."
                
            elif map_feature == 1:
                info1 = "You stepped into ladder block."
                algoalgo_step.ladder(message.author)
            
            elif map_feature == 2:
                info1 = "You stepped into SNAKE block."
                snake_value = algoalgo_step.check_items(message.author, "SNAKE")
                if snake_value > 0:
                    embed = discord.Embed(title="Snake!",description="Do you want to run?")
                    embed.add_field(name='**사용법**',value='SNAKE 아이템을 사용하려면 Y를 입력해주세요. N을 입력하시면 뱀을 타고 내려갑니다.\nY, N을 제외한 값을 입력하시면 무조건 아이템을 사용하지 않습니다.',inline=False)
                    embed.add_field(name='보유한 SNAKE 수',value=f"{snake_value} 개",inline=False)
                    await message.channel.send(embed=embed)

                    def use(mes): # 답장하는 사람이 메세지를 보낸 사람과 일치하는지 
                        return mes.author == message.author and mes.channel == message.channel
                    try:
                        msg = await client.wait_for('message',timeout=15.0, check=use) 
                    except asyncio.TimeoutError:
                        e_msg = "**TIME OUT**\nCome again!\n입력 시간이 지났습니다. 처음부터 다시 진행해주세요."
                        raise algoalgo_error.UserDefinedException(e_msg)

                    else: # 사용자 입력값 검사
                        if msg.content == "Y": 
                            algoalgo_step.use_items(message.author, "SNAKE")
                            embed = discord.Embed(title="성공!",description="뱀을 무사히 피했습니다!")
                            await message.channel.send(embed=embed)

                        else:
                            algoalgo_map.snake(message.author)
                            embed = None
                            if msg.content == "N":
                                embed = discord.Embed(title="이런!",description="뱀을 피하다가 발을 헛디뎌 밑으로 내려왔어요!")
                            else:
                                embed = discord.Embed(title="이런!",description="고민하다가 잘못 선택해서 밑으로 내려왔어요!")
                            await message.channel.send(embed=embed)
                else:
                    algoalgo_map.snake(message.author)
                    embed = discord.Embed(title="이런!",description="뱀을 잘못 밟아 미끄러지고 말았어요!")
                    await message.channel.send(embed=embed)

            elif map_feature == 3:
                e_msg = "보스 칸에 도착하셨습니다.\n아직 보스 기능이 완성되지 않았습니다. 보스가 오픈된 이후에도 이 메세지를 보신다면 스텝에게 연락해주세요."
                raise algoalgo_error.UserDefinedException(e_msg)
            
            else:
                e_msg = "Feature is now unidentified. Please contact to staff.\n현재 feature 값에 오류가 발생했습니다. 스탭에게 연락해주세요."
                raise algoalgo_error.UserDefinedException(e_msg)
                
            
            # final : update status&daily_step into 0 and remove step item in list 
            algoalgo_step.use_items(message.author, "STEP")
            algoalgo_step.update_dailystep(message.author)
            algoalgo_step.update_status(message.author)

            # outputs
            final_location = algoalgo_step.get_location(message.author)
            info2 = f"Your Location : {final_location}"

            embed = discord.Embed(title="STEP Complete",description=info1)
            embed.add_field(name='**도착 위치**',value=info2)
            await message.channel.send(embed=embed)


        except Exception as ex:
            # 에러가 발생하면 다시 location 원상복귀 
            algoalgo_step.update_location_dst(message.author, user_location)
            embed = discord.Embed(title="[!] STEP error",description=f"Error : {ex}")
            await message.channel.send(embed=embed)
            return


    #################################
    # item 관련 명령어
    # 담당자 : 2018111321 김선미
    # 보조 : 2018111339 신유림
    #################################
    # !useitem 
    if message.content.startswith('!useitem'):
        try:
            result = algoalgo_item.useitem(str(message.author))

            #아이템 목록 출력하는 칸임
            if result == 0:
                embed = discord.Embed(title="**NO Item**",description="please buy item first")
                await message.channel.send(embed=embed)
                return

            item_msg = f"""```
[idx] item_name | values
[1] STUN        | {result['STUN']}
[2] ASSASSIN    | {result['ASSASSIN']}
[3] REDEMPTION  | {result['REDEMPTION']} ```"""

            embed = discord.Embed(title="Ha ha, What do you want?", description="15초 안에 아이템 번호를 입력해주세요")
            embed.add_field(name='**사용법**',value='**사용하고자 할 아이템 번호를 입력해주세요. 단, assassin, stun, bomb는 번호와 유저이름을 입력**',inline=False)
            embed.add_field(name='**예시**',value='**`1`, `2`,`3`,`1 kim`,`3 park`**',inline=False)
            embed.add_field(name='**보유중인 아이템**', value = item_msg, inline=False)
            channel = message.channel
            await message.channel.send(embed=embed)  
        except Exception as ex:
            embed = discord.Embed(title="Error",description=f"[!] Error in listing Items... \nError : {ex}")
            await message.channel.send(embed=embed)
            return
        
        def buy(mes):
            return mes.author == message.author and mes.channel and channel
        try:
            msg = await client.wait_for('message',timeout=15.0, check=buy) 
        except asyncio.TimeoutError:
            embed = discord.Embed(title="TIME OUT",description="oh you don't need it? oKay... BYE!")
            await message.channel.send(embed=embed)
            return
        else:
            msg_content = msg.content.split()
            user_res = ""
            user_atk = ""

            item_list = ['STEP', 'STUN', 'ASSASSIN', 'REDEMPTION']
            # 사용자 입력값 검사
            try:
                if len(msg_content) != 1 and len(msg_content) != 2:
                    e_msg = "Invalid Input\nUsage: <item_idx> <target_discord_id>"
                    raise algoalgo_error.UserDefinedException(e_msg)
                    
                # 아이템 인덱스가 제대로 들어오는지
                user_res = int(msg_content[0]) 
                
                # 추가적인 arg - 제대로 된 target id가 들어오는지 
                if len(msg_content) == 2: 
                    user_atk = msg_content[1]

                    check_user = algoalgo_item.checkMember(user_atk)
                    if not check_user:
                        e_msg = f"No User named '{user_atk}'"
                        raise algoalgo_error.UserDefinedException(e_msg)
                    
                if not 1 <= user_res <= 3:
                    e_msg = "Invalid Item indicies"
                    raise algoalgo_error.UserDefinedException(e_msg)
                
                if result[item_list[user_res]] == 0:
                    e_msg = "Not enough value to use"
                    raise algoalgo_error.UserDefinedException(e_msg)
                    
            except Exception as ex:
                    embed = discord.Embed(title="Error",description=f"[!] Input value is not valid... \nError : {ex}")
                    await message.channel.send(embed=embed)
                    return


            try: # 아이템 업데이트 진행에 대한 try-except
                user_res2 = item_list[user_res] # user_res2 = 아이템 명
            
                if user_res2 == 'STUN' :
                    if len(msg_content) != 2:
                        e_msg = "No Target user in arg\nUsage : 1 <target_discord_id>"
                        raise algoalgo_error.UserDefinedException(e_msg)
                    
                    # 상대방 status = -1 로 업데이트
                    result2 = algoalgo_item.setStun(user_atk)
                    # stun 없애기
                    algoalgo_item.updateitem(str(message.author),"STUN;")
                    await message.channel.send(result2)
                    return

                if user_res2 == 'REDEMPTION':
                    # 문제 못풀었을 때 이동 가능
                    result2 = algoalgo_item.setRedemption(str(message.author))
                    # redemption 없애기
                    algoalgo_item.updateitem(str(message.author),"REDEMPTION;")
                    await message.channel.send(result2)
                    return

                if user_res2 == 'ASSASSIN' and len(msg.content)>2 :
                    # 상대방 뒤로 옮기기
                    result2 = algoalgo_item.setAssassin(user_atk)
                    # assassin 뒤로 옮기기
                    algoalgo_item.updateitem(str(message.author),"ASSASSIN;")
                    await message.channel.send(result2)
                    return

                
                embed = discord.Embed(title="Check your answer",description=f"this is not right type '{user_res2}'")
                await message.channel.send(embed=embed)
                return
            except Exception as ex:
                embed = discord.Embed(title="Error",description=f"[!] Error while Using Item \nError : {ex}")
                await message.channel.send(embed=embed)
                return

           


sched = AsyncIOScheduler()
sched.add_job(db_refresh, 'cron', hour=0)
sched.start()

client.run(os.environ['discord-token'])

