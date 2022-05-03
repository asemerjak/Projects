
class Matrix:
    def __init__(self, arg):
        if isinstance(arg, tuple):
            self.rows, self.cols = arg
            self.m = [[]]
            self.param = 0
            self.m = [[self.param for r in range(self.cols)] for c in range(self.rows)]
        else:
            self.rows = len(arg)
            self.cols = len(arg[0])
            self.m = arg

    def __add__(self, other):
        if self.rows == other.rows and self.cols == other.cols:
            added_matrix = [[self.m[r][c] + other.m[r][c] for c in range(self.cols)] for r in range(self.rows)]
            return Matrix(added_matrix)
        else:
            raise ValueError("Wrong matrix sizes!")

    def __mul__(self, other):
        if self.cols == other.rows:
            multiplied_matrix = [[0 for r in range(other.cols)] for c in range(self.rows)]
            for r1 in range(self.rows):
                for c2 in range(other.cols):
                    temp = 0
                    for r2 in range(other.rows):
                        temp = temp + self.m[r1][r2] * other.m[r2][c2]
                    multiplied_matrix[r1][c2] = temp
            return Matrix(multiplied_matrix)
        else:
            raise ValueError("Wrong matrix sizes!")

    def __getitem__(self, item):
        return self.m[item]

    def __str__(self):
        matrix_str = ''
        for row in range(self.rows):
            matrix_str = matrix_str + str(self.m[row]) + '\n'
        return matrix_str

    def change_rows(self, r1, r2):
        temp = self.m[r1]
        self.m[r1] = self.m[r2]
        self.m[r2] = temp


    def chio(self, matrix):

        if matrix[0][0] == 0:
            for i in range(matrix.rows):
                if matrix[i][0] != 0:
                    matrix.change_rows(i, 0)

        if matrix.rows > 1 and matrix.rows == matrix.cols:
            new_matrix = [[(matrix[0][0] * matrix[i+1][j+1] - matrix[0][j+1] * matrix[i+1][0]) for j in range(matrix.cols-1)] for i in range(matrix.rows-1)]
            if matrix.rows > 2:
                return 1/(matrix[0][0]**(matrix.rows-2)) * self.chio(Matrix(new_matrix))
            else:
                return 1/(matrix[0][0]**(matrix.rows-2)) * new_matrix[0][0]
        elif matrix.rows != matrix.cols:
            raise ValueError("Wrong matrix size!")


def transpose(matrix):
    transposed_matrix = [[matrix[row][col] for row in range(matrix.rows)] for col in range(matrix.cols)]
    return Matrix(transposed_matrix)


matrix1 = Matrix([[1, 0, 2], [-1, 3, 1]])
matrix1_transposed = transpose(matrix1)
print("Macierz1:")
print(matrix1)
print("Macierz1 po transpozycji:")
print(matrix1_transposed)

matrix2 = Matrix([[-1, 3, 1], [1, 0, 2]])
print("Macierz2:")
print(matrix2)
print("Macierz1 + Macierz2 = ")
print(matrix1 + matrix2)

matrix3 = Matrix([[3, 1], [2, 1], [1, 0]])
print("Macierz3:")
print(matrix3)
print("Macierz1 * Macierz3 =")
print(matrix1 * matrix3)


matrix4 = Matrix([
[5, 1, 1, 2, 3],
[4, 2, 1, 7, 3],
[2, 1, 2, 4, 7],
[9, 1, 0, 7, 0],
[1, 4, 7, 2, 2]])

print("Macierz4:")
print(matrix4)
print("wyznacznik macierzy4 =", matrix4.chio(matrix4))

matrix5 = Matrix([
     [0, 1, 1, 2, 3],
     [4, 2, 1, 7, 3],
     [2, 1, 2, 4, 7],
     [9, 1, 0, 7, 0],
     [1, 4, 7, 2, 2]])
#rozwiązanie problemu (czyli a11=0) polega na zamianie miejscami wiersza pierwszego i innego, którego pierwszy wyraz jest niezerowy.
#w tym celu została stworzona pomocnicza metoda change_rows
print("\nMacierz5:")
print(matrix5)
print("wyznacznik macierzy5 =", matrix5.chio(matrix5))
