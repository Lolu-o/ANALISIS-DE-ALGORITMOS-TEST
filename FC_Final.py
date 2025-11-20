import time
import random
import statistics
import matplotlib.pyplot as plt
import sys

#SRTBOT
#S: Sufijos 2n -> 0, 2 Players (p): 0 = Profesor, 1 = Hermana de profesor 
#R: Para Profesor: st(i,0) = sum_profesor(i) + st(i,1) // Incluye el paso de control al otro player despues de la call 
##: Para Hermana de profesor: st(i,1) = max {inicio:{0 : n}} ultima(i,start) // Incluye el paso de control al otro player despues de la call para el ultimo trozo de torta
#T: n decrementa -> 2n decrementa hasta 0 
#B: st(0,0) = n/2 trozos comidos -> st(n/2,1) -> buscar el minimo valor v_st[i] de la lista restante y sumar al profesor
#O: MayorSt = max{0 ≤ i < 2n} para st(i,0)
#T: n subproblemas de tamaño n, O(n^2)


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


###Funcion auxiliar para medir tiempos y generar graficos, se generan V_ST de tamanios [16, 32, 64, 128, 256] con valores aleatorios####
def medir_tiempos(total_list, trials=5, seed=42):
    random.seed(seed)
    tiempos_array = []
    tiempos_hash = []

    for total_run in total_list:
        # Preparamos v_st y variables globales requeridas por las funciones
        global v_st, n, total, rebanadas_profe, rebanadas_hermana, memo_arr, memo_hash

        total = total_run               # longitud total de v_st
        n = total // 2
        rebanadas_profe = total // 2
        rebanadas_hermana = total // 2 - 1

        # Generar v_st aleatorio (pueden ser negativos según enunciado)
        v_st = [random.randint(-10, 10) for _ in range(total)]

        # Arrays para almacenar tiempos de cada trial
        tiempos_this_array = []
        tiempos_this_hash = []

        for t in range(trials):
            # ----------------- Medir FC_array (memo en arreglos) -----------------
            memo_arr = [[-float("inf") for _ in range(2)] for _ in range(total + 1)]
            # Aseguramos memo_hash limpio para no afectar
            memo_hash = {}

            start = time.perf_counter()
            _ = FC_array(0, v_st, 0)   # llamamos tu función con la firma actual
            elapsed = time.perf_counter() - start
            tiempos_this_array.append(elapsed)

            # ----------------- Medir FC_hash (memo en diccionario) -----------------
            memo_hash = {}
            memo_arr = [[-float("inf") for _ in range(2)] for _ in range(total + 1)]

            start = time.perf_counter()
            _ = FC_hash(0, v_st, 0)
            elapsed = time.perf_counter() - start
            tiempos_this_hash.append(elapsed)

        # Promedios y almacenamiento
        avg_array = statistics.mean(tiempos_this_array)
        avg_hash = statistics.mean(tiempos_this_hash)
        tiempos_array.append(avg_array)
        tiempos_hash.append(avg_hash)

        print(f"total={total:4d} | FC_array avg={avg_array:.6f}s over {trials} runs | FC_hash avg={avg_hash:.6f}s")

    return tiempos_array, tiempos_hash

if __name__ == "__main__":


    resultado = -float("inf")
    for start in range(total):
        resultado = max(resultado, FC_array(start, v_st, 0))

    print("Resultado CASO DE PRUEBA EN Array:",resultado)

    resultado_h = -float("inf")
    for start in range(total):
        resultado_h = max(resultado_h, FC_hash(start, v_st, 0))

    print("Resultado CASO DE PRUEBA EN Tabla Hash:",resultado_h)


    #########################ZONA DE PRUEBAS########################
    # Recomiendo empezar con tamaños moderados para no chocar con recursionlimit.
    totals_to_test = [16, 32, 64, 128, 256]   # puedes ajustar o añadir más
    trials_per_size = 5

    tiempos_arr, tiempos_hsh = medir_tiempos(totals_to_test, trials=trials_per_size, seed=123)

    # Graficar resultados
    plt.figure(figsize=(8,5))
    plt.plot(totals_to_test, tiempos_arr, marker='o', label='FC_array (tabla)')
    plt.plot(totals_to_test, tiempos_hsh, marker='s', label='FC_hash (diccionario)')
    plt.xlabel('longitud de v_st (total = 2n)')
    plt.ylabel('tiempo promedio (segundos)')
    plt.title('Comparación tiempos: memo en array vs memo en hash')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


###Fin funcion auxiliar para medir tiempos y generar graficos####

