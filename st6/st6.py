import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 



#read data
def readData(filename):
    return pd.read_csv(filename)
    
    
def iterateData():
    dfdict = {}
    filedict = {}
    for directory in os.listdir("./data/"):
        dflst = []
        filelst = []
        for filename in os.listdir("./data/"+directory):
            print(f"Reading {filename} ")
            dflst.append(readData("./data/"+directory+"/"+filename))
            filelst.append(filename)
        dfdict[directory] = dflst
        filedict[directory] = filelst
    return dfdict, filedict

def meanDict(df, filename, slicedf=None, example=False):
    if not example:
        if slicedf:
            df = df.loc[df['time'] < slicedf]
        if list(df.keys()) == ['time', ' Feed Pressure [bara]','time.1', ' Permeate Pressure [bara]', 'time.2',' Retentate Pressure [bara]', 'time.3', ' O_2  Permeate [%]', 'time.4', ' O_2 Retentate [%]', 'time.5', ' Flow Meter [l/min]','time.6', ' Flow Controller Range (0-50 SLPM) [l/min]']:
            d = {
                'filename': filename,
                'Feed Pressure [Pa]': df[' Feed Pressure [bara]'].mean() * 10**5,
                'Permeate Pressure [Pa]': df[' Permeate Pressure [bara]'].mean() * 10**5,
                'Retentate Pressure [Pa]': df[' Retentate Pressure [bara]'].mean() * 10**5,
                'O_2  Permeate': df[' O_2  Permeate [%]'].mean()/100,
                'O_2 Retentate': df[' O_2 Retentate [%]'].mean()/100,
                'Permeate flow [m^3/s]': df[' Flow Meter [l/min]'].mean() * (10**(-3)/60),
                'Retentate flow [m^3/s]': df[' Flow Controller Range (0-50 SLPM) [l/min]'].mean() * (10**(-3)/60),
                }
            return d
        else:
            print("ERROR invalid keys in csv file")
            return {'filename': filename}
    else:
        return {
                'filename': "testfile",
                'Feed Pressure [Pa]': 4.7 * 10**5,
                'Permeate Pressure [Pa]': 0.9 * 10**5,
                'Retentate Pressure [Pa]': 4.6 * 10**5,
                'O_2  Permeate': 40.7/100,
                'O_2 Retentate': 16/100,
                'Permeate flow [m^3/s]': 4.1 * (10**(-3)/1),#permeate flow
                'Retentate flow [m^3/s]': 21.3 * (10**(-3)/1),#rententate flow
                }

        

#formulas

def massBalance(V_r, V_p):
    return V_r + V_p

def yN(yO):
    return 1-yO

def componentBalanceYf(V_f,V_p, V_r,y_r_c,y_p_c):
    return (V_p*y_p_c+V_r*y_r_c)/V_f

def cutRate(V_p, V_f):
    return V_p/V_f

def pressureRatio(p_f, p_p):
    return p_f/p_p

def recovery(y_rp_c,V_rp, y_f_c, V_f):
    return (y_rp_c * V_rp)/(y_f_c * V_f)

def example():
    d = meanDict(None,None,example=True)
    d['Feed flow [m^3/s]'] = massBalance(d['Retentate flow [m^3/s]'], d['Permeate flow [m^3/s]'])
    d['N_2  Permeate'] = yN(d['O_2  Permeate'])
    d['N_2  Retentate'] = yN(d['O_2 Retentate'])
    d['O_2  Feed'] = componentBalanceYf(d['Feed flow [m^3/s]'],d['Permeate flow [m^3/s]'], d['Retentate flow [m^3/s]'],d['O_2 Retentate'],d['O_2  Permeate'])
    d['N_2  Feed'] = componentBalanceYf(d['Feed flow [m^3/s]'],d['Permeate flow [m^3/s]'], d['Retentate flow [m^3/s]'],d['N_2  Retentate'],d['N_2  Permeate'])
    d['Cut rate'] = cutRate(d['Permeate flow [m^3/s]'], d['Feed flow [m^3/s]'])
    d['Pressure ratio'] = pressureRatio(d['Feed Pressure [Pa]'], d['Permeate Pressure [Pa]'])
    d['Recovery O_2'] = recovery(d['O_2  Permeate'],d['Permeate flow [m^3/s]'], d['O_2  Feed'], d['Feed flow [m^3/s]'])
    d['Recovery N_2'] = recovery(d['N_2  Retentate'],d['Retentate flow [m^3/s]'], d['N_2  Feed'], d['Feed flow [m^3/s]'])
    print()
    for key,value in d.items():
        print(key, "    ", value)
        
