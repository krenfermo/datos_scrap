from datos_computrabajo import computrabajo
from datos_zonajobs import zonajobs
from datos_linkedin import linkedin
from datos_adlatina import adlatina
import sys
import datetime



#if sys.argv[1]:
print("INICIA scrapers: "+str(datetime.datetime.now()))
try:
    job=adlatina()
    if job==0:
        pass
    else:
        job=adlatina()

except Exception as ex:
    print(ex)


try:
    job=computrabajo()
    if job==0:
        pass
    else:
        job=computrabajo()

except Exception as ex:
    print(ex)


try:
    job=zonajobs()
    if job==0:
        pass
    else:
        job=zonajobs()
            
except Exception as ex:
    print(ex)


try:
    job=linkedin()
    if job==0:
        pass
    else:
        job=linkedin()
            
except Exception as ex:
    print(ex)

print("TERMINA scrapers: "+str(datetime.datetime.now()))
