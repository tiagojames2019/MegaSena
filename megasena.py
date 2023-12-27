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
    
    time.sleep(2)

    link = f'https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/{i}'
    headers =  {"Content-Type":"application/json"}
    res = get(link, headers, verify=False)
    resposta = res.json()
    sorteados.append(sorted(resposta['dezenasSorteadasOrdemSorteio']))
    sorteados_ordenados = sorted(sorteados)
    concurso.append(i)


for x in range(1,len(sorteados)+1):
    index.append(x)

#Verificando numeros Repetidos
for i in sorteados:
    for x in i:
        if x in base:
            if x  not in repetidos:
                repetidos.append(x)
        else:
            base.append(x)


print(100*' '  )

print("Gerando Palpite")

for x in tqdm(range(qtdPalpite)):
    time.sleep(0.01)
    a = str(choices(base, k=1)).strip("'[]'")
    a = int(a)
    palpite = []
    contador = 0
    if a not in palpite:
        palpite.append(a)
        while (len(palpite) < 6):
            a = str(choices(base, k=1)).strip("'[]'")
            a = int(a)
            if a not in palpite:
                palpite.append(a)
            contador +=1
    
    if palpite not in palpites:
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

print(sorted(base))

print(100*' '  )

print(10*'*','CONCURSO ANALISADOS',10*'*'  )
print(df)

print(100*' '  )

print(10*'*','PALPITES GERADOS ',10*'*'  )

print(100*' '  )

for y in palpites:
    print(y)

print(100*' '  )
print("Quantidade de Palpites Gerados :",len(palpites) )

#Valição para verificar se algum palpite já foi Sorteado 

todoConc = 'https://www.portalconfiraloterias.com.br/loteria/ConferirResultadoNovoJson.php?loteria=megasena&jogo=00 00 00 00 00 00&concursoIni=1&concursoFim=5000&premio=0&time=&mes='
headers =  {"Content-Type":"application/json"}
retorno = get(todoConc, headers)
decoded_data = retorno.content.decode('utf-8-sig')
data = json.loads(decoded_data)
df2 = pd(data)

#Adicionando numero sorteado a uma lista para usar em comparações

lista = []
totalsorteado = []

for i in range(len(df2)):
    lista1 = []
    compara = str(df2['numeros'][i]).strip()
    compara = compara.replace(' ',',')

    for x in compara.split(','):
        x= int(x)
        lista1.append(x)
    lista.append(lista1)

for i in range(len(palpites)):

    if palpites[i] in lista:
        print('Palpite já sorteado', palpites[i] )
        totalsorteado.append(palpites[i])
        
print(100*' '  )

print('TOTAL DE PALPITES JÁ SORTEADOS: ',len(totalsorteado))  

#Gerando Arquivos printando de Saidas

with open('resultados.txt', 'w') as arquivo:

    arquivo.write(f"Proximo concurso  = {conc_final}\n\n" )
    arquivo.write('*****  PALPITES GERADOS *****\n')
    
    for linha in palpites:

        arquivo.write(str(linha))
        arquivo.write('\n')
      
arquivo.close()