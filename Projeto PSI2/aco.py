import random


class Grafo(object):
    def __init__(self, custo_matrix: list, rank: int):
        self.matrix = custo_matrix
        self.rank = rank
        self.feromonio = [[1 / (rank * rank) for j in range(rank)] for i in range(rank)]


class ACO(object):
    def __init__(self, contador_formiga: int, geracoes: int, alfa: float, beta: float, coeficiente: float, q: int,
                 estrategia: int):
        self.Q = q
        self.coeficiente = coeficiente #coeficiente residual do feromonio
        self.beta = beta
        self.alfa = alfa
        self.contador_formiga = contador_formiga
        self.geracoes = geracoes
        self.atualizar_estrategia = estrategia

    def atualizar_feromonio(self, grafo: Grafo, formigas: list):
        for i, linha in enumerate(grafo.feromonio):
            for j, coluna in enumerate(linha):
                grafo.feromonio[i][j] *= self.coeficiente
                for formiga in formigas:
                    grafo.feromonio[i][j] += formiga.feromonio_delta[i][j]

    def resolver(self, grafo: Grafo):
        """
        :param grafo:
        """
        melhor_custo = float('inf')
        melhor_solucao = []
        for gen in range(self.geracoes):
            formigas = [Formiga(self, grafo) for i in range(self.contador_formiga)]
            for formiga in formigas:
                for i in range(grafo.rank - 1):
                    formiga.selecionar_proximo()
                formiga.custo_total += grafo.matrix[formiga.removidos[-1]][formiga.removidos[0]]
                if formiga.custo_total < melhor_custo:
                    melhor_custo = formiga.custo_total
                    melhor_solucao = [] + formiga.removidos
                 #atualizar feromonio
                formiga.atualizar_feromonio_delta()
            self.atualizar_feromonio(grafo, formigas)
        return melhor_solucao, melhor_custo


class Formiga(object):
    def __init__(self, aco: ACO, grafo: Grafo):
        self.coluna = aco
        self.grafo = grafo
        self.custo_total = 0.0
        self.removidos = []  
        self.feromonio_delta = []  # adição de feromônio
        self.permitido = [i for i in range(grafo.rank)]  #nodos que são permitidos para a proxima seleção
        self.eta = [[0 if i == j else 1 / grafo.matrix[i][j] for j in range(grafo.rank)] for i in
                    range(grafo.rank)] 
        inicio = random.randint(0, grafo.rank - 1)  
        self.removidos.append(inicio)
        self.atual = inicio
        self.permitido.remove(inicio)

    def selecionar_proximo(self):
        denominador = 0
        for i in self.permitido:
            denominador += self.grafo.feromonio[self.atual][i] ** self.coluna.alfa * self.eta[self.atual][i] ** self.coluna.beta
        probabilidades = [0 for i in range(self.grafo.rank)]  
        for i in range(self.grafo.rank):
            try:
                self.permitido.index(i)  
                probabilidades[i] = self.grafo.feromonio[self.atual][i] ** self.coluna.alfa * \
                    self.eta[self.atual][i] ** self.coluna.beta / denominador
            except ValueError:
                pass  
        selecionado = 0
        rand = random.random()
        for i, probabilidade in enumerate(probabilidades):
            rand -= probabilidade
            if rand <= 0:
                selecionado = i
                break
        self.permitido.remove(selecionado)
        self.removidos.append(selecionado)
        self.custo_total += self.grafo.matrix[self.atual][selecionado]
        self.atual = selecionado

    def atualizar_feromonio_delta(self):
        self.feromonio_delta = [[0 for j in range(self.grafo.rank)] for i in range(self.grafo.rank)]
        for _ in range(1, len(self.removidos)):
            i = self.removidos[_ - 1]
            j = self.removidos[_]
            if self.coluna.atualizar_estrategia == 1: 
                self.feromonio_delta[i][j] = self.coluna.Q
            elif self.coluna.atualizar_estrategia == 2:  
                self.feromonio_delta[i][j] = self.coluna.Q / self.grafo.matrix[i][j]
            else:
                self.feromonio_delta[i][j] = self.coluna.Q / self.custo_total
