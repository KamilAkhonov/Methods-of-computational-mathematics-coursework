import numpy as np
import time
import numpy.linalg as lin
import pandas as pd

L_x = 2
L_y = 1
h_x = 0.1
h_y = 0.1
eps = 10 ** (-8)

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
            return 0
        case 2:
            return -2
        case 3:
            return -1 * np.exp(
                (np.sin(x)) ** 2 + (np.cos(y)) ** 2) * \
                   ((np.sin(2 * x)) ** 2 + 2 * np.cos(
                       2 * x) + np.sin(2 * y) -
                    2 * np.cos(2 * y))


# Метод простой итерации(Якоби)
def Cross_Jac(f, h_1, h_2, y0, ep):
    tic = time.perf_counter()
    C_0 = (0.5 * (h_1 ** 2) * (h_2 ** 2)) / (
            h_1 ** 2 + h_2 ** 2)
    C_1 = (0.5 * (h_1 ** 2)) / (h_1 ** 2 + h_2 ** 2)
    C_2 = (0.5 * (h_2 ** 2)) / (h_1 ** 2 + h_2 ** 2)
    Nx = int(L_x / h_1) + 1
    Ny = int(L_y / h_2) + 1
    U = np.zeros((Ny, Nx))
    U_m = np.zeros((Ny, Nx))
    x = np.linspace(0, L_x, Nx)
    y = np.linspace(0, L_y, Ny)
    X, Y = np.meshgrid(x, y)
    Z = func_u(X, Y)

    # Заполняем начальное приближение с учетом нач.условий
    for i in range(0, Ny):
        for j in range(0, Nx):
            U[i][j] = y0(x[j], 0)
    for i in range(0, Nx):  # y = 1
        U[Ny - 1][i] = y0(x[i], L_y)
    for i in range(0, Ny):  # x = 1
        U[i][Nx - 1] = y0(L_x, y[i])
    for i in range(0, Ny):  # x = 0
        U[i][0] = y0(0, y[i])

    norm = 1
    k = 0
    for i in range(0, Ny):
        for j in range(0, Nx):
            U_m[i][j] = y0(x[j], 0)
    for i in range(0, Nx):  # y = 1
        U_m[Ny - 1][i] = y0(x[i], L_y)
    for i in range(0, Ny):  # x = 1
        U_m[i][Nx - 1] = y0(L_x, y[i])
    for i in range(0, Ny):  # x = 0
        U_m[i][0] = y0(0, y[i])

    while norm > ep:

        for i in range(Nx - 2, 0, -1):
            for j in range(1, Ny - 1):
                U_m[j][i] = C_0 * f(x[i], y[j]) + C_1 * (
                        U[j - 1][i] + U[j + 1][
                    i]) + C_2 * (U[j][i - 1] + U[j][
                    i + 1])
        norm = np.max(np.abs(U_m - U))
        k += 1
        # print(k)
        for i in range(0, Ny):
            for j in range(0, Nx):
                U[i][j] = U_m[i][j]
        print(norm)


    toc = time.perf_counter()
    tme = round(toc - tic, 4)
    print("Время = ", tme)
    print("Погрешность с точным решением: ", lin.norm(Z - U_m))
    print("Количество итераций = ", k)
    return U_m


print("***********************Jacobi***********************")


sol = Cross_Jac(func_f, h_x, h_y, func_u, eps)


# Точное решение
def solve_of_task(U):
    trsol = np.zeros((N_x + 1, N_y + 1))
    for i in range(N_x+1):
        for j in range(N_y + 1):
            trsol[i][j] = U(i*h_x, j*h_y)
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


# произведение матрицы системы A на произвольный массив p
def multA(p):
    Ap = np.copy(p)
    for i in range(1, Ap.shape[0] - 1):
        for j in range(1, Ap.shape[1] - 1):
            Ap[i][j] = -1 * ((p[i - 1][j] - 2 * p[i][j] + p[i + 1][j]) / h_x ** 2 + (
                    p[i][j - 1] - 2 * p[i][j] + p[i][j + 1]) / h_y ** 2)
    return Ap


# скалярное произведение вектор-матриц
def Scr(a, b):
    sum = 0
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            sum += a[i][j] * b[i][j]
    return sum


