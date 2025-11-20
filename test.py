v_st = [7,8,2,3,1,1,5,6]

n = len(v_st) // 2
total = 2 * n
rebanadas_profe = total // 2
rebanadas_hermana = total // 2 - 1

memo_arr = [[-float("inf") for _ in range(2)] for _ in range(total + 1)]

def suma_circular(v, inicio, largo):
    return sum(v[(inicio + i) % len(v)] for i in range(largo)) #Estandar de sumas circulares estilo recorrer angulos

def FC_array(cs, index, v_st, p):
    if memo_arr[index][p] != -float("inf"):
        return memo_arr[index][p]

    if p == 0:

        res = suma_circular(v_st, index, rebanadas_profe) + FC_array(cs, index, v_st, 1)
        memo_arr[index][p] = res
        return res

    else:
        # Hermana: elegir su mejor bloque de tamaño n−1
        seg_prof = {(index + i) % total for i in range(rebanadas_profe)}
        restantes = [i for i in range(total) if i not in seg_prof]

        L = len(restantes)  # siempre n+1
        mejor_ultima = None
        mejor_h = -float("inf")

        for s in range(L):
            suma_h = sum(v_st[restantes[(s + k) % L]] for k in range(rebanadas_hermana))
            idx_ultima = restantes[(s + rebanadas_hermana) % L]
            if suma_h > mejor_h:
                mejor_h = suma_h
                mejor_ultima = v_st[idx_ultima]

        memo_arr[index][p] = mejor_ultima
        return mejor_ultima


# Evaluar todos los posibles inicios del profesor
resultado = max(FC_array(0, start, v_st, 0) for start in range(total))
print(resultado)   # 27
