#i = {0,1,...,2n}
#v_st (valores de satisfaccion) = {random_0,random_1,...,random_2n}

#SRTBOT
#S: Prefijos i -> 2n, 2 Players (p): 0 = Profesor, 1 = Hermana de profesor
#R: Para Profesor: st(i,2n,p) = max{st(i,2n,0), st(i+1,2n,1) + v_st[i]} // Incluye el paso de control al otro player despues de la call
##: Para Hermana de profesor:st(i,2n,p) = max{st(i,2n,1), st(i+1,2n,0)} // Incluye el paso de control al otro player despues de la call
#T: i aumenta
#B: st(2n-1,2n,0) = v_st, st(2n-1,2n,1) = v_st
#O: st(0,2n,1)
#T: n subproblemas de tamano n, O(n^2)

v_st = [7,8,2,3,1,1,5,6]

n = len(v_st) // 2
total = 2 * n

memo_arr = [[-float("inf") for _ in range(2)] for _ in range(total + 1)]
memo_hash = {}


def FC_array(i,v_st,p):

    if memo_arr[i][p] != -float("inf"):
        return memo_arr[i][p]
    
    if (i >= len(v_st)-1):
        q = v_st[i]

    else:
        if (p == 0):
        
            max_value = max(FC_array(i+1 , v_st, 0), 
                    v_st[i] + FC_array(i+1 , v_st , 1))
            
            

    memo_arr[i][p] = q
    return q

v = FC_array(0,0,v_st, 0)
print (v)

















#
#def FC_hash(i,v_st,p):
#    if (i,p) in memo_hash:
#        return memo_hash[(i,p)]
#    if (i == total - 1):
#        q = v_st[i]
#    else:
#        if (p == 0):
#            q = max(FC_hash(i+1,v_st,0),
#                    v_st[i] + FC_hash(i+1,v_st,1))
#        else:
#            q = max(FC_hash(i+1,v_st,1),
#                    FC_hash(i+1,v_st,0))
#    memo_hash[(i,p)] = q
#    return q
#
#h = FC_hash(0,v_st, 0)
#print (h)