#     1   2   3   4   5
S = [10, 40, 30, 20, 50] 
temp = 20

def intercambiol(S, x, y):
    temporal = S[x] # S[x], S[y] = S[y], S[x], tambien se puede hacer asi, se omite lo demas y prosigue el print
    S[x] = S[y]
    S[y] = temporal

print(S); intercambiol(S, 1, 3)
print(S)