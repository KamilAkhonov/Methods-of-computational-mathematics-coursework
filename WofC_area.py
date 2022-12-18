import numpy as np
import time
import numpy.linalg as lin
# import pandas as pd
import matplotlib.pyplot as plt

dim = 1
L_x = 5 * dim
L_y = 4 * dim
h_x = 0.25
h_y = 0.25
eps = 0.00001

##########################################
# ----------------Плоскость---------------#
# test = 1


# ----------------Параболоид--------------#
# test = 2


# ---------Индивидуальная функция---------#
# test = 3


##########################################

def func_u(x, y):
    match test:
        case 1:
            return 2 * x + 3 * y - 5
        case 2:
            return 3 * x ** 2 - 2 * y ** 2 - 1
        case 3:
            return np.exp((np.sin(x)) ** 2 + (np.cos(y)) ** 2)


def func_f(x, y):
    match test:
        case 1:
            return 0 + x - x
        case 2:
            return -2 + x - x
        case 3:
            return -1 * np.exp(
                (np.sin(x)) ** 2 + (np.cos(y)) ** 2) * \
                   ((np.sin(2 * x)) ** 2 + 2 * np.cos(
                       2 * x) + np.sin(2 * y) -
                    2 * np.cos(2 * y))


# Метод простой итерации(Якоби)
def Cross_Jac(f, h_1, h_2, y0, ep):
    C_0 = (0.5 * (h_1 ** 2) * (h_2 ** 2)) / (
            h_1 ** 2 + h_2 ** 2)
    C_1 = (0.5 * (h_2 ** 2)) / (h_1 ** 2 + h_2 ** 2)

    C_2 = (0.5 * (h_1 ** 2)) / (h_1 ** 2 + h_2 ** 2)
    Nx = int(L_x / h_1) + 1
    Ny = int(L_y / h_2) + 1
    x = np.linspace(0, L_x, Nx)
    y = np.linspace(0, L_y, Ny)

    # 4 subareas
    # 1:
    Ny_1 = int((Ny - 1) / 4) + 1
    Nx_1 = int(2 * (Nx - 1) / 5) + 1
    U_sub_1 = np.zeros((Ny_1, Nx_1))
    # 2:
    Ny_2 = int((Ny - 1) / 4) + 1
    Nx_2 = int(4 * (Nx - 1) / 5) + 1
    U_sub_2 = np.zeros((Ny_2, Nx_2))
    # 3:
    Ny_3 = int((Ny - 1) / 4) + 1
    Nx_3 = int(4 * (Nx - 1) / 5) + 1
    U_sub_3 = np.zeros((Ny_3, Nx_3))
    # 4:
    Ny_4 = int((Ny - 1) / 4) + 1
    Nx_4 = int(2 * (Nx - 1) / 5) + 1
    U_sub_4 = np.zeros((Ny_4, Nx_4))

    # input initial values
    # First area
    for i in range(Ny_1):
        for j in range(Nx_1):
            U_sub_1[i][j] = y0(x[int((Nx - 1) / 5) + j], y[Ny - 1])
    for i in range(Ny_1):
        U_sub_1[i][0] = y0(x[int((Nx - 1) / 5)], y[Ny - 1 - i])
    for i in range(Ny_1):
        U_sub_1[i][Nx_1 - 1] = y0(x[int(3 * (Nx - 1) / 5)], y[Ny - 1 - i])

    # Second area
    for i in range(Ny_2):
        for j in range(Nx_2):
            U_sub_2[i][j] = y0(x[j], y[Ny - 1])
    for j in range(int((Nx - 1) / 5) + 1):
        U_sub_2[0][j] = y0(x[j], y[int(3 * (Ny - 1) / 4)])
    for i in range(Ny_2):
        U_sub_2[i][0] = y0(x[0], y[int(3 * (Ny - 1) / 4) - i])
    for j in range(int((Nx - 1) / 5) + 1):
        U_sub_2[Ny_2 - 1][j] = y0(x[j], y[int(2 * (Ny - 1) / 4)])
    for j in range(int((Nx - 1) / 5) + 1):
        U_sub_2[0][j + int(3 * (Nx_2 - 1) / 4)] = y0(x[int(3 * (Nx - 1) / 5) + j], y[int(3 * (Ny - 1) / 4)])
    for i in range(int(Ny_2)):
        U_sub_2[i][Nx_2 - 1] = y0(x[int(4 * (Nx - 1) / 5)], y[int(3 * (Ny - 1) / 4) - i])

    # Third area
    for i in range(Ny_3):
        for j in range(Nx_3):
            U_sub_3[i][j] = y0(x[j + int((Nx - 1) / 5)], y[Ny - 1])
    for i in range(Ny_3):
        U_sub_3[i][0] = y0(x[int((Nx - 1) / 5)], y[int(2 * (Ny - 1) / 4) - i])
    for j in range(Ny_3):
        U_sub_3[Ny_3 - 1][j] = y0(x[int((Nx - 1) / 5) + j], y[int((Ny - 1) / 4)])
    for j in range(Ny_3):
        U_sub_3[Ny_3 - 1][j + int(3 * (Nx_3 - 1) / 4)] = y0(x[int(4 * (Nx - 1) / 5) + j], y[int((Ny - 1) / 4)])
    for i in range(Ny_3):
        U_sub_3[i][Nx_3 - 1] = y0(x[Nx - 1], y[int(2 * (Ny - 1) / 4) - i])
    for j in range(Ny_3):
        U_sub_3[0][j + int(3 * (Nx_3 - 1) / 4)] = y0(x[int(4 * (Nx - 1) / 5) + j], y[int(2 * (Ny - 1) / 4)])

    # fourth area
    for i in range(Ny_4):
        for j in range(Nx_4):
            U_sub_4[i][j] = y0(x[int(2 * (Nx - 1) / 5) + j], y[Ny - 1])
    for i in range(Ny_4):
        U_sub_4[i][0] = y0(x[int(2 * (Nx - 1) / 5)], y[int((Ny - 1) / 4) - i])
    for j in range(Nx_4):
        U_sub_4[Ny_4 - 1][j] = y0(x[int(2 * (Nx - 1) / 5) + j], y[0])
    for i in range(Ny_4):
        U_sub_4[i][Nx_4 - 1] = y0(x[int(4 * (Nx - 1) / 5)], y[int((Ny - 1) / 4) - i])

    # Обходим =)

    prev_sol1 = U_sub_1.copy()
    prev_sol2 = U_sub_2.copy()
    prev_sol3 = U_sub_3.copy()
    prev_sol4 = U_sub_4.copy()
    it = 0
    nrm = 1
    while nrm > eps:
        # верно  1
        for i in range(1, Ny_1 - 1):
            for j in range(1, Nx_1 - 1):
                U_sub_1[i][j] = C_0 * f(x[j + int((Nx - 1) / 5)], y[Ny - 1 - i]) + C_1 * (
                        U_sub_1[i + 1][j] + U_sub_1[i - 1][j]) \
                                + C_2 * (U_sub_1[i][j - 1] + U_sub_1[i][j + 1])
        # верно граница
        for j in range(1, Nx_1 - 1):
            U_sub_1[Ny_1 - 1][j] = C_0 * f(x[j + int((Nx - 1) / 5)], y[Ny - Ny_1]) + C_1 * (
                    U_sub_2[1][int((Nx_2 - 1) / 4) + j] + U_sub_1[Ny_1 - 2][j]) \
                                   + C_2 * (U_sub_1[Ny_1 - 1][j - 1] + U_sub_1[Ny_1 - 1][j + 1])
            U_sub_2[0][int((Nx_2 - 1) / 4) + j] = U_sub_1[Ny_1 - 1][j]

        # верно 2
        for i in range(1, Ny_2 - 1):
            for j in range(1, Nx_2 - 1):
                U_sub_2[i][j] = C_0 * f(x[j], y[int(3 * (Ny - 1) / 4) - i]) + C_1 * (
                        U_sub_2[i + 1][j] + U_sub_2[i - 1][j]) \
                                + C_2 * (U_sub_2[i][j - 1] + U_sub_2[i][j + 1])
        # верно граница
        for j in range(int((Nx_2 - 1) / 4) + 1, Nx_2 - 1):
            U_sub_2[Ny_2 - 1][j] = C_0 * f(x[j], y[int(3 * (Ny - 1) / 4) - Ny_2 + 1]) + C_1 * (
                    U_sub_3[1][j - int((Nx_2 - 1) / 4)] + U_sub_2[Ny_2 - 2][j]) \
                                   + C_2 * (U_sub_2[Ny_2 - 1][j - 1] + U_sub_2[Ny_2 - 1][j + 1])
            U_sub_3[0][j - int((Nx_2 - 1) / 4)] = U_sub_2[Ny_2 - 1][j]
        # верно 3
        for i in range(1, Ny_3 - 1):
            for j in range(1, Nx_3 - 1):
                U_sub_3[i][j] = C_0 * f(x[int((Nx - 1) / 5) + j], y[int(2 * (Ny - 1) / 4) - i]) + C_1 * (
                        U_sub_3[i + 1][j] + U_sub_3[i - 1][j]) \
                                + C_2 * (U_sub_3[i][j - 1] + U_sub_3[i][j + 1])
        # верно граница
        for j in range(int((Nx_3 - 1) / 4) + 1, Nx_3 - int((Nx_3 - 1) / 4) - 1):
            U_sub_3[Ny_3 - 1][j] = C_0 * f(x[int((Nx - 1) / 5) + j], y[int(2 * (Ny - 1) / 4) - Ny_3 + 1]) + C_1 * (
                    U_sub_4[1][j - int((Nx_3 - 1) / 4)] + U_sub_3[Ny_3 - 2][j]) \
                                   + C_2 * (U_sub_3[Ny_3 - 1][j - 1] + U_sub_3[Ny_3 - 1][j + 1])
            U_sub_4[0][j - int((Nx_3 - 1) / 4)] = U_sub_3[Ny_3 - 1][j]

        for i in range(1, Ny_4 - 1):
            for j in range(1, Nx_4 - 1):
                U_sub_4[i][j] = C_0 * f(x[int(2 * (Nx - 1) / 5) + j], y[int((Ny - 1) / 4) - i]) + C_1 * (
                        U_sub_4[i + 1][j] + U_sub_4[i - 1][j]) \
                                + C_2 * (U_sub_4[i][j - 1] + U_sub_4[i][j + 1])

        mx1 = lin.norm(np.abs(prev_sol1 - U_sub_1))
        mx2 = lin.norm(np.abs(prev_sol2 - U_sub_2))
        mx3 = lin.norm(np.abs(prev_sol3 - U_sub_3))
        mx4 = lin.norm(np.abs(prev_sol4 - U_sub_4))
        nrm = max(mx1, mx2, mx3, mx4)

        prev_sol1 = U_sub_1.copy()
        prev_sol2 = U_sub_2.copy()
        prev_sol3 = U_sub_3.copy()
        prev_sol4 = U_sub_4.copy()

        print(nrm)
        it += 1

    # r1 = lin.norm(sub1_z - U_sub_1)
    # r2 = lin.norm(sub2_z - U_sub_2)
    # r3 = lin.norm(sub3_z - U_sub_3)
    # r4 = lin.norm(sub4_z - U_sub_4)

    # r1 = lin.norm()

    # r = max(r1, r2, r3, r4)
    return nrm, it


