import sys, os, glob, fnmatch, platform, json

from PySide2.QtWidgets import *
from PySide2.QtCore import QDir, Qt, QSortFilterProxyModel, QCoreApplication

from uiHoudiniLauncher import Ui_HoudiniLauncher


class MainWindow(QMainWindow, Ui_HoudiniLauncher):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.checkOS()
        self.initTable()
        self.onStart()


        
        ##self.listProjects()
        ##self.setDefaultPath()

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
        

        #self.projects_location.textChanged.connect(self.populate)
        self.projects_location.editingFinished.connect(self.updateProjectsList)
        #self.treeView.selectionModel().selectionChanged.connect(self.setPath)
        #self.treeView.selectionModel().selectionChanged.connect(self.onStart)
        #self.treeView.selectionModel().selectionChanged.connect(self.populate)
        ##self.treeView.selectionModel().selectionChanged.connect(self.listProjects)
        #self.projects_list.currentTextChanged.connect(self.setProject)
        #self.tasksList.currentTextChanged.connect(self.setProject)
        ##self.tasksList.currentTextChanged.connect(self.listShots)
        ##self.tasksList.currentTextChanged.connect(self.setTasks)

        ##self.projects_list.currentTextChanged.connect(self.populateBrowser)
        ##self.shotsList.currentTextChanged.connect(self.populateBrowser)
        ##self.taskTypeList.currentTextChanged.connect(self.populateBrowser)

        self.projects_list.currentTextChanged.connect(self.updateTasksList)
        self.projects_list.currentTextChanged.connect(self.updateShotsList)
        self.projects_list.currentTextChanged.connect(self.updateTaskTypeList)
        self.projects_list.currentTextChanged.connect(self.populateBrowser)

        self.tasksList.currentTextChanged.connect(self.updateShotsList)
        self.tasksList.currentTextChanged.connect(self.updateTaskTypeList)
        self.tasksList.currentTextChanged.connect(self.populateBrowser)

        self.shotsList.currentTextChanged.connect(self.populateBrowser)

        self.taskTypeList.currentTextChanged.connect(self.populateBrowser)

        self.checkLoadFile.stateChanged.connect(self.updateTaskTypeList)



        #self.savePreset.clicked.connect(self.onQuit)
        #self.launch_project.clicked.connect(self.onQuit)
        self.launch_project.clicked.connect(self.launchHoudini)
        self.launch_project.clicked.connect(self.close)

    def checkOS(self):
        system = platform.system()
        if(system == "Windows"):
            self.projects_location.setText("T:\\projects\\")
            self.os = "Windows"

    def initTable(self):
        self.hda_folders = glob.glob("/media/white/tools/otls/hda_*")
        self.hda_labels = []
        [self.hda_labels.append(os.path.split(path)[1][4:]) for path in self.hda_folders]


        for row, label in enumerate(self.hda_labels):
            
            item = QListWidgetItem("{}".format(label))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            #item.setCheckable(True)
            #if inHdaFolder:
            #    item.setCheckState(QtCore.Qt.CheckState.Checked)
            self.listWidget.addItem(item)

            

    """
        self.model.setHorizontalHeaderLabels(self.hda_labels)
        self.proxy = QtCore.QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.tableView.setModel(self.proxy)
        
        self.tableView.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    """
    def onStart(self):
        #print("Start")
        try:
            settings = json.load(open(os.path.join(os.environ["HOME"], ".houdiniLauncher.conf")))
            #print(self.listWidget.count())
            
            for index in range(self.listWidget.count()):
                item = self.listWidget.item(index)
                if settings["check{}".format(item.text())]:
                    state = Qt.Checked
                else:
                    state = Qt.Unchecked
                item.setCheckState(state)
                
            """            
            self.checkLoadFile.setChecked(settings["checkLoadFile"])
            self.checkDefaultEnv.setChecked(settings["checkDefaultEnv"])
            self.checkProjectEnv.setChecked(settings["checkProjectEnv"])
            self.checkWowsEnv.setChecked(settings["checkWowsEnv"])
            self.checkOrcEnv.setChecked(settings["checkOrcEnv"])
            self.checkShEnv.setChecked(settings["checkShEnv"])
            
            """
            self.checkFx.setChecked(settings["checkFx"])
            self.projects_location.setText(settings["projects_location"])
            self.updateProjectsList()
            self.projects_list.setCurrentIndex(settings["projects_list_current"])
            self.updateTasksList()
            self.tasksList.setCurrentIndex(settings["tasksList_current"])
            self.updateTaskTypeList()
            self.taskTypeList.setCurrentIndex(settings["taskTypeList_current"])
            self.updateShotsList()
            self.shotsList.setCurrentIndex(settings["shotsList_current"])
            self.updateTaskTypeList()
            self.populateBrowser()

        except (FileExistsError, KeyError) as e:
            print("Exception")
            #self.setDefaultPath()
            self.updateProjectsList()
            self.updateTasksList()
            self.updateTaskTypeList()
            self.updateShotsList()
            self.populateBrowser()


    def closeEvent(self, event):
        self.onQuit()
        
    def onQuit(self):
        settings = {}
        settings["projects_location"] = self.projects_location.text()
        settings["projects_list_current"] = self.projects_list.currentIndex()
        settings["checkLoadFile"] = self.checkLoadFile.isChecked()
        settings["tasksList_current"] = self.tasksList.currentIndex()
        settings["taskTypeList_current"] = self.taskTypeList.currentIndex()
        settings["shotsList_current"] = self.shotsList.currentIndex()
        settings["checkFx"] = self.checkFx.isChecked()

        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            isChecked = item.checkState() == Qt.Checked
            settings["check{}".format(item.text())] = isChecked
        #print(settings)

        """
        settings["checkDefaultEnv"] = self.checkDefaultEnv.isChecked()
        settings["checkProjectEnv"] = self.checkProjectEnv.isChecked()
        settings["checkWowsEnv"] = self.checkWowsEnv.isChecked()
        settings["checkOrcEnv"] = self.checkOrcEnv.isChecked()
        settings["checkShEnv"] = self.checkShEnv.isChecked()
        """
        #print("Exiting")
        f = open(os.path.join(os.environ["HOME"], ".houdiniLauncher.conf"), "w")
        jsn = json.dumps(settings, indent = 4)
        #print(jsn)
        f.write(jsn)
        f.close()
        
        #print(settings)

    def launchHoudini(self):
        prj = self.projects_list.currentData()
        #houdini_tools = os.path.join(prj, "houdini_tools")
        houdini_otls = "/media/white/tools/otls"
        houdini_otlscan_path = os.environ["HOUDINI_OTLSCAN_PATH"]

        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            isChecked = item.checkState() == Qt.Checked
            otl_dirname = "hda_{}".format(item.text())
            otl_path = os.path.join(houdini_otls, otl_dirname)
            if isChecked and not otl_path in os.environ["HOUDINI_OTLSCAN_PATH"]:
                os.environ["HOUDINI_OTLSCAN_PATH"] = "{};{}".format(otl_path, os.environ["HOUDINI_OTLSCAN_PATH"])


        """
        otls_default = os.path.join(houdini_otls, "global")
        otls_orc = os.path.join(houdini_otls, "orc")
        otls_sh = os.path.join(houdini_otls, "SH")
        otls_wows = os.path.join(houdini_otls, "wows")


        if self.checkDefaultEnv.isChecked() and not otls_default in houdini_otlscan_path:
            os.environ["HOUDINI_OTLSCAN_PATH"] = otls_default + ";" + houdini_otlscan_path

        if self.checkOrcEnv.isChecked() and not otls_orc in houdini_otlscan_path:
            os.environ["HOUDINI_OTLSCAN_PATH"] = otls_orc + ";" + houdini_otlscan_path

        if self.checkShEnv.isChecked() and not otls_sh in houdini_otlscan_path:
            os.environ["HOUDINI_OTLSCAN_PATH"] = otls_sh + ";" + houdini_otlscan_path

        if self.checkWowsEnv.isChecked() and not otls_wows in houdini_otlscan_path:
            os.environ["HOUDINI_OTLSCAN_PATH"] = otls_wows + ";" + houdini_otlscan_path
        """
        print("HOUDINI_OTLSCAN_PATH={}\n".format(os.environ["HOUDINI_OTLSCAN_PATH"]))
        if self.checkFx.isChecked():
            houdini = "houdinifx"
        else:
            houdini = "houdini"
        print("run '{}'".format(houdini))
        if not self.checkLoadFile.isChecked():
            os.system('/bin/bash -c "{}"'.format(houdini))
        else:
            index = self.treeViewShots.currentIndex()
            file = self.shotsModel.filePath(index)
            
            os.system('/bin/bash -c "{} {}"'.format(houdini, file))

    def walk(self, path, pattern):
        matches = []
        for root, dirnames, filenames in os.walk(path):
            isShot = 0
            for filename in fnmatch.filter(filenames, pattern):
                matches.append(os.path.join(root, filename))
        return matches

    def checkLoad(self):
        if not self.checkLoadFile.isChecked():
            self.tasksList.hide()
            self.shotsList.hide()
            self.label_5.hide()
            self.label_6.hide()
            self.treeViewShots.hide()
            self.label_3.hide()
            self.label_7.hide()
            self.taskTypeList.hide()
            
            self.adjustSize()

        else:
            self.tasksList.show()
            self.shotsList.show()
            self.label_5.show()
            self.label_6.show()
            self.treeViewShots.show()
            self.label_3.show()
            self.label_7.show()
            self.taskTypeList.show()
            
            #self.adjustSize() 
        if self.tasksList.currentText() == "LOOKDEV" or not self.checkLoadFile.isChecked():
        
            self.shotsList.hide()
            self.label_5.hide()
        else:
            self.shotsList.show()
            self.label_5.show()        

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

    def updateTaskTypeList(self):
        taskType = self.tasksList.currentText()
        defaultTasks = ["animation", "fx", "lighting", "layout"]
        self.taskTypeList.clear()
        if taskType == "LOOKDEV" or not self.checkLoadFile.isChecked():
            #print("text {}".format(self.tasksList.currentText()))
            #print("data {}".format(self.tasksList.currentData()))
            defaultTasks = os.listdir(self.tasksList.currentData())
            self.shotsList.hide()
            self.label_5.hide()
        else:
            self.shotsList.show()
            self.label_5.show()
        #print(defaultTasks)
        #print(taskType)
        for task in defaultTasks:
            self.taskTypeList.addItem(task)

    def updateProjectsList(self):
        listd = QDir.entryList(QDir(self.projects_location.text()), QDir.Dirs)
        #print(listd)
        self.projects_list.clear()
        for d in listd:
            #print(d.encode('utf-8'))
            if d != "." and d != ".." and not d.startswith("!"):
                self.projects_list.addItem(d, str(os.path.join(self.projects_location.text(), d)))

    def updateShotsList(self):
        path = [self.projects_list.currentData(), self.tasksList.currentText()]
        try:
            path = os.path.join(*path)
        except TypeError:
            pass
        #print(path)

        self.shotsList.clear()
        #print("Shots location {}".format(os.listdir(path)))
        try:
            listdir = os.listdir(path)
            for shot in listdir:
                if not shot.startswith("."):
                    self.shotsList.addItem(shot, os.path.join(path, shot))
        except TypeError:
            pass
        

    def populateBrowser(self):
        self.shotsModel = QFileSystemModel()
        self.shotsModel.setRootPath(self.projects_list.currentData())
        self.treeViewShots.setModel(self.shotsModel)
        if self.tasksList.currentText() == "CGI" and self.shotsList.currentData() != None:
            root = os.path.join(self.shotsList.currentData(), self.taskTypeList.currentText())
        else:
            root = ""
        
        if self.tasksList.currentText() == "LOOKDEV":
            #print("Tasks type data {}".format(self.tasksList.currentData()))
            #print("Task text {}".format(self.taskTypeList.currentText()))        
            root = os.path.join(self.tasksList.currentData(), self.taskTypeList.currentText())
        #print(root)
        #else:
        #    root = os.path.join(root, "houdini")
        self.treeViewShots.setRootIndex(self.shotsModel.index(root))
        self.treeViewShots.setSortingEnabled(True)
        self.treeViewShots.sortByColumn(0, Qt.AscendingOrder)
        self.treeViewShots.setColumnHidden(2, True)
        self.treeViewShots.setColumnHidden(1, True)

    def updateTasksList(self):
        filter_tasks = ["CGI", "LOOKDEV"]
        tasks = os.listdir(self.projects_list.currentData())
        self.tasksList.clear()
        for task in tasks:
            if task in filter_tasks:
                self.tasksList.addItem(task, os.path.join(self.projects_list.currentData(), task))        

    def setProject(self):
        self.project = self.projects_list.currentText()
        self.project_path = self.projects_list.currentData()
        #filter_tasks = ["CGI", "LOOKDEV"]

        #tasks = os.listdir(self.project_path)

        #self.tasksList.clear()
        
        #for task in tasks:
        #    if task in filter_tasks:
        #        self.tasksList.addItem(task, os.path.join(self.project_path, task))

        #self.listShots()
        #self.populateBrowser()

        ##self.shotsModel = QFileSystemModel()
        ##self.shotsModel.setRootPath(self.project_path)

        ##self.proxyModel = QSortFilterProxyModel()
        ##self.proxyModel.setSourceModel(self.shotsModel)
        #self.proxyModel.setRecursiveFilteringEnabled(True)
        #self.proxyModel.setFilterWildcard("|".join(filter_tasks))


        ##self.treeViewShots.setModel(self.shotsModel)
        ##rootId = self.shotsModel.index(os.path.join(self.project_path, self.tasksList.currentText()))
        ##mappedId = self.proxyModel.mapFromSource(rootId)
        
        ##self.treeViewShots.setRootIndex(self.shotsModel.index(os.path.join(self.project_path, self.tasksList.currentText())))
        ##self.treeViewShots.setSortingEnabled(True)
        ##self.treeViewShots.sortByColumn(0, Qt.AscendingOrder)
        ##self.treeViewShots.setColumnHidden(2, True)
        ##self.treeViewShots.setColumnHidden(1, True)
        
        ###
        #print(self.project_path)
        #hipFiles = self.walk(self.project_path, "*.hip")
        pth = [self.project_path, self.tasksList.currentText(), "*", self.taskTypeList.currentText(),"/*/*.hip"]
        #print(pth)
        pattern = os.path.join(*pth)
        #print(pattern)
        hipFiles = glob.glob(os.path.join(self.project_path, pattern))
        #print(hipFiles)


            

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()
    ret = app.exec_()
    sys.exit( ret )