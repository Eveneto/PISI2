import random

class Grafo(object):
    def __init__(self, custo_matriz: list, rank: int):
        self.matriz = custo_matriz
        self.rank = rank
        self.feromonio = [[1 / (rank * rank) for j in range(rank)] for i in range(rank)]

class ACF(object):
    def __init__(self, contador_drone: int, geracoes: int, alfa: float, beta: float, crf: float, estrategia: int):
        self.Q = q
        self.crf = crf #coeficiente residual do feromonio
        self.beta = beta
        self.alfa = alfa
        self.contador_drone = contador_drone
        self.geracoes = geracoes
        self.atualizar_estrategia = estrategia
    
    def atualizar_feromonio(self, grafo: Grafo, drones: list):
        for i, row in enumerate(grafo.feromonio):
            for j, col in enumerate(row):
                grafo.feromonio[i][j] *= self.crf
                for drone in drones:
                    grafo.feromonio[i][j] += drone.feromonio_delta[i][j]
    
    def resolver(self, grafo: Grafo):
        melhor_custo = float('inf')
        melhor_solucao = []
        for gen in range(self.geracoes):
            drones = [Drone(self, grafo) for i in range(self.contador_drone)]
            for drone in drones:
                for i in range(grafo.rank - 1):
                    drone.selecionar_proximo()
                drone.custo_total += grafo.matriz[drone.tabu[-1]][drone.tabu[0]]
                if drone.custo_total < melhor_custo:
                    melhor_custo = drone.custo_total
                    melhor_solucao = [] + drone.tabu
                #atualizar feromonio
                drone.atualizar_feromonio_delta()
            self.atualizar_feromonio(grafo, drones)
        return melhor_solucao, melhor_custo

class Drone(object):
    def __init__(self, acf: ACF, grafo: Grafo):
        self.colonia = acf
        self.grafo = grafo
        self.custo_total = 0.0
        self.tabu = [] 
        self.feromonio_delta = [] #adição de feromonio
        self.permitido = [i for i in range(grafo.rank)] #nodos que são permitidos para a proxima seleção
        self.eta = [[0 if i == j else 1 / grafo.matriz[i][j] for j in range(grafo.rank)] for i in range(grafo.rank)]
        inicio = random.randint(0, grafo.rank - 1) #começa de qualquer nodo
        self.tabu.append(inicio)
        self.atual = inicio
        self.permitido.remove(inicio)

    def selecionar_proximo(self):
        denominador = 0
        for i in self.permitido:
            denominador += self.grafo.feromonio[self.atual][i] ** self.colonia.alfa * self.eta[self.atual][i] ** self.colonia.beta
            probabilidades = [0 for i in range(self.grafo.rank)] #probabilidades de se mover para um nó na próxima etapa
            for i in range(self.grafo.rank):
                try:
                    self.permitido.index(i) #testa se a lista de permitidos contem i
                    probabilidades[i] = self.grafo.feromonio[self.atual][i] ** self.colonia.alfa * \
                        self.eta[self.atual][i] ** self.colonia.beta / denominador
                except ValueError:
                    pass #fazer nada
            #seleciona o proximo nodo pela roleta de probabilidade
            selecionado = 0
            rand = random.random()
            for i, probabilidade in enumerate(probabilidades):
                rand -= probabilidade
                if rand <= 0:
                    selecionado = 1
                    break
            self.permitido.remove(selecionado)
            self.tabu.append(selecionado)
            self.custo_total += self.grafo.matriz[self.atual][selecionado]
            self.atual = selecionado

    def atualizar_feromonio_delta(self):
        self.feromonio_delta = [[0 for j in range(self.grafo.rank)] for i in range(self.grafo.rank)]
        for _ in range(1, len(self.tabu)):
            i = self.tabu[_ - 1]
            j = self.tabu[_]
            if self.colonia.atualizar_estrategia == 1:
                self.feromonio_delta[i][j] = self.colonia.Q
            elif self.colonia.atualizar_estrategia == 2:
                self.feromonio_delta[i][j] = self.colonia.Q / self.grafo.matriz[i][j]
            else: 
                self.feromonio_delta[i][j] = self.colonia.Q / self.custo_total 