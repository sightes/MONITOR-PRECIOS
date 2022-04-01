
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
     ValorPropiedad=valprop
     MontoCre=monto
     Plazo=plz
     UF=uf
     plz_fijo=3



     http = urllib3.PoolManager()
     financiamiento=MontoCre/ValorPropiedad
     result = []

     if prod=='mixta' and plz_fijo==3:
          tipotasa="MA"
     elif prod=='mixta' and plz_fijo==5:
          tipotasa="MI"
     elif prod=='mixta' and plz_fijo==8:
          tipotasa="MO"
     else :
          tipotasa="ME"     
     
     url = 'https://www.scotiabank.cl/cgi-bin/emula?TRANS=vt_SimCreHipCae&TMPL=/emulacion/resultado_simulacion.htm& \
     UF=@UF&vpro=@VPROP&vcre=@MCRE&finalidad=V%20%20%20&dfl2=N&porfin=@PORC&estado=0001&gracia=0&tipocre=@tipotasa& \
     destino=V%20%20%20&valcre=@MCRE&valcrepesos=@MCRE_$ &valpro=@VPROP &fdfl2=N&fnueva=0001&mgracia=0& \
     mtoprouf=@VPROP &mtopropesos=@VPROP_$ &mtocreuf=@MCRE&mtocrepesos=@MCRE_$ &pfin=@PORFIN'
     url=url.replace('@VPROP_$',str(int(ValorPropiedad*UF))). \
     replace('@MCRE_$',str(int(MontoCre*UF))). \
     replace('@PORC',str(int(100*((MontoCre*UF)/(ValorPropiedad*UF))))). \
     replace('@PIE_$',str(int((ValorPropiedad-MontoCre)*UF))). \
     replace('\n','').replace(' ',''). \
     replace('@PORFIN',str( round(financiamiento*100))). \
     replace('@VPROP',str(ValorPropiedad)). \
     replace('@UF',str(int(UF))). \
     replace('@tipotasa',tipotasa). \
     replace('@MCRE',str(MontoCre)).replace(' ','')



     r = http.request('GET', url, headers={'Content-Type': 'text/html', 
                                                  'Referer': 'https://www.scotiabank.cl/formularios/credito_hipotecario_tf/index.shtml', 
                                                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                                                  } )
     root = lxml.html.fromstring(r.data)
     col=['Tasa','Dividendo_SSEG','SEG_DESG','SEG_INC_SIS','CAE']
     curr_table=pd.DataFrame([],columns=col)
     for n_row in range(1,8):
        records = root.xpath("////*/th[ contains(text(),'Tasa') ]/ancestor::table/tbody/tr[position()="+ str(n_row) +"]/td[position()>0]")
        curr_table=curr_table.append(pd.DataFrame(np.asarray([ records[:][i].text.replace( ' ' ,'').replace('$','').replace('UF','').replace('%','').strip().replace('.', '').replace(',','.') for i in [1,2,3,4,6]]).reshape(1,-1),
                 columns=col),ignore_index=True)
     curr_table['Plazo']=[5,8,10,12,15,20,25]  
     curr_table=curr_table.iloc[np.where(curr_table.Plazo==Plazo)].astype('float')
     tt=pd.DataFrame([])
     tt['Tasa']=curr_table['Tasa']
     tt['CAE']=curr_table['CAE']
     tt['Div_SSEG']=curr_table['Dividendo_SSEG']
     tt['SEG_INCSIS']=curr_table['SEG_INC_SIS']
     tt['SEG_DESG']=curr_table['SEG_DESG']
     tt['PRIM_DIV']=0
     tt['COSTO_TOTCRED']=0
     tt['TOT_DIVUF']=0
     tt['TOT_DIV$']=0
     tt['Plazo']=curr_table['Plazo']
     tt['TOT_Seg']=curr_table['SEG_INC_SIS']+curr_table['SEG_DESG']
     tt['Dividendo_CSEG']=0
     tt['ValorProp']=int(valprop)
     tt['MontoCre']=int(monto)
     tt['Fecha']=date.today()
     tt['Producto']='HIP-FIJA'
     tt['PlazoFijo']=plz_fijo
     tt['Banco']='ESTADO'
     if prod=='mixta':
          tt=tt.dropna()
          tt['Producto']='HIP-MIX'+ str(plz_fijo)+'Y'
     else :
          tt['Producto']='HIP-FIJA'
     tt=tt.drop_duplicates()
     
     return (tt)
print(simulador(Rut='15654317',Dv='9',valprop=3750,monto=3000,plz=20,plz_fijo=5,prod='mixta',uf=31740)) 