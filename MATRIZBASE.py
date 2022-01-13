import pandas as pd 
import numpy as np
from datetime import date, datetime, timedelta
import lxml.html
import json
import time
import random
import matplotlib.pyplot as plt 
import numpy as np 
import math 

def Matrices_Basicas(matriz_CF,matriz_TMC,i_Ajuste):
    global CF,TMC,Base_CF,Base_TMC,M_BASE,Diff_TMC,T_BASE,Tramos_monto
    CF=pd.DataFrame(np.asarray(matriz_CF).reshape(1,-1))
    CF.columns= ['p5','p8','p10','p12','p15','p20','p25','p30']
    Tramos_monto=['m1499','m1999','m2499','m2999','m3999','m4999','m7999','m11999','m99999']
    TMC=pd.DataFrame(np.asarray(matriz_TMC).reshape(1,-1))
    TMC.columns=['TMC3B','TMC3C','TMC2C','TMC2D']
    #Base Costo Fondo
    Base_CF=pd.DataFrame([[Tramos_monto[i],CF['p5'][0],CF['p8'][0],CF['p10'][0],CF['p12'][0],
                           CF['p15'][0],CF['p20'][0],CF['p25'][0],CF['p30'][0]] 
                           for i in range(0, len(Tramos_monto ))])
    Base_CF.columns=['tramo_monto','p5','p8','p10','p12','p15','p20','p25','p30']
    Base_CF=Base_CF.set_index('tramo_monto')
    #Base TMC
    Base_TMC=[]
    for i in Tramos_monto:
         if i=='m1499' or i=='m1999': 
               curr_tmc=TMC['TMC3B'][0] 
               Base_TMC.append([i,curr_tmc,curr_tmc,curr_tmc,curr_tmc,curr_tmc,curr_tmc,curr_tmc,curr_tmc] )
         else:
               curr_tmc=TMC['TMC3C'][0] 
               Base_TMC.append([i,curr_tmc,curr_tmc,curr_tmc,curr_tmc,curr_tmc,curr_tmc,curr_tmc,curr_tmc] )
    Base_TMC=pd.DataFrame(Base_TMC)
    Base_TMC.columns=['tramo_monto','p5','p8','p10','p12','p15','p20','p25','p30']
    Base_TMC=Base_TMC.set_index('tramo_monto')
    M_BASE=[]
    Diff_TMC=TMC['TMC3B'][0] -TMC['TMC3C'][0] 
    #Diff_TMC=0.23
    for i in Tramos_monto:
         if i=='m1499' or i=='m1999': 
               curr_tmc=TMC['TMC3B'][0] 
               M_BASE.append([i,i_Ajuste,i_Ajuste,i_Ajuste,i_Ajuste,i_Ajuste,i_Ajuste,i_Ajuste,i_Ajuste] )
         else:
               curr_tmc=TMC['TMC3C'][0] 
               M_BASE.append([i,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC] )
    M_BASE=pd.DataFrame(M_BASE)
    M_BASE.columns=['tramo_monto','p5','p8','p10','p12','p15','p20','p25','p30']
    M_BASE=M_BASE.set_index('tramo_monto')
    M_BASE=(((M_BASE+Base_CF)>Base_TMC)*Base_TMC)-(((M_BASE+Base_CF)>Base_TMC)*Base_CF)+((M_BASE+Base_CF)<=Base_TMC)*M_BASE
    for i in Tramos_monto:
         if i=='m1499' or i=='m1999': 
               M_BASE.append([i,i_Ajuste,i_Ajuste,i_Ajuste,i_Ajuste,i_Ajuste,i_Ajuste,i_Ajuste,i_Ajuste] )
         else:
               M_BASE.append([i,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC,i_Ajuste-Diff_TMC] )
    M_BASE=np.round(M_BASE,2)            
    T_BASE=M_BASE+Base_CF
    Iniciativa_Tramos_monto=np.array(Tramos_monto)[np.array(np.where(np.array(Tramos_monto)!='m2999')).astype(int)][0]
    Pizarra_Tramos_monto=np.array(Tramos_monto)[np.array(np.where(np.array(Tramos_monto)!='m11999')).astype(int)][0]
    opt={'CF': CF, 
      'TMC':TMC,
      'Base_CF':Base_CF,
      'Base_TMC':Base_TMC,
      'M_BASE':M_BASE,
      'Diff_TMC':Diff_TMC,
      'T_BASE':T_BASE,
      'Tramos_monto':Tramos_monto,
       'Iniciativa_Tramos_monto':Iniciativa_Tramos_monto,
       'Pizarra_Tramos_monto':Pizarra_Tramos_monto
     }
    ## TRAMOS MONTOS
    return(opt)

# FUNCION FORMA TARIFAS
def Funcion_Tarifa(u,r,op=0):
    x = np.linspace(-(r*(1-u)),r*u,8) 
    if r<0:
        z = 1/(1 +(1* np.exp(x)))
    else: 
        z = 1/(1 +(1* np.exp(-x)))
    z=z-z.min()
    z= z/z.max()
    if op==1:
        plt.plot(x, z) 
        plt.xlabel("x") 
        plt.ylabel("Sigmoid(X)") 
        plt.show()
    return(z)


#matriz_CF=[2.66,3.16,3.35,3.38,3.49,3.7,3.82,3.91]
#matriz_TMC=[6.24,5.57,22.26,7.80]
#i_Ajuste=4
#opt= Matrices_Basicas(matriz_CF,matriz_TMC,i_Ajuste)   
#print(opt['M_BASE'])