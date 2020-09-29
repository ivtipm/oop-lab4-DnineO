#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, QtCore

import csv
import os
from PyQt5.Qt import *
from database import mydatabase 

class MainWindow(QMainWindow):
    ''' A class used to represent main window

    Attributes
    ----------
    mydatabase : mydatabase
        instance of the class mydatabase
    table : QTableWidget
        table for displaying data from database

    Methods
    -------
    initUI
        Initializes user interface
    loaddb(grid_layout)
        Loads database and display it in table
    createdb(grid_layout,colnumber,valuelist)
        Creates new database and display it in table
    displaytable(grid_layout,colnumber,rownumber,data)
        Displays data in table
    savefile
        Saves data in csv file
    requesteditrow(grid_layout)
        Asks user to input data for editing cell
    requaestdelrow(grid_layout)
        Asks user to input data for deleting row
    requestaddrow(grid_layout)
        Asks user to input data for adding row
    askforsearch
        Asks user to input data for finding row
    openfilename
        Asks user to select file for opening
    savefilepath
        Asks user to select file for saving
    requestcolnumber(grid_layout)
        Asks user to input data for creating new database
    showabout
        Shows message with information about developer
    on_cell_item_clicked(item)
        Allows user to edit cell by double clicking on cell's item
    showmessage(title,text)
        Shows  message box with given title and text
    '''

    def __init__(self):
        super().__init__()
        self.table = QTableWidget()  # Создаём таблицу
        self.table.itemDoubleClicked.connect(self.on_cell_item_clicked)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.initUI()


    def initUI(self):
        '''Initializes user interface
        '''

        central_widget = QWidget(self)                  # Создаём центральный виджет
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет

        grid_layout = QGridLayout()             # Создаём QGridLayout
        central_widget.setLayout(grid_layout)   # Устанавливаем данное размещение в центральный виджет
        
         

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit from application')
        exitAction.setIcon(QIcon('exit.svg'))
        exitAction.triggered.connect(self.close)

        loadAction = QAction('Load',self)
        loadAction.setShortcut('Ctrl+O')
        loadAction.setStatusTip('Load database from cvs file')
        loadAction.setIcon(QIcon('load.svg'))
        loadAction.triggered.connect(lambda: self.loaddb(grid_layout))

        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save database into cvs file')
        saveAction.setIcon(QIcon('save.svg'))
        saveAction.triggered.connect(self.savefile)

        createAction = QAction('Create', self)
        createAction.setShortcut('Ctrl+N')
        createAction.setStatusTip('Create new database')
        createAction.setIcon(QIcon("new.svg"))
        createAction.triggered.connect(lambda: self.requestcolnumber(grid_layout))


        deleterowAction = QAction('Delete row',self)
        deleterowAction.setStatusTip('Delete row from database')
        deleterowAction.setIcon(QIcon('delete.svg'))
        deleterowAction.triggered.connect(lambda: self.requaestdelrow(grid_layout))

        addrowAction = QAction('Add row', self)
        addrowAction.setStatusTip('Add row to database')
        addrowAction.setIcon(QIcon('add.svg'))
        addrowAction.triggered.connect(lambda: self.requestaddrow(grid_layout)) 

        editrowAction = QAction('Edit row',self)
        editrowAction.setStatusTip('Edit row in database')
        editrowAction.setIcon(QIcon('edit.svg'))
        editrowAction.triggered.connect(lambda: self.requesteditrow(grid_layout))

        searchAction = QAction('Find row',self)
        searchAction.setShortcut('Ctrl+F')
        searchAction.setStatusTip('Find row in database')
        searchAction.setIcon(QIcon('find.svg'))
        searchAction.triggered.connect(self.askforsearch)

        aboutAction = QAction('About us', self)
        aboutAction.setStatusTip('About us')
        aboutAction.setIcon(QIcon('about.svg'))
        aboutAction.triggered.connect(self.showabout)


        self.statusBar()

        menubar = self.menuBar()


        fileMenu = menubar.addMenu('&File')
        editMenu = menubar.addMenu('&Edit')
        moreMenu = menubar.addMenu('&More')
        helpMenu = menubar.addMenu('&Help')
        

        fileMenu.addAction(loadAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(createAction)
        fileMenu.addAction(exitAction)

        editMenu.addAction(deleterowAction)
        editMenu.addAction(addrowAction)
        editMenu.addAction(editrowAction)

        moreMenu.addAction(searchAction)

        helpMenu.addAction(aboutAction)
        
        self.setWindowTitle('База данных') # название окна
        self.setWindowIcon(QIcon('icon.jpg'))
        self.show()

    def loaddb(self,grid_layout):
        '''Loads database and display it in table
        Parameters
        ----------
        :param grid_layout: QGridLayout
        '''
        filename = self.openfilename()
        if os.path.exists(filename):
            self.mydatabase = mydatabase(filename)
            rownumber,colnumber,data = self.mydatabase.readdatafromcsv(filename)
            self.displaytable(grid_layout,colnumber,rownumber,data)

    def createdb(self,grid_layout,colnumber,valuelist):
        ''' Creates new database and display it in table
        Parameters
        ----------
        :param grid_layout: QGridLayout
        :param colnumber: number of columns
        :param valuelist: list of values
        '''
        self.mydatabase = mydatabase('')
        colnumber=colnumber+1
        newdb = self.mydatabase.create(colnumber,valuelist[0:colnumber])
        self.mydatabase.add(valuelist[colnumber:len(valuelist)])
        rownumber = 2
        data=[valuelist[0:colnumber]]
        data.append(valuelist[colnumber:len(valuelist)])
        self.displaytable(grid_layout,colnumber,rownumber,data)

    def displaytable(self,grid_layout,colnumber,rownumber,data):
        '''Displays data in table
        Parameters
        ----------
        :param grid_layout: QGridLayout
        :param colnumber: number of columns
        :param rownumber: number of rows
        :param data: data
        '''
        self.table.setColumnCount(colnumber)
        self.table.setRowCount(rownumber-1)  
        if type(data[0]) == list:
            headerlist=data[0]
            self.table.setHorizontalHeaderLabels(headerlist)
            data=data[1:]
            for i in range(rownumber-1):
                for j in range(colnumber):
                    # print('i, j, data[i][j]',i,j,data[i][j])
                    self.table.setItem(i, j, QTableWidgetItem(str(data[i][j])))
        else:
            headerlist = ['столбец '+str(i) for i in range(1,colnumber+1)]
            self.table.setHorizontalHeaderLabels(headerlist)
            for j in range(colnumber):
                    self.table.setItem(0, j, QTableWidgetItem(str(data[j])))
        grid_layout.addWidget(self.table, 0, 0)   # Добавляем таблицу в сетку 
 
    def savefile(self):
        ''' Saves data in csv file
        '''
        savepath = self.savefilepath()
        print('savepath',savepath)
        if len(savepath) < 4:
            print('length',len(savepath))
            savepath=savepath+".csv"
        else:
            if savepath[-4:] !=".csv":
                print('1',savepath[-4:])
                savepath=savepath+".csv"
                print('2',savepath)
        try:            
            self.mydatabase.dumpdb(savepath)
        except Exception as e:
            pass

    def requesteditrow(self,grid_layout):
        ''' Asks user to input data for editing cell
        Parameters
        ----------
        :param grid_layout: QGridLayout
        '''
        try:
            row, ok = QInputDialog.getInt(self, 'Редактировать ячейку', 'Введите номер строки \n(Вы также можете редактировать ячейку дважды кликнув по ней)',min=1,max=len(self.mydatabase.db.keys())-1)
            col, ok = QInputDialog.getInt(self, 'Редактировать ячейку', 'Введите номер столбца',min=1,max=len(self.mydatabase.db[0])-1)
            value, ok = QInputDialog.getText(self, 'Редактировать ячейку', 'Введите значение ячейки')
            is_successful = self.mydatabase.set(row,col,value)
            if is_successful == True:
                colnumber = len(self.mydatabase.db[0])
                rownumber = len(self.mydatabase.db.keys())
                data = []
                for key in self.mydatabase.db:
                    data.append(self.mydatabase.db[key])
                print('data',data)
                self.displaytable(grid_layout,colnumber,rownumber,data)
        except Exception as e:
            self.showmessage("Внимание","Чтобы редактировать строку, нужно сначала загрузить из файла или создать базу данных")
   

    def requaestdelrow(self,grid_layout):
        ''' Asks user to input data for deleting row
        Parameters
        ----------
        :param grid_layout: QGridLayout
        '''
        try:
            # key, ok = QInputDialog.getInt(self, 'Удалить строку', 'Введите номер строки, которую хотите удалить',min=1,max=len(self.mydatabase.db.keys()))    
            key = int(self.table.selectedItems()[0].text())
            if len(self.table.selectedItems()) == len(self.mydatabase.db[0]):
                is_successful = self.mydatabase.delete(key+1)
                print('key',key,'database',self.mydatabase.db)
                if is_successful == True:
                    colnumber = len(self.mydatabase.db[0])
                    rownumber = len(self.mydatabase.db.keys())
                    data = []
                    for key in self.mydatabase.db:
                        data.append(self.mydatabase.db[key])
                    self.displaytable(grid_layout,colnumber,rownumber,data)
                else:
                    self.showmessage("Внимание","Вы пытаетесь удалить несуществующую строку")

            else:
                self.showmessage("Внимание","Вы выделили столбец")

        except IndexError:
            self.showmessage("Внимание","Чтобы удалить строку, сначала выделите ее в таблице")

        except Exception as e:
            self.showmessage("Внимание","Чтобы удалить строку, нужно сначала загрузить из файла или создать базу данных")



    def requestaddrow(self,grid_layout):
        ''' Asks user to input data for adding row
        Parameters
        ----------
        :param grid_layout: QGridLayout
        '''
        try:
            colnumber = len(self.mydatabase.db[0])
            valuelist=[str(len(self.mydatabase.db.keys())-1)]
            ok = True
            for i in range(colnumber-1):
                value=''
                while value == '' and ok == True:
                    value, ok = QInputDialog.getText(self, 'Создание БД', 'Введите значение для '+str(i+1)+'-го поля:')
                    if value: 
                        valuelist.append(value)
            self.mydatabase.add(valuelist) #добавили строку в БД
            rownumber = len(self.mydatabase.db.keys())
            data = []
            for key in self.mydatabase.db:
                data.append(self.mydatabase.db[key])
            self.displaytable(grid_layout,colnumber,rownumber,data)
        except IndexError:
            self.showmessage("Внимание","Вы заполнили не все поля")
        
        except Exception as e:
            self.showmessage("Внимание","Чтобы добавить строку, нужно сначала загрузить из файла или создать базу данных")        

    def askforsearch(self):
        ''' Asks user to input data for finding row

        '''
        try:
            colnumber = self.table.currentColumn() 
            print('colnumber',colnumber,len(self.table.selectedItems()),len(self.mydatabase.db.keys())-1)
            print('db',self.mydatabase.db[1][colnumber])
            if len(self.table.selectedItems()) == len(self.mydatabase.db.keys())-1:
                value, ok = QInputDialog.getText(self, 'Поиск по столбцу', 'Введите значение, которое нужно найти: ')
                if value:
                    keylist = self.mydatabase.search(colnumber,value)
                    self.table.clearSelection()
                    for key in keylist:
                        for i in range(len(self.mydatabase.db[0])-1):
                            self.table.item(key-1,i).setSelected(True)
                    print('keys',keylist)
            else:
                self.showmessage("Внимание","Выделите столбец")
                
        except Exception as e:
            self.showmessage("Внимание","Чтобы выполнить поиск, сначала создайте или загрузите базу данных")
            


    def openfilename(self):
        ''' Asks user to select file for opening
        '''
        path = os.getcwd()
        fname = QFileDialog.getOpenFileName(self, 'Open file',path,"*.csv")[0]
        print(fname)
        return fname



    def savefilepath(self):
        '''Asks user to select file for saving
        '''
        path = os.getcwd()
        path = QFileDialog.getSaveFileName(self,'Save file',path,'*.csv')[0]
        print('path',path)
        return path



    def requestcolnumber(self,grid_layout):
        '''Asks user to input data for creating new database
        Parameters
        ----------
        :param grid_layout: QGridLayout
        '''
        colnumber, ok = QInputDialog.getInt(self, 'Создание БД', 'Введите число полей', min = 1)
        if ok == True:
            valuelist=['']
            ok = True
            for i in range(colnumber):
                value=''
                while value == '' and ok == True:
                    value, ok = QInputDialog.getText(self, 'Создание БД', 'Введите название для '+str(i+1)+'-го поля:')
                    if value: 
                        valuelist.append(value)
            valuelist.append(0)
            for i in range(colnumber):
                value=''
                while value == '' and ok == True:
                    value, ok = QInputDialog.getText(self, 'Создание БД', 'Введите значение для '+str(i+1)+'-го поля:')
                    if value: 
                        valuelist.append(value)
            if ok == True:
                self.createdb(grid_layout,colnumber,valuelist)


    def showabout(self):
        ''' Shows message with information about developer
        '''
        self.showmessage("О разработчике","Студент Роман Забаровский")
     


    def on_cell_item_clicked(self, item):
        ''' Allows user to edit cell by double clicking on cell's item
        Parameters
        ----------
        :param item: QTableWidget::item
        '''
        print(item, item.column())
        if item.column() != 0:
            new_text, ok = QInputDialog.getText(self, 'Редактирование ячейки', 'Введите новое значение поля', text=item.text())
            row=item.row()+1
            is_successful = self.mydatabase.set(row,item.column(),new_text)
            print('is_successful',is_successful, 'db',self.mydatabase.db[row])
            if ok:
                item.setText(new_text)


    def showmessage(self,title,text):
        ''' Shows  message box with given title and text
        Parameters
        ----------
        :param title: the title of message box
        :param text: the text in message box
        '''
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        x = msg.exec_()



style = """
    QMainWindow {
        background-color: #DCDCDC;
    }
    QMenuBar {
        background-color: #2F4F4F;
        color: white;
    }
    QMenuBar::item {
        background-color: transparent;
        color: white;
    }
    QMenuBar::item:selected {
        background-color: #FFFFFF;
        color: black;
    }
    QMenu{
        background-color: #A9A9A9;
        color: white;
    }
    QMenu::item:selected{
        background-color: #facd60;
        color: black;
    }
    QStatusBar {
        background-color: #2F4F4F;
        color: white;
    }

    QTableWidget QHeaderView::section {
        font-size: 15px;
        font-weight: bold;
        background-color: #808080;
        color: white;
        padding-left: 4px;
        border: 1px solid #6c6c6c;
    }

    QTableCornerButton::section {
        background-color: #facd60;
    }

    QTableWidget::item {
        background-color: #778899;
        color: white; 
    }
     
    QTableWidget::item:selected {
        background-color: #fdfa66;
        color: #e74645; 
    }
    QMessageBox {
        background-color: #C0C0C0;
        color: #e74645;
    }
    QMessageBox QLabel {
        color: #000000;
    }
    QTableWidget QScrollBar {
        background-color: #808080;
    }
"""

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    w = MainWindow()
    sys.exit(app.exec_())