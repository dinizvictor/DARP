
# coding: utf-8

# In[61]:


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import time
from copy import deepcopy

# Gerando Grafo

'''
grafo = nx.Graph()

grafo.add_nodes_from("ABCDEFGHIUV")

grafo.add_weighted_edges_from([('A', 'B', 1), ('B', 'C', 1), ('C', 'D', 1), ('D', 'F', 1), ('E', 'F', 1), ('A', 'I', 1),
                               ('C', 'U', 1), ('U', 'V', 1), ('V', 'E', 1), ('V', 'I', 1), ('I', 'H', 1), ('F', 'H', 1),
                               ('F', 'G', 1), ('H', 'G', 1)])
'''

#grafo = nx.gnm_random_graph(15, 30)

grafo1 = nx.grid_2d_graph(10, 10)
grafo2 = nx.grid_2d_graph(10, 15)
grafo3 = nx.grid_2d_graph(10, 20)
grafo4 = nx.grid_2d_graph(10, 3)
grafo5 = nx.grid_2d_graph(10, 5)
grafo6 = nx.grid_2d_graph(10, 18)

for (u, v) in grafo1.edges:
    grafo1.edges[u,v]['weight'] = random.randint(20,50)

for (u, v) in grafo2.edges:
    grafo2.edges[u,v]['weight'] = random.randint(20,50)

for (u, v) in grafo3.edges:
    grafo3.edges[u,v]['weight'] = random.randint(20,50)

for (u, v) in grafo4.edges:
    grafo4.edges[u,v]['weight'] = random.randint(20,50)
    
for (u, v) in grafo5.edges:
    grafo5.edges[u,v]['weight'] = random.randint(20,50)
    
for (u, v) in grafo6.edges:
    grafo6.edges[u,v]['weight'] = random.randint(20,50)


# In[17]:


#Grafo 1
pos = nx.spring_layout(grafo1)
nx.draw(grafo1, pos, node_size=10, with_labels = False)
plt.show()


# In[18]:


#Grafo 2
pos = nx.spring_layout(grafo2)
nx.draw(grafo2, pos, node_size=10, with_labels = False)
plt.show()


# In[19]:


#Grafo 3
pos = nx.spring_layout(grafo3)
nx.draw(grafo3, pos, node_size=10, with_labels = False)
plt.show()


# In[42]:


def isCicloDominante(grafo, ciclo, k):
    sg = grafo.subgraph(ciclo)
    allEdges = list(grafo.edges)
    dominatingEdges = []
    dominante = True
    
    #Verifica se e um ciclo.
    aux = [] #Variavel de verificação de vertice repetido.
    for i in range(len(ciclo) - 1):
        if ciclo[i] in aux:
            return False
        if not ciclo[i] in grafo.neighbors(ciclo[i+1]):
            return False
        aux.append(ciclo[i])
    if not ciclo[-1] in grafo.neighbors(ciclo[0]):
        return False
    if ciclo[-1] in aux:
        return False

    for sgEdge in sg.edges:
        dominatingEdges.append(sgEdge)

    for sgEdge in sg.edges:
        for edge in allEdges:  # edge[0] = i e edge[1] = j | sgEdge[0] = u e sgEdge[1] = v
            invertido = (edge[1], edge[0])
            if nx.shortest_path_length(grafo, edge[0], sgEdge[0]) and nx.shortest_path_length(grafo, edge[1],
                                                                                              sgEdge[0]) <= k:
                if edge not in dominatingEdges and invertido not in dominatingEdges:
                    dominatingEdges.append(edge)
            elif nx.shortest_path_length(grafo, edge[0], sgEdge[1]) and nx.shortest_path_length(grafo, edge[1],
                                                                                                sgEdge[1]) <= k:
                if edge not in dominatingEdges and invertido not in dominatingEdges:
                    dominatingEdges.append(edge)
            elif nx.shortest_path_length(grafo, edge[0], sgEdge[1]) and nx.shortest_path_length(grafo, edge[1],
                                                                                                sgEdge[0]) <= k:
                if edge not in dominatingEdges and invertido not in dominatingEdges:
                    dominatingEdges.append(edge)
            elif nx.shortest_path_length(grafo, edge[0], sgEdge[0]) and nx.shortest_path_length(grafo, edge[1],
                                                                                                sgEdge[1]) <= k:
                if edge not in dominatingEdges and invertido not in dominatingEdges:
                    dominatingEdges.append(edge)

    for i in allEdges:
        inverso = (i[1], i[0])
        if i not in dominatingEdges and inverso not in dominatingEdges:
            dominante = False

    return dominante


