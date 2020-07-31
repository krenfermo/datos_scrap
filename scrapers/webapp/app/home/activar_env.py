import subprocess

result = subprocess.run(['pwd'], stdout=subprocess.PIPE)
        
path=result.stdout.decode('utf-8').replace("/scrapers","").replace("/webapp\n","")
script=result.stdout.decode('utf-8').replace("/webapp\n","")+"/run.py"
python=path.replace("scrapers/","")
src_bash=python+"/scrapers/webapp/app/home/activar.sh"
python = python +"/env/bin/python3"
#activate=python.replace("python3","activate")

#result2 = subprocess.run([python,script])
#result2 = subprocess.run([python,script])

with open(src_bash,"w") as file:
    file.write("#!/usr/bin/env bash \nsource "+str(python)+"\npython3 "+str(script))

#result2 = subprocess.run(["bash ",src_bash])

import os
myCmd = 'bash ' + src_bash
os.system(myCmd)