print("***********************Jacobi***********************")

ts = time.time()
sol, pop = Cross_Jac(func_f, h_x, h_y, func_u, eps)
tf = time.time()
print('Невязка = ', sol)
print('Итераций = ', pop)
print('Время = ', tf - ts)


# Точное решение
def solve_of_task(U):
    trsol = np.zeros((N_x + 1, N_y + 1))
    for i in range(N_x + 1):
        for j in range(N_y + 1):
            trsol[i][j] = U(i * h_x, j * h_y)
    return trsol


# Вращения Гивенса
def givens(A, N):
    for l in range(N - 1):
        for i in range(N - 1, 0 + l, -1):
            j = i - 1
            if A[i][l] != 0:
                alem = A[j][l]
                belem = A[i][l]
                if np.abs(belem) > np.abs(alem):
                    tau = alem / belem
                    S = 1 / np.sqrt(1 + tau ** 2)
                    C = S * tau
                else:
                    tau = belem / alem
                    C = 1 / np.sqrt(1 + tau ** 2)
                    S = C * tau
                A[i], A[j] = A[i] * C - A[j] * S, A[j] * C + A[i] * S
    return A


# обратный ход метода Гаусса
def Gauss_back_step(A, B, N):
    sol = np.zeros(N)
    for i in range(N - 1, -1, -1):
        s = 0
        if i == N - 1:
            sol[i] = B[i] / A[i][i]
        else:
            for j in range(i + 1, N, 1):
                s += A[i][j] * sol[j]
            sol[i] = (B[i] - s) / A[i][i]
    return sol


