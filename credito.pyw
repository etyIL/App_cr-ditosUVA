# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 15:12:59 2024

@author: Estefania
"""
import sys
import os
import ctypes
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import requests
import json
import urllib.request
from urllib.request import urlopen

if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

ventana = Tk()
ventana.config(bg= 'Purple2')
ventana.resizable(1,1)
ventana.title('Simulador de cuotas crédito hipotecario ARGENTINA')
ventana.iconbitmap('credito-hipotecario.ico')

frame= Frame(ventana, bg= 'Purple2', width= 750, height= 800)
frame.pack()
dolar= StringVar(frame)
uva= StringVar(frame)

global cuadro_banco, valor_prop, cuadro_dolar, cuadro_finan, cuadro_uva, cuadro_interes, cuadro_años, Aprestar

def cot_dolar():
    url = "https://dolarapi.com/v1/dolares/oficial"
    req = urllib.request.Request(url,
    headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urlopen(req)
        data = json.loads(response.read())
        valor_dolar = data['venta']
    except:
        messagebox.showerror(message='Hay un problema con la conexión a la API', title='Error')
    dolar.set(valor_dolar)
    return dolar

def cot_uva():
    auth_token='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTEzMDUwNTMsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJldHlpbGluY2hldGFfODVAaG90bWFpbC5jb20ifQ.BppMdqRegdwp8wIidAryMvAUmiBs854PgJf20NIYvnUx4_VxsgAU8--sELBzSxjZRJHI7GmD2xdwJY4WdjVBEw'
    head = {'Authorization': 'Bearer ' + auth_token}
    url= 'https://api.bcra.gob.ar/estadisticas/v2.0/principalesvariables'
    try: 
        response = requests.get(url, headers= head, verify= False)
        json_data=response.json()
        data= pd.DataFrame(json_data['results'])
        UVA= data.iloc[27]['valor']
        uva.set(UVA)
    except:
        messagebox.showerror(message='Hay un problema con la conexión a la API', title='Error')
    return uva
    
        
boton_dolar= Button(frame, text= 'Cotización dólar hoy', foreground= 'white', width=30, command= cot_dolar, bg= 'grey', font= ('Calibri 11 bold'))
boton_dolar.grid(column=0, row=0, pady=4)
cuadro_dolar= Entry(frame, textvariable= dolar, width= 30)
cuadro_dolar.grid(column=0, row=1, pady= 10)

boton_uva= Button(frame, text= 'Cotización UVA hoy',foreground= 'white',  width= 30, command= cot_uva, bg= 'grey', font= ('Calibri 11 bold'))
boton_uva.grid(column=1, row=0, pady=4)
cuadro_uva= Entry(frame, textvariable= uva, width= 30)
cuadro_uva.grid(column=1, row=1, pady=10)

bancos= {
    
    'Nación': {
        'Financiación': 75,
        'Cliente': {
            'Sí': 4.5,
            'No': 8},
        },
    'Macro':{
        'Financiación': 80,
        'Cliente': {
            'Sí': 9.5,
            'No': 11},
        },
    'Del Sol': {
        'Financiación': 80,
        'Cliente': {
            'Sí': 9,
            'No': 12.5},
        },
    'Galicia': {
        'Financiación': 70,
        'Cliente': {
            'Sí': 10,
            'No': 10},
        },
    'BBVA': {
        'Financiación': 80,
        'Cliente': {
            'Sí': 9.5,
            'No': 12.5},
                },
    
    'Supervielle': {
        'Financiación': 80,
        'Cliente': {
            'Sí': 8.5,
            'No': 8.5},
        },
    'Patagonia': {
        'Financiación': 75,
        'Cliente': {
            'Sí': 8.5,
            'No': 9.9},
        },
    'Santander': {
        'Financiación': 80,
        'Cliente': {
            'Sí': 9.5,
            'No': 'No admite'},
        },
    'Hipotecario': {
        'Financiación': 80,
        'Cliente': {
            'Sí': 9.5,
            'No': 9.5},
        },
    'ICBC': {
        'Financiación': 75,
        'Cliente': {
            'Sí': 8.9,
            'No': 10.5},
        },
    
    'BruBank': {
        'Financiación': 70,
        'Cliente': {
            'Sí': 5.5,
            'No': 8},
        },
    'Credicoop': {
        'Financiación': 70,
        'Cliente': {
            'Sí': 7.5,
            'No': 8.5},
        },
    'BPN': {
        'Financiación': 80,
        'Cliente': {
            'Sí': 3.5,
            'No': 8.5},
        },
    'Otro': {
        },
    }



banco_años= {
    'Ciudad': (20,30),
    'Nación': (5, 10, 15, 20, 25, 30),
    'Macro': (20),
    'Del Sol': (20),
    'Galicia': (20),
    'BBVA': (20),
    'Bancor': (20),
    'Supervielle': (20,30),
    'Patagonia': (20,30),
    'Santander': (30),
    'Hipotecario': (20,30),
    'ICBC': (15),
    'BanCO': (20),
    'BruBank': (20,30),
    'Credicoop': (20,30),
    'BPN': (20),
    'Otro': '',
    }



label_banco= Label(frame, text= 'BANCO', foreground= 'white', width=30, bg= 'Purple2', font= ('Calibri', 11, 'bold'))
label_banco.grid(columnspan=2, row=3)


financiacion= StringVar(frame)

def Financiacion():
    banco= cuadro_banco.get()
    if banco != '' and banco!= 'Otro':
        finan_bco= bancos[banco]['Financiación']
        financiacion.set(finan_bco)      
    elif banco== 'Otro':
        ventana2= Tk()
        ventana2.config(bg= 'Purple2')
        ventana2.resizable(1,1)
        ventana2.geometry('520x400')
        ventana2.title('Simulador de cuotas crédito hipotecario ARGENTINA')
        ventana2.iconbitmap('credito-hipotecario.ico')
        label_banco2= Label(ventana2, text= 'Ingrese BANCO', font= ('Calibri',11, 'bold'), foreground= 'white', bg= 'Purple2')
        label_banco2.grid(column= 1, row= 1, pady= 4, padx= 6)
        banco= Entry(ventana2, width= 20)
        banco.grid(column= 1, row= 2, pady= 4)
        label_financiacion2= Label(ventana2, text= 'Financiación (%)', font= ('Calibri', 11, 'bold'), foreground= 'white', bg= 'Purple2')
        label_financiacion2.grid(column= 0, row= 3, pady= 4, padx= 6)
        financiacion2= Entry(ventana2, width= 20)
        financiacion2.grid(column= 0, row= 4, pady= 4, padx= 6)
        label_tasa= Label(ventana2, text= 'Tasa de interés', font= ('Calibri', 11, 'bold'), foreground= 'white', bg= 'Purple2')
        label_tasa.grid(column= 1, row= 3, pady= 4, padx= 6)
        tasa= Entry(ventana2, width= 20)
        tasa.grid(column= 1, row= 4, pady= 4, padx= 6)
        label_años2= Label(ventana2, text= 'Años', font= ('Calibri', 11, 'bold'), foreground= 'white', bg= 'Purple2')
        label_años2.grid(column= 2, row= 3, pady= 4, padx= 6)
        años2= ttk.Combobox(ventana2, state= 'readonly', values= ['15','20','25','30'], width= 20)
        años2.grid(column= 2, row= 4, pady= 4, padx= 6)
        label_prop= Label(ventana2, text= 'Valor propiedad (USD)', font= ('Calibri', 11, 'bold'), foreground= 'white', bg= 'Purple2')
        label_prop.grid(column= 1, row= 5, pady= 4, padx= 6)
        prop= Entry(ventana2, width= 20)
        prop.grid(column= 1, row= 6, pady= 4, padx= 6)
        
        def prestamo():
            if prop!= '':
                try:
                    propiedad= prop.get()
                    propiedad= float(propiedad)
                    valor= StringVar(ventana2)
                    finan2= financiacion2.get()
                    finan2= int(finan2)
                    finan2= float(finan2*0.01)
                    dolar= cuadro_dolar.get()
                    dolar= float(dolar)
                    prestar= propiedad*finan2*dolar
                    valor.set(prestar)
                    prestamo_ARS= Entry(ventana2, textvariable= valor, width= 20)
                    prestamo_ARS.grid(column= 1, row= 7, pady= 4, padx= 4)
                    
                except:
                    messagebox.showerror(message='Hay campos sin completar', title='Error')
                    banco.delete(0, END)
                    financiacion2.delete(0, END)
                    tasa.delete(0, END)
                    años2.set('')
                    prop.delete(0, END)
                    
                else:
                    def borrar_pres():
                        prestamo_ARS.delete(0, END)
                        
                    borrar_pres= Button(ventana2, text= 'Borrar', bg= 'grey', foreground= 'white', font= ('Calibri 11 bold'), command= borrar_pres)
                    borrar_pres.grid(column= 2, row= 7, padx= 6)
                   
                    return prestar
          
        def UVA():
            try:
                si_prestamo= prestamo()
                UVAs= StringVar(ventana2)
                tasa_int= tasa.get()
                tasa_int= float(tasa_int)
                UVA_= cuadro_uva.get()
                UVA_= float(UVA_)
                
                i= float(tasa_int*(0.0833)*(0.01))
                años= años2.get()
                años= int(años)
                meses= int(años*12)
                F1= (1+i)**(-meses)
                F2= (1-F1)/i
                enuva= si_prestamo/UVA_
                cuotauva= round(enuva/F2, 2)
                UVAs.set(cuotauva)
                cuota_UVA= Entry(ventana2, textvariable= UVAs, width= 20)
                cuota_UVA.grid(column= 1, row= 8)
                
            except:
                messagebox.showerror(message='Hay campos sin completar', title='Error')
                banco.delete(0, END)
                financiacion2.delete(0, END)
                tasa.delete(0, END)
                años2.set('')
                prop.delete(0, END)  
            
            else:
                def borrar_uva():
                    cuota_UVA.delete(0, END)
                uva_borrar= Button(ventana2, text= 'Borrar', bg= 'grey', foreground= 'white', font= ('Calibri 11 bold'), command= borrar_uva)
                uva_borrar.grid(column= 2, row= 8, padx= 6)
                
                return cuotauva
        
        def pesos():
            try:
                si_uva= UVA()
                PESOS= StringVar(ventana2)
                UVa= cuadro_uva.get()
                UVa= float(UVa)
                cuotapesos= round(UVa*si_uva, 2)
                PESOS.set(cuotapesos)
                cuadro_pesos= Entry(ventana2, textvariable= PESOS, width= 20)
                cuadro_pesos.grid(column=1, row=9)
                
            except:
                messagebox.showerror(message='Hay campos sin completar', title='Error')
                banco.delete(0, END)
                financiacion2.delete(0, END)
                tasa.delete(0, END)
                años2.set('')
                prop.delete(0, END)
                
            else:
                def pesos_borrar():
                    cuadro_pesos.delete(0, END)
                
                borrar_pesos= Button(ventana2, text= 'Borrar', bg= 'grey', foreground= 'white', font= ('Calibri 11 bold'), command= pesos_borrar)
                borrar_pesos.grid(column= 2, row= 9, padx= 6)
                
                return cuotapesos

        boton_prestar= Button(ventana2, text= 'Calcular préstamo (ARS)', foreground= 'white', bg= 'grey', font= ('Calibri 11 bold'), command= prestamo, width= 20)
        boton_prestar.grid(column= 0, row= 7, padx= 4, pady= 4)
        
        boton_uva= Button(ventana2, text= 'Calcular cuota UVA hoy', foreground= 'white', bg= 'grey', font= ('Calibri 11 bold'), command= UVA, width= 20)
        boton_uva.grid(column= 0, row= 8, padx= 4, pady= 4)
        
        boton_pesos= Button(ventana2, text= 'Calcular cuota ARS hoy', foreground= 'white', bg= 'grey', font= ('Calibri 11 bold'), command= pesos, width= 20)
        boton_pesos.grid(column= 0, row= 9, padx= 4, pady= 4)
        
        def borrar_():
            banco.delete(0, END)
            financiacion2.delete(0, END)
            tasa.delete(0, END)
            años2.set('')
            prop.delete(0, END)
            
            
        def cerrar_():
            ventana2.destroy()
            
        borrar_boton= Button(ventana2, text= 'Borrar', foreground= 'white', bg= 'grey', font= ('Calibri 11 bold'), command= borrar_, width= 20)
        borrar_boton.grid(column= 0, columnspan= 2, row= 11, pady= 6, padx= 6)
        
        borrar_boton= Button(ventana2, text= 'Cerrar', foreground= 'white', bg= 'grey', font= ('Calibri 11 bold'), command= cerrar_, width= 20)
        borrar_boton.grid(column= 2, row= 11, pady= 6, padx= 6)
           
     
    else:
        messagebox.showerror(message='Seleccione un banco', title='Error')
    return financiacion

boton_financiacion= Button(frame, text= ' Ver financiación (%)', foreground= 'white', bg= 'grey', font= ('Calibri 11 bold'), command= Financiacion, width= 20)
boton_financiacion.grid(columnspan=2, row=5, pady=10)

cuadro_finan= Entry(frame, textvariable=financiacion , width= 10)
cuadro_finan.grid(columnspan=2, row=6, pady=4)

label_años= Label(frame, text= 'Cantidad de años', foreground= 'white', font= ('Calibri', 11, 'bold'), width= 30, bg= 'Purple2')
label_años.grid(column=0, row=7)


def on_combobox_select(event):
    cuadro_años.set("")
    cuadro_años.config(values=banco_años[cuadro_banco.get()])

cuadro_banco= ttk.Combobox(frame, state= 'readonly', values=tuple(banco_años.keys()), width= 20)
cuadro_banco.grid(columnspan=2, row=4)
cuadro_banco.bind("<<ComboboxSelected>>", on_combobox_select)

cuadro_años= ttk.Combobox(frame, width= 20, state="readonly")
cuadro_años.grid(column= 0, row=8, pady=4)

label_cliente= Label(frame, text= 'Cliente', foreground= 'white', font= ('Calibri', 11,'bold'), width= 20, bg= 'Purple2')
label_cliente.grid(column=1, row=7)


def on_combobox_select2(event):
    if cuadro_banco!= '':
        try: 
            banco= cuadro_banco.get()
            interes= StringVar(frame)
            value= bancos[banco]['Cliente'][cuadro_cliente.get()]
            interes.set(value)
            
            label_interes= Label(frame, text= 'Tasa de interés', foreground= 'white', font= ('Calibri', 11, 'bold'), width= 30, bg= 'Purple2')
            label_interes.grid(columnspan=2, row=9, pady= 4)
            cuadro_interes= Entry(frame, textvariable= interes, state= 'readonly', width= 20)
            cuadro_interes.grid(columnspan=2, row=10)
            label_valor_prop= Label(frame, text= 'Valor de la propiedad (USD)', foreground= 'white', font= ('Calibri', 11, 'bold'), width= 30, bg= 'Purple2')
            label_valor_prop.grid(columnspan=2, row=11, pady=4)
            valor_prop= Entry(frame, width= 20)
            valor_prop.grid(columnspan=2, row= 12, pady=4)
            
            def cal_prestamo():
                try:
                    pres= StringVar(frame)
                    prop= valor_prop.get()
                    prop= float(prop)
                    
                    dolar= cuadro_dolar.get()
                    dolar= float(dolar)
                    
                    finan= cuadro_finan.get()
                    finan= int(finan)
                    finan= float(finan*0.01)
                    
                    Aprestar= prop*dolar*finan
                    pres.set(Aprestar)
                    prestamo= Entry(frame, textvariable= pres, width= 20)
                    prestamo.grid(column=1, row=13, pady=4 )
                    
                except:
                    cuadro_dolar.delete(0, END)
                    valor_prop.delete(0, END)
                    cuadro_finan.delete(0, END)
                    cuadro_uva.delete(0, END)
                     
                    cuadro_banco.set('')
                    cuadro_interes.delete(0, END)
                    cuadro_años.set('')
                    messagebox.showerror(message='Por favor, ingrese el valor de la propiedad y/o verifique el resto de los campos', title='Error')
                
                else:   
                    def borrar1():
                        prestamo.delete(0, END)
                        valor_prop.delete(0, END)
                        
                    boton_borrar_pres= Button(frame, text= 'Borrar', foreground= 'white', font= ('Calibri 11 bold'), bg= 'grey', command= borrar1)
                    boton_borrar_pres.grid(column=1, row=14)
                    
                    return Aprestar
            
            def cuota_UVA():
                #if cal_prestamo()== True:
                    try:
                        Aprestar= cal_prestamo()
                        cuota_uva= StringVar(frame)
                        tasa= cuadro_interes.get()
                        tasa= float(tasa)
                        
                        UVA= cuadro_uva.get()
                        UVA= float(UVA)
                        
                        i= float(tasa*(0.0833)*(0.01))
                        años= cuadro_años.get()
                        años= int(años)
                        meses= int(años*12)
                        F1= (1+i)**(-meses)
                        
                        F2= (1-F1)/i
                        valor_enuva= Aprestar/UVA
                        cuota= round(valor_enuva/F2, 2)
                        cuota_uva.set(cuota)
                        cuadro_cuota_UVA= Entry(frame, textvariable= cuota_uva, width= 20)
                        cuadro_cuota_UVA.grid(column=1, row=15)
                        
                    except:
                        cuadro_dolar.delete(0, END)
                        valor_prop.delete(0, END)
                        cuadro_finan.delete(0, END)
                        cuadro_uva.delete(0, END)
                        
                        cuadro_banco.set('')
                        cuadro_interes.delete(0, END)
                        cuadro_años.set('')
                        messagebox.showerror(message='Faltan las cotizaciones del día o algún dato. Revise y vuelva a intentarlo', title='Error')
                    
                    else:
                        def borrar2():
                            cuadro_cuota_UVA.delete(0, END)
                        
                        boton_borrar_uva= Button(frame, text= 'Borrar', foreground= 'white', font= ('Calibri 11 bold'), bg= 'grey', command= borrar2)
                        boton_borrar_uva.grid(column=1, row=16)
                
                        return cuota
              
            def cuota_pesos():
                    try:
                        pesos= StringVar(frame)
                        uvas= cuota_UVA()
                        valor_uva= cuadro_uva.get()
                        valor_uva= float(valor_uva)
                        cuota_pesos= round((valor_uva*uvas), 2)
                        pesos.set(cuota_pesos)
                        cuadro_cuota_pesos= Entry(frame, textvariable= pesos, width= 20)
                        cuadro_cuota_pesos.grid(column=1, row=17)
                        
                    except:
                        cuadro_dolar.delete(0, END)
                        valor_prop.delete(0, END)
                        cuadro_finan.delete(0, END)
                        cuadro_uva.delete(0, END)
                        
                        cuadro_banco.set('')
                        cuadro_interes.delete(0, END)
                        cuadro_años.set('')
                        messagebox.showerror(message='Faltan las cotizaciones del día o algún dato. Revise y vuelva a intentarlo', title='Error')
                    
                    else:
                        def borrar3():
                            cuadro_cuota_pesos.delete(0, END)
                            interes.set('')
                        
                        boton_borrar_pesos= Button(frame, text= 'Borrar', foreground= 'white', font= ('Calibri 11 bold'), bg= 'grey', command= borrar3)
                        boton_borrar_pesos.grid(column=1, row=18)
                        
                        return cuota_pesos
                      
            boton_prestamo= Button(frame, text= 'Ver monto a prestar (ARS)', foreground= 'white', font= ('Calibri 11 bold'), bg= 'grey', command= cal_prestamo, width= 30)
            boton_prestamo.grid(column=0, row=13, pady=4)
            
            boton_cuota_UVA= Button(frame, text= 'Cuota en UVAs hoy', foreground= 'white', font= ('Calibri 11 bold'), bg= 'grey', command= cuota_UVA, width= 30)
            boton_cuota_UVA.grid(column=0, row=15, pady=4, padx=4)
            
            boton_cuota_pesos= Button(frame, text= 'Cuota en pesos (ARS) hoy', foreground= 'white', font= ('Calibri 11 bold'), bg= 'grey', command= cuota_pesos, width= 30)
            boton_cuota_pesos.grid(column=0, row=17, pady=4, padx=4)
                
        except:
            messagebox.showerror(message='Por favor, seleccione un banco y vuelva a intentarlo', title='Error')
            
        return interes  
        
cuadro_cliente= ttk.Combobox(frame, state= 'readonly', values= ['Sí', 'No'], width= 20)
cuadro_cliente.grid(column= 1, row= 8, pady= 4)
cuadro_cliente.bind("<<ComboboxSelected>>", on_combobox_select2)

def borrar():
    cuadro_dolar.delete(0, END)
    cuadro_uva.delete(0, END)
    cuadro_banco.set('')
    cuadro_finan.delete(0, END)
    cuadro_años.set('')
    cuadro_cliente.set('')
    
        
def cerrar():
    ventana.destroy()

boton_borrar= Button(frame, text= 'Borrar', foreground= 'white', font= ('Calibri 11 bold'), bg= 'grey', command= borrar, width= 20)
boton_borrar.grid(column= 0, row= 20, pady= 4, padx= 4)

boton_cerrar= Button(frame, text= 'Cerrar', foreground= 'white', font= ('Calibri 11 bold'), bg= 'grey', command= cerrar, width= 20)
boton_cerrar.grid(column= 1, row= 20, pady= 4, padx= 4)
     
  
ventana.mainloop()

