import discord
import UnitData
import NukeTest
import UpgradeTest
import re
import os
import asyncio
import ReceiveNewUpdate
import JuckPae
from BotData import *
shutOutNewUpdateChannel = None
testVoiceChannel =None
async def onNewUpdate(response):
    if shutOutNewUpdateChannel is not None:
        await shutOutNewUpdateChannel.send(response)
receiver = ReceiveNewUpdate.Receiver(onNewUpdate)
client = discord.Client()
voiceClient = None



def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


nukeTargetDict = {}
upgradeInfoDict = {}
@client.event
async def on_resume():
    print('resume')
@client.event
async def on_ready():
    global shutOutNewUpdateChannel, testVoiceChannel
    print('We have logged in as {0.user}'.format(client))
    JuckPae.loadAllComment()
    for ch in client.guilds:
        nukeTargetDict[ch] = NukeTest.NukeTargetInfo()
        upgradeInfoDict[ch] = UpgradeTest.UpgradeInfo()
        try:
            os.mkdir('TestData\\' + str(ch))
        except:
            pass
    for ch in client.get_all_channels():
        if ch.name == '업데이트알림':
            shutOutNewUpdateChannel = ch
        elif ch.name.startswith('일반_TEST_TEST'):
            testVoiceChannel = ch
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("사용설명은 도움!!"))

# @voiceClient.event