def multA(area1, area2, area3, area4):
    # initialization mult
    mult_area1 = np.copy(area1)
    mult_area2 = np.copy(area2)
    mult_area3 = np.copy(area3)
    mult_area4 = np.copy(area4)

    # first area
    for i in range(1, mult_area1.shape[0] - 1):
        for j in range(1, mult_area1.shape[1] - 1):
            mult_area1[i][j] = -1 * ((area1[i - 1][j] - 2 * area1[i][j] + area1[i + 1][j]) / h_x ** 2 + (
                    area1[i][j - 1] - 2 * area1[i][j] + area1[i][j + 1]) / h_y ** 2)
    for j in range(1, mult_area1.shape[1] - 1):
        mult_area1[mult_area1.shape[0] - 1][j] = -1 * (
                (area1[mult_area1.shape[0] - 2][j] - 2 * area1[mult_area1.shape[0] - 1][j] + area2[1][int((area2.shape[1] - 1) / 4) + j]) / h_y ** 2 + (
                area1[mult_area1.shape[0] - 1][j - 1] - 2 * area1[mult_area1.shape[0] - 1][j] + area1[mult_area1.shape[0] - 1][j + 1]) / h_x ** 2)

    # second area
    for i in range(1, mult_area2.shape[0] - 1):
        for j in range(1, mult_area2.shape[1] - 1):
            mult_area2[i][j] = -1 * ((area2[i - 1][j] - 2 * area2[i][j] + area2[i + 1][j]) / h_x ** 2 + (
                    area2[i][j - 1] - 2 * area2[i][j] + area2[i][j + 1]) / h_y ** 2)
    for j in range(int((mult_area2.shape[1] - 1) / 4) + 1, mult_area2.shape[1] - 1):
        mult_area2[mult_area2.shape[0] - 1][j] = -1 * ((area2[mult_area2.shape[0] - 2][j] - 2 * area2[mult_area2.shape[0] - 1][j] + area3[1][
            j - int((mult_area2.shape[1] - 1) / 4)]) / h_x ** 2 + (
                                                               area2[mult_area2.shape[0] - 1][j - 1] - 2 * area2[mult_area2.shape[0] - 1][j] +
                                                               area2[mult_area2.shape[0] - 1][j + 1]) / h_y ** 2)
    # third area
    for i in range(1, mult_area3.shape[0] - 1):
        for j in range(1, mult_area3.shape[1] - 1):
            mult_area3[i][j] = -1 * ((area3[i - 1][j] - 2 * area3[i][j] + area3[i + 1][j]) / h_x ** 2 + (
                    area3[i][j - 1] - 2 * area3[i][j] + area3[i][j + 1]) / h_y ** 2)
    for j in range(int((mult_area3.shape[1] - 1) / 4) + 1, mult_area3.shape[1] - int((mult_area3.shape[1] - 1) / 4) - 1):
        mult_area3[mult_area3.shape[0] - 1][j] = -1 * ((area3[mult_area3.shape[0] - 2][j] - 2 * area3[mult_area3.shape[0] - 1][j] + area4[1][
            j - int((mult_area3.shape[1] - 1) / 4)]) / h_x ** 2 + (
                                                               area3[mult_area3.shape[0] - 1][j - 1] - 2 * area3[mult_area3.shape[0] - 1][j] +
                                                               area3[mult_area3.shape[0] - 1][j + 1]) / h_y ** 2)

    # fourth area
    for i in range(1, mult_area4.shape[0] - 1):
        for j in range(1, mult_area4.shape[1] - 1):
            mult_area4[i][j] = -1 * ((area4[i - 1][j] - 2 * area4[i][j] + area4[i + 1][j]) / h_x ** 2 + (
                    area4[i][j - 1] - 2 * area4[i][j] + area4[i][j + 1]) / h_y ** 2)

    return mult_area1, mult_area2, mult_area3, mult_area4


