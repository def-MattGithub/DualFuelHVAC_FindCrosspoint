import pandas as pd
from sklearn.linear_model import LinearRegression


"""---Start Global Variables---"""
CostPerTherm = 2.21
CostPerKWH = .34

# setup variables
AFUE = 80
DataHi = (45, 3.62)
DataLo = (17, 2.44)
"""---End Global Variables---"""


def FindCOP(outtemp, datahi, datalo):
    if outtemp != None:
        df = pd.DataFrame({'Temp': [datahi[0], datalo[0]],
                        'COP': [datahi[1], datalo[1]]})
        model = LinearRegression()
        model.fit(df[['Temp']], df['COP'])
        modelCoef = model.coef_[0]
        modelIncpt = model.intercept_
        outFloat = float(outtemp)
        calc = modelCoef * outFloat + modelIncpt
        return calc


def AFUEloss(afue):
    if 70 <= afue <= 98:
        afueloss = (1 - (afue * 0.01)) + 1
        return afueloss
    else:
        exit(0)


def TempToCOPDict(outlow, outhigh, granularity):
    outhigh = outhigh + 1
    temp = 0
    result = {}
    for temp in range(outlow, outhigh, granularity):
            COP = FindCOP(temp, DataHi, DataLo)
            result.update({temp: COP})
            temp += granularity
    return result

def PumpOrBurn(costtherm, costelec, cop, afueloss):
    ThermtokWH = (costtherm / 29.3)
    WithLoss = (ThermtokWH * afueloss)
    ElectricEquiv = (WithLoss * cop)
    diff = float(ElectricEquiv - costelec)
    if diff >= float(0):
        return 'Pump'
    elif diff < float(0):
        return 'Burn'
    else:
        exit(1)


AFUECalc = AFUEloss(AFUE)
COPTable = TempToCOPDict(-20, 75, 5)


def FindCrosspoint():
    Calc = ''
    for key in COPTable.keys():
        Calc = PumpOrBurn(CostPerTherm, CostPerKWH, COPTable.get(key), AFUECalc)
        if Calc == 'Pump':
            return key


Result = FindCrosspoint()
print(Result)
