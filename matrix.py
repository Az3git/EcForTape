import field


class Matrix:
    """A matrix with elements in a 2^n finite field."""

    def __init__(self, num_rows, num_cols, field):
        self.field_ = field
        self.elements_ = [[0] * num_cols for i in range(num_rows)]

    def num_rows(self):
        return len(self.elements_)

    def num_cols(self):
        return len(self.elements_[0])

    def get_element(self, i, j):
        return self.elements_[i][j]

    def set_element(self, i, j, value):
        self.elements_[i][j] = self.field_.validated(value)

    def display(self):
        for row in self.elements_:
            print(row)


    def submatrix(self, excluded_rows, excluded_cols):
        sub_num_rows = self.num_rows() - len(excluded_rows)
        sub_num_cols = self.num_cols() - len(excluded_cols)
        result = Matrix(sub_num_rows, sub_num_cols, self.field_)
        i = 0
        for r in range(self.num_rows()):
            if r in excluded_rows:
                continue
            j = 0
            for c in range(self.num_cols()):
                if c in excluded_cols:
                    continue
                result.set_element(i, j, self.get_element(r, c))
                j = j + 1
            i = i + 1
        return result

    def det(self):
        assert self.num_rows() == self.num_cols()

        if self.num_rows() == 1:
            return self.get_element(0, 0)

        result = 0
        for c in range(self.num_cols()):
            x = self.field_.multiply(
                self.get_element(0, c), self.submatrix([0], [c]).det())
            if c % 2 == 1:
                x = self.field_.negate(x)
            result = self.field_.add(result, x)
        return result

    def cofactors(self):
        assert self.num_rows() == self.num_cols()

        result = Matrix(self.num_rows(), self.num_cols(), self.field_)
        for r in range(self.num_rows()):
            for c in range(self.num_cols()):
                result.set_element(r, c, self.submatrix([r], [c]).det())
                if (r + c) % 2 == 1:
                    result.set_element(
                        r, c, self.field_.negate(result.get_element(r, c)))
        return result

    def transpose(self):
        assert self.num_rows() == self.num_cols()

        result = Matrix(self.num_rows(), self.num_cols(), self.field_)
        for r in range(self.num_rows()):
            for c in range(self.num_cols()):
                result.set_element(r, c, self.get_element(c, r))
        return result

    def scale(self, factor):
        assert self.num_rows() == self.num_cols()

        result = Matrix(self.num_rows(), self.num_cols(), self.field_)
        for r in range(self.num_rows()):
            for c in range(self.num_cols()):
                result.set_element(r, c, self.field_.multiply(
                    self.get_element(r, c), factor))
        return result

    def invert(self):
        return self.cofactors().transpose().scale(
            self.field_.invert(self.det()))

    def multiply(self, B):
        assert self.num_cols() == B.num_rows()

        result = Matrix(self.num_rows(), B.num_cols(), self.field_)
        for r in range(self.num_rows()):
            for c in range(B.num_cols()):
                for i in range(self.num_cols()):
                    result.set_element(r, c, self.field_.add(
                        result.get_element(r, c), self.field_.multiply(
                            self.get_element(r, i), B.get_element(i, c))))
        return result



class Generation_matrix:
    def __init__(self):
        self.field = field


    def generation(self, field, k = 4, n = 6 ):
        print(k, n)
        x = [1, 2]
        y = [3, 4, 5, 6]
        gener_matr = Matrix(n, k, field)
        for i in range(k):
            gener_matr.set_element(i, i, 1)
        for i in range(n - k):
            for j in range(k):
                gener_matr.set_element(i + 4, j, field.divide(1, field.add(x[i], y[j])))
        return gener_matr
