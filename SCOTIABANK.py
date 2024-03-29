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
    from urllib3.exceptions import InsecureRequestWarning 

    if prod=='mixta':
        prodcode='8'
    elif prod =='fija':
        prodcode='23'
    else:
        print('Producto no existe')
    plz_fijo=str(plz_fijo)
    plz=str(plz)
    pie=str(valprop-monto)
    pie_clp=str(int((valprop-monto)*uf))
    cre_clp=str(int((monto)*uf))
    valprop=str(valprop)
    monto=str(monto)

    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    http = urllib3.PoolManager()
    result = []
    url = 'https://cloudservtrx.scotiabank.cl/sweb/bff/digital-onboarding/v1/subject'
    data ='{"fullName":"Sebastian","birthDate":"1983-12-09","documentId":"156543179","documentNumber":"516352572","nationality":"CL","employmentSituation":"renewable","employmentSalary":"1800000","flow":"mortgage","mail":"a@a.cl","phone":"22222222"}'
    session=requests.Session()
    session.verify=False
    r = session.post(url, data, headers={'Host': 'cloudservtrx.scotiabank.cl','Connection': 'keep-alive','Content-Length': '238','sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google     Chrome";v="96"','Accept': 'application/json, text/plain, */*','Content-Type': 'application/json;charset=UTF-8','sec-ch-ua-mobile': '?0','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36','sec-ch-ua-platform': "Windows",'Origin': 'https://cloudservtrx.scotiabank.cl','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty','Referer': 'https://cloudservtrx.scotiabank.cl/sweb/mfe/digital-mortgage/','Accept-Encoding': 'gzip, deflate, br','Accept-Language': 'es-ES,es;q=0.9','Cookie': '_gcl_au=1.1.788135032.1639139775; _ga=GA1.2.853226005.1639139764; _gid=GA1.2.2039130611.1639139764; _fbp=fb.1.1639139775491.511865; _gat_UA-16719465-13=1; _gali=simulation-button'}, verify=False )

    url = 'https://cloudservtrx.scotiabank.cl/sweb/bff/mortgage-loan/v1/simulator-period'
    data =''.join(('{"uuid":"'+r.json()['uuid']+'","customer_id":"'+Rut+'",',
                    '"customer_id_dv":"'+Dv+'","salary":"1800000","credit_term":["15","20","25"],',
                    '"credit_customer":true,"product_information":{"product_type_public":"MORTGAGE",',
                    '"credi_amount":"'+cre_clp+'","credi_amount_uf":"'+ monto+'","housing_situation":"new",',
                    '"credit_term":"'+plz+'","down_payment":"'+pie_clp+'","down_payment_uf":"'+pie+'","grace_months":"0"}}'))
    session=requests.Session()
    session.verify=False
    r = session.post(url, data, headers={'Host': 'cloudservtrx.scotiabank.cl',
    'Connection':'keep-alive',
    'Content-Length': '389',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://cloudservtrx.scotiabank.cl',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://cloudservtrx.scotiabank.cl/sweb/mfe/digital-mortgage/credit-simulator',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'es-ES,es;q=0.9',}, verify=False )

    a=json.loads(r.text)
    col=['Tasa','CAE','Div_SSEG','SEG_INCSIS','SEG_DESG','PRIM_DIV','COSTO_TOTCRED','TOT_DIVUF','TOT_DIV$','Plazo','TOT_Seg','Dividendo_CSEG','ValorProp','MontoCre','Fecha','Producto','PlazoFijo','Banco']
    tt=pd.DataFrame([], columns=col)
    for n in [0,1,2]:
        plz=float(a['calculator'][n]['years_credit'])
        tasa=float(a['calculator'][n]['annual_rate'])
        CAE=float(a['calculator'][n]['cae'])
        divsseg=float(a['calculator'][n]['value_dividend_uf'])
        incseg=float(a['calculator'][n]['safe_eire_earthquake'])
        desseg=float(a['calculator'][n]['insurance_uf'])
        totdiv=float(a['calculator'][n]['value_dividend_uf'])
        totdivclp=float(a['calculator'][n]['value_dividend'])
        tt=tt.append(
        pd.DataFrame(np.asarray([tasa,CAE,divsseg,incseg,desseg,0,0,totdiv,totdivclp,plz,desseg+incseg,
        totdiv,int(valprop),int(monto),date.today(),'HIP-FIJA',int(plz_fijo),'SCOTIABANK' ]).reshape(1,-1),columns=col))
    if prod=='mixta':
        tt=tt.dropna()
        tt['Producto']='HIP-MIX'+ plz_fijo+'Y'
    else :
        tt['Producto']='HIP-FIJA'
        
    tt=tt.round(2) 
    tt=tt.drop_duplicates() 
    return(tt)

#print(simulador(Rut='15654317',Dv='9',valprop=3750,monto=3000,plz=20,plz_fijo=5,prod='mixta',uf=29650))   