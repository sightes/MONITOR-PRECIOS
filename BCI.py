import pandas as pd 
import numpy as np
from datetime import date, datetime, timedelta
import urllib3
import json
import requests 
import time
import random
import lxml
import lxml.html
import json

def simulador(Rut=0,Dv='',valprop=0,monto=0,plz=0,plz_fijo=0,prod='',uf=0):
    if prod=='mixta':
        prodcode='8'
    elif prod =='fija':
        prodcode='23'
    else:
        print('Producto no existe') 
    plz_fijo=str(plz_fijo)
    plz=str(plz)
    pie=str(valprop-monto)
    valprop=str(valprop)
    monto=str(monto)
    from urllib3.exceptions import InsecureRequestWarning 
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    http = urllib3.PoolManager()
    result = []
    url = 'https://apiprogram.bci.cl/prod/v1/api-widget-hipotecario/simulation'
    data =''.join(('{"PurchaseIntentionDate":"01-03-2022","DownPayment":'+pie+',"Term":'+plz+',',
                '"PropertyNew":true,"PropertyType":"CASA","PropertyValue":'+valprop+',' ,
                '"Applicant":{"Email":"a@a.cl","Salary":600000,',
                '"DocumentNumber":"'+Rut+'","SerialNumber":"'+Dv+'"},"FixedRateCredit":true,',
                '"YearsFixedRateCredit":'+plz_fijo+',"Refinancing":false,"ProductCode":'+prodcode+',',
                '"SiteMark":"Publico","SimulationFlowMark":"Comprar","VendorMark":""}'))
    session=requests.Session()
    session.verify=False
    r = session.post(url, data, headers={'Host': 'apiprogram.bci.cl',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0','Accept': 'application/json, text/plain, */*','Accept-Language': 'es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br','Referer': 'https://www.bci.cl/personas/credito-hipotecario/simulador','x-apikey': 'Kqsy2XwB8kfeSPVpdJ6mMcdXa4qKNyAZ','Content-Type': 'application/json',
    'Content-Length': '375','Origin': 'https://www.bci.cl','Connection': 'keep-alive','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-site'}, verify=False )
    a=json.loads(r.text)
    col=['Tasa','CAE','Div_SSEG','SEG_INCSIS','SEG_DESG','PRIM_DIV','COSTO_TOTCRED','TOT_DIVUF','TOT_DIV$','Plazo','TOT_Seg','Dividendo_CSEG','ValorProp','MontoCre','Fecha','Producto','PlazoFijo','Banco']
    tt=pd.DataFrame([], columns=col)
    for n in [0,1,2]:
        plz=a['Data']['Simulations'][n]['simulation']['Term']
        tasa=a['Data']['Simulations'][n]['simulation']['Rate']
        divsseg=a['Data']['Simulations'][n]['simulation']['UninsuredDividendUF']
        incseg=a['Data']['Simulations'][n]['simulation']['FireInsuranceAmount']
        desseg=a['Data']['Simulations'][n]['simulation']['DeductionInsuranceAmount']
        totdiv=a['Data']['Simulations'][n]['simulation']['TotalDividendInsuranceUF']
        totdivclp=a['Data']['Simulations'][n]['simulation']['TotalDividendInsurancePesos']
        tt=tt.append(
        pd.DataFrame(np.asarray([tasa,0,divsseg,incseg,desseg,0,0,totdiv,totdivclp,plz,divsseg+incseg,
        totdiv,int(valprop),int(monto),date.today(),'HIP-FIJA',int(plz_fijo),'BCI' ]).reshape(1,-1),columns=col))
    if prod=='mixta':
        tt=tt.dropna()
        tt['Producto']='HIP-MIX'+ plz_fijo+'Y'
    else :
        tt['Producto']='HIP-FIJA'
    return(tt)



#print(BANCO_bci(Rut='15654317',Dv='9',valprop=3750,monto=3000,plz=20,plz_fijo=2,prod='mixta',uf=29650))  