import matplotlib.pyplot as plt
from sklearn import cluster #Vẽ biểu đồ
from sklearn.cluster import KMeans
import numpy

#Doc buc anh 
img = plt.imread("a.jpg")

#Tim chieu dai chieu rong
#Chieu dai chieu rong la 1 tuple
width = img.shape[0]
height = img.shape[1]

#lam lai buc anh thanh bi
img = img.reshape(width*height,3)


#Thuat toan KMeans
kmeans = KMeans(n_clusters=4).fit((img))
labels = kmeans.predict(img)
clusters = kmeans.cluster_centers_

#Tao anh moi giong img
# img2 = numpy.zeros_like(img)

#Gan mau
# for i in range(len(img2)):
#     img2[i] = clusters[labels[i]]

#Khoi phuc lai anh co 3 chieu nhu cu hrhykuukm
# img2 = img2.reshape(width,height,3)


#Cach2
index = 0
img2 = numpy.zeros((width,height,3),dtype=numpy.uint8)
for i in range(width):
    for j in range(height):
        label_of_pixel = labels[index]
        img2[i][j] = clusters[label_of_pixel]
        index += 1
#Ve lai buc anh 
plt.imshow(img2)
plt.show()