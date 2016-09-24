#!/usr/bin/env python
# -*- coding: utf-8 -*-
# reduce.py: Cambia encabezado y elimina columnas innecesarias. Genera archivo de salida
# Alberto Pacheco © 2016 (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/

import csv

class FileCSV: # Lectores y Escritores de archivos CSV
    @staticmethod
    def reader(fn):
        return csv.reader(open(fn,mode='rU'))
    @staticmethod
    def writer(fn):
        return csv.writer(open(fn,mode='w'), delimiter=',')


nomEnt = 'EncuestaMOOC.csv'
nomSal = 'encuesta.csv'
fila1  = [     # Encabezado
    'hora',    # remover
    'nombre',  # remover
    'sexo','edad',
    'correo',  # remover
    'tecnm','plantel','semestre',
    'escuela', # remover
    'tipo',
    'ciudad',  # remover
    'estado','nivel','difusion','red','twitter','recurso','internet','mejor',
    'peor','audio','lectura','duracion','videos','plataforma','servidor',
    'cantidad','dificultad','calidad','originalidad','motivacion','utilidad',
    'tiempos','fechas','mejorar','repetir','recomendar','comentario']
excluye = ['hora','nombre','correo','escuela','ciudad'] # columnas a eliminar
elimCol = sorted(map(lambda x: fila1.index(x), excluye), reverse=True) # extrae indices
for i in elimCol: # Para cada indice-columna...
    fila1.pop(i)  #   elimina columna del encabezado
numFila = 0 # contador de filas procesadas
try:
    dataset = FileCSV.reader(nomEnt) # tabla original
    salida  = FileCSV.writer(nomSal) # tabla modificada
    for fila in dataset: # Para cada fila en el archivo
        numFila += 1
        if numFila == 1: # Reemplaza primer fila con nuevo encabezado
            salida.writerow(fila1)
            continue
        for col in elimCol: # Elimina campos no deseados
            fila.pop(col) # en orden descendente (derecha a izquierda)
        salida.writerow(fila) # Graba fila modificada
except csv.Error as e:
    print "Error: %s\nNo fue posible leer archivo %s" % (e, nomEnt)
print "Archivo generado: %s\n(%d columnas x %d filas)" % (nomSal, len(fila1), numFila)
