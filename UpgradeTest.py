class UpgradeInfo():
    def __init__(self):
        self.baseCost_mineral = 100
        self.baseCost_gas = 100
        self.baseCost_time = 266
        self.upgradeFactor_mineral = 50
        self.upgradeFactor_gas = 50
        self.upgradeFactor_time = 32
    def GetInfo(self):
        res = f'초기비용 : {self.baseCost_mineral}M / {self.baseCost_gas}G / {self.baseCost_time}T\n'
        res += f'1단계당 추가비용 : {self.upgradeFactor_mineral}M / {self.upgradeFactor_gas}G / {self.upgradeFactor_time}T\n'
        return res
    def GetUpgradeCost(self, n):
        return self.baseCost_mineral + (n-1)*self.upgradeFactor_mineral, self.baseCost_gas + (n-1)*self.upgradeFactor_gas, self.baseCost_time + (n-1)*self.upgradeFactor_time
    def calcN2N(self, startUpgrade, endUpgrade):
        all_mineral = 0
        all_gas = 0
        all_time = 0

        while startUpgrade <= endUpgrade:
            mineral, gas, time = self.GetUpgradeCost(startUpgrade)
            all_mineral += mineral
            all_gas += gas
            all_time += time
            startUpgrade += 1
        return all_mineral,all_gas,all_time
        