
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
    Rut=Rut;Dv=Dv;ValorPropiedad=valprop;MontoCre=monto;producto=prod;
    UF=uf;financiamiento=MontoCre/ValorPropiedad;
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if producto=='mixta':
      PROD=6
      PLZFIJO=plz_fijo
      PLZVAR=plz
      RESHA=1
    elif producto =='fija':
      PROD=4
      PLZFIJO=0
      RESHA=21
      PLZVAR=0
    else: 
      print('Producto no existe')
    if financiamiento>0.8:
      print ('Financiamiento no puede ser mayor a 80%')
    else :
      http = urllib3.PoolManager()
      result = []
      url = 'https://servicios.asicom.cl/itau/simulacion.do?method=calculo'
      data ='''
      nombre=test&rut_aux=@RUT&fono_celular=999999999&idInstitucion=itau&email=s%40s.cl&
      fono_fijo=&producto=@PROD&valor_propiedad_aux=@VPROP%2C00&
      monto_uf_aux=@MCRE%2C00&financiamiento=@PORC&gracia=0&objetivo=1&
      plazoAseg=@PLZFIJO&plazo=@PLZVAR&propiedad=100&tipoSeguro=2&dfl2=0&
      mtoPropiedad=@VPROP&mtoCredito=@MCRE&mtoSeguro=0.0&rut=@RUTNUM&dv=@DV&minimoCredito=0.0&
      maximoPorcentajeVivienda=80.0&maximoPorcentajeGeneral=70.0&auxtipoSeguro=0&
      auxpropiedad=0&auxdfl2=0&auxobjetivo=0&
      auxgracia=00'''.replace('@VPROP_$',str(int(ValorPropiedad*UF))). \
      replace('@MCRE_$',str(int(MontoCre*UF))). \
      replace('@PORC',str(int(100*((MontoCre)/(ValorPropiedad))))). \
      replace('@PIE_$',str(int((ValorPropiedad-MontoCre)*UF))). \
      replace('@RUT',Rut+'-'+Dv).replace('@VPROP',str(ValorPropiedad)).replace('@PLZVAR',str(PLZVAR)). \
      replace('@MCRE',str(MontoCre)).replace('@PORFIN',str(financiamiento)).replace('@PLZFIJO',str(PLZFIJO)). \
      replace('@RUTNUM',Rut).replace('@DV',Dv).replace('@PROD',str(PROD)).replace('\n','').replace(' ','')

      session=requests.Session()
      session.verify=False
      r = session.post(url, data, headers={'Content-Type': 'application/x-www-form-urlencoded', 
                                                            'Referer': 'https://servicios.asicom.cl/itau/simulador.jsp?institucion=itau&&?cod=/wps/portal/BICPublico/productos/parausted/hipotecarios', 
                                                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                                                            }, verify=False )
      root = lxml.html.fromstring(r.text)
      records = root.xpath("////*/td[ contains(text(),'Tasa Crédito') ]/ancestor::table/tr[position()>1]/td[position()>1]/strong")
      tt = [ float(record.text.replace('%','').strip().replace('.', '').replace(',','.')) for record in records]
      tt=pd.DataFrame(np.asarray(tt).reshape(9,RESHA)).round(2)
      records = root.xpath("////*/td[ contains(text(),'Tasa Crédito') ]/ancestor::table/tr[position()>0]/th[position()>1]")
      tt=tt.append([[int(record.text) for record in records]])
      tt=tt.transpose()
      #$tt_plazo=root.xpath("////*/th[ contains(text(),'Plazo') ]/ancestor::table/tr[position()=1]/th[position()>1]")
      #tt_plazo = [ float(record.text.replace('%','').strip().replace('.', '').replace(',','.'))  for record in tt_plazo]
      tt.columns=['Tasa','CAE','Div_SSEG','SEG_INCSIS','SEG_DESG','PRIM_DIV','COSTO_TOTCRED','TOT_DIVUF','TOT_DIV$','Plazo']
      tt['TOT_Seg']=(tt.SEG_INCSIS)+(tt.SEG_DESG)
      tt['Dividendo_CSEG']=(tt.Div_SSEG)+(tt.SEG_INCSIS)+(tt.SEG_DESG)
      tt['ValorProp']=ValorPropiedad
      tt['MontoCre']=MontoCre
      tt['Fecha']=date.today()
      tt['Producto']='HIP-FIJA'
      tt['PlazoFijo']=PLZFIJO
      tt['Banco']='ITAU' 
      if producto=='mixta':
          tt=tt.dropna()
          tt['Producto']='HIP-MIX'+ str(PLZFIJO)+'Y'
      else :
          tt['Producto']='HIP-FIJA'
      tt=tt.round(2)
      tt=tt.drop_duplicates() 
      return(tt)#,str(r.data).replace('\\n','').replace('\\r','').replace('\\t',''))

print(simulador(Rut='15654317',Dv='9',valprop=3750,monto=3000,plz=20,plz_fijo=2,prod='mixta',uf=29650))   
