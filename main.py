import math

from acf import ACF, Grafo
from plot import plot

def distancia(cidade1: dict, cidade2: dict):
    return math.sqrt((cidade1['x'] - cidade2['x']) ** 2 + (cidade1['x'] - cidade2['y']) ** 2)

def main(): 
    cidades = []
    pontos = [] 
    with open('entrada.txt') as f: 
        for line in f.readlines():
            cidade = line.split(' ')
            cidades.append(dict(index=int(cidade[0]), x = int(cidade[1]), y = int(cidade[2])))
            pontos.append((int(cidade[1]), int(cidade[2])))
        custo_matriz = []
        rank = len(cidades)
        for i in range(rank):
            linha = []
            for j in range(rank):
                linha.append(distancia(cidades[i], cidades[j]))
            custo_matriz.append(linha)
        acf = ACF(10, 100, 1.0, 10.0, 0.5, 10, 2)
        grafo = Grafo(custo_matriz, rank)
        caminho, custo = acf.resolver(grafo)
        print('custo: {}, caminho: {}' .format(custo, caminho))
        plot(pontos, caminho)

if __name__ == '__main__':
    main()