def custoCaminho(grafo, ciclo):
    subgrafo = grafo.subgraph(ciclo)
    custo = sum(grafo[u][v]['weight'] for (u, v) in subgrafo.edges)
    return custo

def melhorSolucaoPopulacao(grafo, populacao):
    melhorSolucao = populacao[0]
    for i in range(1, len(populacao)):
        if custoCaminho(grafo, populacao[i]) < custoCaminho(grafo, melhorSolucao):
            melhorSolucao = populacao[i]
    
    return melhorSolucao
    

def geraPopulacaoInicial(grafo, k, tamPopulacao):
  
    verticesEscolhidos = set()
    listaCiclos = []
    lista = []
    listaCiclosDominante = []
    
    while len(listaCiclosDominante) < tamPopulacao:
    
        v = random.choice(list(grafo.nodes))
        while v in verticesEscolhidos:
            v = random.choice(list(grafo.nodes))
        
        verticesEscolhidos.add(v)
        
        indice = 0        
        aux = nx.cycle_basis(grafo, v)
        #Retirando possiveis repeticoes de ciclos
        sets = [set(x) for x in aux]
        for i in sets:
            if i not in lista:
                lista.append(i)
                listaCiclos.append(aux[indice])
            indice += 1
        
        for ciclo in listaCiclos:
            if len(listaCiclosDominante) < tamPopulacao:
                if isCicloDominante(grafo, ciclo, k):
                    listaCiclosDominante.append(ciclo)
    
    return listaCiclosDominante


# Selecao

def selecao(grafo, listaCiclosDominantes, tam_torneio):
    torneio = random.sample(listaCiclosDominantes, tam_torneio)
    listaCustos = []
    pais = []
    for ciclo in torneio:
        listaCustos.append(custoCaminho(grafo, ciclo))

    for i in range(2):
        pais.append(torneio[listaCustos.index(min(listaCustos))])
        del(torneio[listaCustos.index(min(listaCustos))])
        del(listaCustos[listaCustos.index(min(listaCustos))])

    return pais

# Crossover

def crossoverC1(pais):
    corte = random.randint(0, len(pais[0]) - 1)
    #print("Corte realizado na posição {} do primeiro pai. ".format(corte))
    filho = pais[0][0:corte + 1] + pais[1][corte + 1:len(pais[1]) + 1]
    return filho


def crossoverPMX(pais):
    if (len(pais[0]) < len(pais[1])):
        inicioJanela = random.randint(1, int(len(pais[0]) / 2))
        fimJanela = random.randint(int(len(pais[0]) / 2) + 1, len(pais[0]) - 1)
    else:
        inicioJanela = random.randint(0, int(len(pais[1]) / 2))
        fimJanela = random.randint(int(len(pais[1]) / 2) + 1, len(pais[1]) - 1)
    
    #print("Inicio janela: {}".format(inicioJanela))
    #print("Fim janela: {}".format(fimJanela))
    
    janelaP1 = pais[0][inicioJanela:fimJanela + 1]
    janelaP2 = pais[1][inicioJanela:fimJanela + 1]

    pais[0][inicioJanela:fimJanela + 1] = janelaP2
    pais[1][inicioJanela:fimJanela + 1] = janelaP1
    
    mapeamentos = []
    
    mapeado = False
    
    for i in range(len(janelaP1)):
        for m in mapeamentos:
            if janelaP1[i] in m:
                m.add(janelaP1[i])
                m.add(janelaP2[i])
                mapeado = True
            if janelaP2[i] in m:
                m.add(janelaP2[i])
                m.add(janelaP1[i])
                mapeado = True
        if not mapeado:
            mapeamentos.append(set([janelaP1[i],janelaP2[i]]))
        
        mapeado = False            
    
    for i in range(len(pais[0])):
        for j in range(len(pais[1])):
            if (i < inicioJanela or i > fimJanela) and (j < inicioJanela or j > fimJanela):
                if pais[0][i] != pais[1][j]:
                    for m in mapeamentos:
                        if pais[0][i] in m and pais[1][j] in m:
                            aux = pais[0][i]
                            pais[0][i] = pais[1][j]
                            pais[1][j] = aux
    
    #print("Mapeamentos:")
    #print(mapeamentos)
    return pais

