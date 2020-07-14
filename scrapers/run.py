from datos_computrabajo import computrabajo
from datos_zonajobs import zonajobs


try:
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
print("TERMINA")
