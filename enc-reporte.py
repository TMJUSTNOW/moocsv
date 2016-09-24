#!/usr/bin/env python
# -*- coding: utf-8 -*-
# enc-reporte.py: Generar reporte de encuesta en formato CSV
# Alberto Pacheco © 2016 (CC BY-NC-SA 4.0) https://creativecommons.org/licenses/by-nc-sa/4.0/

from encuesta import *
import timeit

start = timeit.default_timer()
arch_csv = Encuesta('encuesta.csv')

for col in arch_csv.columnas:
    if col == 'edad':
        resultados = Edades()
    elif col == 'comentario':
        resultados = Comentarios()
    else:
        resultados = Resultados()
    arch_csv.frec(col, resultados)
    print '\n>> %d. Columna "%s" <<' % (resultados.indice+1, col)
    if resultados.nulos > 0:
        print "Sin contestar = %d encuestados" % resultados.nulos
    for k, v in ordenar(resultados.frec): # sort by value
        print "\t%s = %d respuestas (%.2f %%)" % (k, v, v/resultados.tot*100.0)
    print "Total = %d" % resultados.tot
print "Tiempo de procesamiento = %.2f segs." % (timeit.default_timer() - start)
