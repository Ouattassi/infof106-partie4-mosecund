from source.constantes import *


class Quickhull:

    def __init__(self,s):
        self.s = s

    def estalinterieur(self,a, b, c, p):
        x, y = p
        x1, y1 = a
        x2, y2 = b
        x3, y3 = c

        A = self.air(x1, y1, x2, y2, x3, y3)  # Calcule l'air du triange ABC
        A1 = self.air(x, y, x2, y2, x3, y3)
        A2 = self.air(x1, y1, x, y, x3, y3)
        A3 = self.air(x1, y1, x2, y2, x, y)

        if (A == A1 + A2 + A3):  # vérifie si la somme de A1, A2 et A3 est égal à A
            return True
        else:
            return False

    def air(self,x1, y1, x2, y2, x3, y3):
        """

        fonction qui vérifie si le point P(x, y) est dans le triangle formé par  A(x1, y1), B(x2, y2) et C(x3, y3)

        """

        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

    def label_all_components(self,grid):
        labels = []
        id = 0
        for i in range(len(grid)):
            labels.append([])
            for j in range(len(grid[0])):
                labels[i].append(0)

        for i in range(0, len(grid)):
            for j in range(0, len(grid[0])):
                if grid[i][j] != FLECHE and labels[i][j] == 0:
                    id += 1
                    self.label_component(grid, id, labels, j, i)

        return labels  # @TODO: enlever le return

    def label_component(self,grid, id, labels, i, j):
        liste_delta = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        labels[j][i] = id

        for k in range(len(liste_delta)):
            delta_i, delta_j = liste_delta[k]
            i2 = delta_i + i
            j2 = delta_j + j

            if j2 < len(grid[0]) and i2 < len(grid) and i2 >= 0 and j2 >= 0 and grid[j2][i2] != FLECHE and labels[j2][
                i2] == 0:
                self.label_component(grid, id, labels, i2, j2)

    def distance(self,a, b, c):  # ax+by+c = 0

        d = a[0] - b[0]
        e = b[1] - a[1]
        f = a[1] * b[0] - b[1] * a[0]

        return abs(d * c[1] + e * c[0] + f) / (d * d + e * e) ** (1 / 2)

    def separation(self,a, b, s):

        S0 = []
        S1 = []

        if a[1] == b[1]:
            """
            Cas horizontal
            """
            for point in s:
                if point[0] > a[0]:
                    S0.append(point)

                elif point[0] < a[0]:
                    S1.append(point)

            res = S0, S1

        elif a[0] == b[0]:
            """
            Cas vertical 
            """

            for point in s:
                if point[1] > a[1]:  # partie à droite
                    S0.append(point)


                elif point[1] < a[1]:  # partie à gauche
                    S1.append(point)

            res = S0, S1  # droite/haut, gauche/bas"""

        else:

            m = (b[1] - a[1]) / (b[0] - a[0])  # y = mx+p

            p = - m * a[0] + a[1]  # p = y -mx

            for point in s:
                if point[1] > m * point[0] + p:  # partie à droite
                    S0.append(point)

                elif point[1] < m * point[0] + p:  # partie à gauche
                    S1.append(point)
            if a in S0:
                S0.remove(a)
            if b in S0:
                S0.remove(b)
            if a in S1:
                S1.remove(a)
            if b in S1:
                S1.remove(b)

            res = S0, S1  # droite, gauche

        return res

    def find_hull(self,S, a, b,
                  C):  # S = ensemble de tous les points // C = ensemble de point qui font l'enveloppe de convexe

        if S == []:
            return

        else:
            distance_max = 0
            c = None
            for point in S:

                res1 = self.distance(a, b, point)

                if res1 > distance_max:
                    c = point
                    distance_max = res1

            if c != None:
                C.append(c)
                S0_temp = []
                for point in S:
                    if c is not None and self.estalinterieur(a, b, c, point) == True:
                        S0_temp.append(point)

                for point in S0_temp:
                    S.remove(point)
                S1_temp = self.separation(a, c, S)[1]
                S2_temp = self.separation(b, c, S)[1]

                self.find_hull(S1_temp, a, c, C)
                self.find_hull(S2_temp, c, b, C)

    def quickhull(self,s):
        if len(s) == 1:
            return s
        a = min(s)
        b = max(s)
        C = [a, b]
        S0 = self.separation(a, b, s)[0]
        S1 = self.separation(a, b, s)[1]

        self.find_hull(S0, a, b, C)
        self.find_hull(S1, b, a, C)

        return C

    def quickhull_calcul(self,s, label_blanc, label_noir):
        res = []
        res_blanc = 0
        res_noir = 0
        for indice, i in enumerate(s):
            if len(i) == 1:
                if indice in label_noir:

                    res_noir += 0

                elif indice in label_blanc:

                    res_blanc += 0


            elif len(i) == 2:
                if indice in label_noir:

                    res_noir += (((max(i)[0] - min(i)[0]) ** 2) + ((max(i)[1] - min(i)[1]) ** 2) ** (1 / 2))

                elif indice in label_blanc:
                    res_blanc += (((max(i)[0] - min(i)[0]) ** 2) + ((max(i)[1] - min(i)[1]) ** 2) ** (1 / 2))

            elif len(i) == 3:
                if indice in label_noir:

                    res_noir += (self.pointdanstriangle(i[0], i[1], i[2]))

                elif indice in label_blanc:
                    res_blanc += (self.pointdanstriangle(i[0], i[1], i[2]))

            elif len(i) == 4:
                if indice in label_noir:
                    res_noir += (((i[1][0] - i[0][0]) - 1) * ((i[1][1] - i[0][1]) - 1))

                elif indice in label_blanc:
                    res_blanc += (((i[1][0] - i[0][0]) - 1) * ((i[1][1] - i[0][1]) - 1))

        return res_blanc, res_noir

    def pgcd(self,a, b):
        if (b == 0):
            return a

        return self.pgcd(b, a % b)

    def pointintegral(self,p, q):
        # verifie si la ligne est parralele à l'axe
        if (p[0] == q[0]):
            return abs(p[1] - q[1]) - 1
        if (p[1] == q[1]):
            return abs(p[0] - q[0]) - 1

        return self.pgcd(abs(p[0] - q[0]),
                    abs(p[1] - q[1])) - 1

    def pointdanstriangle(self,a, b, c):

        base = (self.pointintegral(a, b) + self.pointintegral(a, c) + self.pointintegral(b, c) + 3)
        aire = abs(a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))

        return (aire - base + 2) // 2

    def indice_dans_matrice(self,matrice, valeur):
        liste_indice = []
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                if matrice[i][j] == valeur:
                    liste_indice.append((i, j))

        return liste_indice

    def maximum_dans_matrice(self,matrice):
        res = 0
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                if matrice[i][j] > res:
                    res = matrice[i][j]

        return res