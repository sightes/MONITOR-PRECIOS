def simulador(monto,plz):
    import pandas as pd 
    import numpy as np
    from datetime import date, datetime, timedelta
    import lxml.html
    import urllib3
    import json
    import requests 
    import time
    import random

    url = 'https://servicios.cmfchile.cl/simuladorhipotecario/aplicacion?indice=101.2.3 \
    &maxuf=20000&minuf=100&maxpeso=652419400&minpeso=3262097&paso=2&template=entidades&tipomoneda=1 \
    &monto=@MONTO_$&tipocredito=3&tipotasa=1&plazo=@PLAZO_$&inst=OK& \
    marcados=1&marcados=9&marcados=12&marcados=14&marcados=16&marcados=28&marcados=37&marcados=39&marcados=51&marcados=672'

    url=url.replace('@PLAZO_$',str(int(plz))).replace('@MONTO_$',str(int(monto)))


    session=requests.Session()
    session.verify=False

    r = session.get( url.replace(' ',''), headers={
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded', \
    'Referer': 'https://servicios.cmfchile.cl/simuladorhipotecario/aplicacion?indice=101.2.1', \
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'} )
    root = lxml.html.fromstring(r.text)

    #test cuantos bancos en el listado 
    nbancos=len(root.xpath("////*/div[@id = 'simuladorCreditoHipotecario']/table/tbody/tr"))
    aux1=[];
    for i in range(1,nbancos):
        banco=root.xpath("////*/div[@id = 'simuladorCreditoHipotecario']/table/tbody/tr["+ str(i) + "]/td")[0].text
        tipo=root.xpath("////*/div[@id = 'simuladorCreditoHipotecario']/table/tbody/tr["+ str(i) + "]/td")[1].text
        dividendo=root.xpath("////*/div[@id = 'simuladorCreditoHipotecario']/table/tbody/tr["+ str(i) + "]/td")[2].text
        dividendo=dividendo.replace('\xa0','').replace('$','').replace('UF','').replace('\n','').replace('.','').replace(',','.').replace('\t','').replace(' ','')
        moneda=root.xpath("////*/div[@id = 'simuladorCreditoHipotecario']/table/tbody/tr["+ str(i) + "]/td")[3].text
        tipotasa=root.xpath("////*/div[@id = 'simuladorCreditoHipotecario']/table/tbody/tr["+ str(i) + "]/td")[4].text
        tasa=root.xpath("////*/div[@id = 'simuladorCreditoHipotecario']/table/tbody/tr["+ str(i) + "]/td")[5].text
        tasa=tasa.replace('\xa0','').replace('$','').replace('UF','').replace('\n','').replace('.','').replace(',','.').replace('\t','').replace(' ','').replace('%','')
    
        CAE=root.xpath("////*/div[@id = 'simuladorCreditoHipotecario']/table/tbody/tr["+ str(i) + "]/td")[6].text
        CAE=CAE.replace('\xa0','').replace('$','').replace('UF','').replace('\n','').replace('.','').replace(',','.').replace('\t','').replace(' ','').replace('%','')
    
        
        
        aux1=aux1+[[banco,tipo,dividendo,moneda,tipotasa,tasa,CAE]]
    aux1=pd.DataFrame(aux1,columns=['banco','tipo','dividendo','moneda','tipotasa','tasa','CAE'])
    ## part1 
    a=root.xpath("////*/div[contains(@id,'targetSimulacion')]/div[1]/ul[1]/li[contains(@class,'list-group-item')]")
    aux=[]
    for i in range(0, len(a)):
        b=a[i].text
        c=b.split(' ')
        d=[c[len(c)-1].replace('\xa0','').replace('\n','').replace(',','.')]
        aux=aux+[float(c[len(c)-1].replace('\xa0\n','').replace(',','.'))]
    e=pd.DataFrame(np.array(aux).reshape(int(len(aux)/3),3),columns=['Etitulos','GastoNotarial','TasacionUF'])
    aux1=aux1.join(e)

    a=root.xpath("////*/div[contains(@id,'targetSimulacion')]/div[2]/ul[1]/li[contains(@class,'list-group-item')]")
    aux=[]
    for i in range(0, len(a)):
        b=a[i].text
        c=b.split(' ')
        d=c[len(c)-1].replace('\xa0','').replace('$','').replace('UF','').replace('\n','').replace('.','').replace(',','.')
        aux=aux+[float(d)]
    e=pd.DataFrame(np.array(aux).reshape(int(len(aux)/2),2),columns=['divSinSeg_UF','divSinSeg_clp'])
    aux1=aux1.join(e)

    a=root.xpath("////*/div[contains(@id,'targetSimulacion')]/div[3]/ul[1]/li[contains(@class,'list-group-item')]")
    aux=[]
    for i in range(0, len(a)):
        b=a[i].text
        c=b.split(' ')
        d=c[len(c)-1].replace('\xa0','').replace('$','').replace('UF','').replace('\n','').replace('.','').replace(',','.')
        aux=aux+[float(d)]
    e=pd.DataFrame(np.array(aux).reshape(int(len(aux)/2),2),columns=['SegDesgravamenUF','SegDesgravamenCLP'])
    aux1=aux1.join(e)

    a=root.xpath("////*/div[contains(@id,'targetSimulacion')]/div[4]/ul[1]/li[contains(@class,'list-group-item')]")
    aux=[]
    for i in range(0,len(a)):
        if i/2!=int(i/2):
            b=a[i].text
            c=b.split(' ')
            d=c[len(c)-1].replace('\xa0','').replace('Chile','').replace('$','').replace('UF','').replace('\n','').replace('.','').replace(',','.')
            aux=aux+[d]
    e=pd.DataFrame(np.array(aux).reshape(int(len(aux)/1),1),columns=['fecha Actualizacion'])
    aux1=aux1.join(e)

    a=root.xpath("////*/div[contains(@id,'targetSimulacion')]/div[3]/ul[2]/li[contains(@class,'list-group-item')]")
    aux=[]
    for i in range(0, len(a)):
        b=a[i].text
        c=b.split(' ')
        d=c[len(c)-1].replace('\xa0','').replace('$','').replace('UF','').replace('\n','').replace('.','').replace(',','.')
        aux=aux+[float(d)]
    e=pd.DataFrame(np.array(aux).reshape(int(len(aux)/2),2),columns=['SegIncendioUF','SegIncendioCLP'])
    aux1=aux1.join(e)

    a=root.xpath("////*/div[contains(@id,'targetSimulacion')]/div[3]/ul[3]/li[contains(@class,'list-group-item')]")
    aux=[]
    for i in range(0, len(a)):
        b=a[i].text
        c=b.split(' ')
        d=c[len(c)-1].replace('\xa0','').replace('$','').replace('UF','').replace('\n','').replace('.','').replace(',','.')
        aux=aux+[float(d)]
    e=pd.DataFrame(np.array(aux).reshape(int(len(aux)/2),2),columns=['divConSeg_UF','divConSeg_clp'])
    aux1=aux1.join(e)
    aux1['monto_simulado']=monto
    aux1['plazo_simulado']=plz
    aux1['producto']='SIMULADOR_SBIF'    
    return(aux1)

print(simulador(2800,15))


