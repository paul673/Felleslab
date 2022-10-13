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
    color = [[(255/255,0/255,0/255),(170/255,0/255,0/255)],[(0/255,255/255,0/255),(0/255,170/255,0/255)],[(0/255,0/255,255/255),(0/255,0/255,170/255)],[(255/255,255/255,0/255),(170/255,170/255,0/255)],[(0/255,255/255,255/255),(0/255,170/255,170/255)]]
    for d in plotKeys:
        for i in range(len(d["y"])):
            if d["type"] == "plot":
                for j, listDict in enumerate(lstlistDict):
                    parallel = listDict["filename"][0].replace("_1.csv", "").replace("1.csv", "").replace("_", " ")
                    if "single" in parallel:
                        plt.scatter(listDict[d["x"][0]], listDict[d["y"][i]], label=d["label"][i]+" "+parallel, color=color[j][i])
                    else:
                        plt.plot(listDict[d["x"][0]], listDict[d["y"][i]], label=d["label"][i]+" "+parallel, color=color[j][i])
            elif d["type"] == "scatter":
                for listDict in lstlistDict:
                    parallel = listDict["filename"][0].replace("_1.csv", "").replace("1.csv", "").replace("_", " ")
                    plt.scatter(listDict[d["x"][0]], listDict[d["y"][i]], label=d["label"][i]+" "+parallel, color=color[j][i])
        plt.xlabel(d["axis"][0])
        plt.ylabel(d["axis"][1])
        plt.legend()
        plt.grid()
        plt.show()
    
def plotLstKeys():
    #{"x": [""], "y":[""]}
    return [
        {"x": ["Pressure ratio"], "y":["O_2  Permeate"],"type": "plot", "label": [r"O$_2$  Permeate"], "axis": [r"Pressure ratio",r"O$_2$  Permeate (purity)"]},
        {"x": ["Pressure ratio"], "y":["N_2  Retentate"],"type": "plot", "label": [r"N$_2$  Retentate"], "axis": [r"Pressure ratio",r"N$_2$  Retentate (purity)"]},
        {"x": ["Pressure ratio"], "y":["Recovery O_2", "Recovery N_2"],"type": "plot", "label": [r"Recovery O$_2$", r"Recovery N$_2$"], "axis": [r"Pressure ratio",r"Recovery"]},
        {"x": ["Cut rate"], "y":["O_2  Permeate"],"type": "plot", "label": [r"O$_2$  Permeate"], "axis":  [r"Cut rate",r"O$_2$  Permeate (purity)"]},
        {"x": ["Cut rate"], "y":["N_2  Retentate"],"type": "plot", "label": [r"N$_2$ Retentate"], "axis":  [r"Cut rate",r"N$_2$ Retentate (purity)"]},
        {"x": ["Cut rate"], "y":["Recovery O_2", "Recovery N_2"], "type": "plot", "label": [r"Recovery O$_2$", r"Recovery N$_2$"], "axis": [r"Cut rate",r"Recovery"]},
        {"x": ["O_2  Permeate"], "y":["Recovery O_2"], "type": "plot", "label": [r"Recovery O$_2$"], "axis": [r"O$_2$ Permeate (purity)",r"Recovery O$_2$"]},
        {"x": ["N_2  Retentate"], "y":["Recovery N_2"], "type": "plot", "label": [r"Recovery N$_2$"], "axis": [r"N$_2$ Retentate (purity)",r"Recovery N$_2$"]}
        ]

def createDataDict():
    dDict = {}
    lstlistDict = []
    dfdict, filedict = iterateData()
    #print(filedict)
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

def scatterParallels(listDictSerie):
    for key, value in listDictSerie.items():
        if type(value[0]) == np.float64:
            print(key, value, "mean: ",round(np.mean(value),5), "std: ", round(np.std(value),5))
        else:
            print(key, value)
    return

def main():
    lstlistDict = createDataDict()
    listDictSingle={}
    listDictSerie ={}
    listDictParallel3 ={}
    listDictParallel4 ={}
    for i, d in enumerate(lstlistDict):
        if "single" in d["filename"][0]:
            #listDictSingle = lstlistDict.pop(i)
            listDictSingle = lstlistDict[i]
        elif "serie" in d["filename"][0]:
            listDictSerie = lstlistDict[i]
        elif "parallel_4" in d["filename"][0]:
            listDictParallel4 = lstlistDict[i]
        elif "parallel_3" in d["filename"][0]:
            listDictParallel3 = lstlistDict[i]
    scatterParallels(listDictSingle)  
    #print(lstlistDict)
            
    
        
    
    plotKeys = plotLstKeys()
    plot(plotKeys,lstlistDict)
    
    #example()
    
    
    
main()