def addToDict(d):
    d['Feed flow [m^3/s]'] = massBalance(d['Retentate flow [m^3/s]'], d['Permeate flow [m^3/s]'])
    d['N_2  Permeate'] = yN(d['O_2  Permeate'])
    d['N_2  Retentate'] = yN(d['O_2 Retentate'])
    d['O_2  Feed'] = componentBalanceYf(d['Feed flow [m^3/s]'],d['Permeate flow [m^3/s]'], d['Retentate flow [m^3/s]'],d['O_2 Retentate'],d['O_2  Permeate'])
    d['N_2  Feed'] = componentBalanceYf(d['Feed flow [m^3/s]'],d['Permeate flow [m^3/s]'], d['Retentate flow [m^3/s]'],d['N_2  Retentate'],d['N_2  Permeate'])
    d['Cut rate'] = cutRate(d['Permeate flow [m^3/s]'], d['Feed flow [m^3/s]'])
    d['Pressure ratio'] = pressureRatio(d['Feed Pressure [Pa]'], d['Permeate Pressure [Pa]'])
    d['Recovery O_2'] = recovery(d['O_2  Permeate'],d['Permeate flow [m^3/s]'], d['O_2  Feed'], d['Feed flow [m^3/s]'])
    d['Recovery N_2'] = recovery(d['N_2  Retentate'],d['Retentate flow [m^3/s]'], d['N_2  Feed'], d['Feed flow [m^3/s]'])
    return d
    
def meanDataLst(dlist):
    lstDict = {}
    for key in dlist[0].keys():
        lstDict[key] = []
    for d in dlist:
        for key in d:
            lstDict[key].append(d[key])
    return lstDict
        
def plot(plotKeys,lstlistDict):
    
    for d in plotKeys:
        for i in range(len(d["y"])):
            if d["type"] == "plot":
                for listDict in lstlistDict:
                    plt.plot(listDict[d["x"][0]], listDict[d["y"][i]], label=d["y"][i])
            elif d["type"] == "scatter":
                for listDict in lstlistDict:
                    plt.scatter(listDict[d["x"][0]], listDict[d["y"][i]])
        plt.xlabel(d["x"][0])
        plt.ylabel(d["y"][i])
        plt.legend()
        plt.grid()
        plt.show()
    
def plotLstKeys():
    #{"x": [""], "y":[""]}
    return [{"x": ["Pressure ratio"], "y":["O_2  Permeate", "N_2  Permeate"], "type": "plot"},{"x": ["Pressure ratio"], "y":["Recovery O_2", "Recovery N_2"], "type": "plot"}, {"x": ["Cut rate"], "y":["O_2  Permeate", "N_2  Permeate"], "type": "plot"}, {"x": ["Cut rate"], "y":["Recovery O_2", "Recovery N_2"], "type": "plot"},{"x": ["O_2  Permeate"], "y":["Recovery O_2", "Recovery N_2"], "type": "plot"}]

def createDataDict():
    dDict = {}
    lstlistDict = []
    dfdict, filedict = iterateData()
    print(filedict)
    for key, dflist in dfdict.items():
        dlst = []
        
        for count, df in enumerate(dflist):
            d = meanDict(df,filedict[key][count])
            d = addToDict(d)
            dlst.append(d)
        #for i in dlst:
            #print(i)
        dDict[key] = dlst
        lstlistDict.append(meanDataLst(dlst))
    return lstlistDict

def main():
    lstlistDict = createDataDict()
    listDictSerie={}
    for i, d in enumerate(lstlistDict):
        if "single" in d["filename"][0]:
            listDictSerie = lstlistDict.pop(i)
            
    print(lstlistDict)
            
    
        

    plotKeys = plotLstKeys()
    plot(plotKeys,lstlistDict)
    
    #example()
    
    
    
main()