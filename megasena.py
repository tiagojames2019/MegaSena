from requests import get
import json
from pandas import DataFrame as pd
import urllib3
from random import choices
urllib3.disable_warnings()
from pprint import pprint
import time
from tqdm import tqdm

lmega = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/'
headers =  {"Content-Type":"application/json"}
resmega = get(lmega, headers, verify=False)
resmega = resmega.json()
conc_final = int(resmega['numeroConcursoProximo'])

print("Proximo concurso  = ", conc_final)

print(100*' '  )
'''
Variaveis 
'''
sorteados=[]
concurso =[]
index=[]
base = []
repetidos = []
palpites = []

qtdAnalise = int(input('Informe a quantidade de Concurso a Analisar: '))
qtdPalpite = int(input('Informe a quantidade de Palpites a Gerar: '))

print(100*' '  )

print("Analisando Concurso")

for i in tqdm(range(conc_final-qtdAnalise, conc_final)):
    
    time.sleep(1)

    link = f'https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/{i}'
    headers =  {"Content-Type":"application/json"}
    res = get(link, headers, verify=False)
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

base = sorted(base)

print(100*' '  )

print("Gerando Palpite")

for x in tqdm(range(qtdPalpite)):
    time.sleep(0.5)
    a = choices(base, k=1)
    palpite = []
    contador = 0
    if a not in palpite:
        palpite.append(a)
        while (len(palpite) < 6):
            a = choices(base, k=1)
            if a not in palpite:
                palpite.append(a)
            contador +=1
    palpites.append(sorted(palpite))

df = {
        'Concurso':concurso,
        'Numeros Sorteados':sorteados,
    }   

df = pd(df,index=index)

print(100*' '  )

print(10*'*','TOTAL DE NUMERO A SER ANALISADOS',10*'*'  )
print(len(base))

print(100*' '  )

print(10*'*','BASE UTILIZADA',10*'*'  )

print(base)

print(100*' '  )

print(10*'*','CONCURSO ANALISADOS',10*'*'  )
print(df)

print(100*' '  )

print(10*'*','PALPITES GERADOS ',10*'*'  )

print(100*' '  )

for y in palpites:
    print(y)