N_x = int(L_x / h_x)
N_y = int(L_x / h_x)
# задание правой части
B2 = np.zeros((N_x + 1, N_y + 1))
for i in range(N_y + 1):
    B2[0][i] = func_u(0 * h_x, i * h_y)
    B2[N_x][i] = func_u(N_x * h_x, i * h_y)
for i in range(N_x + 1):
    B2[i][0] = func_u(i * h_x, 0 * h_y)
    B2[i][N_y] = func_u(i * h_x, N_y * h_y)
for i in range(1, N_x):
    for j in range(1, N_y):
        B2[i][j] = func_f(i * h_x, j * h_y)


# Проекционный метод IOM(m)

def IOM_m(vec_b, m):
    solution = np.zeros((N_x + 1, N_y + 1))
    k = 1  # количество векторов, к которым будет ортогонален очередной вектор
    x0 = np.zeros((N_x + 1, N_y + 1))  # Начальное приближение
    # задание краевых значений
    for ik in range(N_y + 1):
        x0[0][ik] = func_u(0 * h_x, ik * h_y)
        x0[N_x][ik] = func_u(N_x * h_x, ik * h_y)
    for jk in range(N_x + 1):
        x0[jk][0] = func_u(jk * h_x, 0 * h_y)
        x0[jk][N_y] = func_u(jk * h_x, N_y * h_y)


    r0 = vec_b - multA(x0)  # вектор начальной невязки
    count_iter = 0
    while abs(lin.norm(r0)) > eps:
        V = np.zeros((N_x + 1, (m + 1) * (N_y + 1)))  # матрица базисных векторов из пространства K
        H = np.zeros((m + 1, m))  # матрица коэффициентов ортогонализации
        r0 = vec_b - multA(x0)  # вектор начальной невязки
        beta = lin.norm(r0)  # норма начальной невязки
        V[:, :N_y + 1] = r0 / beta  # первый базисный вектор пространства K
        for j in range(1, m + 1):
            omega_j = multA(V[:, (j - 1) * (N_y + 1): j * (N_y + 1)])  # базисный вектор пространства L
            for i in range(max(1, j - k + 1), j + 1):
                H[i - 1][j - 1] = Scr(omega_j,
                                      V[:, (i - 1) * (N_y + 1): i * (N_y + 1)])  # вычисление коэффициента орт-ции
                omega_j = omega_j - H[i - 1][j - 1] * V[:, (i - 1) * (N_y + 1): i * (
                        N_y + 1)]  # орт-ция очередного базисного вектора про-ва L
            H[j][j - 1] = lin.norm(omega_j)  # норма орт-го вектора
            if abs(H[j][j - 1]) < 10 ** (-8):
                m = j
                break
            V[:, j * (N_y + 1): (j + 1) * (N_y + 1)] = omega_j / H[j][j - 1]  # вычисление следующего вектора про-ва K
        e_1 = np.zeros(m + 1)  # орт
        e_1[0] = 1
        g = beta * e_1  # вектор правой части вспопогательной СЛАУ
        H = np.c_[H, g]  # добавление к матрице системы правой части
        H = givens(H, m + 1)  # зануляем поддиагональ вращениями Гивенса
        g = H[:m, m]  # перезаписываем измененую правую часть
        H = np.delete(np.delete(H, m, 1), m, 0)  # удаляем вектор правой части из системы
        y = Gauss_back_step(H, g, m)  # обратный ход метода Гауса
        # Уточнение решения
        sumyivi = np.zeros((N_x + 1, N_y + 1))  # уточняющий вектор
        for f in range(1, m + 1):
            sumyivi += y[f - 1] * V[:, (f - 1) * (N_y + 1): f * (N_y + 1)]  # вычисление уточняющего вектора
        solution = x0 + sumyivi  # уточнение
        r0 = vec_b - multA(solution)  # вычисление вектора начальной невязки
        x0 = solution  # изменение начального приближения
        # print(lin.norm(r0))
        count_iter += 1
    return solution, count_iter


print("***********************projection***********************")
ts = time.time()
lol, ver = IOM_m(B2, 3)
tf = time.time()
sol_anal = solve_of_task(func_u)
print('Время = ', tf - ts)
print('Погрешность с точным решением: = ', lin.norm(sol_anal - lol))
print('Количество итераций = ', ver)








