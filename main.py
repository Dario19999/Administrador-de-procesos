from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
import sys, time, os

class Admin(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'admin_procesos.ui'), self)
       
        self.thread={}
        self.iniciar_1.clicked.connect(self.iniciar_p1)
        self.iniciar_2.clicked.connect(self.iniciar_p2)
        self.iniciar_3.clicked.connect(self.iniciar_p3)
        self.iniciar_4.clicked.connect(self.iniciar_p4)
        self.iniciar_5.clicked.connect(self.iniciar_p5)
        
        self.pausar_1.clicked.connect(self.pausar_p1)
        self.pausar_2.clicked.connect(self.pausar_p2)
        self.pausar_3.clicked.connect(self.pausar_p3)
        self.pausar_4.clicked.connect(self.pausar_p4)
        self.pausar_5.clicked.connect(self.pausar_p5)
        
        self.cancelar_1.clicked.connect(self.cancelar_p1)
        self.cancelar_2.clicked.connect(self.cancelar_p2)
        self.cancelar_3.clicked.connect(self.cancelar_p3)
        self.cancelar_4.clicked.connect(self.cancelar_p4)
        self.cancelar_5.clicked.connect(self.cancelar_p5)
        
        self.lotes_btn.clicked.connect(self.iniciar_p1)
        self.multi_btn.clicked.connect(self.multiprogramacion)
        self.reset_btn.clicked.connect(self.reset)
        
   
        self.thread[1] = Thread(parent=None, index=1)
        self.thread[2] = Thread(parent=None, index=2)
        self.thread[3] = Thread(parent=None, index=3)
        self.thread[4] = Thread(parent=None, index=4)
        self.thread[5] = Thread(parent=None, index=5)
    
    def iniciar_p1 (self):
        self.thread[1].start()
        self.thread[1].signal.connect(self.procesar)
        self.thread[1].finished.connect(self.iniciar_p2)
        self.iniciar_1.setEnabled(False)
        self.pausar_1.setEnabled(True)
        
        
    def iniciar_p2 (self):
        self.thread[2].start()
        self.thread[2].signal.connect(self.procesar)
        self.thread[2].finished.connect(self.iniciar_p3)
        self.iniciar_2.setEnabled(False)
        self.pausar_2.setEnabled(True)
        
    def iniciar_p3 (self):
        self.thread[3].start()
        self.thread[3].signal.connect(self.procesar)
        self.thread[3].finished.connect(self.iniciar_p4)
        self.iniciar_3.setEnabled(False)
        self.pausar_3.setEnabled(True)      
        
    def iniciar_p4 (self):
        self.thread[4].start()
        self.thread[4].signal.connect(self.procesar)
        self.thread[4].finished.connect(self.iniciar_p5)
        self.iniciar_4.setEnabled(False)
        self.pausar_4.setEnabled(True)
        
    def iniciar_p5 (self):
        self.thread[5].start()
        self.thread[5].signal.connect(self.procesar)
        self.iniciar_5.setEnabled(False)
        self.pausar_5.setEnabled(True)
    
    def pausar_p1 (self):
        self.thread[1].stop()
        self.iniciar_1.setEnabled(True)
        self.pausar_1.setEnabled(False)
  
    def pausar_p2 (self):
        self.thread[2].stop()
        self.iniciar_2.setEnabled(True)
        self.pausar_2.setEnabled(False)

        
    def pausar_p3 (self):
        self.thread[3].stop()
        self.iniciar_3.setEnabled(True)
        self.pausar_3.setEnabled(False)

        
    def pausar_p4 (self):
        self.thread[4].stop()
        self.iniciar_4.setEnabled(True)
        self.pausar_4.setEnabled(False)

        
    def pausar_p5 (self):
        self.thread[5].stop()
        self.iniciar_5.setEnabled(True)
        self.pausar_5.setEnabled(False)

    
    def cancelar_p1 (self):
        self.thread[1].stop()
        self.thread[1].contador = 0
        self.progressBar_1.setValue(0)
        self.iniciar_1.setEnabled(True)
        self.pausar_1.setEnabled(False)
        
    def cancelar_p2 (self):
        self.thread[2].stop()
        self.thread[2].contador = 0
        self.progressBar_2.setValue(0)
        self.iniciar_2.setEnabled(True)
        self.pausar_2.setEnabled(False)
        
    def cancelar_p3 (self):
        self.thread[3].stop()
        self.thread[3].contador = 0
        self.progressBar_3.setValue(0)
        self.iniciar_3.setEnabled(True)
        self.pausar_3.setEnabled(False)
        
    def cancelar_p4 (self):
        self.thread[4].stop()
        self.thread[4].contador = 0
        self.progressBar_4.setValue(0)
        self.iniciar_4.setEnabled(True)
        self.pausar_4.setEnabled(False)
        
    def cancelar_p5 (self):
        self.thread[5].stop()
        self.thread[5].contador = 0
        self.progressBar_5.setValue(0)
        self.iniciar_5.setEnabled(True)
        self.pausar_5.setEnabled(False)
    
    def procesar(self, contador):
        index = self.sender().index
        self.thread[index].cnt = contador
        if index==1:
            if self.thread[index].cnt == 101:
                self.pausar_p1()
            else:
                self.progressBar_1.setValue(self.thread[index].cnt)
        if index==2:
            if self.thread[index].cnt == 101:
                self.pausar_p2()
            else:
                self.progressBar_2.setValue(self.thread[index].cnt)
        if index==3:
            if self.thread[index].cnt == 101:
                self.pausar_p3()
            else:
                self.progressBar_3.setValue(self.thread[index].cnt)
        if index==4:
            if self.thread[index].cnt == 101:
                self.pausar_p4()
            else:
                self.progressBar_4.setValue(self.thread[index].cnt)
        if index==5:
            if self.thread[index].cnt == 101:
                self.pausar_p5()
            else:
                self.progressBar_5.setValue(self.thread[index].cnt)  
    
    def multiprogramacion(self):
        self.iniciar_p1()
        self.iniciar_p2()
        self.iniciar_p3()
        self.iniciar_p4()
        self.iniciar_p5()
        
    def reset(self):
        self.progressBar_1.setValue(0)
        self.thread[1] = Thread(parent=None, index=1)
        self.progressBar_2.setValue(0)
        self.thread[2] = Thread(parent=None, index=2)
        self.progressBar_3.setValue(0)
        self.thread[3] = Thread(parent=None, index=3)
        self.progressBar_4.setValue(0)
        self.thread[4] = Thread(parent=None, index=4)
        self.progressBar_5.setValue(0)
        self.thread[5] = Thread(parent=None, index=5)
        
class Thread(QtCore.QThread):

    signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, index=0):
        super(Thread, self).__init__(parent)
        self.index = index
        self.is_running = True
        self.contador = 0
  
    def run(self):
        print('Iniciando proceso...', self.index)
        cnt = self.contador
        while (cnt <= 100):
            cnt += 1
            time.sleep(0.03)
            self.contador = cnt
            self.signal.emit(cnt)
    
    def stop(self):
        self.is_running = False
        print('Deteniendo proceso...', self.index)
        self.terminate()
  
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = Admin()
	mainWindow.resize(810, 480)
	mainWindow.show()
	sys.exit(app.exec_())