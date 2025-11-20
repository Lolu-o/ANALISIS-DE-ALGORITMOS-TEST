#SRTBOT
#S: Sufijos 2n -> 0, 2 Players (p): 0 = Profesor, 1 = Hermana de profesor 
#R: Para Profesor: st(i,0) = sum_profesor(i) + st(i,1) // Incluye el paso de control al otro player despues de la call 
##: Para Hermana de profesor: st(i,1) = max {inicio:{0 : n}} ultima(i,start) // Incluye el paso de control al otro player despues de la call para el ultimo trozo de torta
#T: n decrementa -> 2n decrementa hasta 0 
#B: st(0,0) = n/2 trozos comidos -> st(n/2,1) -> buscar el minimo valor v_st[i] de la lista restante y sumar al profesor
#O: Respuesta = max{0 ≤ i < 2n} para st(i,0)
#T: n subproblemas de tamaño n^2, O(n^3)


v_st = [7,8,2,3,1,1,5,6]

n = len(v_st) // 2
total = 2 * n
rebanadas_profe = total // 2
rebanadas_hermana = total // 2 - 1
memo_arr = [[-float("inf") for _ in range(2)] for _ in range(total + 1)]
memo_hash = {}

def suma_circular(v, inicio, largo): #Entra con largo = rebanadas profe = n/2, O(n/2) = O(n)
    s = 0
    m = len(v)
    for i in range(largo):
        s += v[(inicio + i) % m]
    return s

def FC_array(index, v_st, p):

    if memo_arr[index][p] != -float("inf"):
        return memo_arr[index][p]

    if p == 0:

        suma_prof = suma_circular(v_st, index, rebanadas_profe) #Rebanadas profe = n/2, simula partir de un alfa_i hasta un alfa_i + pi = mitad de la torta
        trozo_restante_hermana = FC_array(index, v_st, 1) #se entrega el control a la hermana para obtener la slice restante, especificado en el pdf
        q = suma_prof + trozo_restante_hermana #Suma de la seleccion del profesor + el slice restante de la hermana
        memo_arr[index][p] = q
        return q

    else:

        segmento_prof = set((index + i) % total for i in range(rebanadas_profe)) #trabajamos con indices en lugar del valor bruto en la lista para optimizar
        restantes = []

        for i in range(total): #O(n)
            if i not in segmento_prof: #O(1) dada la naturaleza de Check In Set
                restantes.append(v_st[i])

        #el profesor recibe la rebanada de menor v_st disponible
        q = min(restantes) #O(n)

        memo_arr[index][p] = q
        return q
    

def FC_hash(index, v_st, p):

    if (index,p) in memo_hash:
        return memo_hash[(index,p)]

    if p == 0:

        suma_prof = suma_circular(v_st, index, rebanadas_profe) #Rebanadas profe = n/2, simula partir de un alfa_i hasta un alfa_i + pi = mitad de la torta
        trozo_restante_hermana = FC_array(index, v_st, 1) #se entrega el control a la hermana para obtener la slice restante, especificado en el pdf
        q = suma_prof + trozo_restante_hermana #Suma de la seleccion del profesor + el slice restante de la hermana
        memo_hash[(index,p)] = q
        return q

    else:

        segmento_prof = set((index + i) % total for i in range(rebanadas_profe)) #trabajamos con indices en lugar del valor bruto en la lista para optimizar
        restantes = []

        for i in range(total): #O(n)
            if i not in segmento_prof: #O(1) dada la naturaleza de Check In Set
                restantes.append(v_st[i])

        #el profesor recibe la rebanada de menor v_st disponible
        q = min(restantes) #O(n)

        memo_hash[(index,p)] = q
        return q
    
def main():

    resultado = -float("inf")
    for start in range(total):
        resultado = max(resultado, FC_array(start, v_st, 0))

    print("Resultado arrays:",resultado)

    resultado_h = -float("inf")
    for start in range(total):
        resultado_h = max(resultado_h, FC_hash(start, v_st, 0))
    
    print("Resultado hash:",resultado_h)

if __name__ == "__main__":
    main()
