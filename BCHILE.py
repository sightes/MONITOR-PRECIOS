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
    Rut=Rut;Dv=Dv;ValorPropiedad=valprop;MontoCre=monto;producto=prod;UF=uf;financiamiento=MontoCre/ValorPropiedad;
    pie=ValorPropiedad-MontoCre
    financiamiento=MontoCre/ValorPropiedad
    result = []
    data='rut=@RUT& \
    rangorenta1=%3F& \
    rangorenta=& \
    tipo_pro=1& \
    valor_uf=@VPROP& \
    tipoCredito=1& \
    plazoFijo=%7B%22id%22%3A%221%22%2C%22name%22%3A%221%22%7D& \
    montoPie=@PORFIN& \
    monto-pie=@PIE& \
    monto-credito=@MCRE& \
    plazoCredito=@PLAZO& \
    mGracia=0& \
    enviar='
    data=data.replace('@PORC',str(int(100*((MontoCre*UF)/(ValorPropiedad*UF))))). \
    replace('@RUT',"{0:,}".format(int(Rut)).replace(',','.')+ '-' + Dv). \
    replace('@PIE',str(int((ValorPropiedad-MontoCre)))). \
    replace('\n','').replace(' ',''). \
    replace('@PORFIN',str( 100-round(financiamiento*100))). \
    replace('@VPROP',str(ValorPropiedad)). \
    replace('@UF',str(int(UF))). \
    replace('@MCRE',str(MontoCre)). \
    replace('@PLAZO',str(plz)). \
    replace('@RUTNUM',Rut).replace('@DV',Dv). \
    replace(' ','')
    headers = {'content-type': 'application/x-www-form-urlencoded',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
               }
    r = requests.post('https://promociones.bancochile.cl/simuladorhipotecario/bchnew/inicio-proc.asp',headers=headers,data=data,verify=False)
    root = lxml.html.fromstring(r.text)
    Tasa=root.xpath("////*/div[ contains(@class, 'item')]/div/div/p/strong")[1].text.replace(',','.').replace('%','')
    CAE=root.xpath("////*/div[ contains(@class, 'item')]/div/div/p/strong")[2].text.replace(',','.').replace('%','')
    a=root.xpath("////*/div[@id='option1']/ul[2]/li")
    SEG_DESG=a[1].text_content().replace('Seguro de Desgravamen: ','').replace(' UF','').replace(',','.')
    SEG_INC_SIS=float(a[2].text_content().replace('Seguro de Incendio: ','').replace(' UF','').replace(',','.'))+ \
    float(a[3].text_content().replace('Seguro de Sismo:  ','').replace(' UF','').replace(',','.'))
    Dividendo_SSEG=float(a[4].text_content().replace('Dividendo sin los Seguros  :  ','').replace(' UF','').replace(',','.'))
    a=[float(Tasa),float(CAE),float(Dividendo_SSEG),float(SEG_INC_SIS),float(SEG_DESG),0,0,
       float(Dividendo_SSEG)+float(SEG_INC_SIS)+float(SEG_DESG),0,plz,float(SEG_INC_SIS)+float(SEG_DESG),0, 
       ValorPropiedad,MontoCre,date.today(),'HIP-FIJA',0,'BCHILE']
  
    a=pd.DataFrame(np.asarray(a).reshape(1,-1))
    a.columns=['Tasa', 'CAE', 'Div_SSEG', 'SEG_INCSIS', 'SEG_DESG', 'PRIM_DIV',
       'COSTO_TOTCRED', 'TOT_DIVUF', 'TOT_DIV$', 'Plazo', 'TOT_Seg',
       'Dividendo_CSEG', 'ValorProp', 'MontoCre', 'Fecha', 'Producto',
       'PlazoFijo', 'Banco']
    return(a)#,str(r.data).replace('\\n','').replace('\\r','').replace('\\t',''))


#print(BANCO_Bchile(Rut='15654317',Dv='9',valprop=3750,monto=3000,plz=15,plz_fijo=3,prod='fija',uf=29650))      



