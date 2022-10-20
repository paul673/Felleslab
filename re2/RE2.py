import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root


#constants
V_tot    = 0.35 #L
c0_NaOH  = 1 #mol/l
rho_NaOH = 1040 #g/l
rho_DMSO = 1100 #g/l
rho_H2O  = 997 #g/L
rho_C2H5I = 1.940*1000 #g/l
rho_HCl = rho_H2O #0.01 M almost water CHECK!!
Mm_C2H5I = 155.966 #g/mol
Mm_DMSO  = 78.13 #g/mol
Mm_H2O   = 18.02 #g/mol
Mm_HCl = 36.458 #g/mol
c1_NaOH = 0.06  # mol/l
x_DMSO  = np.array([0.2, 0.4, 0.6]) #molfraction
V_sample = 5/1000 #l




def measurements():
     return [{
        "m_NaOH": 21.8,
        "m_DMSO": 179.31,
        "m_H2O": 165.5,
        "m_C2H5I": 3.29, 
        "t": np.array([0,45,110,155,200,245,290,355,405,455,495]), #s 540 second wrong
        "V_HCl": np.array([28.2,29.5,28.2,29.2,28.6,28.9,28.6,28.7,28.7,28.9,29.2])/1000 #l
        },
           {
        "m_NaOH": 21.75,
        "m_DMSO": 261.52,
        "m_H2O": 90.55,
        "m_C2H5I": 3.28, 
        "t": np.array([0,45,90,135,180,225,270,317,360,405,450,495]),
        "V_HCl": np.array([28.3,28.8,28.4,28.4,28.3,27.7,27.8,27.6,26.8,26.2,26.6,26.5])/1000
        },
    {
        "m_NaOH": 21.79,
        "m_DMSO": 309.36,
        "m_H2O": 47.58,
        "m_C2H5I": 3.30, 
        "t": np.array([0,45,90,135,180,225,270,315,360,405,449,495]),
        "V_HCl": np.array([28.7,27.0,24.8,23.2,21.8,19.6,18.6,17.1,16.2,15.1,14.4,13.2])/1000
        }]
    
def calculateParameters(measurementlst):
    for m in measurementlst:
        m["V_NaOH"] = m["m_NaOH"]/rho_NaOH
        m["V_DMSO"] = m["m_DMSO"]/rho_DMSO
        m["V_H2O"] = m["m_H2O"]/rho_H2O
        m["V_C2H5I"] = m["m_C2H5I"]/rho_C2H5I
        m["V_tot"] = m["V_NaOH"] + m["V_DMSO"] + m["V_H2O"] + m["V_C2H5I"]
        m["n_NaOH sample"] = m["V_HCl"]*rho_HCl/Mm_HCl
        m["C_OH sample"] = m["n_NaOH sample"]/V_sample
    return measurementlst


def eq(unknown, index):
    V_DMSO = unknown[0]
    V_NaOH = unknown[1]
    m_NaOH = unknown[2]
    V_H2O = unknown[3]
    m_H2O = unknown[4]
    n_H2O = unknown[5]
    n_DMSO = unknown[6]
    m_DMSO = unknown[7]
    eq1 = ((c1_NaOH*V_tot)/c0_NaOH) -V_NaOH
    eq2 = (V_NaOH*rho_NaOH) - m_NaOH
    eq3 = (V_tot - V_DMSO - V_NaOH) - V_H2O
    eq4 = (V_H2O*rho_H2O) - m_H2O
    eq5 = (m_H2O/Mm_H2O) - n_H2O
    eq6 = ((n_H2O*x_DMSO[index])/(1-x_DMSO[index])) - n_DMSO
    eq7 = (n_DMSO*Mm_DMSO) - m_DMSO
    eq8 = (m_DMSO/rho_DMSO) - V_DMSO
    #print(np.array([eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8]))
    return np.array([eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8])

