from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib import messages
from .models import Project
from .functions import handle_uploaded_file
from .functions import filename
from .functions import mainApp1Function
from .forms import StudentForm

import json
from celery import shared_task,current_task
from numpy import random
from scipy.fftpack import fft
from scipy import optimize

import numpy as np
from numpy import array,zeros, matrix
import matplotlib as plt

import scipy.optimize
from scipy.stats import norm

import csv
import random
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import math
import datetime
import re
import calendar

# Create your views here.
def home(request):
        return render(request,"core/dashboard.html",{})

def App1(request):
    if request.method == 'POST':
        student = StudentForm(request.POST, request.FILES)
        if student.is_valid():
            id_file='core/static/core/data/cb' + str(np.random.randint(100)) + '.csv'
         #id_file='/opt/bitnami/apps/django/django_projects/cb_v4/core/static/core/data/cb' + str(np.random.randint(100)) + '.csv'
            handle_uploaded_file(request.FILES['file'], id_file)
            messages.success(request, "Archivo CSV preparado")
            return render(request,"core/home.html",{'form':student, 'id_file': id_file, 'display':'block'})
    else:
        student = StudentForm()
        return render(request,"core/home.html",{'form':student, 'display':'none'})

def App2(request):
        res = mainApp1Function()
        return render(request,"core/app2.html",{'res':res})
def App3(request):
        projects = Project.objects.all()
        return render(request,"core/app3.html",{'proyectos':projects})
def App4(request):
        return render(request,"core/app4.html",{})
def App5(request):
        return render(request,"core/app5.html",{})
def App6(request):
        return render(request,"core/app6.html",{})

def about(request):
        return HttpResponse("<h2>Acerca de</h2>")

def calc_tir(request):
    if request.method=="POST":
        return render(request,"core/home.html",{ 'display':'none'})

