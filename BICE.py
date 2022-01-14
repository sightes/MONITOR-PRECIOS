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
        ValorPropiedad=valprop
        MontoCre=monto
        plazo=plz
        from urllib3.exceptions import InsecureRequestWarning 
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        http = urllib3.PoolManager()
        session=requests.Session()
        session.verify=False
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        , 'Content-Type': 'application/json'}
        r = session.post('https://mova.bice.cl/simuladorPubSesion/'
        , headers=headers
        , json = {"tipoCred":"1"
        ,"rutCliente":"0156543179"}, verify=False  
        )
        r2 = session.post("https://mova.bice.cl/portalServices/PP3015/"
        , headers=headers
        , json = {
        "app": "SIMCREDCON"
        , "dispositivo": "01fdebdecbd154a3712aa807d23d5b8e"
        , "encodedData": r.json()['edPublico']
        , "plataforma": "Linux x86_64"
        , "sistemaOperativo": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        } )
        r3 = requests.post( "https://mova.bice.cl/portalServices/PP320/"
        , headers=headers
        , json = {
        "dispositivo": "4d895dd96529307295c09a99c4d02a47"
        , "rut": r2.json()["rutCliente"]
        , "token": r2.json()["tokenOag"]
        })
        a=json.loads(r3.text)
        tasas=[]
        for i in range(0,len(a[0]['tarifas'])):
            tasas.append([
                float(a[0]['tarifas'][i]['Tasa']),
                int(a[0]['tarifas'][i]['MontoUFinicial']),
                int(a[0]['tarifas'][i]['MontoUFFinal']),
                int(a[0]['tarifas'][i]['PlazoMinimo']),
                int(a[0]['tarifas'][i]['PlazoMaximo'])])
        tasas=pd.DataFrame(tasas,columns=['tasa','montoini','montofin','plazoini','plazofin']).round(2)
        tasas=tasas.iloc[np.where((tasas.montoini<=max(MontoCre,1000))&
        (tasas.montofin>=max(MontoCre,1000))&(tasas.plazoini<=max(plazo,8))&
        (tasas.plazofin>=max(plazo,8)))].sort_values('plazofin').iloc[0]
        col=['Tasa','CAE','Div_SSEG','SEG_INCSIS','SEG_DESG','PRIM_DIV','COSTO_TOTCRED','TOT_DIVUF','TOT_DIV$','Plazo','TOT_Seg','Dividendo_CSEG','ValorProp','MontoCre','Fecha','Producto','PlazoFijo','Banco']
        tt=pd.DataFrame([], columns=col)
        plz=float(plazo)
        tasa=float(tasas.tasa)
        CAE=float(0)
        divsseg=float(0)
        incseg=float(0)
        desseg=float(0)
        totdiv=float(0)
        totdivclp=float(0)
        tt=tt.append(
                pd.DataFrame(np.asarray([tasa,CAE,divsseg,incseg,desseg,0,0,totdiv,totdivclp,plz,desseg+incseg,
                totdiv,int(ValorPropiedad),int(MontoCre),date.today(),'HIP-FIJA',0,'BICE' ]).reshape(1,-1),columns=col))
        return(tt)

##print(simulador(Rut='15654317',Dv='9',valprop=3750,monto=3000,plz=5,plz_fijo=5,prod='mixta',uf=29650))