def singlePlot(measurementlst, pltdict, colorlst, show=True, save=False):
    x_key = pltdict["x_key"]
    y_key = pltdict["y_key"]
    x_eq = pltdict["x_eq"]
    y_eq = pltdict["y_eq"]
    x_str = pltdict["x_str"]
    y_str = pltdict["y_str"]
    xlabel = pltdict["xlabel"]
    ylabel = pltdict["ylabel"]
    filename = pltdict["filename"]
    for i, m in enumerate(measurementlst):
        x = x_eq(m[x_key])
        y = y_eq(m[y_key])
        color = colorlst[i][0]
        a,b = np.polyfit(x,y, deg=1)
        r2 = (np.corrcoef(x,y=y)[0,1])**2
        roundindex = 8
        if b >= 0:
            label = y_str + r" = "+ str(round(a,roundindex))+" "+x_str+r" + "+str(round(b,roundindex)) + ",   R$^2$ = " + str(round(r2,roundindex))
        else:
           label = y_str + r" = "+ str(round(a,roundindex))+" "+x_str+r" - "+str(round(b*(-1),roundindex)) + ",   R$^2$ = " + str(round(r2,roundindex))
        plt.scatter(x, y, color=color)
        plt.plot(x, a * x + b, color=color, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    if show and save:
        plt.savefig(filename)
        plt.show()
    elif show:
        plt.show()
    elif save:
        plt.savefig(filename)
        plt.clf()

def plot():
    measurementlst = calculateParameters(measurements())
    colorlst = [[(255/255,0/255,0/255),(170/255,0/255,0/255)],[(0/255,255/255,0/255),(0/255,170/255,0/255)],[(0/255,0/255,255/255),(0/255,0/255,170/255)]]
    pltlst = [
        {
    "x_key" : "t",
    "y_key": "C_OH sample",
    "x_eq" : lambda x_: x_,
    "y_eq" : lambda y_: y_, 
    "x_str" : r"t",
    "y_str" : r"C$_{OH^-}$",
    "xlabel" : r"t [s]",
    "ylabel" : r"C$_{OH^-}$ $\left[\frac{mol}{l}\right]$",
    "filename": "C_OH-vs-t"
    },{
    "x_key" : "t",
    "y_key": "C_OH sample",
    "x_eq" : lambda x_: x_,
    "y_eq" : lambda y_: np.log(y_/y_[0]), 
    "x_str" : r"t",
    "y_str" : r"$ln\left(\frac{C_{OH^-}}{C_{OH^-,0}}\right)$",
    "xlabel" : r"t [s]",
    "ylabel" : r"$ln\left(\frac{C_{OH^-}}{C_{OH^-,0}}\right)$",
    "filename": "ln(C_OHdC_OH0)-vs-t"
    },{
    "x_key" : "t",
    "y_key": "C_OH sample",
    "x_eq" : lambda x_: x_,
    "y_eq" : lambda y_: (1/y_)-(1/y_[0]), 
    "x_str" : r"t",
    "y_str" : r"$\frac{1}{C_{OH^-}}-\frac{1}{C_{OH^-, 0}}$",
    "xlabel" : r"t [s]",
    "ylabel" : r"$\frac{1}{C_{OH^-}}-\frac{1}{C_{OH^-, 0}}$ $\left[\frac{l}{mol}\right]$",
    "filename": "1dC_OH-1dC_OH0-vs-t"
    },
    ]
    for pltdict in pltlst:
        singlePlot(measurementlst, pltdict,colorlst, show=True, save=True)
   
    
    

def main():
    #End concentrations
    variableDict = {
        "V_DMSO": 0,
        "V_NaOH": 1,
        "m_NaOH": 2,
        "V_H2O": 3,
        "m_H2O": 4,
        "n_H2O": 5,
        "n_DMSO": 6,
        "m_DMSO": 7
        }
    for count, x in enumerate(x_DMSO):
        sol = root(eq,np.array([20 for i in range(8)]), args=(count))
        print()
        print("X_DMSO: ", x)
        print("Success: ",sol["success"])
        for variable, index in variableDict.items():
            print(variable, ": ", sol["x"][index])
        print("n_NaOH: ", sol["x"][variableDict["V_NaOH"]], " mol")
        print("m_EI: ", (sol["x"][variableDict["V_NaOH"]] * Mm_C2H5I), " g")
        print("V_EI: ", (sol["x"][variableDict["V_NaOH"]] * Mm_C2H5I)/rho_C2H5I, " L") #l * mol/l * g/mol /g/ml => ml
        
    plot()



main()