def matrix_size(matrix_name):
    while True:
        try:
            print('Matrix {}: '.format(matrix_name))
            width = int(input('Width (columns): '))
            height = int(input('Height (rows): '))
            if width < 1 or height < 1:
                raise SyntaxError('No valid size of matrix.')
            else:
                return width, height
        except ValueError:
            print("Please enter integers.")


def matrix_input(matrix_name, width, height):
    print('Input matrix {}: '.format(matrix_name))
    matrix = []
    for i in range(0, height):
        row = input()
        if len(row.split()) != width:
            raise Exception(
                'Width of row must be same as width of matrix. {} numbers in row are required.'.format(width))
        matrix.append([float(j) for j in row.split()])
    return matrix


def multiplication(first, second):
    return [[sum(a * b for a, b in zip(X_row, Y_col)) for Y_col in zip(*second)] for X_row in first]


if __name__ == '__main__':
    first_m = 'A'
    second_m = 'B'
    width_a, height_a = matrix_size(first_m)
    width_b, height_b = matrix_size(second_m)

    if width_a != height_b:
        raise Exception(
            'Height of matrix B must be same as width of matrix A. The width of matrix A was: {}'.format(width_a))

    matrix_a = matrix_input(matrix_name=first_m, width=width_a, height=height_a)
    matrix_b = matrix_input(matrix_name=second_m, width=width_b, height=height_b)
    result = multiplication(matrix_a, matrix_b)

    print("Result: ")
    for r in result:
        print(r)
