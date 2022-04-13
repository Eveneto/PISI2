def troca(vetor, i, j):
    auxiliar = vetor[i]
    vetor[i] = vetor[j]
    vetor[j] = auxiliar

def permuta(vetor, inferior, superior):
    if(inferior == superior):
        for i in range(superior+1):
            print(vetor[i])
        print("\n") 
    else:
        i = inferior
        for i in range(superior+1):
            troca(vetor, inferior, i)
            permuta(vetor, inferior + 1, superior)
            troca(vetor, inferior, i) 

vetor = [1, 2, 3]
tamanho_vetor = len(vetor)

permuta(vetor, 0, tamanho_vetor - 1)



