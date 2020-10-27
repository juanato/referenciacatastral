#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib3
import base64
import requests
import time 
import re
import pandas as oExcel
from pandas import ExcelWriter
from pandas import ExcelFile
from urllib.request import urlopen
import urllib.request
import math
import os
import csv
import sys
from datetime import datetime


try:
    from PyQt5 import QtCore

except:
    from PyQt4 import QtCore


 
def HuboError(cTexto):
  print(cTexto)
  oFichero.write(str(cTexto)+"\n")
#Método empty() de Xbase
def empty(cCadena):
    lDevuelto = False
    if cCadena and cCadena.strip():
        lDevuelto = True
        
    return lDevuelto
# Sólo valida fincas urbanas

    """
    Sólo se comprueban las referencias catastrales con 20 carácteres alfanuméricos,
	los dos últimos corresponden a los dígitos de control.
    """

def CalculaPesoPosicionCadena(cCadena):

    cCadenasDC = ""
    cDigitoControlCalculado = ""
    nAcumulaValoresPosiciones = ""
    nPesoPosicion = ""
    nPosicion = 0
    aPesoPosicion = [13,15,12,5,4,17,9,21,3,7,1]
    
    
    cElemento = ""
    cDigitoControlCalculado = ''
    nPesoPosicion = 0
    nPosicion = -1
    nAcumulaValoresPosiciones = 0
    HuboError("Calculando pesos de la subcadena "+cCadena)  
    for cElemento in cCadena:
     
            
           
        """"
        Valor por el que se debe multiplicar cada posición de cada subcadena
        1�=13, 2�=15, 3�=12, 4�=5, 5�=4, 6�=17, 7�=9, 8�=21, 9�=3, 10�=7, 11�=1
    
            Para el cálculo de cada dígito de control, se deben de sumar cada
            uno de los carácteres de cada cadena.
            Si el carácter no es numérico el valor corresponde de la siguiente 
            manera: A = 1, B = 2, ..., Z = 27. Un salto de 64 posiciones ASCII

            A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8, I=9, J=10, K=11, L=12, M=13, N=14, �=15, O=16, P=17, Q=18, R=19, S=20, T=21, U=22, V=23, W=24, X=25, Y=26 y Z=27
        """
        cValorPosicion =  cElemento
        nPosicion      =  nPosicion +1
        nPesoPosicion  =  0

        HuboError( "Cadena  "+ cCadena + " en Posicion Actual "+  str(nPosicion)  + " tiene como Elemento cadena " + cValorPosicion  )

                 
        if cValorPosicion >= 'A' and cValorPosicion <='N':
            nPesoPosicion = ord( cValorPosicion ) - 64
            HuboError(txtcolores.BOLD+ "Detectado como ALFABETICO A-N"  )   
        if  cValorPosicion =='Ñ':
            nPesoPosicion = 15           
            HuboError(txtcolores.BOLD+ "Detectado como caso especial Ñ")
               
        if  cValorPosicion  > 'N':
            nPesoPosicion =  ord( cValorPosicion ) - 63
            HuboError(txtcolores.BOLD+ "Detectado como ALFABETICO posterior a N")
        if cValorPosicion.isnumeric():
            nPesoPosicion = int( cValorPosicion ) 
            HuboError(txtcolores.BOLD+ "Detectado como NUMÉRICO")
        #nPesoPosicion = nPesoPosicion - 1  # Es python, indice inferior es 0
           
        HuboError( " Elemento cadena " + cValorPosicion  )
        HuboError( " POSICION EN UNICODE-> "  +  str( nPesoPosicion ) )
        HuboError( " PESO POSICION     -> "  +  str( aPesoPosicion[ nPosicion ])  )
        HuboError( " PRODUCTO POSICION*PESO  -> "  +  str(nPesoPosicion * aPesoPosicion[ nPosicion ])  )
        nAcumulaValoresPosiciones = nAcumulaValoresPosiciones + ( nPesoPosicion * aPesoPosicion[ nPosicion ] ) 
         ##Valor del dígito de control calculado
         ##cLetraDc.

    HuboError( "ACUMULADOR PRODUCTOS DE PESOS/POSICION  DE LA CADENA " + str(nAcumulaValoresPosiciones)  )
    return (nAcumulaValoresPosiciones % 23)