# async def on_ready
@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    if type(message.channel) == discord.channel.DMChannel: # DM 인가?
        await message.channel.send("DM에서는 명령어를 받지 않습니다.")
        return

    if not message.channel.name in ['스타-실험소', '봇명령']: # 채팅채널의 이름 검사
        if message.guild.name !='TeampleRPG Fam-':
            return

    print(message.guild)
    if message.content == '맵텟!!':
        print(message.author)
        if message.author.voice is None:
            await message.channel.send('음성채널에 입장하고있어야합니다.')
        else:
            print(message.author.voice)
            if message.author.voice.channel is not None:
                if len(client.voice_clients) > 0:
                    await client.voice_clients[0].disconnect()
                await message.author.voice.channel.connect()
                voiceClient = client.voice_clients[0]
                print(voiceClient)
    if message.content == '맵텟끝!!':
        if len(client.voice_clients) > 0:
            await client.voice_clients[0].disconnect()


    
    stripMessage = message.content.strip()
    if '도움!!' in stripMessage:
        if message.guild.name =='TeampleRPG Fam-':
            await message.channel.send(helpMessage + teampleRPG_message)
        else:
            await message.channel.send(helpMessage)
    ###help처리
    if 'help' in stripMessage:
        command = stripMessage.split('help')[0].strip()
        if command in NukeTestCommandHelpDict:
            await message.channel.send(NukeTestCommandHelpDict[command])
        elif command in UpgradeTestCommandHelpDict:
            await message.channel.send(UpgradeTestCommandHelpDict[command])
        elif command in TeampleRPG_CommandHelpDict:
            await message.channel.send(TeampleRPG_CommandHelpDict[command])
    else:        
        ### 서비스 시작
        if message.content.upper() == 'SCMD2_최신버전!!':
            with open('../ScmDraft2 Update Check/dist/CheckSCMD2Update/latest version.txt','rt') as f:
                latestVersion = f.readline()
            fileName = f'Scmdraft 2 - {latestVersion}.zip'
            testFile = discord.File(fp=f'../ScmDraft2 Update Check/dist/CheckSCMD2Update/{fileName}',filename=fileName)
            await message.channel.send(f'마지막으로 확인된 버전은 {latestVersion}입니다.',file=testFile)
        elif message.content.upper() in ('팀알_최신버전!!','팀플RPG_최신버전!!','팀알_최신버젼!!','팀플RPG_최신버젼!!'):
            latestVersion = '20.09.02'
            await message.channel.send(f'현재 팀플 RPG의 최신 버전은 {latestVersion} 입니다.\n다운로드 링크: https://cafe.naver.com/teamplerpg/1775')
        elif message.content == '봇정보!!' or message.content == '봇 정보!!':
            await message.channel.send(BotInfoMessage)
        elif '핵을 쏴라!!' in stripMessage or '핵을쏴라!!' in stripMessage:
            if '죽을 때까지' in stripMessage or '죽을때까지' in stripMessage:
                step = 0
                response = ''
                if '빠르게' in stripMessage or '빨리' in stripMessage or '결과만' in stripMessage:
                    while nukeTargetDict[message.guild].curHP != 0:
                        step+=1
                        nukeTargetDict[message.guild].Damage()
                else:
                    sleepTime = 1.0
                    while nukeTargetDict[message.guild].curHP != 0:
                        step+=1
                        if sleepTime > 0.1:
                            nukeTargetDict[message.guild].Damage()
                            response = f'{step}) 펑!! 남은 쉴드,체력 : {nukeTargetDict[message.guild].curShield}, {nukeTargetDict[message.guild].curHP}'
                            await message.channel.send(response)
                            await asyncio.sleep(sleepTime)
                            sleepTime -= 0.1
                        else:
                            await message.channel.send('(중략)')
                            while nukeTargetDict[message.guild].curHP != 0:
                                step += 1
                                nukeTargetDict[message.guild].Damage()
                await message.channel.send(f'핵 쏜 횟수 : {step}')
            else:
                if '설명' in stripMessage:
                    await message.channel.send(nukeTargetDict[message.guild].Damage(True))
                else:
                    await message.channel.send(nukeTargetDict[message.guild].Damage(False))
        elif message.content == '실험정보!!':
            await message.channel.send('실험당할 유닛 정보 ㅠㅠ\n' + nukeTargetDict[message.guild].GetInfo())
        elif message.content.startswith('실험수정_') and '!!' in message.content:
            if message.content.startswith('실험수정_체력!!'):
                newHP = message.content.split('실험수정_체력!!')[1].strip()
                splitRes = newHP.split('/')
                if len(splitRes) > 2:
                    await message.channel.send(f'체력 매개변수 잘못됨. 양식 : 현재체력/최대체력 (현재체력 생략시 최대체력만 기입')
                else:
                    if len(splitRes) == 2:
                        curHP, maxHP = splitRes[0:2]
                        curHP, maxHP = int(curHP), int(maxHP)
                    else:
                        maxHP = int(splitRes[0])
                        curHP = maxHP
                    nukeTargetDict[message.guild].curHP = curHP
                    nukeTargetDict[message.guild].maxHP = maxHP
                    await message.channel.send(f'체력 수정됨 : {nukeTargetDict[message.guild].curHP} / {nukeTargetDict[message.guild].maxHP}')
            elif message.content.startswith('실험수정_쉴드!!') or message.content.startswith('실험수정_실드!!'):
                newShield = message.content.split('!!')[1].strip()
                splitRes = newShield.split('/')
                if len(splitRes) > 2:
                    await message.channel.send(f'쉴드 매개변수 잘못됨. 양식 : 현재쉴드/최대쉴드 (현재쉴드 생략시 최대쉴드만 기입')
                else:
                    if len(splitRes) == 2:
                        curShield, maxShield = splitRes[0:2]
                        curShield, maxShield = int(curShield), int(maxShield)
                    else:
                        maxShield = int(splitRes[0])
                        curShield = maxShield
                    nukeTargetDict[message.guild].curShield = curShield
                    nukeTargetDict[message.guild].maxShield = maxShield
                    await message.channel.send(f'쉴드 수정됨 : {nukeTargetDict[message.guild].curShield} / {nukeTargetDict[message.guild].maxShield}')
            elif message.content.startswith('실험수정_체력방어력!!'):
                newHPArmor = message.content.split('실험수정_체력방어력!!')[1].strip()
                if RepresentsInt(newHPArmor):
                    nukeTargetDict[message.guild].hpArmor = int(newHPArmor)
                    await message.channel.send(f'체력방어력 수정됨 : {nukeTargetDict[message.guild].hpArmor}')
                else:
                    await message.channel.send(f'방어력 수정됨 : {nukeTargetDict[message.guild].hpArmor}')
            elif message.content.startswith('실험수정_쉴드방어력!!'):
                newShieldArmor = message.content.split('실험수정_쉴드방어력!!')[1].strip()
                nukeTargetDict[message.guild].shieldArmor = int(newShieldArmor)
                await message.channel.send(f'쉴드방어력 수정됨 : {nukeTargetDict[message.guild].shieldArmor}')
            elif message.content.startswith('실험수정_타격위치!!'):
                newCoeffPosType = message.content.split('실험수정_타격위치!!')[1].strip()
                if newCoeffPosType in UnitData.CoeffPosTypes:
                    nukeTargetDict[message.guild].coeffPosType = newCoeffPosType
                    await message.channel.send(f'타격위치 수정됨 : {nukeTargetDict[message.guild].coeffPosType}')
                else:
                    await message.channel.send(f'타격위치 매개변수가 잘못되었습니다.\n 가능한 매개변수 : {CoeffPosTypes}')
            elif message.content.startswith('실험수정_유닛크기!!'):
                newCoeffScaleType = message.content.split('실험수정_유닛크기!!')[1].strip()
                if newCoeffScaleType in UnitData.CoeffScaleTypes:
                    nukeTargetDict[message.guild].coeffScaleType = newCoeffScaleType
                    await message.channel.send(f'유닛크기 수정됨 : {nukeTargetDict[message.guild].coeffScaleType}')
                else:
                    await message.channel.send(f'유닛크기 매개변수가 잘못되었습니다.\n 가능한 매개변수 : {CoeffScaleTypes}')
            elif message.content.startswith('실험수정_유닛회복!!'):
                nukeTargetDict[message.guild].Heal()
                await message.channel.send('유닛이 최대체력으로 회복되었습니다.')
            elif message.content.startswith('실험수정_기존유닛!!'):
                unitName = message.content.split('실험수정_기존유닛!!')[1].strip()
                unitInfo = UnitData.GetUnitInfo(unitName)
                if unitInfo is not None:
                    nukeTargetDict[message.guild].maxHP = unitInfo.HP
                    nukeTargetDict[message.guild].maxShield = unitInfo.Shield
                    nukeTargetDict[message.guild].hpArmor = unitInfo.HPArmor
                    nukeTargetDict[message.guild].coeffScaleType = unitInfo.coeffScaleType
                    nukeTargetDict[message.guild].Heal()
                    await message.channel.send(f'유닛이 {unitName}의 능력치로 수정되었습니다.')
                else:
                    await message.channel.send('등록되지 않은 유닛입니다.')
            elif message.content.startswith('실험수정_데미지맞춤!!'):
                goalDamage = message.content.split('실험수정_데미지맞춤!!')[1].strip()
                if RepresentsInt(goalDamage):
                    goalDamage = int(goalDamage)
                    baseHP, alphaHP = nukeTargetDict[message.guild].MakeHPforGoalDamage(goalDamage)
                    res = f'가능한 체력중 가장 낮은 체력으로 설정되었습니다.\n'
                    res += f'현재 실험에서 체력이 {goalDamage}만큼 깎이려면 기본체력이 {baseHP}가 되어야하며 {alphaHP}를 원하는 만큼 더하여 그 이상의 체력을 만들 수 있습니다.\n'
                    res += f'가능한 체력 예시)\n'
                    for i in range(3):
                        res += f' {baseHP + i*alphaHP}\n'
                    await message.channel.send(res)
                else:
                    await message.channel.send('데미지 입력이 잘못되었습니다.')
            elif message.content.startswith('실험수정_커스텀!!'):
                unitInfo = message.content.split('실험수정_커스텀!!')[1].strip()
                res = ''
                ## 체력
                if '체력=' in unitInfo:
                    newHP = unitInfo.split('체력=')[1].split(',')[0].strip()
                else:
                    newHP = None
                if newHP is not None:
                    splitRes = newHP.split('/')
                    if len(splitRes) > 2:
                        res += f'체력 매개변수 잘못됨. 양식 : 현재체력/최대체력 (현재체력 생략시 최대체력만 기입\n'
                    else:
                        if len(splitRes) == 2:
                            curHP, maxHP = splitRes[0:2]
                            curHP, maxHP = int(curHP), int(maxHP)
                        else:
                            maxHP = int(splitRes[0])
                            curHP = maxHP
                        nukeTargetDict[message.guild].curHP = curHP
                        nukeTargetDict[message.guild].maxHP = maxHP
                        res += f'체력={curHP} / {maxHP}\n'
                ## 실드
                if "쉴드=" in unitInfo:
                    newShield = unitInfo.split('쉴드=')[1].split(',')[0].strip()
                elif "실드=" in unitInfo:
                    newShield = unitInfo.split('실드=')[1].split(',')[0].strip()
                else:
                    newShield = None
                if newShield is not None:
                    splitRes = newShield.split('/')
                    if len(splitRes) > 2:
                        res += f'쉴드 매개변수 잘못됨. 양식 : 현재쉴드/최대쉴드 (현재쉴드 생략시 최대쉴드만 기입\n'
                    else:
                        if len(splitRes) == 2:
                            curShield, maxShield = splitRes[0:2]
                            curShield, maxShield = int(curShield), int(maxShield)
                        else:
                            maxShield = int(splitRes[0])
                            curShield = maxShield
                        nukeTargetDict[message.guild].curShield = curShield
                        nukeTargetDict[message.guild].maxShield = maxShield
                        res += f'실드={curShield} / {maxShield}\n'
                ## 체력방어력
                if "체력방어력=" in unitInfo:
                    newHPArmor = unitInfo.split('체력방어력=')[1].split(',')[0].strip()
                else:
                    newHPArmor = None
                if newHPArmor is not None:
                    if RepresentsInt(newHPArmor):
                        newHPArmor = int(newHPArmor)
                        nukeTargetDict[message.guild].hpArmor = newHPArmor
                        res += f'체력방어력={newHPArmor}\n'
                ## 실드방어력
                if "쉴드방어력=" in unitInfo:
                    newShieldArmor = unitInfo.split('쉴드방어력=')[1].split(',')[0].strip()
                elif "실드방어력=" in unitInfo:
                    newShieldArmor = unitInfo.split('실드방어력=')[1].split(',')[0].strip()
                else:
                    newShieldArmor = None
                if newShieldArmor is not None:
                    if RepresentsInt(newShieldArmor):
                        newShieldArmor = int(newShieldArmor)
                        nukeTargetDict[message.guild].shieldArmor = newShieldArmor
                        res += f'쉴드방어력={newShieldArmor}\n'
                ## 유닛크기
                if "유닛크기=" in unitInfo:
                    newScaleType = unitInfo.split('유닛크기=')[1].split(',')[0].strip()
                else:
                    newScaleType = None
                if newScaleType is not None:
                    if newScaleType in UnitData.CoeffScaleTypes:
                        nukeTargetDict[message.guild].coeffScaleType = newScaleType
                        res += f'유닛크기={newScaleType}\n'
                ## 타격위치
                if "타격위치=" in unitInfo:
                    newPosType = unitInfo.split('타격위치=')[1].split(',')[0].strip()
                else:
                    newPosType = None
                if newPosType is not None:
                    if newPosType in UnitData.CoeffPosTypes:
                        nukeTargetDict[message.guild].coeffPosType = newPosType
                        res += f'타격위치={newPosType}\n'
                await message.channel.send(res)
            await message.channel.send(nukeTargetDict[message.guild].GetInfo())
        elif message.content.startswith('실험저장목록!!'):
            testList =os.listdir('TestData\\' + str(message.guild))
            response = '==저장되어있는 실험들 목록=='
            for test in testList:
                response += '\n' + test
            await message.channel.send(response)
        elif message.content.startswith('실험저장!!'):
            TestName = message.content.split('실험저장!!')[1].strip()
            if TestName == "":
                await message.channel.send(f'저장할 이름이 공백입니다.')
            else:
                if nukeTargetDict[message.guild].Save(str(message.guild), TestName):
                    await message.channel.send(f'{TestName}으로 저장되었습니다.')
                else:
                    await message.channel.send('저장실패!')
        elif message.content.startswith('실험불러오기!!'):
            TestName = message.content.split('실험불러오기!!')[1].strip()
            if TestName == "":
                await message.channel.send(f'불러올 이름이 공백입니다.')
            else:
                res = nukeTargetDict[message.guild].Load(str(message.guild), TestName)
                if res is None:
                    await message.channel.send(f'{TestName}이 로드되었습니다.')
                    await message.channel.send(nukeTargetDict[message.guild].GetInfo())
                else:
                    await message.channel.send('불러오기 실패! : ' + res)
        elif message.content.startswith('업글정보!!'):
            await message.channel.send('현재 업그레이드 정보\n' + upgradeInfoDict[message.guild].GetInfo())
        elif message.content.startswith('업글수정_') and '!!' in message.content:
            if message.content.startswith('업글수정_초기비용!!'):
                newHP = message.content.split('업글수정_초기비용!!')[1].strip()
                splitRes = newHP.split('/')
                if len(splitRes) > 3:
                    await message.channel.send(f'초기비용 매개변수 잘못됨. 양식 : 미네랄/가스/시간 (뒤에서부터 하나씩 생략가능)')
                else:
                    mineral = -1
                    gas = -1
                    time = -1
                    if len(splitRes) == 3:
                        mineral, gas, time = splitRes[0:3]
                        mineral, gas, time = int(mineral), int(gas), int(time)
                    elif len(splitRes) == 2:
                        mineral, gas = splitRes[0:2]
                        mineral, gas = int(mineral), int(gas)
                    elif len(splitRes) == 1:
                        mineral = splitRes[0]
                        mineral = int(mineral)

                    if mineral != -1:
                        upgradeInfoDict[message.guild].baseCost_mineral = mineral
                    if gas != -1:
                        upgradeInfoDict[message.guild].baseCost_gas = gas
                    if time != -1:
                        upgradeInfoDict[message.guild].baseCost_time = time
                    await message.channel.send(f'초기비용 수정됨 : {upgradeInfoDict[message.guild].baseCost_mineral}M / {upgradeInfoDict[message.guild].baseCost_gas}G / {upgradeInfoDict[message.guild].baseCost_time}T')
            elif message.content.startswith('업글수정_추가비용!!'):
                newUpgradeFactor = message.content.split('업글수정_추가비용!!')[1].strip()
                splitRes = newUpgradeFactor.split('/')
                if len(splitRes) > 3:
                    await message.channel.send(f'추가비용 매개변수 잘못됨. 양식 : 미네랄/가스/시간 (뒤에서부터 하나씩 생략가능)')
                else:
                    mineral = -1
                    gas = -1
                    time = -1
                    if len(splitRes) == 3:
                        mineral, gas, time = splitRes[0:3]
                        mineral, gas, time = int(mineral), int(gas), int(time)
                    elif len(splitRes) == 2:
                        mineral, gas = splitRes[0:2]
                        mineral, gas = int(mineral), int(gas)
                    elif len(splitRes) == 1:
                        mineral = splitRes[0]
                        mineral = int(mineral)

                    if mineral != -1:
                        upgradeInfoDict[message.guild].upgradeFactor_mineral = mineral
                    if gas != -1:
                        upgradeInfoDict[message.guild].upgradeFactor_gas = gas
                    if time != -1:
                        upgradeInfoDict[message.guild].upgradeFactor_time = time
                    await message.channel.send(f'추가비용 수정됨 : {upgradeInfoDict[message.guild].upgradeFactor_mineral}M / {upgradeInfoDict[message.guild].upgradeFactor_gas}G / {upgradeInfoDict[message.guild].upgradeFactor_time}T')
            await message.channel.send(upgradeInfoDict[message.guild].GetInfo())
        elif '업글비용!!' in message.content:
            splitRes = message.content.split('부터')
            if len(splitRes) >= 2:
                startStr,endStr = splitRes[0:2]
                startUpgrade = int(re.search(r'\d+',startStr).group())
                endUpgrade = int(re.search(r'\d+',endStr).group())
                mineral, gas, time = upgradeInfoDict[message.guild].calcN2N(startUpgrade,endUpgrade)
                await message.channel.send(f'{startUpgrade}업부터 {endUpgrade}업까지의 비용 : {mineral}M / {gas}G / {time}T')
            elif len(splitRes) == 1:
                nUpgrade = int(re.search(r'\d+',splitRes[0]).group())
                mineral, gas, time = upgradeInfoDict[message.guild].GetUpgradeCost(nUpgrade)
                await message.channel.send(f'{nUpgrade}번째 업그레이드의 비용 : {mineral}M / {gas}G / {time}T')
        elif message.content.startswith('직업평가!!'):
            commentString = message.content.split('직업평가!!')[1].strip()
            print('commentString', commentString)
            charName = commentString.split(' ')[0].strip()
            content = commentString.split(charName)[1]
            content = content.split('\n')[0].strip()
            if charName == '네크로멘서':
                charName = '네크로맨서'
            print('charName', charName)
            print('content', content)
            print('author = ',message.author.display_name)
            print('content = ',content)
            if JuckPae.isCharacter(charName):
                if content == '':
                    await message.channel.send("내용이 없어 무시되었습니다.")
                else:
                    JuckPae.addComment(charName, JuckPae.Comment(message.author.display_name,content))
                    await message.channel.send("등록완료")
        elif message.content.startswith('직업목록!!'):
            await message.channel.send(JuckPae.getCharNames())
        elif message.content.endswith('!!'):
            charName = message.content.split('!!')[0]
            if charName == '네크로멘서':
                charName = '네크로맨서'
            if JuckPae.isCharacter(charName):
                comments = JuckPae.getComments(charName)
                if comments == "":
                    await message.channel.send("아직 작성된 코맨트가 없습니다.")
                else:    
                    await message.channel.send(comments)

try:
    with open('DiscordBot_Password.txt') as f:
        client.run(f.readline())
except:
    import traceback
    traceback.print_exc()