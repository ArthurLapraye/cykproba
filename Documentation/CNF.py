# coding: utf-8

def ALGO_CNF(G):
    """

    :param G: Grammaire propre et sans productions unitaires
    :return: Grammaire sous forme normale de chomsky
    """
    N_prim = set([]) | G.X
    P_prim = {}
    for q in G.Q:
        P_prim.update({q.upper()+q:q})
    for (lhs, rhs) in G.P:
        if rhs in G.Q:
            P_prim[lhs] = rhs
    for (lhs, rhs) in G.P:
        if ((len(rhs)>1) and (isinstance(rhs,list))):
            temp = [rh in G.Q for rh in rhs]
