import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster
from skimage import io

# CITIREA IMAGINII
img = io.imread('4.2.06.tiff')
originShape = img.shape

# REARANJAREA PIXELILOR
clust = np.reshape(img, [-1,3])
# Stim ca pentru metoda fit_predict datele trebuie sa vina in format N X M (N esantioane a cate M trasaturi)
# Fiecare pixel este descris de un triplet RGB, deci 3 trasaturi. Functia np.reshape va rearanja pixelii
# astfel incat cele 3 coloane sa fie valorile de rosu, verde si albastru ale fiecarui pixel.
# Valoarea -1 ii spune functiei sa calculeze de cate linii are nevoie, astfel incat noua forma sa fie 
# compatibila cu cea veche

# CLUSTERING SI VIZUALIZARE
km = cluster.KMeans(n_clusters = 10, n_init=20, max_iter = 20)
labels = km.fit_predict(clust)
plt.figure()
plt.scatter(clust[:,1],clust[:,2],c=km.cluster_centers_[labels,:]/255)
plt.scatter(km.cluster_centers_[:,1],km.cluster_centers_[:,2])
# Avand date 3D (R,G si B) nu se pot afisa toate trasaturile intr-un grafic 2D, astfel ca s-a ales
# afisarea valorilor de verde si albastru pentru fiecare pixel. Cu alte modificari asupra codului,
# Matplotlib poate afisa si grafice 3D.
    
# REFACEREA IMAGINII CU NOILE CULORI SI AFISAREA EI
segmentedImg = km.cluster_centers_[np.reshape(labels, img.shape[:2])]
plt.figure()
plt.imshow(segmentedImg/255)
plt.show()