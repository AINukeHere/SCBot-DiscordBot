botVersion = 1.04

BotInfoMessage = f'SCBot {botVersion}\n'
BotInfoMessage += '1.03 패치내역\n'
BotInfoMessage += '핵 데미지가 중형인 유닛에게 데미지가 잘못 들어가던 문제 해결\n'
BotInfoMessage += '1.04 패치내역\n'
BotInfoMessage += '핵 데미지로 쉴드를 다 못깎는 상황인데 체력이 깍여버리는 문제 해결\n'
BotInfoMessage += 'made by 천재일까'
helpMessage = ''
helpMessage += '명령어 목록 (명령어 뒤에 help를 입력하면 도움말을 볼 수 있습니다.\n'
helpMessage += '1. 핵 실험 (원하는 상황을 만들어 핵을 쏴볼 수 있습니다.)\n'
helpMessage += '```\n'
NukeTestCommandHelpDict={
    '실험정보!!':'```실험정보!!```\n현재 핵을 어떤 상황에서 쏠 것인지를 보여줍니다.',
    '핵을쏴라!!':'```핵을쏴라!! [설명] [죽을때까지] [결과만]```\n현재실험환경에서 핵을 쏩니다.\n"결과만" 옵션은 "죽을때까지" 옵션이 있어야합니다.\n사용예) 핵을쏴라!! 설명\n사용예2) 죽을때까지 핵을쏴라!!',
    '실험수정_체력!!':'```실험수정_체력!! 현재체력[/최대체력]```\n핵 맞을 유닛의 현재체력 및 최대체력을 설정합니다.\n사용예) 실험수정_체력!! 60/80 (현재체력 생략시 최대체력만 기입)',
    '실험수정_쉴드!!':'```실험수정_쉴드!! 현재쉴드[/최대쉴드]```\n핵 맞을 유닛의 현재쉴드 및 최대쉴드를 설정합니다.\n사용예) 실험수정_쉴드!! 60/60 (현재쉴드 생략시 최대쉴드만 기입)',
    '실험수정_체력방어력!!':'```실험수정_체력방어력!! 체력방어력```\n핵 맞을 유닛의 체력방어력을 설정합니다.\n사용예) 실험수정_체력방어력!! 100',
    '실험수정_쉴드방어력!!':'```실험수정_쉴드방어력!! 쉴드방어력```\n핵 맞을 유닛의 쉴드방어력을 설정합니다.\n사용예) 실험수정_쉴드방어력!! 50',
    '실험수정_타격위치!!':'```실험수정_타격위치!! 타격위치```\n핵 발사지점으로부터 해당유닛이 얼마나 멀리 떨어져있는지를 설정합니다. 타격위치는 [직격/빗맞음/맞았나] 중 하나입니다.\n사용예) 실험수정_타격위치!! 직격',
    '실험수정_유닛크기!!':'```실험수정_유닛크기!! 유닛크기```\n핵 맞을 유닛의 유닛크기를 설정합니다. 유닛크기는 [소형/중형/대형] 중 하나입니다.\n사용예) 실험수정_유닛크기!! 중형',
    '실험수정_유닛회복!!':'```실험수정_유닛회복!!```\n핵 맞을 유닛의 체력과 쉴드를 최대값으로 설정합니다.',
    '실험수정_데미지맞춤!!':'```실험수정_데미지맞춤!! 데미지```\n현재 체력을 제외한 실험환경에서 핵의 데미지가 원하는 만큼 들어가도록 하기 위한 체력들을 나열하고 최소체력으로 맞춰줍니다.\n사용예) 실험수정_데미지맞춤!! 1000',
    '실험수정_커스텀!!':'```실험수정_커스텀!! [능력치명=능력치값],[능력치명=능력치값],...,[능력치명=능력치값]```\n핵 맞을 유닛의 능력치들을 한번에 수정할 수 있는 명령어입니다. [능력치명=능력치정보]를 ,로 구분하여 나열하면 됩니다.\n사용예) 실험수정_커스텀!! 체력=123/456, 쉴드=789, 쉴드방어력=255, 체력방어력=400',
    '실험저장!!':'```실험저장!! 이름```\n현재 설정된 실험환경을 특정이름으로 저장합니다.\n사용예) 실험저장!! 최종보스',
    '실험불러오기!!':'```실험불러오기!! 이름```\n저장해둔 실험환경을 불러옵니다.\n사용예) 실험불러오기!! 최종보스',
    '실험저장목록!!':'```실험저장목록!!```\n저장되어있는 실험환경들을 출력합니다.',
}
for command in NukeTestCommandHelpDict:
    helpMessage += command + ' '
helpMessage += '```\n'
helpMessage += '2. 업글 비용 계산 (원하는 업그레이드정보에서 특정구간의 비용을 계산합니다.\n'
helpMessage += '```\n'
UpgradeTestCommandHelpDict={
    '업글정보!!':'```업글정보!!```\n현재의 업그레이드 정보를 보여줍니다.',
    '업글수정_초기비용!!':'```업글수정_초기비용!! 미네랄[/가스][/시간]```\n업그레이드의 초기비용(1업 비용)을 설정합니다. (뒤에서부터 하나씩 생략가능합니다.)\n사용예) 업글수정_초기비용!! 100/200/0\n사용예) 업글수정_초기비용!! 100',
    '업글수정_추가비용!!':'```업글수정_추가비용!! 미네랄[/가스][/시간]```\n업그레이드의 추가비용을 설정합니다. (뒤에서부터 하나씩 생략가능합니다.)\n사용예) 업글수정_추가비용!! 100/200/0\n사용예) 업글수정_추가비용!! 100',
    'n업업글비용!!':'```n업업글비용!!```\n특정 업그레이드의 비용을 보여줍니다.\n사용예) 25업 업글비용!!',
    'n업부터m업까지 업글비용!!':'```n업부터m업까지 업글비용!!```\n특정수치부터 특정수치까지의 업그레이드 비용을 보여줍니다.\n사용예) 10업부터 20업까지 업글비용!!'
}
for command in UpgradeTestCommandHelpDict:
    helpMessage += command + ' '
helpMessage += '```\n'
helpMessage += '3. 기타\n'
helpMessage += '```\n'
helpMessage += 'SCMD2_최신버전!! '
helpMessage += '봇정보!! '
helpMessage += '```\n'

teampleRPG_message = '4. 팀플RPG 전용\n'
teampleRPG_message += '```\n'
TeampleRPG_CommandHelpDict={
    '팀알_최신버전!!':'```팀알_최신버전!!```\n팀플RPG의 최신버전을 보여줍니다.',
    '직업평가!!':'```직업평가!! [직업이름] [코맨트]```\n특정 직업에 간단한 코맨트를 답니다. [직업이름]!! 으로 해당 직업의 코맨트들을 볼 수 있습니다.',
}
for command in TeampleRPG_CommandHelpDict:
    teampleRPG_message += command + ' '
teampleRPG_message += '직업목록!! '
teampleRPG_message += '[직업이름]!! '
teampleRPG_message += '```\n'