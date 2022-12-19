import requests
import json
import pandas as pd
import urllib3
import pandas as pd
import random
urllib3.disable_warnings()
from pprint import pprint
import time

lmega = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/'
headers =  {"Content-Type":"application/json"}
resmega = requests.get(lmega, headers, verify=False)
resmega = resmega.json()
conc_final = int(resmega['numeroConcursoProximo'])

print("Ultimo concurso  = ", conc_final)
'''
Variaveis 
'''
sorteados=[]
concurso =[]
index=[]
base = []
repetidos = []
palpites = []

qtdAnalise = int(input('Informe a quantidade de Concurso a Analisar'))
qtdPalpite = int(input('Informe a quantidade de Palpites a Gerar'))

for i in range(conc_final-qtdAnalise, conc_final):
    
    time.sleep(1)

    link = f'https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/{i}'
    headers =  {"Content-Type":"application/json"}
    res = requests.get(link, headers, verify=False)
    #, "Authorization": f"Bearer {token}"
    resposta = res.json()
    sorteados.append(sorted(resposta['dezenasSorteadasOrdemSorteio']))
    sorteados_ordenados = sorted(sorteados)
    concurso.append(i)

for x in range(1,len(sorteados)+1):
    index.append(x)

for i in sorteados:
    for x in i:
        if x in base:
            if x  not in repetidos:
                repetidos.append(x)
        else:
            base.append(x)



for x in range(qtdPalpite):
    a = random.choices(base, k=1)
    palpite = []
    contador = 0
    if a not in palpite:
        palpite.append(a)
        while (len(palpite) < 6):
            a = random.choices(base, k=1)
            if a not in palpite:
                palpite.append(a)
            contador +=1
    palpites.append(sorted(palpite))

df = {
        'Concurso':concurso,
        'Numeros Sorteados':sorteados,
    }   

df = pd.DataFrame(df,index=index)

print(10*'*','BASE UTILIZADA',10*'*'  )
print(base)

print(10*'*','CONCURSO ANALISADOS',10*'*'  )
print(df)

print(10*'*','PALPITES GERADOS ',10*'*'  )

for y in palpites:
    print(y)