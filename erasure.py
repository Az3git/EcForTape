import matrix
import field
import random
import lto

# create GF(2^4)
gf = field.BinaryFiniteField(4)

# create generation matrix for n = 6, k = 4 on GF(2^4)
k = 4
n = 6
gener_matr = matrix.Generation_matrix().generation(gf, 4, 6)


# create simple random data size of q*520 bytes
q = 6
data = []

for i in range(520*q):
    data.append(random.randint(0, 15))
data_matrix = []
stripe_size = len(data)/4
matrix_stripe = []

i = 0
j = 0
while i < len(data):
    while j < stripe_size:
        matrix_stripe.append(data[i])
        i = i + 1
        j = j + 1
    data_matrix.append(matrix_stripe)
    matrix_stripe = []
    j = 0

disk0 = lto.Lto(0)
disk1 = lto.Lto(1)
disk2 = lto.Lto(2)
disk3 = lto.Lto(3)
disk4 = lto.Lto(4)
disk5 = lto.Lto(5)




# encode data of the data node
vector = matrix.Matrix(k,1,gf)

for i in range(int(stripe_size)):
    message = [data_matrix[k-4][i],data_matrix[k-3][i],data_matrix[k-2][i],data_matrix[k-1][i]]
    for j in range(k):
        vector.set_element(j, 0, message[j])
    encode = gener_matr.multiply(vector)
    disk0.append(encode.get_element(n-6,0))
    disk1.append(encode.get_element(n-5,0))
    disk2.append(encode.get_element(n-4,0))
    disk3.append(encode.get_element(n-3, 0))
    disk4.append(encode.get_element(n-2, 0))
    disk5.append(encode.get_element(n-1, 0))



# Checking for the end
disk_check = disk5


# Imagine, that disk1 and disk5 crush


# Recover input data
invert = gener_matr.submatrix([1,5],[]).invert()

surv_mess = matrix.Matrix(6,1,gf)

stripe0 = []
stripe1 = []
stripe2 = []
stripe3 = []

data_recover = []

for i in range(int(q*520/k)):
    surv_mess.set_element(0,0,disk0[i])
    surv_mess.set_element(1,0,disk1[i])
    surv_mess.set_element(2,0, disk2[i])
    surv_mess.set_element(3,0, disk3[i])
    surv_mess.set_element(4,0, disk4[i])
    surv_mess.set_element(5,0, disk5[i])
    decode = invert.multiply(surv_mess.submatrix([1,5],[]))
    stripe0.append(decode.get_element(0,0))
    stripe1.append(decode.get_element(1,0))
    stripe2.append(decode.get_element(2,0))
    stripe3.append(decode.get_element(3,0))


data_recover = stripe0 + stripe1 + stripe2 + stripe3

print(data==data_recover)

# recover fails disk
# Disk 1 recover in last step

disk5.append(stripe1)

# for recover D5 replai

for i in range(int(stripe_size)):
    message = [stripe0[i], stripe1[i],stripe2[i],stripe3[i]]
    for j in range(k):
        vector.set_element(j, 0, message[j])
    encode = gener_matr.multiply(vector)
    disk5.append(encode.get_element(n-1, 0))

print(disk5==disk_check)