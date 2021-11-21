import sys, os, glob, fnmatch

from PySide2.QtWidgets import *
from PySide2.QtCore import QDir, Qt, QSortFilterProxyModel, QCoreApplication

from uiHoudiniLauncher_002 import Ui_HoudiniLauncher


class MainWindow(QMainWindow, Ui_HoudiniLauncher):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.onStart()
        self.listProjects()
        self.setDefaultPath()

        ### Setup completer

        model = QFileSystemModel()
        model.setRootPath(QDir.rootPath())
        self.completer = QCompleter(self.projects_location)
        self.completer.setModel(model)
        self.completer.setCompletionColumn(0)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionPrefix(self.projects_location.text())
        self.projects_location.setCompleter(self.completer)

        ###

        self.checkLoad()
        self.checkLoadFile.stateChanged.connect(self.checkLoad)

        ###
        
        self.setProject()
        #self.projects_location.textChanged.connect(self.populate)
        self.projects_location.editingFinished.connect(self.listProjects)
        #self.treeView.selectionModel().selectionChanged.connect(self.setPath)
        #self.treeView.selectionModel().selectionChanged.connect(self.onStart)
        #self.treeView.selectionModel().selectionChanged.connect(self.populate)
        #self.treeView.selectionModel().selectionChanged.connect(self.listProjects)
        self.projects_list.currentTextChanged.connect(self.setProject)

        self.launch_project.clicked.connect(self.onQuit)
        self.launch_project.clicked.connect(self.close)

    def onStart(self):
        print("Start")

    def onQuit(self):
        settings = {}
        
        print("Quit")

    def walk(self, path, pattern):
        matches = []
        for root, dirnames, filenames in os.walk(path):
            isShot = 0
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename))
        return matches

    def checkLoad(self):
        if(not self.checkLoadFile.isChecked()):
            self.tasksList.hide()
            self.shotsList.hide()
            self.label_5.hide()
            self.label_6.hide()
            self.treeViewShots.hide()
            self.label_3.hide()
        else:
            self.tasksList.show()
            self.shotsList.show()
            self.label_5.show()
            self.label_6.show()
            self.treeViewShots.show()
            self.label_3.show()

            


    def pr(self):
        print(self.completer.completionPrefix())

    def populate(self):
        path = self.projects_location.text()
        self.model = QFileSystemModel()
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.Dirs)
        self.model.setRootPath(QDir.rootPath())
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)
        self.treeView.sortByColumn(0, Qt.AscendingOrder)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(1, True)

    def setDefaultPath(self):

        self.project_path = self.projects_list.currentData()

    def setPath(self):
        path = self.model.filePath(index)
        self.projects_location.setText(path)

    def listProjects(self):
        listd = QDir.entryList(QDir(self.projects_location.text()), QDir.Dirs)
        #print(listd)
        self.projects_list.clear()
        for d in listd[2:]:
            #print(d.encode('utf-8'))
            self.projects_list.addItem(d.encode('utf-8'), os.path.join(self.projects_location.text().encode('utf-8'), d.encode('utf-8')))

    def setProject(self):
        self.project = self.projects_list.currentText()
        self.project_path = self.projects_list.currentData()

        self.shotsModel = QFileSystemModel()
        self.shotsModel.setRootPath(QDir.rootPath())

        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(self.shotsModel)
        self.proxyModel.setRecursiveFilteringEnabled(True)
        #self.proxyModel.setFilterWildcard("*.hip")

        self.treeViewShots.setModel(self.proxyModel)
        rootId = self.shotsModel.index(self.project_path)
        mappedId = self.proxyModel.mapFromSource(rootId)
        
        self.treeViewShots.setRootIndex(mappedId)
        self.treeViewShots.setSortingEnabled(True)
        self.treeViewShots.sortByColumn(0, Qt.AscendingOrder)
        self.treeViewShots.setColumnHidden(2, True)
        self.treeViewShots.setColumnHidden(1, True)
        
        ###
        print(self.project_path)
        hipFiles = self.walk(self.project_path, "*.hip")
        #print(hipFiles)
        tasks = os.listdir(self.project_path)
        print(tasks)
        for task in tasks:
            self.tasksList.addItem(task, os.path.join(self.project_path, task))

            

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()
    ret = app.exec_()
    sys.exit( ret )