import os
import sys
from PySide.QtCore import *
from PySide import QtGui, QtUiTools
from createUi import Ui_MainWindow
import csv


class Window(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(Window, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        uifile = QFile(r"D:\Pipeline\createCSV.ui")
        uifile.open(QFile.ReadOnly)
        self.ui = loader.load(uifile,self)
        uifile.close()
        self.setupUi(self)
        self.setGeometry( 500,500,383,430 )
        self.setWindowTitle("PITA")
        self.setWindowIcon(QtGui.QIcon(r'C:\mnt\animation\Pipeline\icons\favicon.ico')) 
        
        self.numOfSeqBox.returnPressed.connect(self.sequenceTree)
        
        self.addSelectedBt.clicked.connect(self.addSelBt)

        self.removeBt.clicked.connect(self.clearBt)

        self.submitBt.clicked.connect(self.makeCSV)
    
    def sequenceTree(self):
        self.sqList = []
        self.seqNum = self.numOfSeqBox.text()
        assert self.seqNum.isdigit(), "Must be a number!!"
        self.sqName=[]
        for q in xrange(int(self.seqNum)):
            q = q+1
            self.sqList.append(os.path.join('%03d'%q))
            self.sqName.append(QtGui.QTreeWidgetItem(self.seqTree,['sq'+'%03d'%q]))

            
        self.seqTree.expandItem(QtGui.QTreeWidgetItem(self.sqName))
        self.seqTree.addTopLevelItems(self.sqName)
        self.seqTree.sortItems(0,Qt.SortOrder(0))

    def addSelBt(self):
        self.noSubItem = self.subItemBox.text()
        assert self.noSubItem.isdigit(), "Must be a number!!"
        selectedItems = self.seqTree.selectedItems()
        self.scnName = []
        self.shtName = []
        if selectedItems[0].childCount() == 0:
            if len(selectedItems) > 0:
                
                for i in xrange(int(self.noSubItem)):
                    i = i+1
                    if "sc" not in selectedItems[0].text(0):
                        selectedItems[0].addChild(QtGui.QTreeWidgetItem([('sc'+'%03d'%i)]))
                        self.scnName.append(QtGui.QTreeWidgetItem([('sc'+'%03d'%i)]).text(0))
                        continue
                        
                    else:
                        QtGui.QTreeWidgetItem(selectedItems[0],[('sh'+'%03d'%i)])
                        self.shtName.append(QtGui.QTreeWidgetItem([('sh'+'%03d'%i)]).text(0))
            else:
                assert (len(selectedItems) > 0), "Nothing is selected!"
                
        else:
            if len(selectedItems) > 0:
                for j in xrange(int(self.noSubItem)):
                    k = j + int((selectedItems[0].child(j).text(0))[-1])
                    k = k + 1
                    if "sc" not in selectedItems[0].text(0):
                        selectedItems[0].addChild(QtGui.QTreeWidgetItem([('sc'+'%03d'%k)]))
                        self.scnName.append(QtGui.QTreeWidgetItem([('sc'+'%03d'%i)]).text(0))
                        continue
                    else:
                        self.shtName.append(QtGui.QTreeWidgetItem(selectedItems[0],[('sh'+'%03d'%k)]))
            else:
                assert (len(selectedItems) > 0), "Nothing is selected!"

    def clearBt(self):
        selectedRemove = self.seqTree.selectedItems()
        if len(selectedRemove) > 0:
            selectedRemove[0].takeChildren()
        else:
            assert (len(selectedRemove) > 0), "Nothing is selected!"

    def makeCSV(self):
        sq=[]
        outputFileA = os.path.join("D:\\"+"temp"+".csv")
        header = ["Sequence","Scene","Shot"]
        with open(outputFileA,'wb') as g:
            fieldnames = ["Sequence","Scene","Shot"]
            wr = csv.DictWriter(g,fieldnames=fieldnames)
            wr.writeheader()

            for j in self.sqName:
                sq.append(j.text(0).split("q")[-1])
                for scItem in range(0,j.childCount()):
                    scItem = scItem + 1
                    if j.child(scItem-1).text(0) != None:
                        scene = j.child(scItem-1)
                        
                        for shItem in range(0,scene.childCount()):
                            shItem = shItem + 1
                            if scene.child(shItem-1).text(0) != None:
                                shot = scene.child(shItem-1)

                                wr.writerow({
                                            fieldnames[0]:j.text(0).split("q")[-1],
                                            fieldnames[1]:scene.text(0).split("c")[-1],
                                            fieldnames[2]:shot.text(0)
                                            })
                                
        projName = self.projNameBox.text()
        outputFileB = os.path.join("D:\\"+projName+"_"+"tacticData"+".csv")
        print len(sq)
        print len(self.sqList)
        print len(self.scnName)
        
        with open(outputFileA,'r') as inf:
            with open(outputFileB,'wb') as outf:
                reader = inf.readlines()
                for ind, q in enumerate(reader):
                    if ind == 0:
                        reader[ind] = "Sq,"+q
                    else:
                        if ind-1 >= len(sq):
                            reader[ind] = ","+q
                        else:
                            reader[ind] = self.sqList[ind-1]+","+q

                    outf.write(reader[ind])
                    
        os.remove(outputFileA)
                            

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myGUI = Window()
    myGUI.show()
    sys.exit(app.exec_())

