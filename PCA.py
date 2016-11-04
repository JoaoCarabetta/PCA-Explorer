from sklearn.decomposition import PCA as sklearnPCA
from matplotlib import pyplot as plt
import pandas as pd

def import_data(path):

    data = pd.read_csv(path) # read from file

    data = data.sort_values(by='participant')
    del data['group-id']
    del data['n-comments']
    del data['n-votes']
    del data['n-agree']
    del data['n-disagree']

    data = data.fillna(value=0)
    #data = data.as_matrix() # transform into a numpy matrix



    return data


def get_oposition(data, comment='10', id_original=1):

    resposta_original =  data[comment].iloc[id_original]

    resposta_contraria = resposta_original * -1

    outdata = data.loc[data[comment] == resposta_contraria]

    outdata = outdata.append(data.iloc[id_original])

    del outdata[comment]

    return outdata


def PCA(data):

    sklearn_pca = sklearnPCA(n_components=2)
    sklearn_transf = sklearn_pca.fit_transform(data)

    return sklearn_transf


def plot(sklearn_transf):

    plt.plot(sklearn_transf[:-2,0],sklearn_transf[:-2,1], 'o', markersize=7, color='blue', alpha=0.5)
    plt.plot(sklearn_transf[-1,0],sklearn_transf[-1,1], 'o', markersize=7, color='red', alpha=0.5)
    plt.xlabel('x_values')
    plt.ylabel('y_values')

    plt.legend()
    plt.title('Transformed samples with class labels from matplotlib.mlab.PCA()')

    plt.show()

if __name__ == '__main__':
    data = import_data("./data/participants-votes.csv")

    outdata = get_oposition(data)

    pca = PCA(outdata)

    plot(pca)


