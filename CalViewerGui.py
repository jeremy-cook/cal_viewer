import sys
import json
import pathlib
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QFrame
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRect, Qt


class MainWindow(QWidget):
	def __init__(self,parent=None):
		super().__init__(parent=parent)
		## --- Initialize Properties --- ##
		self.shiftTypeTrees = {}
		self.activeShiftType = ''
		self.activeShift = ''
		## --- Initialization Locals --- ##
		windowWidth = 900
		windowHeight = 500
		## --- Window Creation --- ##
		self.resize(windowWidth, windowHeight)
		self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
		self.setWindowTitle('CalViewer')
		self.setAccessibleName("MainWindow")
		self.setObjectName("MainWindow")
		self.setStyleSheet(".MainWindow {background-color:grey;}")
		## --- Set Vertical Stretch Layout --- ##
		self.MainLayout = QtWidgets.QVBoxLayout(self)
		self.MainLayout.setSpacing(0)
		self.MainLayout.setObjectName("MainLayout")
		self.MainLayout.setContentsMargins(5, 5, 5, 0) ## (Left, Top, Right, Bottom)
		## --- Set Top "NavBar" --- ##
		self.NavBar = QtWidgets.QHBoxLayout()
		self.NavBar.setObjectName("NavBar")
		## --- Set Shift Selection Box --- ##
		self.ShiftSelect = QtWidgets.QComboBox(self)
		self.ShiftSelect.setMinimumSize(QtCore.QSize(100, 0))
		self.ShiftSelect.setObjectName("ShiftSelect")
		self.NavBar.addWidget(self.ShiftSelect)
		## --- Set Calibration Section Box --- ##
		self.SectionSelect = QtWidgets.QComboBox(self)
		self.SectionSelect.setMinimumSize(QtCore.QSize(250, 0))
		self.SectionSelect.setObjectName("SectionSelect")
		self.NavBar.addWidget(self.SectionSelect)
		## --- Set Calibration Selection Box --- ##
		self.CalibrationSelect = QtWidgets.QComboBox(self)
		self.CalibrationSelect.setMinimumSize(QtCore.QSize(250, 0))
		self.CalibrationSelect.setObjectName("CalibrationSelect")
		self.NavBar.addWidget(self.CalibrationSelect)
		## --- Create Spacer --- ##
		self.NavBarSpacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.NavBar.addItem(self.NavBarSpacer)
		## --- Create "Company" Logo --- ##
		self.Logo = QtWidgets.QLabel(self)
		self.Logo.setObjectName("Logo")
		self.Logo.setText('') ## Leave Empty For Now
		self.NavBar.addWidget(self.Logo)
		## --- Set Navbar to Main --- ##
		self.MainLayout.addLayout(self.NavBar)
		## --- Create a splitter layout --- ##
		self.Splitter = QtWidgets.QSplitter(self)
		self.Splitter.setOrientation(QtCore.Qt.Horizontal)
		self.Splitter.setObjectName("Splitter")
		## --- Create a Calibrations Selection List --- ##
		self.CalibrationsList = QtWidgets.QTreeWidget(self.Splitter)
		self.CalibrationsList.setObjectName("CalibrationsList")
		self.CalibrationsList.setColumnCount(1)
		self.CalibrationsList.setSortingEnabled(False)
		self.CalibrationsList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
		self.CalibrationsList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		## --- Create a Calibration Viewing Table --- ##
		self.CalibrationTable = QtWidgets.QTableWidget(self.Splitter)
		self.CalibrationTable.setObjectName("CalibrationTable")
		## --- Add Splitter to Main --- ##
		self.MainLayout.addWidget(self.Splitter)
		## --- Set Splitter Window Proportions, Now that children exist --- ##
		self.Splitter.setSizes((windowWidth//4, windowWidth - windowWidth//4))
		## --- Create a Status Bar --- ##
		self.StatusBar = QtWidgets.QLabel(self)
		self.StatusBar.setText("Status: Not Connected")
		self.StatusBar.setObjectName("StatusBar")
		self.StatusBar.setMargin(5)
		self.MainLayout.addWidget(self.StatusBar)
		## --- Tell MainLayout to only stretch the middle section on resize --- ##
		self.MainLayout.setStretch(1, 1)
		## --- Load Data into Window --- ##
		try:
			self.loadConfig()
			self.initializeNavBar()
			self.initializeTrees()
			self.connectSignals()
			## --- Data Intialization is Done, Start Initializing the Visible Window --- ##
			self.updateTree(self.ShiftSelect.currentText())

		except BaseException as error:
			print(error)
			sys.exit()

	def loadConfig(self):
		with open('./CalibrationLayout.json', 'r') as f:
			self.Config = json.load(f)

		## --- Fill Shift Select Combo Box --- ##
	def initializeNavBar(self):
		idx = 0
		SeparatorIndices = []
		for ShiftType in self.Config.keys():
			for Shift in self.Config[ShiftType]["Shifts"]:
				self.ShiftSelect.addItem('%s:%s' % (ShiftType,Shift))
				idx += 1
			SeparatorIndices.append(idx)
			idx += 1
		del SeparatorIndices[-1]
		for SeparatorIndex in SeparatorIndices:
			self.ShiftSelect.insertSeparator(SeparatorIndex)

	def connectSignals(self):
		self.ShiftSelect.currentIndexChanged[str].connect(self.updateTree)

	def initializeTrees(self):
		## --- Create Local Function to Save Memory -- ##
		def buildTreeItem(parentItem,structureDict):
			for key, value in structureDict.items():
				if value["Type"] == 'Category':
					CategoryItem = QtWidgets.QTreeWidgetItem(parentItem,(key,))
					CategoryItem.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
					if "Children" in value:
						buildTreeItem(CategoryItem, value["Children"])
				elif value["Type"] == 'Calibration':
					CalibrationItem = QtWidgets.QTreeWidgetItem(parentItem,(key,))
					CalibrationItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemNeverHasChildren)
		## --- Loop through Config and Build Menu Trees --- ##
		for shiftTypeKey, shiftTypeDict in self.Config.items():
			## Create a Psuedo Top Level Item ##
			shiftTypeWidgetItem = QtWidgets.QTreeWidgetItem()
			buildTreeItem(shiftTypeWidgetItem,shiftTypeDict["Structure"])
			self.shiftTypeTrees[shiftTypeKey] = shiftTypeWidgetItem.takeChildren()
			self.CalibrationsList.invisibleRootItem().addChildren(self.shiftTypeTrees[shiftTypeKey])

	def updateTree(self,ShiftSelection):
		ShiftType = ShiftSelection.split(":")[0]
		if self.activeShiftType != ShiftType:
			## --- Freeze Draw Events --- ##
			self.CalibrationsList.setUpdatesEnabled(False)
			## --- Set New Header --- ##
			self.CalibrationsList.headerItem().setText(0, ShiftType)
			## --- Get TreeWidget Top Level Item --- ##
			invisibleRoot = self.CalibrationsList.invisibleRootItem()
			## --- Hide all Visible Tree Branches --- ##
			for childIdx in range(invisibleRoot.childCount()):
				invisibleRoot.child(childIdx).setHidden(True)
			## --- Unhide the Desired Tree Branch --- ##
			for child in self.shiftTypeTrees[ShiftType]:
				child.setHidden(False)
			## --- Set New Active Shift Type --- ##
			self.activeShiftType = ShiftType
			## --- Unfreeze Draw Events --- ##
			self.CalibrationsList.setUpdatesEnabled(True)


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    Main = MainWindow()
    Main.show()
    sys.exit(app.exec_())