CoeffPosTypes = (
    '직격', '빗맞음', '맞았나'
)
CoeffScaleTypes = (
    '소형', '중형', '대형'
)
class UnitInfo:
    def __init__(self, hp, shield, armor, scale):
        self.HP = hp
        self.Shield = shield
        self.HPArmor = armor
        self.coeffScaleType = scale

unitSet = {
    'Terran Marine' : UnitInfo(hp=40, shield=0, armor=0, scale='소형'),
    'Terran Battlecruiser' : UnitInfo(hp=500, shield=0, armor=3, scale='대형'),
    'Terran Supply Depot' : UnitInfo(hp=500, shield=0, armor=1, scale='대형'),
}
def GetUnitInfo(unitName):
    try:
        return unitSet[unitName]
    except:
        return None