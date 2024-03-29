
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
  rut=Rut
  dv=Dv
  ValorPropiedad=valprop
  MontoCre=monto
  plazo=plz
  if prod=='mixta':
      plz_fijo=5
      tipotasa="2"
  else :
      plz_fijo=0
      tipotasa="1"
  monto=MontoCre
  pie=ValorPropiedad-MontoCre
  http = urllib3.PoolManager()
  rutDv = rutDv = f"{int(rut):,}".replace(',','.') + '-' +dv
  ## rut formato 9.999.999-9
  result = pd.DataFrame([],columns=['Banco','Tasa','Dividendo_SSEG','SEG_DESG','SEG_INC_SIS','CAE','Plazo'])
  url = 'https://www.santander.cl/simuladores/simulador_hipotecario/simulacion.asp'

  #for dtramo in ['111','112','156','135','131','121','120','110']: 
  col=['Tasa','CAE','Div_SSEG','SEG_INCSIS','SEG_DESG','PRIM_DIV','COSTO_TOTCRED','TOT_DIVUF','TOT_DIV$','Plazo','TOT_Seg','Dividendo_CSEG','ValorProp','MontoCre','Fecha','Producto','PlazoFijo','Banco']
  tt=pd.DataFrame([], columns=col)
  for dtramo in ['156','131','120','110']: 
      curr_result=[]
      #Tramos_Renta_SANT=pd.DataFrame( [['111','0-0.4'],['112','0.4-0.55'],['156','0.55-0.8'],
      #                                  ['135',' 0.8-1.3'],['131','1.3-1.7'],['121','1.7-2.5'],
      #                                      ['120','2.5-5'],['110','>5']] , columns=['COD', 'TRAMO'])
      Tramos_Renta_SANT=pd.DataFrame( [['156','0.55-0.8'],['131','1.3-1.7'],['120','2.5-5'],['110','>5']] , columns=['COD', 'TRAMO'])
      CURR_TRAMO=Tramos_Renta_SANT.iloc[np.where(Tramos_Renta_SANT.COD==dtramo)[0][0]].TRAMO
      data = "montoCalculado="+ f"{monto:,}".replace(',','.') + "&noaprob=0&camp_id=&valcamp=&d_pin=&uf=" + f"{uf:,}".replace(',','.') + "%2C34&IDLOGIN=BancoSantander&o=&val1=&cl=false&origen=PB&utm_source=&utm_medium=&utm_campaign=&utm_term=&utm_content=&id_gdconv=" + datetime.now().strftime('%Y%m%d') +"9%3A49%3A23&d_rut="+ rutDv +"&rut=&nombre=sad&apaterno=asd&amaterno=asd&email=a@b.com&codigoarea=2&telefono=22222222&fec_fono=26-5-2022&region=&comuna=BUIN&valor_propiedad="+f"{ValorPropiedad:,}".replace(',','.')+"&valor_propiedad2="+f"{(ValorPropiedad-pie):,}".replace(',','.')+"&valor_pie="+f"{pie:,}".replace(',','.')+"&monto="+f"{MontoCre:,}".replace(',','.')+"&monto2="+f"{MontoCre:,}".replace(',','.')+"&porcentaj="+ str(int(100*((MontoCre)/(ValorPropiedad)))) +"&plazo=" + str(plazo) + "&tipo_tasa="+ tipotasa +"&propiedad=Casa&tipo_propiedad=Nueva&sg_desgravamen=1&sg_incendio=1&dtramo="+ dtramo +"&valuedtramo=&opc=&otrorut=&region1=RM&comuna1=BUIN&z=&valorpyme="                                                                                                                                                                                                                              
      session=requests.Session()
      session.verify=False
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
      t_sleep=random.randrange(25,30)
      #t_sleep=35
      time.sleep(t_sleep)
      print('Pausa para no sobrecargar servidor'+str(t_sleep)+ 'Seg :)')

      tt=tt.append(pd.DataFrame(np.asarray([float(tasa[0]),
      float(cae[0]),
      float(dividendo[1]),
      float(SEG_INC_SIS [0]),
      float(SEG_DESG [0]),
      0,
      0,
      float(dividendo[1])+float(SEG_INC_SIS [0])+float(SEG_DESG [0]),
      (float(dividendo[1])+float(SEG_INC_SIS [0])+float(SEG_DESG [0]))*uf,
      plazo,
      float(SEG_INC_SIS [0])+float(SEG_DESG [0]),
      float(dividendo[1])+float(SEG_INC_SIS [0])+float(SEG_DESG [0]),
      ValorPropiedad,
      MontoCre,
      date.today(),
      'HIP-FIJA',
      plz_fijo,
      'SANT'+CURR_TRAMO ]).reshape(1,-1),columns=col))
      if prod=='mixta':
          tt=tt.dropna()
          tt['Producto']='HIP-MIX'+ str(plz_fijo)+'Y'
      else :
          tt['Producto']='HIP-FIJA'
  tt=tt.drop_duplicates()   
  #asd      
  return(tt)#,str(r.data).replace('\\n','').replace('\\r','').replace('\\t',''))

#print(simulador(Rut='15654317',Dv='9',valprop=3750,monto=3000,plz=20,plz_fijo=5,prod='mixta',uf=29650))   

