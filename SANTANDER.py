
import pandas as pd 
import numpy as np
from datetime import date, datetime, timedelta
import lxml.html
import urllib3
import json
import requests 
import time
import random


def Simulador_Hipotecario_Santander(rut, dv, ValorPropiedad, MontoCre, plazo,uf):
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    monto=MontoCre
    pie=ValorPropiedad-MontoCre
    http = urllib3.PoolManager()
    rutDv = rut.replace(',','.') + '-' +dv
    ## rut formato 9.999.999-9
    result = pd.DataFrame([],columns=['Banco','Tasa','Dividendo_SSEG','SEG_DESG','SEG_INC_SIS','CAE','Plazo'])
    url = 'https://www.santander.cl/simuladores/simulador_hipotecario/simulacion.asp'
    session=requests.Session()
    session.verify=False
    for dtramo in ['111','112','156','135','131','121','120','110']: 
        curr_result=[]
        Tramos_Renta_SANT=pd.DataFrame( [['111','0-0.4'],['112','0.4-0.55'],['156','0.55-0.8'],
                                          ['135',' 0.8-1.3'],['131','1.3-1.7'],['121','1.7-2.5'],
                                              ['120','2.5-5'],['110','>5']] , columns=['COD', 'TRAMO'])
        CURR_TRAMO=Tramos_Renta_SANT.iloc[np.where(Tramos_Renta_SANT.COD==dtramo)[0][0]].TRAMO
        data = "montoCalculado="+ str(monto) + "&noaprob=0&camp_id=&valcamp=&d_pin=&uf=" + str(float(uf)) + "&IDLOGIN=BancoSantander&o=&val1=&cl=false&origen=PB&utm_source=&utm_medium=&utm_campaign=&utm_term=&utm_content=&id_gdconv=" + datetime.now().strftime('%Y%m%d%H:%M:%S') +"&d_rut="+ rutDv +"&rut="+ rutDv + "&nombre=a&apaterno=b&amaterno=c&email=a@b.com&codigoarea=&telefono=&fec_fono=&region=&comuna=SANTIAGO+CENTRO&valor_propiedad="+str(ValorPropiedad)+"&valor_propiedad2=&valor_pie="+str(pie)+"&monto="+str(MontoCre)+"&monto2=&porcentaj="+ str(int(100*((MontoCre)/(ValorPropiedad)))) +"&plazo=" + str(plazo) + "&tipo_tasa=1&propiedad=Casa&tipo_propiedad=Nueva&sg_desgravamen=1&sg_incendio=1&dtramo="+ dtramo +"&valuedtramo=&opc=&otrorut=&region1=RM&comuna1=SANTIAGO+CENTRO&z=&valorpyme=false"
        
        r = session.post( url,data, \
                           headers={'Content-Type': 'application/x-www-form-urlencoded', 'Referer': 'https://www.santander.cl/simuladores/simulador_hipotecario/simulador.asp', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'} )
        root = lxml.html.fromstring(r.text)

        records = root.xpath("////*/table[@class = 'd-simulacion']/tr[1]/td[5]/strong")
        tasa = [ record.text.replace('%','').strip().replace(',','.') for record in records]
        records = root.xpath("////*/td[text() = 'Simulación' ]/ancestor::tr/td[@class = 'verde']/strong")
        dividendo = [ record.text.replace('UF','').strip().replace(',','.') for record in records]
        records = root.xpath("////*/td[text() = 'Simulación' ]/ancestor::tr/td[4]/strong")
        SEG_DESG = [ record.text.replace('UF','').strip().replace(',','.') for record in records]
        records = root.xpath("////*/td[text() = 'Simulación' ]/ancestor::tr/td[5]/strong")
        SEG_INC_SIS = [ record.text.replace('UF','').strip().replace(',','.') for record in records]
        records = root.xpath("////*/td[text() = 'Porcentaje de Financiamiento' ]/ancestor::tr/td[2]/strong")
        ltv = [ record.text.replace('%','').strip() for record in records]
        ##Total Crédito
        records = root.xpath("////*/td[text() = 'Total Crédito' ]/ancestor::tr/td[2]/strong")
        monto_credito = [ record.text.replace('UF','').strip() for record in records]
        ## cae
        records = root.xpath("////*/td[text() = 'Carga Anual Equivalente (CAE)' ]/ancestor::tr/td[2]/strong")
        cae = [ record.text.replace('%','').strip().replace(',','.') for record in records]
        t_sleep=random.randrange(30,40)
        #t_sleep=35
        time.sleep(t_sleep)
        print('Durmiendo '+str(t_sleep)+ 'Seg ....ZzZzZzZzZzZzZzZ')
        result=result.append(pd.DataFrame([[ 'SANTANDER'+CURR_TRAMO,float(tasa[0]),float(dividendo[1]),float(SEG_DESG [0]),float(SEG_INC_SIS [0]),float(cae[0]),plazo]],columns=['Banco','Tasa','Dividendo_SSEG','SEG_DESG','SEG_INC_SIS','CAE','Plazo']), ignore_index=True)
    return(result,str(r.data).replace('\\n','').replace('\\r','').replace('\\t',''))



Simulador_Hipotecario_Santander(rut='15654317',dv= '9', ValorPropiedad=3750,MontoCre=3000, plazo=20, uf=30000)