# Mutacao

def mutacaoSwapRange(f1):

    ok = True
    while (ok):
        corte_gene1 = random.randint(0, len(f1) - 1)
        corte_gene2 = random.randint(0, len(f1) - 1)
        if (corte_gene1 != corte_gene2 and corte_gene1 < corte_gene2):
            ok = False

    while (corte_gene1 < corte_gene2):
        aux = f1[corte_gene1]
        f1[corte_gene1] = f1[corte_gene2]
        f1[corte_gene2] = aux
        corte_gene1 = corte_gene1 + 1
        corte_gene2 = corte_gene2 - 1

    #print(f1)
    return(f1)

def mutacaoInvertRange(cromossomo_ciclo):
    
    inicioJanela = random.randint(0, int(len(cromossomo_ciclo) / 2))
    fimJanela = random.randint(inicioJanela + 1, len(cromossomo_ciclo))
    
    #print(inicioJanela)
    #print(fimJanela)
    
    for i in range(inicioJanela, fimJanela - 2):
        aux = cromossomo_ciclo[i]
        cromossomo_ciclo[i] = cromossomo_ciclo[i+1]
        cromossomo_ciclo[i+1] = aux
        i += 1
        
    if math.fabs(inicioJanela - fimJanela) == 1:
        aux = cromossomo_ciclo[inicioJanela]
        cromossomo_ciclo[inicioJanela] = cromossomo_ciclo[fimJanela]
        cromossomo_ciclo[fimJanela] = aux
    
    if math.fabs(inicioJanela - fimJanela) % 2 != 0 and fimJanela == len(cromossomo_ciclo):
        aux = cromossomo_ciclo[0]
        cromossomo_ciclo[0] = cromossomo_ciclo[-1]
        cromossomo_ciclo[-1] = aux
    
    return cromossomo_ciclo

# Algoritmo Genetico
def algoritmoGenetico(grafo, k, tamPopulacao, limiteIteracao):
    cromossomos = geraPopulacaoInicial(grafo, k, tamPopulacao)
    melhorSolucao = cromossomos[0]
    filhos = []
    iSemMelhora = 0
    while iSemMelhora < limiteIteracao:
        while len(filhos) < tamPopulacao:
            cromossomosPais = deepcopy(selecao(grafo, cromossomos, 4))
            escolhasCrossover = [1, 2]
            probabilidadesCrossover = [0.50, 0.50]
            rnd = np.random.choice(escolhasCrossover, p=probabilidadesCrossover)
            if rnd == 1: 
                cromossomoFilho = crossoverC1(cromossomosPais)
            elif rnd == 2:
                cromossomoFilho = random.choice(crossoverPMX(cromossomosPais))

            escolhasMutacao = [1, 2, 3]
            probabilidadesMutacao = [0.03, 0.07, 0.90]
            rnd = np.random.choice(escolhasMutacao, p=probabilidadesMutacao)
            if rnd == 1: 
                mutacaoSwapRange(cromossomoFilho)
                #print("Mutação Swap Range!")
            elif rnd == 2:
                mutacaoInvertRange(cromossomoFilho)
                #print("Mutação Invert Range!")
            
            if isCicloDominante(grafo, cromossomoFilho, k):
                filhos.append(cromossomoFilho)
    
        cromossomos = deepcopy(filhos)
        filhos = []
        melhorSolucaoAtual = melhorSolucaoPopulacao(grafo, cromossomos)
        filhos.append(melhorSolucaoAtual) #Elitismo
        if set(melhorSolucaoAtual) == set(melhorSolucao):
            iSemMelhora += 1
        
        if custoCaminho(grafo, melhorSolucaoAtual) < custoCaminho(grafo, melhorSolucao):
            melhorSolucao = melhorSolucaoAtual
    
    return melhorSolucao

def darp(grafo, kDominancia, nMaxIteracaoSemMelhora = 5):
    tamPopulacao = int(0.25 * len(grafo.nodes))
    #print("Tamanho da Populacao: {}".format(tamPopulacao))
    tInicio = time.time()
    solucao = algoritmoGenetico(grafo, kDominancia, tamPopulacao, nMaxIteracaoSemMelhora)
    tFim = time.time()
    #print("Melhor Solucao:")
    #print(solucao)
    tempoTotal = tFim - tInicio
    custoSolucao = custoCaminho(grafo, solucao)
    
    return (tempoTotal, custoSolucao)