def ValidaRefCatUrb(cRefCat):


    nError = 0
    nValor1DC = 0
    nValor2DC = 0
    cGrupoDC = ""
    cLetraDc = 'MQWERTYUIOPASDFGHJKLBZX'
    cRefCat = cRefCat.strip()
    if len(cRefCat)!=20 and empty(cRefCat):
      #if empty(cRefCat):
      HuboError(txtcolores.FAIL+"Referencia Catastral sin longitud adecuada para validar.")
      nError = 1 
    else:
      cRefCat = str(cRefCat.upper())
      HuboError(txtcolores.OKCYAN+"Validando la RC "+cRefCat)
      ##Para calcular los dos dígito de control se utilizan dos subcadenas
      # Ojo que Python requiere la posición a la derecha como no incluida.
      HuboError( "TRAMO 15-18 Primera subcadena es " +  cRefCat[14:18] + " longitud "+str(len(cRefCat[14:18]))  )
      cCadenaPrimerDC  =  cRefCat[0:7] + cRefCat[14:18]
      HuboError( "Primera subcadena " +  cCadenaPrimerDC   )
      cCadenaSegundoDC =  cRefCat[7:14] + cRefCat[14:18]
      HuboError( "Tramo 7 caractéres Segunda subcadena es " +  cRefCat[7:14]+ " longitud " + str(len(cRefCat[7:14]))  )
      HuboError( "Segunda subcadena " +  cCadenaSegundoDC   )
      nValor1DC =  CalculaPesoPosicionCadena( cCadenaPrimerDC )
      HuboError( "Valor ASCII Elemento1 DC " +  str(nValor1DC)  )
      nValor2DC =  CalculaPesoPosicionCadena( cCadenaSegundoDC )
      HuboError( "Valor ASCII Elemento2 DC " +  str(nValor2DC)  )
      cGrupoDC = cLetraDc[ nValor1DC:nValor1DC+1 ] + cLetraDc[nValor2DC:nValor2DC+1]
      HuboError( "Producto subcadena1 " + str(nValor1DC) + " Producto subcadena2 " + str(nValor2DC) + " grupo DC resultante es " + cGrupoDC  )
      if cGrupoDC != cRefCat[18:20]:
         HuboError(txtcolores.WARNING+"Referencia Catastral con error: dígitos de control inválidos")
         HuboError(txtcolores.BOLD+"Se ha calculado que debe ser "+ cGrupoDC + " pero se ha facilitado una RC con " + cRefCat[18:20] )
         nError = 2
      else:
         nError = 0
         HuboError(txtcolores.OKBLUE+txtcolores.UNDERLINE+"Se ha calculado que debe ser "+ cGrupoDC + " y la RC tiene " + cRefCat[18:20] )
         HuboError("Es correcta la Referencia Catrastal")    

class txtcolores:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    os.system('clear')    
    oFichero = open("errores-refcat-urbana.txt", "a")
    dComienzo = time.time()
    HuboError(dComienzo)
    HuboError(txtcolores.OKGREEN+"Iniciando VALIDADOR REFERENCIA CATASTRAL URBANA ESPAÑA INSULAR-PENINSULAR versión 1.04")
    #cCadenaPrimerDC, cCadenaSegundoDC 
    ValidaRefCatUrb("2339507DG6023N0009FO")
    #"2339507DG6023N0009FO"
    #ValidaRefCatUrb("8407007UH6080N0001PH")
    #str("8407007UH6080N0001PH")
    #"2339507DG6023N0009FO"
    #cRefCast = input("Referencia CATASTRAL URBANA: ")
    
    nSegundos = time.time() - dComienzo
    HuboError("--- %s segundos ---" % ( nSegundos) )  
    HuboError("--- %s minutos ---" % ( nSegundos/60) ) 
    HuboError(txtcolores.OKGREEN+"=Finalizado ejecución VALIDADOR CATASTRAL v1.04 ===========")
    oFichero.close()
except ValueError:
        HuboError(txtcolores.OKWARNING+"Excepción de ejecución "+str(value))
finally:
        print("Se ha terminado la ejecuión del código. ")