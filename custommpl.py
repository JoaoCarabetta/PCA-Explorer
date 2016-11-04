#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4.uic import loadUiType
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import itertools

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import PCA

Ui_MainWindow, QMainWindow = loadUiType('window.ui')

        
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, data):
        super(Main, self).__init__()
        self.setupUi(self)
        self.fig_dict = {}
        self.perguntas_dict = {}
        self.data = data
        self.question_id = -1

        # click Perguntas
        self.mplfigs.itemClicked.connect(self.update_pessoa) # when clicked, change plot
        # click Pessoa
        # on click function
        self.mplfigs_2.cellClicked.connect(self.update_correlacao)

        fig = Figure()
        self.add_plot(fig)



    # ----------------------
    # PERGUNTA TABLE METHODS
    def addpergunta(self, id, name): # add perguntas
        name = name.decode('utf-8')
        self.perguntas_dict[name] = id # add item to perguntas dict, name as key and id as value
        self.mplfigs.addItem(name) # add item to mplfigs

    # ----------------------
    # ----------------------
    # PESSOA TABLE METHODS
    def init_pessoa(self):

        # set table
        row_count = len(self.data.index)
        self.mplfigs_2.setRowCount(row_count)
        self.mplfigs_2.setColumnCount(2)

        # set header
        self.mplfigs_2.setHorizontalHeaderLabels(QString("id;resposta;").split(";"))


    def update_pessoa(self, question):

        # access perguntas dict and get question_id based on click
        try:
            question = question.text()
            question = unicode(question) # to text
        except AttributeError:
            question = question
        question_id = str(self.perguntas_dict[question])
        self.question_id = question_id

        # add data inside table
        data_column = self.data[question_id]
        votos_dict = {'sim': [], 'nao': [], 'nulo': []}
        for i, d in enumerate(data_column):
            self.mplfigs_2.setItem(i, 0, QTableWidgetItem("{}".format(i)))
            self.mplfigs_2.setItem(i, 1, QTableWidgetItem("{}".format(d)))

            if d == 1:
                votos_dict['sim'].append(i)
            elif d == -1:
                votos_dict['nao'].append(i)
            elif d == 0:
                votos_dict['nulo'].append(i)

        self.changefig(self.data, votos_dict)

    # ----------------------
    # CORRELACAO TABLE
    def init_correlacao(self, data):

        # set table
        row_count = len(data.index) - 1
        self.mplfigs_3.setRowCount(row_count)
        self.mplfigs_3.setColumnCount(3)

        # set header
        self.mplfigs_3.setHorizontalHeaderLabels(QString("id; conc; disc;").split(";"))

    def update_correlacao(self, row, col):
        person_id = row
        data_plot = PCA.get_oposition(self.data, self.question_id, person_id)
        self.init_correlacao(data_plot)
        self.changefig(data_plot, person_id)

        self.person = self.data.loc[self.data['participant'] == person_id].drop('participant', axis=1)
        self.person =  map(list, self.person.values) # to list

        ordered_data, name = self.treat_data(data_plot)

        print ordered_data

        self.others = data_plot['participant'].tolist()
        self.size = len(self.data.index)
        for i, o in enumerate(self.others):

            other = self.data.loc[self.data['participant'] == o]
            id = other['participant'].values
            print id
            other = other.drop('participant', axis=1)
            other =  map(list, other.values)


            both_sim, both_nao, both_nulo = 0, 0, 0
            for pair in itertools.izip(self.person[0], other[0]):
                if pair == (1.0, 1.0):
                    both_sim += 1
                elif pair == (0.0, 0.0):
                    both_nulo += 1
                if pair == (-1.0, -1.0):
                    both_nao += 1


            self.sim =  both_sim +  both_nao + both_nulo

            self.nao =  self.size - self.sim

            print self.sim, self.nao

            self.mplfigs_3.setItem(i, 0, QTableWidgetItem("{}".format(id[0])))
            self.mplfigs_3.setItem(i, 1, QTableWidgetItem("{}".format(self.sim)))
            self.mplfigs_3.setItem(i, 2, QTableWidgetItem("{}".format(self.nao)))



        # ----------------------
    # PLOT METHODS
    def changefig(self, data_plot, person_id=-1):  # change plot func

        self.remove_plot()  # clear plot
        fig = self.PCA_plot(data_plot, person_id) # get plot info
        self.add_plot(fig)  # add plot


    def add_plot(self, fig): # add plot
        self.canvas = FigureCanvas(fig) # put matplot fig
        self.mplvl.addWidget(self.canvas) # create widget mplvl space
        self.canvas.draw() # draw canvas
        self.toolbar = NavigationToolbar(self.canvas, # create toolbar
                self.mplwindow, coordinates=True)
        self.mplvl.addWidget(self.toolbar) # add toolbar


    def remove_plot(self, ): # clear cnavas
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()

    def treat_data(self, data):

        

        data, name = data.drop(['participant'], axis=1).as_matrix(), data['participant'].tolist()
        data = PCA.PCA(data)  # PCA it

        return data, name

    def PCA_plot(self, data_plot, evidence=-1):

        # treat data
        data, name = self.treat_data(data_plot)


        # Plot init
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(111)

        # data
        blue, = self.ax1.plot(data[:, 0], data[:, 1], 'o', markersize=7, color='blue', alpha=0.5)
        if evidence != -1: # evidence data
            if isinstance(evidence, dict):
                for e in evidence['nao']:
                    index = name.index(e)
                    red, = self.ax1.plot(data[index, 0], data[index, 1], 'o', markersize=7, color='red', alpha=0.5)
                for e in evidence['nulo']:
                    index = name.index(e)
                    yellow, = self.ax1.plot(data[index, 0], data[index, 1], 'o', markersize=7, color='y', alpha=0.5)
                if not(len(evidence['nao']) == 0 or len(evidence['nulo']) == 0):
                    self.ax1.legend([blue, red, yellow], ['sim', 'nao', 'nulo']) # legenda

            else:
                index = name.index(evidence)
                self.ax1.plot(data[index, 0], data[index, 1], 'o', markersize=7, color='red', alpha=0.5)


        # annotations
        for i, txt in enumerate(name):
            self.ax1.annotate(txt, (data[i, 0], data[i, 1]))
        self.extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
        if evidence == -1 or isinstance(evidence, dict):
            self.ax1.annotate("PCA Geral", xy=(0.05, 0.95), xycoords='axes fraction',
                       fontsize=14)
        else:
            self.ax1.annotate("Sujeito {}".format(evidence), xy=(0.05, 0.95), xycoords='axes fraction',
                              fontsize=14)

        return self.fig


def read_perguntas(path):

    data = pd.read_csv(path)

    return data['comment-id'].tolist(), data['comment-body'].tolist()


if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    from matplotlib.patches import Rectangle
    import pandas as pd

    print 'Up and Running'
    print 'Wait a bit...'

    #DataImports
    data = PCA.import_data("./data/participants-votes.csv")


    app = QtGui.QApplication(sys.argv)
    main = Main(data)

    #addFigures
    main.changefig(data) # start with full PCA

    #initPerguntas
    id, name = read_perguntas("./data/comments.csv")
    for i in range(len(id)):
        main.addpergunta(id[i], name[i])

    # init Pessoa Table
    main.init_pessoa()

    main.show()
    print  'Go!'


    sys.exit(app.exec_())

