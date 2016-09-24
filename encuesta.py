#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encuesta.py: Utilería para procesar datos de encuestas en formato CSV
# Alberto Pacheco © 2016 (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/

import csv
import traceback

class Resultados:
    'Clase auxiliar para empaquetar resultados de Encuesta.frec()'

    def __init__(self):
        self.indice = None
        self.nulos = 0
        self.tot = 0.0
        self.frec = {}

    def update(self, d):
        if not d or len(d)==0:
            self.nulos += 1
            return
        d2 = d.strip()
        if d2 in self.frec:
            self.frec[d2] += 1
        else:
            self.frec[d2] = 1


class Edades(Resultados):
    'Subclase para campo de edades'

    def update(self, d):
        if not d:
            self.nulos += 1
            return
        yr = d.strip()
        tam = len(yr)
        try:
            if tam==0:
                return
            elif tam==4 and int(yr)>0:
                self.change(yr)
            else:
                yr = "19"+yr[-2:]
                self.change(yr)
        except ValueError as e:
            return

    def change(self, d):
        self.tot += 1
        v = int(d)
        if v <= 1968:
            d = '1968 o anterior'
        elif v<= 1990:
            d = '1969-1990'
        elif v<= 1995:
            d = '1991-1995'
        elif v>= 1998:
            d = '1998 o posterior'
        if d in self.frec:
            self.frec[d] += 1
        else:
            self.frec[d] = 1


class Comentarios(Resultados):
    'Subclase para comentarios'
    Fav = [ # class property
        "buen curso",
        "excelente",
        "muy bien",
        "bueno",
        "gracias",
        "felicit" ,
        "me ayud",
        "me gusto",
        "bien explicado",
        "aprendi",
        "sirvio",
        "agrado",
        "estuvo bien",
        "agradable",
        "diverti",
        "encanto",
        "interesante"
    ]
    Neg = [ # class property
        "muy malo",
        "mala",
        "pesim",
        "fallas",
        "le falt",
        "faltaron",
        "errores",
        "pesado",
        "no me gust",
        "pongan mas",
        "agreguen mas",
        "mejoren",
        "correcci",
        "deben mejorar",
        "pueden mejorar",
        "corregir",
        "correcci",
        "aburrido",
        "dificil",
        "dificultad",
        "complicado",
        "confuso",
        "tedioso"
    ]

    def update(self, d):
        if len(self.frec) == 0: # lazy init
            self.frec['Positivo'] = 0
            self.frec['Negativo'] = 0
        if not d:
            self.nulos += 1
            return
        d2 = d.strip()
        try:
            if len(d2)==0:
                self.nulos += 1
                return
            for busq in Comentarios.Fav:
                if d2.find(busq) >= 0:
                    # print self.frec['Positivo'],"POS:",d2
                    self.frec['Positivo'] += 1
                    break
            for busq in Comentarios.Neg:
                if d2.find(busq) >= 0:
                    # print self.frec['Negativo'],"NEG:",d2
                    self.frec['Negativo'] += 1
                    break
        except ValueError as e:
            return


class Encuesta:
    'Obtiene frecuencias por tipo de respuesta de encuesta en formato CSV'

    def __init__(self, nomArch):
        self.dataset    = None
        self.columnas   = None
        self.mapCol     = None
        self.fileHandle = None
        try:
            self.fileHandle = open(nomArch,mode='rU')
            self.dataset = csv.reader(self.fileHandle)
            self.columnas = self.dataset.next() # Encabezado: nombres de columnas
            self.mapCol = dict(zip(self.columnas, range(0,len(self.columnas)))) # dicc aux
        except csv.Error as e:
            print "Error: %s\nNo fue posible leer archivo %s" % (e,nomArch)

    def __getitem__(self, tupla): # Indexación simbólica fila[col]
        fila, nomCol = tupla  # Indices dentro de tupla
        return fila[self.mapCol[nomCol]] # Indexación vía diccionario auxiliar

    def frec(self, nomCol, resultados=None): # Regresa resultados
        self.fileHandle.seek(0) # Reinicia iterador
        self.dataset.next()     # Ignora primer fila (encabezado)
        if not resultados:      # valor default?
            resultados = Resultados() # lazy init
        resultados.indice = self.mapCol[nomCol] # Indice numérico
        if not self.dataset: # Archivo vacío?
            print "Error: no hay datos"
            return resultados
        conta = 0 # Contador
        try:
            for fila in self.dataset: # Para cada fila...
                lstResp = self[fila,nomCol].lower().split(';') # Indexa fila[columna]
                conta += 1 # Actualiza contador
                for resp in lstResp: # Para cada respuesta...
                    resultados.update(resp) # Actualiza frecuencias
            resultados.tot = float(conta) # Filas procesadas
        except (KeyError, Exception) as e:
            traceback.print_exc()
            print "Error: %s\nLlave invalida pos=%s" % (str(e), i)
        return resultados # Regresa objeto con resultados


# Utilería para ordenar descendentemente un diccionario en base a los valores del mismo
def ordenar(s):
    return sorted(s.iteritems(), key=lambda (k,v): (v,k), reverse=True)