def cb_final(request):

    if request.method=="POST":
        data= request.POST

        input_fecha_inicio = data["fecha_inicio"]
        #input_fecha_inicio = "ene-2016"

        rondas = int(data["rondas"])
        #td1
        tasa_des_min = float(data["tasa_des_min"])
        #td2(original .12)
        tasa_des_base = float(data["tasa_des_base"])
        #td3
        tasa_des_max = float(data["tasa_des_max"])
        sitirb = data["tir"]
        separador = data["separador"]
        comillar = data["comillar"]
        id_file = data["id_file"]
        monte_carlo = data["monte_carlo"]
        #sitirb al parecer es una variable temporal.



        fechas = {
            "ene" : 1,
            "feb" : 2,
            "mar" : 3,
            "abr" : 4,
            "may" : 5,
            "jun" : 6,
            "jul" : 7,
            "ago" : 8,
            "sep" : 9,
            "oct" : 10,
            "nov" : 11,
            "dic" : 12
        }
        # Anual divide la cantidad entre 12
        # Cada año pone un uno en un mes y lo repite hasta el otro año

        impacto = {
            "Positivo" : -1,
            "Negativo" : +1
        }



        #proposito solo tiene 2 valores, 0 y 1
        #externalidades solo tiene 2 valores, 0 y 1 (1= si)
        # Modelos

        file_path = id_file
        data_file = np.loadtxt(file_path, delimiter=",", dtype=str, skiprows=1)
        data = data_file
        a = np.array(data)

        tir = False
        separador = ","
        comillar = "doble"
        #sitirb al parecer es una variable temporal.

        try:
            a[0,0]

        except:
            a = np.resize(a, (2,21))
            for x in range(a.shape[1]):
                if(str(a[0,x]) != str(a[0,0]) and str(a[0,x]) != str(a[0,14]) and str(a[0,x]) != str(a[0,15])):
                    a[0,x]=0

        input_fecha_inicio = input_fecha_inicio.split("-")

        try:
            int(a[1][0])
            col_adjust = 1
        except:
            col_adjust = 0

        col_name = {
                "ID" : 0 + col_adjust,
                "Tipo" : 1 + col_adjust,
                "Impacto" : 2 + col_adjust,
                "Categoria" : 3 + col_adjust,
                "Detalles" : 4 + col_adjust,
                "prop" : 5 + col_adjust,
                "Frecuencia" : 6 + col_adjust,
                "Unidad_de_medida" : 7 + col_adjust,
                "Cantidad" : 8 + col_adjust,
                "Cant_pesimista" : 9 + col_adjust,
                "Cant_optimista" : 10 + col_adjust,
                "p" : 11 + col_adjust,
                "p_pes" : 12 + col_adjust,
                "p_opt" : 13 + col_adjust,
                "fecha_inicio" : 14 + col_adjust,
                "fecha_final" : 15 + col_adjust,
                "externalidad" : 16 + col_adjust,
                "modelo" : 17 + col_adjust,
                "coef1" : 18 + col_adjust,
                "coef2" : 19 + col_adjust,
                "coef3" : 20 + col_adjust
        }
        def armar_fecha(fecha):
            cb_fecha_decorado = fecha.split('-')
            cb_fecha_mes = cb_fecha_decorado[0]
            cb_fecha_ano = cb_fecha_decorado[1]
            return(int(cb_fecha_ano),fechas[cb_fecha_mes],1)

        #FUNCION CORRECTA
        def rango_fechas(desde, hasta, diferencia):
            desp=2
            if(desde == hasta or desde > hasta or diferencia):
                desp=0
            #diferencia de dias
            return (hasta.year - desde.year) * 12 +  hasta.month - desde.month + desp

        def logar(x,t,coef1,coef2):
            if(t<=0):
                var = 0
            else:
                var = (float(coef1)+float(coef2)*math.log(t)) * x
            return var

        def taylor(x,t,coef1,coef2, coef3 ):
            if(t<=0):
                var = 0        
            else:    
                var = (float(coef1)+float(coef2)*(t) + float(coef3) *(t**2))*x

            return var

        def fexp(x,t,coef1,coef2, coef3 ):
            if(t<=0):
                var = 0
            else:
                var = (float(coef1)+float(coef2)*math.exp(t*float(coef3)))* x
            return var

        def bass(x,t,coef1,coef2):
            if(t<=0):
                var = 0
            else:
                var = ((((float(coef1)+float(coef2))**2)/float(coef1))*((math.exp(-(float(coef1)+float(coef2))*t))/((1+(float(coef2)/float(coef1))* math.exp(-(float(coef1)+float(coef2))*t))**2))) * (x)
            return var

        def binomial(x,t,coef1,coef2):
            if(t<=0):
                var = 0
            else:
                var = np.random.binomial(float(coef1),float(coef2)) * x
            return var

        try:
            input_fecha_inicio[2]
            dia_split= input_fecha_inicio[0]
            mes_split = input_fecha_inicio[1]
            año_split = input_fecha_inicio[2]
        except:
            mes_split = input_fecha_inicio[0]
            año_split = input_fecha_inicio[1]
            dia_split = 1


        #estas variables son para hacer las operacion de suma y resta de fechas
        fecha_global_R = ""
        cb_fecha_inicio = []
        cb_fecha_final = []
        cb_diferencia_fechas = []

        cb_rango_fechas= []
        cb_mes_inicio = []
        cb_mes_final =[]
        cb_posicion_mes = []

        matrix_mes_inicio = []
        matrix_duracion_meses = []

        #unidad de medida
        cb_unidad_medida = []

        #prop
        cb_tipo = []
        cb_prop = []

        #Variables del doc
        pq = []

        #Variables de texto
        cb_detalle = []


        #variables de control
        ctrl1 = []

        #Esta variable es para colocar los positivos y negativos
        cb_impacto = []
        cb_modelo = []
        cb_coef1 = []
        cb_coef2 = []
        cb_coef3 = []
        #estas variables son para p, pes, opt(precio pesimista, precio, precio optimista)

        cb_p = []
        cb_p_pes = []
        cb_p_opt = []

        #cb cantidades
        cb_cantidad = []
        cb_cantidad_pes = []
        cb_cantidad_opt = []

        cb_externalidad = []
        cb_fuentes = []
        cb_categoria = []
        #frecuencias
        cb_tiempos_periodos = ["Mensual", "Anual", "Bianual", "Trianual", "Sexenal", "Semestral", "Trimestral"]
        cb_tiempos_periodos_int = [1,12,24,36,72,6,3]
        cb_tiempos_meses_str = ["Cada mes", "Cada 2 meses", "Cada 3 meses", "Cada 4 meses", "Cada 5 meses", "Cada 6 meses", "Cada año", "Cada 2 años", "Cada 3 años", "Cada 4 años", "Cada 5 años", "Cada 6 años", "Mensual", "Anual", "Bianual", "Trianual", "Sexenal", "Semestral", "Trimestral"]
        cb_tiempos_meses_int = [1,2,3,4,5,6,12,24,36,48,60,72,1,1,1,1,1,1,1]

        cb_frecuencias = []



        diferencia_base = abs(date(int(año_split),int(fechas[mes_split]),int(dia_split)) - date(1900,1,1))

        fecha_global_R = date(1900,1,1) + timedelta(days=diferencia_base.days)

        diferencia_fechas = 0
        vpn_social_1 = 0.0
        vpn_social_2 = 0.0
        vpn_social_3 = 0.0
        vpn_privado = 0.0
        vpn_externalidades = 0.0
        costos = 0.0
        beneficios = 0.0
        icb = 0.0
        fae1 = 0.0
        fae2 = 0.0
        fae3 = 0.0
        plazo = 0.0
        ice = 0.0
        cantidad_ice = 0.0
        vpn_pesimista = 0.0
        vpn_base = 0.0
        vpn_optimista = 0.0
        tir = 0.0
        casos_positivos = 0.0
        app = 0.0
        random_sel = 0.0
        #columna ID se utiliza al final
        #Columna tipo no se usa

        columnas_totales = a.shape[1]
        filas_totales = a.shape[0]
        np.random.seed(int(monte_carlo))

        if(int(a.shape[1]) > 21):
            col_name.update({'Fuentes' : 21+ col_adjust})   


        for col in range(a.shape[1]):

            if (col == col_name["prop"]):
                    for prop in a[:,col]:
                        cb_prop.append(re.sub('"', '', prop))

            if (col == col_name["Tipo"]):
                    for tipo in a[:,col]:
                        cb_tipo.append(re.sub('"', '', tipo))

            if (col == col_name["Frecuencia"]):
                    for meses in a[:,col]:
                        cb_frecuencias.append(re.sub('"', '', meses))

            if (col == col_name["Impacto"]):
                    for imp in a[:,col]:
                        cb_impacto.append(imp)
            if (col == col_name["Unidad_de_medida"]):
                    for i in a[:,col]:
                           cb_unidad_medida.append(i)
            if (col == col_name["Detalles"]):
                    for det in a[:,col]:
                        cb_detalle.append(det)

            if (col == col_name["p"]):
                    for p in a[:,col]:
                        cb_p.append(p)

            if (col == col_name["p_pes"]):
                    for p_pes in a[:,col]:
                        cb_p_pes.append(p_pes)

            if (col == col_name["p_opt"]):
                    for p_opt in a[:,col]:
                        cb_p_opt.append(p_opt)
                    #PARA CADA ARREGLO YA COMPLETO SE VAN A HACER LAS SIGUIENTES OPERACIONES

            if (col == col_name["externalidad"]):
                    for ext in a[:,col]:
                        cb_externalidad.append(ext)

            if (col == col_name["Categoria"]):
                    for cat in a[:,col]:
                        cb_categoria.append(cat)

            if (col == col_name["modelo"]):
                    for model in a[:,col]:
                        cb_modelo.append(model)

            if(int(a.shape[1]) > 21):
                if (col == col_name["Fuentes"]):
                        for fuente in a[:,col]:
                            cb_fuentes.append(fuente)
            else:
                for fuente in a[:,col]:
                    cb_fuentes.append("Sin fuentes")    
            if (col == col_name["Cantidad"]):
                    for cantidad in a[:,col]:
                        cb_cantidad.append(cantidad)


            if (col == col_name["Cant_pesimista"]):
                    for cant_pesimista in a[:,col]:
                        cb_cantidad_pes.append(cant_pesimista)

            if (col == col_name["Cant_optimista"]):
                    for cant_opt in a[:,col]:
                        cb_cantidad_opt.append(cant_opt)


            if (col == col_name["fecha_inicio"]):
          #          for row in a[:,col]:
          #              if(row == fecha_inicio):
          #                  ctrl1.append("1")
          #              else:
          #                  ctrl1.append("0")

                    for fecha_inicio in a[:,col]:
                        cb_fecha_inicio_decorado = armar_fecha(fecha_inicio)
                        cb_fecha_inicio.append(cb_fecha_inicio_decorado)
                        posicion_mes = fecha_inicio.split("-")
                        posicion_mes = fechas[posicion_mes[0]]
                        cb_posicion_mes.append(posicion_mes)

                    for fecha_final in a[:,col + 1]:
                        cb_fecha_final_decorado = armar_fecha(fecha_final)
                        cb_fecha_final.append(cb_fecha_final_decorado)


            if (col == col_name["coef1"]):
                for coef in a[:,col]:
                    cb_coef1.append(coef)
                for coef in a[:,col + 1 ]:
                    cb_coef2.append(coef)
                for coef in a[:,col + 2 ]:
                    cb_coef3.append(coef)




        for i in range(a.shape[0]):
            cb_diferencia_final = cb_fecha_final[i]
            cb_diferencia_inicio = cb_fecha_inicio[i]

            cb_rango_fechas.append(rango_fechas(datetime.date(cb_fecha_inicio[i][0],cb_fecha_inicio[i][1],cb_fecha_inicio[i][2]), datetime.date(cb_fecha_final[i][0],cb_fecha_final[i][1],cb_fecha_final[i][2]), 0) - 1)

            cb_mes_inicio.append(rango_fechas(fecha_global_R,datetime.date(cb_fecha_inicio[i][0],cb_fecha_inicio[i][1],cb_fecha_inicio[i][2]),1))

            cb_mes_final.append(abs(cb_rango_fechas[i]) + abs(cb_mes_inicio[i]))
            #cb_rango_fechas.append(rango_fechas(datetime.date(1900,1,1), datetime.date(2016,1,1)))


        for i in range(a.shape[0]):
            if(cb_impacto[i] == 'Negativo'):
                cb_p[i] = -(float(cb_p[i]))
                cb_p_pes[i] = -(float(cb_p_pes[i]))
                cb_p_opt[i] = -(float(cb_p_opt[i]))
                #  "uno es de:" + str(cb_diferencia_fechas[i]) + "la longitud del arreglo es de: " + str(len(cb_diferencia_fechas)) )



        ctrl1= []
        ctrl2= zeros([filas_totales, np.amax(cb_mes_final)])
        ctrl1_a = zeros([filas_totales, np.amax(cb_mes_final)])
        ttt=np.amax(cb_mes_final)


        ctrl2=zeros([int(a.shape[0]), ttt])

        for i in range(filas_totales):
            for j in range(cb_rango_fechas[i]):
                for tiempo in range(len(cb_tiempos_meses_str)):
                    if(cb_frecuencias[i] == cb_tiempos_meses_str[tiempo]):
                        for ciclo in range(cb_mes_inicio[i]-1, cb_mes_inicio[i] + cb_rango_fechas[i]-1, cb_tiempos_meses_int[tiempo]):
                            ctrl2[i][ciclo+1] = 1


        for i in range(filas_totales):
                if(cb_frecuencias[i] == "Inicial (única vez)"):
                    ctrl2[i][cb_mes_inicio[i]] = 1



        headers = ["pmin", "pmean", "pmax", "qmin", "qmean", "qmax", "psd", "qsd"]
        colnames = zeros([int(a.shape[0]), 8], dtype = object)
        #for header in range(8):
        #    colnames[0][header] = headers[header]
        for r in range (0, a.shape[0]):
            #pmin
            colnames[r][0] = float(cb_p_pes[r])
            #pmean
            colnames[r][1] = float(cb_p[r])
            #pmax
            colnames[r][2] = float(cb_p_opt[r])
            colnames[r][3] = float(cb_cantidad_pes[r])
            colnames[r][4] = float(cb_cantidad[r])
            colnames[r][5] = float(cb_cantidad_opt[r])
            for j in range(len(cb_tiempos_periodos)):
                if(cb_frecuencias[r] == cb_tiempos_periodos[j]):
                    #qmin
                    colnames[r][3] = float(cb_cantidad_pes[r])/cb_tiempos_periodos_int[j]
                    #qmean
                    colnames[r][4] = float(cb_cantidad[r])/cb_tiempos_periodos_int[j]
                    #qmax
                    colnames[r][5] = float(cb_cantidad_opt[r])/cb_tiempos_periodos_int[j]
            #psd
            colnames[r][6] = abs((float(cb_p_opt[r]) - float(cb_p_pes[r]))/4)
            #qsd
            colnames[r][7] = abs((float(colnames[r][5]) - float(colnames[r][3]))/4)



        p_rand = zeros([a.shape[0], rondas])
        q_rand = zeros([a.shape[0], rondas])

        #aqui se debe escoger tambien por el usuario el tipo de distribucion por default esta la normal


        for n in range (a.shape[0]):
            p_rand[n,:] = np.random.normal(float(colnames[n ,1]), float(colnames[n,6]), rondas)
            q_rand[n,:] = np.random.normal(float(colnames[n ,4]), float(colnames[n,7]), rondas)

        pq_rand = p_rand * q_rand

        desc_v1 = zeros([filas_totales, ttt])
        desc_v2 = zeros([filas_totales, ttt])
        desc_v3 = zeros([filas_totales, ttt])

        for t in range(ttt):
            desc_v1[:,t] = 1.0/(1 + ((1+tasa_des_min)**(1/12.0)-1)) ** (t+1)
            desc_v2[:,t] = 1.0/(1 + ((1+tasa_des_base)**(1/12.0)-1)) ** (t+1)
            desc_v3[:,t] = 1.0/(1 + ((1+tasa_des_max)**(1/12.0)-1)) ** (t+1)
            #BACKUP DE TASA DE DESCUENTO desc_v1[:,t] = 1.0/(1 + tasa_des_min/12.0) ** (t+1)


        ctrl2f = zeros([filas_totales,ttt])
        for t in range(ttt):

            for n in range(filas_totales):
                if(str(cb_modelo[n]) == "Lineal"):
                    ctrl2f[n,t] = ctrl2[n,t]
                if(str(cb_modelo[n]) == "Logarítmica"):
                    ctrl2f[n,t] = ctrl2[n,t]*logar(1,t-cb_mes_inicio[n]+1,cb_coef1[n],cb_coef2[n])
                if(cb_modelo[n] == "Taylor"):
                    if(cb_coef3[n] == ""):
                        cb_coef3[n] = 0
                    ctrl2f[n,t] = ctrl2[n,t]*taylor(1,t-cb_mes_inicio[n]+1,cb_coef1[n],cb_coef2[n],cb_coef3[n])
                if(str(cb_modelo[n]) == "Exponencial"):
                    ctrl2f[n,t] = ctrl2[n,t]*fexp(1,t-cb_mes_inicio[n]+1,cb_coef1[n],cb_coef2[n],cb_coef3[n])
                if(str(cb_modelo[n]) == "Binomial"):
                    ctrl2f[n,t] = ctrl2[n,t]*binomial(1,t-cb_mes_inicio[n]+1,cb_coef1[n],cb_coef2[n])
                if(str(cb_modelo[n]) == "Bass (Modelo de difusión)"):
                    ctrl2f[n,t] = ctrl2[n,t]*bass(1,t-cb_mes_inicio[n]+1,cb_coef1[n],cb_coef2[n])

        for n in range(filas_totales):
            if(str(cb_modelo[n]) == "Bass (Modelo de difusión)" and cb_coef3[n] == "1"):
                ctrl2f[n,:] = np.cumsum(ctrl2f[n,:])

        ctrl3=ctrl2f


        ctrl3_td1 = np.mean(sum(np.dot(np.transpose(ctrl3*desc_v1), pq_rand)))
        ctrl3_td2 = np.mean(sum(np.dot(np.transpose(ctrl3*desc_v2), pq_rand)))
        ctrl3_td3 = np.mean(sum(np.dot(np.transpose(ctrl3*desc_v3), pq_rand)))
        ctrl3_td1e = np.std(sum(np.dot(np.transpose(ctrl3*desc_v1), pq_rand)),ddof=1)
        ctrl3_td2e = np.std(sum(np.dot(np.transpose(ctrl3*desc_v2), pq_rand)),ddof=1)
        ctrl3_td3e = np.std(sum(np.dot(np.transpose(ctrl3*desc_v3), pq_rand)),ddof=1)


        diferencia_fechas = 0
        vpn_social_1 = ctrl3_td2
        vpn_social_1_std = ctrl3_td2e

        vpn_social_2 = ctrl3_td1
        vpn_social_2_std = ctrl3_td1e

        vpn_social_3 = ctrl3_td3
        vpn_social_3_std = ctrl3_td3e


        #VPN BASE


        vpn_min= sum(sum(np.transpose((colnames[:,0]*colnames[:,3]) * np.transpose(ctrl3) * np.transpose(desc_v2))))
        vpn_mean= sum(sum(np.transpose((colnames[:,1]*colnames[:,4]) * np.transpose(ctrl3) * np.transpose(desc_v2))))
        vpn_max= sum(sum(np.transpose((colnames[:,2]*colnames[:,5]) * np.transpose(ctrl3) * np.transpose(desc_v2))))
        #x * np.transpose(np.array([y,]*2))


        vpn_pesimista = vpn_min
        vpn_base = vpn_mean
        vpn_optimista = vpn_max



        #vpn_mean=

        #RESULTADOS

        VPN1=ctrl3_td1
        VPN2=ctrl3_td2
        VPN3=ctrl3_td3

        dumext = zeros([filas_totales])
        dumpriv = zeros([filas_totales]) #NUEVO
		
        for i in range (a.shape[0]):
            if (cb_externalidad[i] == "1"):
                dumext[i] = 1
                dumpriv[i] = 0 #NUEVO
            else:
                dumext[i] = 0
                dumpriv[i] = 1 #NUEVO


        ctrl3_soc = np.mean(np.dot(sum(np.transpose(ctrl3*desc_v2)*(dumext)), pq_rand))

        VPN_soc = ctrl3_soc
        VPN_soc_sig = np.std(np.dot(sum(np.transpose(ctrl3*desc_v2)*(dumext)),pq_rand)) #NUEVO
        VPN_soc_err= 1.96 * (VPN_soc_sig/(rondas**.5)) #NUEVO
        VPN_priv= VPN2-VPN_soc

        VPN_priv_sig = np.std(np.dot(sum(np.transpose(ctrl3*desc_v2)*(dumpriv)),pq_rand)) #NUEVO
        VPN_priv_err = 1.96 * (VPN_priv/(rondas**.5)) #NUEVO
        VPN_priv_perc= 1-VPN_soc/VPN2
        VPN_sig1= np.std(np.dot(sum(np.transpose(ctrl3*desc_v1)),pq_rand))
        VPN_sig2= np.std(np.dot(sum(np.transpose(ctrl3*desc_v2)),pq_rand))
        VPN_sig3= np.std(np.dot(sum(np.transpose(ctrl3*desc_v3)),pq_rand))

        VPN_err1 = 1.96 * (VPN_sig1/(rondas**.5))
        VPN_err2 = 1.96 * (VPN_sig2/(rondas**.5))
        VPN_err3 = 1.96 * (VPN_sig3/(rondas**.5))

        vpn_privado = VPN_priv_perc * 100
        vpn_externalidades = VPN_soc



        ctrl3_cost=sum(np.transpose(ctrl3) * np.apply_along_axis(np.mean,1,pq_rand) * np.transpose(desc_v2)) * (sum(np.transpose(ctrl3) * np.apply_along_axis(np.mean,1,pq_rand) * np.transpose(desc_v2))<0)
        costos = sum(ctrl3_cost)
        costos_sd =np.std(sum(np.dot(np.transpose(ctrl3) * np.transpose(desc_v2)*(sum(np.transpose(ctrl3)*np.apply_along_axis(np.mean,1,pq_rand) * np.transpose(desc_v2))<0),pq_rand)))


        costos_err = 1.96*costos_sd/(rondas**.5)


        #Beneficios

        ctrl3_ben=sum(np.transpose(ctrl3)*np.apply_along_axis(np.mean, 1, pq_rand)*np.transpose(desc_v2))*(sum(np.transpose(ctrl3)*np.apply_along_axis(np.mean,1,pq_rand)*np.transpose(desc_v2))>=0)

        benef = sum(ctrl3_ben)

        benef_sd = np.std(sum(np.dot(np.transpose(ctrl3)*np.transpose(desc_v2)*(sum(np.transpose(ctrl3)*np.apply_along_axis(np.mean, 1, pq_rand)*np.transpose(desc_v2))>=0),pq_rand)))

        benef_err=1.96*benef_sd/(rondas**.5)



        beneficios = benef




        icb = -VPN2/costos

        icb_sd=np.std(sum(np.dot(np.transpose(ctrl3*desc_v2),pq_rand))/(costos))
        icb_err = 1.96* icb_sd/(rondas**.5)



        for row in range(filas_totales):
            if(cb_prop[row] == "1"):
                cb_prop[row] = 1
            else:
                cb_prop[row] = 0

        qice=cb_prop
        qice1=np.arange(0,filas_totales)
        qice2=sum(qice*qice1)



        ice=np.mean(sum((np.dot(np.transpose(ctrl2f*desc_v2),pq_rand)))/sum(desc_v2[1,:])/(sum(
            (np.dot(np.transpose(np.matrix(ctrl2f[qice2,:])),np.matrix(q_rand[qice2,:]))))/ttt))

        ice_sd=np.std(sum((np.dot(np.transpose(ctrl2f*desc_v2),pq_rand))/sum(desc_v2[1,:])/(sum(np.dot(np.transpose(np.matrix(ctrl2f[qice2,])),np.matrix(q_rand[qice2,:])))/ttt)))
        ice_err=1.96*ice_sd/(rondas**.5)

        qqice=np.mean(sum(np.dot(np.transpose(np.matrix(ctrl2f[qice2,:])),np.matrix(q_rand[qice2,:]))))
        qqice_sd=np.std(sum(np.dot(np.transpose(np.matrix(ctrl2f[qice2,:])),np.matrix(q_rand[qice2,:]))))
        qqice_err=1.96*qqice_sd/(rondas**.5)

        if(ice < 0.00001 ):
            ice = 0
        if(ice_sd < 0.00001):
            ice_sd = 0
        if(ice_err < 0.000001):
            ice_err = 0


        cantidad_ice = qqice

        tir = 0.0
        casos_positivos = 0.0
        app = 0.0
        random_sel = 0.0

        tir_mat3=zeros([1,rondas])
        tir_mat3[:,:]= range(0,rondas)

        f_td=[]

        for i in range (a.shape[0]):
            np.matrix.put(ctrl1_a[i,:], [range(0,len(ctrl1_a[0]))],range(1,len(ctrl1_a[0])+1))

        tir_chain= []
        if (sitirb == "1"):
            tir_mat3[:,:]=1
            for x in range (0,rondas):
                def tir1(td):
                    #return (-1000/(1+td)+1200/(1+td)**2)
                    return(sum(np.dot(np.transpose(ctrl3*(1/(1+td/12)**(ctrl1_a))),pq_rand[:,x])))
                #tir_chain.extend(scipy.optimize.fsolve(tir1,0,xtol=0.2,factor=2))
                tir_chain.append(scipy.optimize.bisect(tir1,-200,200))
            #td0 = scipy.optimize.fsolve(tir1,0)
            tir_chain=sorted(tir_chain)
            tir_chain=tir_chain

            tir_1=tir_chain[int(len(tir_chain)/4)]
            tir_2=tir_chain[int(len(tir_chain)/4)*2]
            tir_3=tir_chain[int(len(tir_chain)/4)*3]
            #if(tir_1>10000):
            #    tir_1 = "(10000+)"
            #    tir_2 = "(10000+)"
            #    tir_3 = "(10000+)"


            #tir_mat3=np.apply_along_axis(tir1,len(np.matrix(tir_mat3)), tir_mat3)
            #tir_mat3=np.put(tir_mat3, abs(tir_mat3)>10, NA)
        else:
            tir_1=0
            tir_2=0
            tir_3=0

            tir_mat3[:,:]=0

        factor1=desc_v1[1,:]
        factor2=desc_v2[1,:]
        factor3=desc_v3[1,:]
        factor1=sum(factor1)
        factor2=sum(factor2)
        factor3=sum(factor3)
        fae1=(VPN1/factor1)*12
        fae2=(VPN2/factor2)*12
        fae3=(VPN3/factor3)*12
		
        fae1_sd = (VPN_sig1/factor1)*12 #NUEVO
        fae2_sd = (VPN_sig2/factor1)*12 #NUEVO
        fae3_sd = (VPN_sig3/factor1)*12 #NUEVO
		
        fae1_err = 1.96*fae1_sd/(rondas**.5) #NUEVO
        fae2_err = 1.96*fae2_sd/(rondas**.5) #NUEVO
        fae3_err = 1.96*fae3_sd/(rondas**.5) #NUEVO

        # 8.1.7 Plazo de recuperaciÃ³n


        plazo1=np.cumsum(sum(ctrl3))

        ctrl3_p=ctrl2f

        fctrl3_p1=np.arange(0,rondas)

        for t in range(0,rondas):
            fctrl3_p1[t]=np.amax(cb_mes_final)-np.amax(np.cumsum(np.cumsum(sum(np.transpose(np.transpose(ctrl3_p)*pq_rand[:,t])))>0))+1
            if(np.amax(np.cumsum(np.cumsum(sum(np.transpose(np.transpose(ctrl3_p)*pq_rand[:,t])))>0))==0):
                fctrl3_p1[t]=-1

        ctrl3_p1= fctrl3_p1>=0
        pctrl3_p1 =[]

        for i in range(len(ctrl3_p1)):
            if(ctrl3_p1[i]):
                pctrl3_p1.append(fctrl3_p1[i])

        plazo=np.mean(pctrl3_p1)
        plazo_sd=np.std(pctrl3_p1)
        plazo_err=1.96*plazo_sd/(len(pctrl3_p1))**.5


        # 8.1.8 Flujo anual
        pq=colnames

        flujo_neut=np.transpose(ctrl2f*desc_v2)*pq[:,2]*pq[:,5]

        flujo_neutral_R= []
        flujo_mean_R=[]
        facum_R =[]
        fna_d_R =[]


        #dif_init=min(cb_mes_inicio)

        primer_dic=rango_fechas(fecha_global_R, datetime.date(int(año_split),12,31), 1)+1


        #HAY QUE COMPROBAR QUE EL PRIMER DICIEMBRE (DE UN AÑO INCOMPLETO) SEA DE UN AÑO DISTINTO AL DEL CSV


        if(primer_dic != 12):
            for x in np.arange(primer_dic,(math.floor(ttt/12)*12),12):
                fna = flujo_neut[x:(x+12),:]
                flujo_neutral_R.append(sum(sum(fna)))

            fe_init=zeros([flujo_neut.shape[1], primer_dic])


            for x in np.arange(0,flujo_neut.shape[1]):
                for y in np.arange(0,primer_dic):
                    fe_init[x][y] =flujo_neut[y][x]

            fe_init=[(sum(sum(fe_init)))]

            fe_init.extend(flujo_neutral_R)
            flujo_neutral_R=fe_init
        else:
            primer_dic = 0
        if (((math.floor(ttt/12)*12))!=ttt):
            try:
                fe_last=sum(sum(np.transpose(ctrl2f[:,((math.floor(ttt/12)*12+1)):ttt]*desc_v2[:,((math.floor(ttt/12)*12+1)):ttt])*pq[:,2]*pq[:,5]))
                flujo_neutral_R.append(fe_last)
            except:
                fe_last=sum(np.transpose(ctrl2f[:,((math.floor(ttt/12)*12+1)):ttt]*desc_v2[:,((math.floor(ttt/12)*12+1)):ttt])*pq[:,2]*pq[:,5])
                flujo_neutral_R.append(fe_last)

        flujo_mean=np.transpose(ctrl2f*desc_v2)*(sum(np.transpose(pq_rand)/rondas))

        for x in np.arange(primer_dic,(math.floor(ttt/12)*12),12):
            fna_mean=flujo_mean[x:(x+12),:]
            flujo_mean_R.append(sum(sum(fna_mean)))

        fe_init_mean=zeros([flujo_mean.shape[1], primer_dic])

        for x in np.arange(0,flujo_mean.shape[1]):
            for y in np.arange(0,primer_dic):
                fe_init_mean[x][y] =flujo_mean[y][x]

        fe_init_mean=[(sum(sum(fe_init_mean)))]


        if(primer_dic != 0):
            fe_init_mean.extend(flujo_mean_R)
        else:
            fe_init_mean = flujo_mean_R

        flujo_mean_R=fe_init_mean


        if (((math.floor(ttt/12)*12))!=ttt):
            try:
                fe_last_mean=sum(sum(np.transpose(ctrl2f[:,((math.floor(ttt/12)*12+1)):ttt]*desc_v2[:,((math.floor(ttt/12)*12+1)):ttt])*pq_rand.sum(axis=1)/rondas))
                flujo_mean_R.append(fe_last_mean)
            except:
                fe_last_mean=sum(np.transpose(ctrl2f[:,((math.floor(ttt/12)*12+1)):ttt]*desc_v2[:,((math.floor(ttt/12)*12+1)):ttt])*pq_rand.sum(axis=1)/rondas)
                flujo_mean_R.append(fe_last_mean)


        facum=np.cumsum(flujo_mean_R)

        """
        for x in np.arange(len(flujo_mean_R)):
            if not facum_R:
                facum_R.append(flujo_neutral_R[0])
            else:
                facum_R.extend(facum_R[x-1] + np.cumsum(fna_mean))
        """
        fna_resized = zeros([filas_totales,len(facum)])

        for x in np.arange(primer_dic,(math.floor(ttt/12)*12),12):
            fna_d=np.transpose(flujo_mean)[:,x:(x+12)]
            try:
                fna_d_R.extend(fna_d.sum(axis=1))
            except:
                fna_d_R.extend(fna_d)

        ano_incompleto =[]
        ano_cerrado = True


        for ano in np.arange(0,filas_totales):
            verificador = sum(ctrl2[ano])%12
            if(verificador > 1 and verificador != 0):
                ano_incompleto.append(True)
            else:
                ano_incompleto.append(False)


        if (((math.floor(ttt/12)*12))!=ttt):
            ano_cerrado = False
            try:
                fe_last_d=sum(np.transpose(ctrl2f[:,
                ((math.floor(ttt/12)*12+1)):ttt]*desc_v2[:,((math.floor(ttt/12)*12+1)):ttt])*pq[:,2]*pq[:,5])
                fna_d_R.extend(fe_last_d)

            except:
                fe_last_d=(np.transpose(ctrl2f[:,
                ((math.floor(ttt/12)*12+1)):ttt]*desc_v2[:,((math.floor(ttt/12)*12+1)):ttt])*pq[:,2]*pq[:,5])
                fna_d_R.extend(fe_last_d)





        fna_d2=zeros([filas_totales,len(facum)])
        #fna_d2[:,:]=fna_d_R
        """
        for x in np.arange(0,filas_totales):
            for y in np.arange(0, len(facum)):
                if((y*filas_totales)<len(fna_d_R)):
                    fna_d2[x][y]=fna_d_R[x+y*filas_totales]
        """
        # 8.2 Salida de resultados
        td1=tasa_des_min
        td2=tasa_des_base
        td3=tasa_des_max

        t_desc=[]
        t_desc.extend((td1,td2,td3))
        ymin=[]
        ymin.extend((VPN1-1.64*VPN_sig1,VPN2-1.64*VPN_sig2,VPN3-1.64*VPN_sig3))
        ymean=[]
        ymean.extend((VPN1,VPN2,VPN3))
        ymax=[]
        ymax.extend((VPN1+1.64*VPN_sig1,VPN2+1.64*VPN_sig2,VPN3+1.64*VPN_sig3))
        ypes=[]
        ypes.extend((-1,vpn_min,-1))
        yneut=[]
        yneut.extend((-1,vpn_mean,-1))
        yopt=[]
        yopt.extend((-1,vpn_max,-1))

        x_anio=np.arange(0,len(facum))

        pdf_array_x = [vpn_social_1]
        pdf_array_z = []
        pdf_array_dens = []

        grafica_campana = "VPNS"
        if(vpn_social_1_std==0):
            grafica_campana = "Dado que no hay variación en los parámetros, esta gráfica no aplica"
            vpn_social_1_std = 1
        
        for n in np.arange(0,14):
            pdf_array_x.insert(0,pdf_array_x[0]-vpn_social_1_std/5);
            pdf_array_x.append(pdf_array_x[len(pdf_array_x)-1]+vpn_social_1_std/5);
        for n in np.arange(0,len(pdf_array_x)):
            pdf_array_z.append((pdf_array_x[n]-vpn_social_1)/vpn_social_1_std);
            pdf_array_dens.append(norm.pdf(pdf_array_z[n]))
            print(pdf_array_dens[n])


        proyecto=""
        TipoProyecto=0
        if (VPN_priv>=0 and vpn_externalidades>=0 and VPN2>0):
            proyecto="APP"
            TipoProyecto=1

        if (VPN_priv>=0 and vpn_externalidades<0 and VPN2>0):
            proyecto="RegulaciÃ³n/Impuesto"
            TipoProyecto=2

        if (VPN_priv<0 and vpn_externalidades>=0 and VPN2>0):
            proyecto="Bien pÃºblico/Subsidio"
            TipoProyecto=3

        if (VPN2<0):
            proyecto="Inacción"
            TipoProyecto=4

        casos_positivos = (1-scipy.stats.norm.cdf(-VPN2/VPN_sig2))*100
        for i in np.arange(0,len(fna_d_R)):
            fna_d_R[i] = "{0:.2f}".format(fna_d_R[i])

        ui_unidad_medida = ""

        for i in np.arange(0,len(cb_unidad_medida)):
            if(cb_prop[i]==1):
                ui_unidad_medida = cb_unidad_medida[i]

        vpn_pesimista_R =((1-norm.cdf((vpn_min-VPN2)/VPN_sig2))*100)
        vpn_base_R=((1-norm.cdf((vpn_base-VPN2)/VPN_sig2))*100)
        vpn_optimista_R=((1-norm.cdf((vpn_max-VPN2)/VPN_sig2))*100)

        print("tir chain")
        print(tir_chain)
        print("tir ")
        print(tir_1)
        print(tir_2)
        print(tir_3)
        print(vpn_social_1)

        #columnas_totales = shape[1] osea 22 creo en cb.csv
        #filas_totales = shape[0] osea 4 en el ejemplo de cb.csv
        #print (random.gauss(0,1))
        #print (random.weibullvariate(0,1))
        return HttpResponse(json.dumps(
            {
             'filas_totales': str(filas_totales),
             'vpn_social_1': str(vpn_social_1),
             'vpn_social_1_std': str(vpn_social_1_std),
             'vpn_social_1_err': str("{0:.2f}".format(VPN_err1)),
             'vpn_social_2' : str(vpn_social_2),
             'vpn_social_2_std' : str(vpn_social_2_std),
             'vpn_social_2_err' : str("{0:.2f}".format(VPN_err2)),
             'vpn_social_3' : str(vpn_social_3),
             'vpn_social_3_std' : str(vpn_social_3_std),
             'vpn_social_3_err' : str("{0:.2f}".format(VPN_err3)),
             'vpn_externalidades' : str(vpn_externalidades),
             'vpn_privado' : str("{0:.1f}".format(VPN_priv)),
             'costos' : str(costos),
             'costos_err' : str(costos_err),
             'costos_sd' : str(costos_sd),
             'beneficios' : str(beneficios),
             'beneficios_err' : str(benef_err),
             'beneficios_sd' : str(benef_sd),
             'icb' : str(icb),
             'icb_sd' : str(icb_sd),
             'icb_err' : str(icb_err),
             'fae_1' : str(fae1),
             'fae_2' : str(fae2),
             'fae_3' : str(fae3),
             'plazo' : str("{0:.2f}".format(plazo/12)),
             'plazo_err' : str("{0:.2f}".format(plazo_err)),
             'plazo_sd' : str("{0:.2f}".format(plazo_sd)),
             'ice' : str(ice),
             'ice_err' : str(ice_err),
             'ice_sd' : str(ice_sd),
             'unidad_medida' : str(ui_unidad_medida),
             'cantidad_ice' : str(qqice),
             'cantidad_ice_err' : str(qqice_err),
             'cantidad_ice_sd' : str(qqice_sd),
             'vpn_pesimista' : str(vpn_pesimista),
             'vpn_pesimista_R' : str("{0:.1f}".format(vpn_pesimista_R)),
             'vpn_base' : str(vpn_base),
             'vpn_base_R' : str("{0:.1f}".format(vpn_base_R)),
             'vpn_optimista' : str(vpn_optimista),
             'vpn_optimista_R' : str("{0:.1f}".format(vpn_optimista_R)),
             'tir' : str("{0:.3f}".format(tir_1)),
             'tir_2' : str("{0:.3f}".format(tir_2)),
             'tir_3' : str("{0:.3f}".format(tir_3)),
             'casos_positivos' : str("{0:.2f}".format(casos_positivos)),
             'app' : TipoProyecto,
             't_desc' : t_desc,
             'ymin' : ymin,
             'ymean' : ymean,
             'ymax' : ymax,
             'ypes' : ypes,
             'yneut' : yneut,
             'yopt' : yopt,
             'x_anio' : x_anio.tolist(),
             'flujo_neutral' : flujo_neutral_R,
             'flujo_mean' : flujo_mean_R,
             'fna_d_R' : fna_d_R,
#             'fna_d' : fna_d_R.tolist(),
             'facum' : facum.tolist(),
             'flujo_efectivo' : filas_totales,
             'detalles' : cb_detalle,
             'total_anos' : len(facum),
             'fna_resized' : fna_resized.tolist(),
             'ano_incompleto' : ano_incompleto,
             'cb_mes_final' : max(cb_mes_final),
             'cb_prop' : cb_prop,
             'cb_tipo' : cb_tipo,
             'cb_frecuencias' : cb_frecuencias,
             'cb_impacto' : cb_impacto,
             'cb_unidad_medida' : cb_unidad_medida,
             'cb_detalle' : cb_detalle,
             'cb_p' : cb_p,
             'cb_p_pes' : cb_p_pes,
             'cb_p_opt' : cb_p_opt,
             'cb_categoria' : cb_categoria,
             'cb_modelo' : cb_modelo,
             'cb_cantidad' : cb_cantidad,
             'cb_cantidad_pes' : cb_cantidad_pes,
             'cb_cantidad_opt' : cb_cantidad_opt,
             'cb_fecha_inicio' : cb_fecha_inicio,
             'cb_fecha_final' : cb_fecha_final,
             'cb_externalidad' : cb_externalidad,
             'cb_fuentes' : cb_fuentes,
             'campana' : grafica_campana,
             'cb_coef1' : cb_coef1,
             'cb_coef2' : cb_coef2,
             'cb_coef3' : cb_coef3,
             'pdf_array_x': pdf_array_x,   
             'pdf_array_z': pdf_array_z,  
             'pdf_array_dens': pdf_array_dens,
             'ano_cerrado' : ano_cerrado,
             'random_sel' : str(random_sel),
             'dumpriv'  :    dumpriv.tolist(),
             'VPN_soc' : VPN_soc,
             'VPN_soc_sig' : VPN_soc_sig,
             'VPN_soc_err' : VPN_soc_err,
             'VPN_priv_sig' :VPN_priv_sig,
             'VPN_priv_err' :VPN_priv_err,
             'fae1_sd' : fae1_sd,
             'fae2_sd' : fae2_sd,
             'fae3_sd' : fae3_sd,
             'fae1_err': fae1_err,
             'fae2_err': fae2_err,
             'fae3_err': fae3_err  
            }), content_type="application/json")

    else:
        return redirect("cb_v4/")
