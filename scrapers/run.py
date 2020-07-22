from datos_computrabajo import computrabajo
from datos_zonajobs import zonajobs
from datos_linkedin import linkedin
from datos_adlatina import adlatina
import sys
#if sys.argv[1]:
zona=0
try:
    if zona==1:
       pass
    else:
       computrabajo()
    #pass
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


try:
    job=adlatina()
    if job==0:
        pass
    else:
        job=adlatina()
            
except Exception as ex:
    print(ex)
    
print("TERMINA")
