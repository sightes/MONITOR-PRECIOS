import pandas as pd 
import numpy as np
from datetime import date, datetime, timedelta
import lxml.html
import urllib3
import json
import requests 
import time
import random

def simulador(Rut=0,Dv='',valprop=0,monto=0,plz=0,plz_fijo=0,prod='',uf=0):
    from urllib3.exceptions import InsecureRequestWarning 
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    http = urllib3.PoolManager()
    result = []
    session=requests.Session()
    session.verify=False

    url ='https://asesorhipotecario.serviciosbancoestado.cl/ws_hipotecario/factores.php'
    data={"datos": "vacio"}
    r = session.post(url, data, headers={
    'authority': 'asesorhipotecario.serviciosbancoestado.cl',
    'method': 'POST',
    'path': '/ws_hipotecario/factores.php',
    'scheme': 'https',
    'accept': 'text/html, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
    'content-length': '11',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.bancoestado.cl',
    'referer': 'https://www.bancoestado.cl/',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'   
    }
    , verify=False )
    

    valpropclp='{0:,.0f}'.format(valprop*uf).replace(',','.')   
    pieclp='{0:,.0f}'.format((valprop-monto)*uf).replace(',','.')   
    url ='https://asesorhipotecario.serviciosbancoestado.cl/ws_hipotecario/procesa1.php'
    data={ 'datos':''.join((
        '{"formulario_tipo":"hipotecario","funcionario":"0",',
        '"port_financiera":"1","dia_01":"00","mes_01":"00","anio_01":"0000",',
        '"actividad_01":" ","renta_01":"2","renta_02":"2","dia_02":"01","mes_02":"01",',
        '"anio_02":"1900","actividad_02":" ","ubicacion_01":"0","tcanals":"asesor",',
        '"opcion_01":"1","tipo_01":"1","region_01":"10","condicion_01":"1",',
        '"nombre_01":"sadsadas","rut_01":"'+Rut+'-'+Dv+'","email_01":"asdsadsad@gmail.com",',
        '"uf_01":"'+str(valprop)+',00","pesos_01":"'+valpropclp+'","dolar_01":"","uf_02":"",',
        '"pesos_02":"","dolar_02":"","plazo_entrega":"1","uf_03":"'+str(valprop-monto)+',00",',
        '"pesos_03":"'+pieclp+'","dolar_03":"","plazo_credito":"'+str(plz)+'","uf":"'+r.text.split('|')[0]+'"}'))}
    r = session.post(url, data, headers={
    'authority': 'asesorhipotecario.serviciosbancoestado.cl',
    'method': 'POST',
    'path': '/ws_hipotecario/procesa1.php',
    'scheme': 'https',
    'accept': 'text/html, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
    'content-length': '1042',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.bancoestado.cl',
    'referer': 'https://www.bancoestado.cl/',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'

    }
    , verify=False )
    root=lxml.html.fromstring(r.text)
    Tasas=[root.xpath("////*/td[text() = 'Tasa Anual %' ]/ancestor::tr/td[2]")[i].text for i in range(1,5)]
    divsseg=[root.xpath("////*/td[text() = 'Dividendo sin seguro en UF' ]/ancestor::tr/td[2]")[i].text for i in range(1,5)]
    divssegclp=[root.xpath("////*/td[text() = 'Dividendo sin seguro en $' ]/ancestor::tr/td[2]")[i].text for i in range(1,5)]
    divcseg=[root.xpath("////*/td[text() = 'Dividendo con seguro en UF' ]/ancestor::tr/td[2]")[i].text for i in range(1,5)]
    divcsegclp=[root.xpath("////*/td[text() = 'Dividendo con seguro en $' ]/ancestor::tr/td[2]")[i].text for i in range(1,5)]
    cae=[root.xpath("////*/td[text() = 'Carga Anual Equivalente (CAE)' ]/ancestor::tr/td["+str(i)+"]")[0].text  for i in range(2,6)]
    plz=[root.xpath("////*/th[@class= 'elegida' ]/ancestor::tr/th["+str(i)+"]")[1].text for i in range(2,6)]
    col=['Tasa','CAE','Div_SSEG','SEG_INCSIS','SEG_DESG',
    'PRIM_DIV','COSTO_TOTCRED','TOT_DIVUF','TOT_DIV$','Plazo',
    'TOT_Seg','Dividendo_CSEG','ValorProp','MontoCre','Fecha',
    'Producto','PlazoFijo','Banco']
    tt=pd.DataFrame([], columns=col)
    tt['Tasa']=Tasas
    tt['CAE']=cae
    tt['Div_SSEG']=divsseg
    tt['SEG_INCSIS']=0
    tt['SEG_DESG']=0
    tt['PRIM_DIV']=0
    tt['COSTO_TOTCRED']=0
    tt['TOT_DIVUF']=divcseg
    tt['TOT_DIV$']=divcsegclp
    tt['Plazo']=plz
    tt['TOT_Seg']=0
    tt['Dividendo_CSEG']=divcseg
    tt['ValorProp']=valprop
    tt['MontoCre']=monto
    tt['Fecha']=date.today()
    tt['Producto']='HIP-FIJA'
    tt['PlazoFijo']=0
    tt['Banco']='ESTADO'
    return(tt)
#print(simulador(Rut='15654317',Dv='9',valprop=3750,monto=3000,plz=20,plz_fijo=5,prod='mixta',uf=29650))     