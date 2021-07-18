class NukeTargetInfo():
    def __init__(self):
        self.maxHP = 10000
        self.curHP = self.maxHP // 4 * 3
        self.maxShield = 5000
        self.curShield = self.maxShield // 4 * 3
        self.hpArmor = 100
        self.shieldArmor = 50
        self.coeffPosType = "직격"
        self.coeffScaleType = "중형"
        self.Dot5 = False
        
    def GetCoeffPosValue(self):
        if self.coeffPosType == '직격':
            return 1.
        elif self.coeffPosType == '빗맞음':
            return 0.5
        elif self.coeffPosType == '맞았나':
            return 0.25
        else:
            return -1
    def GetCoeffScaleValue(self):
        if self.coeffScaleType == '소형':
            return 0.5
        elif self.coeffScaleType == '중형':
            return 0.75
        elif self.coeffScaleType == '대형':
            return 1.0
        else:
            return -1
    
    def GetInfo(self):
        res = f'체력 : {self.curHP} / {self.maxHP}, 방어력 : {self.hpArmor}\n'
        res += f'쉴드 : {self.curShield} / {self.maxShield}, 방어력 : {self.shieldArmor}\n'
        res += f'유닛크기 : {self.coeffScaleType}\n'
        res += f'타격위치 : {self.coeffPosType}'
        return res
    def Damage(self, bIncludeDetail = False):
        res = ''
        coeffPosValue = self.GetCoeffPosValue()
        if coeffPosValue == -1 : return 1
        if bIncludeDetail:
            res += '일단 몇가지 계수들을 먼저 계산해둘게\n'
            res += f'{self.coeffPosType}으로 맞았으니 총 데미지를 계산할때 {coeffPosValue}만큼 곱해줄꺼야.\n'
        coeffScaleValue = self.GetCoeffScaleValue()
        if coeffScaleValue == -1 : return 1
        if bIncludeDetail:
            res += f'유닛 크기가 {self.coeffScaleType}이니 나중에 상성을 계산할때 {coeffScaleValue}만큼 곱해줄꺼야.\n'
        
        totalMaxHP = self.maxHP + self.maxShield
        if bIncludeDetail:
            res += f'1. 우선 최대체력이 {self.maxHP}이고 최대쉴드량이 {self.maxShield}이니 대상의 총 최대체력은 {totalMaxHP}이야\n'
        if totalMaxHP >= 750:
            totalDamage = totalMaxHP * 2. / 3. * coeffPosValue
            if bIncludeDetail:
                res += f'2. 체력이 750이상이니 총 데미지는 총 최대체력에 2/3를 곱하고 위에서 계산해둔 거리에 따른 계수 {coeffPosValue}를 곱해서 {totalDamage}가 나와.\n'
        else:
            totalDamage = 500*coeffPosValue
            if bIncludeDetail:
                res += f'2. 체력이 750미만이니 총 데미지는 500에 위에서 계산해둔 거리에 따른 계수 {coeffPosValue}를 곱해서 {totalDamage}가 나와.\n'
        
        if self.curShield > 0:
            if (self.curShield + self.shieldArmor) > totalDamage: # 쉴드선에서 막힌다.
                remainShield = (self.curShield + self.shieldArmor) - int(totalDamage)
                remainHP = self.curHP
                totalDamage = 0
                if bIncludeDetail:
                    res += f'3. 현재 쉴드량이 {self.curShield}이고 쉴드방어력이 {self.shieldArmor}이니 핵 데미지가 쉴드를 뚫지못해.\n'
                    res += f'   결국 쉴드는 {remainShield}만큼 남고 체력은 그대로 {remainHP}가 돼.\n'
            else:
                remainShield = 0
                totalDamage -= (self.curShield + self.shieldArmor) # 쉴드로 막고 남은 데미지 갱신
                if bIncludeDetail:
                    res += f'3. 현재 쉴드량이 {self.curShield}이고 쉴드방어력이 {self.shieldArmor}이니 핵 데미지가 쉴드를 뚫고도 남아.\n'
                    res += f'   결국 쉴드는 {remainShield}이 되고 남은 데미지인 {totalDamage}가 체력을 깎을 거야.\n'
        else:
            remainShield = 0
            if bIncludeDetail:
                res += f'3. 쉴드가 없으니 그대로 총 데미지인 {totalDamage}가 체력을 깎을 거야.\n'
        if totalDamage > 0:
            # 체력이 남은 데미지를 받는다.
            hpDamage = int((totalDamage - self.hpArmor)*coeffScaleValue) % 65536
            if bIncludeDetail:
                res += f'4. 체력이 입는 데미지는 총 데미지 에서 방어력만큼 뺀 뒤에 위에서 계산해둔 유닛크기에 따른 계수를 곱해주고 데미지의 최대치가 65535이므로 65536으로 나머지 연산을 하면 돼.\n'
                res += f'   식으로 표현하면 (({totalDamage} - {self.hpArmor})*{coeffScaleValue}) % 65536 이고 계산결과는 {hpDamage}야.\n'
            if hpDamage == 0:
                if self.Dot5:
                    self.Dot5 = False
                    hpDamage += 1
                    if bIncludeDetail:
                        res += f'   데미지가 0이므로 0.5만큼 데미지가 들어가 이미 체력이 0.5 달았었으니 체력이 1깎인것처럼 보여.'
                else:
                    self.Dot5 = True
                    if bIncludeDetail:
                        res += f'   데미지가 0이므로 0.5만큼 데미지가 들어가 아직은 체력이 그대로 표시돼.'
            remainHP = self.curHP - hpDamage
            if bIncludeDetail:
                res += f'   그러면 결국 남은 체력은 {self.curHP} - {hpDamage} 로 {remainHP}가 돼.\n   어때 간단하지?\n\n'
        res += f'쉴드에 가해진 데미지 : {self.curShield - remainShield}\n'
        res += f'체력에 가해진 데미지 : {self.curHP - remainHP}\n'
        if remainHP < 0:
            remainHP = 0
        res += f'남은 쉴드 : {remainShield}\n'
        res += f'남은 체력 : {remainHP}\n'
        if remainHP == 0:
            res += '죽었다 ㅠㅠ'
        else:
            res += '살았다!'
        self.curShield = remainShield
        self.curHP = remainHP
        return res
    def Heal(self):
        self.curHP = self.maxHP
        self.curShield = self.maxShield
    def Save(self, guildName, fileName):
        try:
            f = open('TestData\\' + guildName + '\\' + fileName,'wt',encoding='utf-8')
            f.write(f'{self.curHP}\n')
            f.write(f'{self.maxHP}\n')
            f.write(f'{self.curShield}\n')
            f.write(f'{self.maxShield}\n')
            f.write(f'{self.hpArmor}\n')
            f.write(f'{self.shieldArmor}\n')
            f.write(f'{self.coeffPosType}\n')
            f.write(f'{self.coeffScaleType}\n')
            f.close()
            return True
        except:
            import traceback
            traceback.print_exc()
            return False
    def Load(self, guildName, fileName):
        try:
            f = open('TestData\\' + guildName + '\\' +  fileName,'rt',encoding='utf-8')
            lines = f.readlines()
            if len(lines) != 8:
                return '잘못된 실험입니다.'
            self.curHP = int(lines[0])
            self.maxHP = int(lines[1])
            self.curShield = int(lines[2])
            self.maxShield = int(lines[3])
            self.hpArmor = int(lines[4])
            self.shieldArmor = int(lines[5])
            self.coeffPosType = lines[6].strip()
            self.coeffScaleType = lines[7].strip()
            f.close()
            return None
        except:
            import traceback
            traceback.print_exc()
            return '해당이름의 실험이 없습니다.'
    def MakeHPforGoalDamage(self, goalDamage):
        coeffPosValue = self.GetCoeffPosValue()
        coeffScaleValue = self.GetCoeffScaleValue()
        baseHP = int(3/(2.*coeffPosValue)*(goalDamage / coeffScaleValue + self.hpArmor))
        alphaHP = int(98304 / (coeffPosValue*coeffScaleValue))
        if self.maxShield > 0:
            if baseHP <= self.maxShield:
                baseHP += alphaHP
            baseHP -= self.maxShield
        if baseHP < 750:
            baseHP += alphaHP
        self.maxHP = baseHP
        self.curHP = self.maxHP
        return baseHP, alphaHP