def Scalar(a1, a2, a3, a4, b1, b2, b3, b4):
    sum = 0
    for i in range(a1.shape[0]):
        for j in range(a1.shape[1]):
            sum += a1[i, j] * b1[i, j]
    for i in range(a2.shape[0]):
        for j in range(a2.shape[1]):
            sum += a2[i, j] * b2[i, j]
    for i in range(a3.shape[0]):
        for j in range(a3.shape[1]):
            sum += a3[i, j] * b3[i, j]
    for i in range(a4.shape[0]):
        for j in range(a4.shape[1]):
            sum += a4[i, j] * b4[i, j]
    return sum


def NNorma(r1, r2, r3, r4):
    e1 = np.linalg.norm(r1)
    e2 = np.linalg.norm(r2)
    e3 = np.linalg.norm(r3)
    e4 = np.linalg.norm(r4)
    return max(e1, e2, e3, e4)

# Проекционный метод IOM(m)

def IOM_m(m):
    # grid
    Nx = int(L_x / h_x) + 1
    Ny = int(L_y / h_y) + 1

    x = np.linspace(0, L_x, Nx)
    y = np.linspace(0, L_y, Ny)

    # initialization right part and initial approximation
    # 1:
    Ny_1 = int((Ny - 1) / 4) + 1
    Nx_1 = int(2 * (Nx - 1) / 5) + 1
    U_sub_1 = np.zeros((Ny_1, Nx_1))
    x_init_1 = U_sub_1.copy()
    # 2:
    Ny_2 = int((Ny - 1) / 4) + 1
    Nx_2 = int(4 * (Nx - 1) / 5) + 1
    U_sub_2 = np.zeros((Ny_2, Nx_2))
    x_init_2 = U_sub_2.copy()
    # 3:
    Ny_3 = int((Ny - 1) / 4) + 1
    Nx_3 = int(4 * (Nx - 1) / 5) + 1
    U_sub_3 = np.zeros((Ny_3, Nx_3))
    x_init_3 = U_sub_3.copy()
    # 4:
    Ny_4 = int((Ny - 1) / 4) + 1
    Nx_4 = int(2 * (Nx - 1) / 5) + 1
    U_sub_4 = np.zeros((Ny_4, Nx_4))
    x_init_4 = U_sub_4.copy()

    # filling in the area
    # First area
    for i in range(1, Ny_1):
        for j in range(1, Nx_1 - 1):
            U_sub_1[i][j] = func_f(x[int((Nx - 1) / 5) + j], y[Ny - 1 - i])
    for j in range(Nx_1):
        U_sub_1[0][j] = func_u(x[int((Nx - 1) / 5) + j], y[Ny - 1])
        x_init_1[0][j] = U_sub_1[0][j].copy()
    for i in range(Ny_1):
        U_sub_1[i][0] = func_u(x[int((Nx - 1) / 5)], y[Ny - 1 - i])
        x_init_1[i][0] = U_sub_1[i][0].copy()
    for i in range(Ny_1):
        U_sub_1[i][Nx_1 - 1] = func_u(x[int(3 * (Nx - 1) / 5)], y[Ny - 1 - i])
        x_init_1[i][Nx_1 - 1] = U_sub_1[i][Nx_1 - 1].copy()

    # Second area
    for i in range(Ny_2):
        for j in range(1, Nx_2):
            U_sub_2[i][j] = func_f(x[j], y[int(3 * (Ny - 1) / 4) - i])
    for j in range(int((Nx - 1) / 5) + 1):
        U_sub_2[0][j] = func_u(x[j], y[int(3 * (Ny - 1) / 4)])
        x_init_2[0][j] = U_sub_2[0][j].copy()
    for i in range(Ny_2):
        U_sub_2[i][0] = func_u(x[0], y[int(3 * (Ny - 1) / 4) - i])
        x_init_2[i][0] = U_sub_2[i][0].copy()
    for j in range(int((Nx - 1) / 5) + 1):
        U_sub_2[Ny_2 - 1][j] = func_u(x[j], y[int(2 * (Ny - 1) / 4)])
        x_init_2[Ny_2 - 1][j] = U_sub_2[Ny_2 - 1][j].copy()
    for j in range(int((Nx - 1) / 5) + 1):
        U_sub_2[0][j + int(3 * (Nx_2 - 1) / 4)] = func_u(x[int(3 * (Nx - 1) / 5) + j], y[int(3 * (Ny - 1) / 4)])
        x_init_2[0][j + int(3 * (Nx_2 - 1) / 4)] = U_sub_2[0][j + int(3 * (Nx_2 - 1) / 4)].copy()
    for i in range(int(Ny_2)):
        U_sub_2[i][Nx_2 - 1] = func_u(x[int(4 * (Nx - 1) / 5)], y[int(3 * (Ny - 1) / 4) - i])
        x_init_2[i][Nx_2 - 1] = U_sub_2[i][Nx_2 - 1].copy()

    # Third area
    for i in range(Ny_3):
        for j in range(1, Nx_3 - 1):
            U_sub_3[i][j] = func_f(x[j + int((Nx - 1) / 5)], y[int(2 * (Ny - 1) / 4) - i])
    for i in range(Ny_3):
        U_sub_3[i][0] = func_u(x[int((Nx - 1) / 5)], y[int(2 * (Ny - 1) / 4) - i])
        x_init_3[i][0] = U_sub_3[i][0].copy()
    for j in range(Ny_3):
        U_sub_3[Ny_3 - 1][j] = func_u(x[int((Nx - 1) / 5) + j], y[int((Ny - 1) / 4)])
        x_init_3[Ny_3 - 1][j] = U_sub_3[Ny_3 - 1][j].copy()
    for j in range(Ny_3):
        U_sub_3[Ny_3 - 1][j + int(3 * (Nx_3 - 1) / 4)] = func_u(x[int(4 * (Nx - 1) / 5) + j], y[int((Ny - 1) / 4)])
        x_init_3[Ny_3 - 1][j + int(3 * (Nx_3 - 1) / 4)] = U_sub_3[Ny_3 - 1][j + int(3 * (Nx_3 - 1) / 4)].copy()
    for i in range(Ny_3):
        U_sub_3[i][Nx_3 - 1] = func_u(x[Nx - 1], y[int(2 * (Ny - 1) / 4) - i])
        x_init_3[i][Nx_3 - 1] = U_sub_3[i][Nx_3 - 1].copy()
    for j in range(Ny_3):
        U_sub_3[0][j + int(3 * (Nx_3 - 1) / 4)] = func_u(x[int(4 * (Nx - 1) / 5) + j], y[int(2 * (Ny - 1) / 4)])
        x_init_3[0][j + int(3 * (Nx_3 - 1) / 4)] = U_sub_3[0][j + int(3 * (Nx_3 - 1) / 4)].copy()

    # fourth area
    for i in range(Ny_4):
        for j in range(1, Nx_4 - 1):
            U_sub_4[i][j] = func_f(x[int(2 * (Nx - 1) / 5) + j], y[int((Ny - 1) / 4) - i])
    for i in range(Ny_4):
        U_sub_4[i][0] = func_u(x[int(2 * (Nx - 1) / 5)], y[int((Ny - 1) / 4) - i])
        x_init_4[i][0] = U_sub_4[i][0].copy()
    for j in range(Nx_4):
        U_sub_4[Ny_4 - 1][j] = func_u(x[int(2 * (Nx - 1) / 5) + j], y[0])
        x_init_4[Ny_4 - 1][j] = U_sub_4[Ny_4 - 1][j].copy()
    for i in range(Ny_4):
        U_sub_4[i][Nx_4 - 1] = func_u(x[int(4 * (Nx - 1) / 5)], y[int((Ny - 1) / 4) - i])
        x_init_4[i][Nx_4 - 1] = U_sub_4[i][Nx_4 - 1].copy()

    k = 2  # количество векторов, к которым будет ортогонален очередной вектор

    mu1, mu2, mu3, mu4 = multA(x_init_1, x_init_2, x_init_3, x_init_4)

    # векторы начальных невязок
    r01 = U_sub_1 - mu1
    r02 = U_sub_2 - mu2
    r03 = U_sub_3 - mu3
    r04 = U_sub_4 - mu4

    iter = 0
    while NNorma(r01, r02, r03, r04) > eps:

        print(NNorma(r01, r02, r03, r04))

        # матрицы базисных векторов из пространства K
        V1 = np.zeros((Ny_1, (m + 1) * Nx_1))
        V2 = np.zeros((Ny_2, (m + 1) * Nx_2))
        V3 = np.zeros((Ny_3, (m + 1) * Nx_3))
        V4 = np.zeros((Ny_4, (m + 1) * Nx_4))

        # матрица коэффициентов ортогонализации
        H = np.zeros((m + 1, m))

        mu1, mu2, mu3, mu4 = multA(x_init_1, x_init_2, x_init_3, x_init_4)

        # векторы начальных невязок
        r01 = U_sub_1 - mu1
        r02 = U_sub_2 - mu2
        r03 = U_sub_3 - mu3
        r04 = U_sub_4 - mu4

        # нормы начальных невязок
        beta = NNorma(r01, r02, r03, r04)

        # первые базисные вектора пространства K
        V1[:, :Nx_1] = r01 / beta
        V2[:, :Nx_2] = r02 / beta
        V3[:, :Nx_3] = r03 / beta
        V4[:, :Nx_4] = r04 / beta

        for j in range(1, m + 1):
            # базисные вектора пространства L
            omega_j1, omega_j2, omega_j3, omega_j4 = multA(V1[:, (j - 1) * Nx_1: j * Nx_1],
                                                           V2[:, (j - 1) * Nx_2: j * Nx_2],
                                                           V3[:, (j - 1) * Nx_3: j * Nx_3],
                                                           V4[:, (j - 1) * Nx_4: j * Nx_4])
            for i in range(max(1, j - k + 1), j + 1):
                # вычисление коэффициентов орт-ции
                H[i - 1][j - 1] = Scalar(omega_j1, omega_j2, omega_j3, omega_j4,
                                         V1[:, (j - 1) * Nx_1: j * Nx_1],
                                         V2[:, (j - 1) * Nx_2: j * Nx_2],
                                         V3[:, (j - 1) * Nx_3: j * Nx_3],
                                         V4[:, (j - 1) * Nx_4: j * Nx_4])

                # ортогонализация очередных базисных векторов про-ва L
                omega_j1 = omega_j1 - H[i - 1][j - 1] * V1[:, (i - 1) * Nx_1: i * Nx_1]
                omega_j2 = omega_j2 - H[i - 1][j - 1] * V2[:, (i - 1) * Nx_2: i * Nx_2]
                omega_j3 = omega_j3 - H[i - 1][j - 1] * V3[:, (i - 1) * Nx_3: i * Nx_3]
                omega_j4 = omega_j4 - H[i - 1][j - 1] * V4[:, (i - 1) * Nx_4: i * Nx_4]

            # норма орт-го вектора
            H[j][j - 1] = NNorma(omega_j1, omega_j2, omega_j3, omega_j4)

            if abs(H[j][j - 1]) < 10 ** (-8):
                m = j
                break

            # вычисление следующих векторов про-ва K
            V1[:, j * Nx_1: (j + 1) * Nx_1] = omega_j1 / H[j][j - 1]
            V2[:, j * Nx_2: (j + 1) * Nx_2] = omega_j2 / H[j][j - 1]
            V3[:, j * Nx_3: (j + 1) * Nx_3] = omega_j3 / H[j][j - 1]
            V4[:, j * Nx_4: (j + 1) * Nx_4] = omega_j4 / H[j][j - 1]

        e_1 = np.zeros(m + 1)  # орт
        e_1[0] = 1
        g = beta * e_1  # вектор правой части вспопогательной СЛАУ
        H = np.c_[H, g]  # добавление к матрице системы правой части
        H = givens(H, m + 1)  # зануляем поддиагональ вращениями Гивенса
        g = H[:m, m]  # перезаписываем измененую правую часть
        H = np.delete(np.delete(H, m, 1), m, 0)  # удаляем вектор правой части из системы
        y = Gauss_back_step(H, g, m)  # обратный ход метода Гауса

        # Уточнение решения
        sumyivi1 = np.zeros((Ny_1, Nx_1))  # уточняющий вектор
        sumyivi2 = np.zeros((Ny_2, Nx_2))  # уточняющий вектор
        sumyivi3 = np.zeros((Ny_3, Nx_3))  # уточняющий вектор
        sumyivi4 = np.zeros((Ny_4, Nx_4))  # уточняющий вектор

        for f in range(1, m + 1):
            sumyivi1 += y[f - 1] * V1[:, (f - 1) * Nx_1: f * Nx_1]  # вычисление уточняющего вектора
            sumyivi2 += y[f - 1] * V2[:, (f - 1) * Nx_2: f * Nx_2]  # вычисление уточняющего вектора
            sumyivi3 += y[f - 1] * V3[:, (f - 1) * Nx_3: f * Nx_3]  # вычисление уточняющего вектора
            sumyivi4 += y[f - 1] * V4[:, (f - 1) * Nx_4: f * Nx_4]  # вычисление уточняющего вектора

        solution1 = x_init_1 + sumyivi1  # уточнение
        solution2 = x_init_2 + sumyivi2  # уточнение
        solution3 = x_init_3 + sumyivi3  # уточнение
        solution4 = x_init_4 + sumyivi4  # уточнение

        musol1, musol2, musol3, musol4 = multA(solution1, solution2, solution3, solution4)
        r01 = U_sub_1 - musol1  # вычисление вектора невязки
        r02 = U_sub_2 - musol2  # вычисление вектора невязки
        r03 = U_sub_3 - musol3  # вычисление вектора невязки
        r04 = U_sub_4 - musol4  # вычисление вектора невязки

        x_init_1 = solution1.copy()
        x_init_2 = solution2.copy()
        x_init_3 = solution3.copy()
        x_init_4 = solution4.copy()
        iter += 1

    return NNorma(r01, r02, r03, r04), iter


print("***********************IOM(m)***********************")
ts = time.time()
nev, tr = IOM_m(100)
tf = time.time()
print("Невязка = ", nev)
print("Итераций = ", tr)
print('Время = ', tf - ts)
