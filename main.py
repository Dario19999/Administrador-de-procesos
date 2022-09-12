from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
import sys, time, os

class Admin(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'admin_procesos.ui'), self)
       
        self.thread={}
        self.iniciar_1.clicked.connect(lambda: self.iniciar(1))
        self.iniciar_2.clicked.connect(lambda: self.iniciar(2))
        self.iniciar_3.clicked.connect(lambda: self.iniciar(3))
        self.iniciar_4.clicked.connect(lambda: self.iniciar(4))
        self.iniciar_5.clicked.connect(lambda: self.iniciar(5))
        
        self.pausar_1.clicked.connect(lambda: self.pausar(1))
        self.pausar_2.clicked.connect(lambda: self.pausar(2))
        self.pausar_3.clicked.connect(lambda: self.pausar(3))
        self.pausar_4.clicked.connect(lambda: self.pausar(4))
        self.pausar_5.clicked.connect(lambda: self.pausar(5))
        
        self.cancelar_1.clicked.connect(lambda: self.cancelar(1))
        self.cancelar_2.clicked.connect(lambda: self.cancelar(2))
        self.cancelar_3.clicked.connect(lambda: self.cancelar(3))
        self.cancelar_4.clicked.connect(lambda: self.cancelar(4))
        self.cancelar_5.clicked.connect(lambda: self.cancelar(5))
        
        self.lotes_btn.clicked.connect(lambda: self.iniciar(1, 'lotes'))
        self.multi_btn.clicked.connect(self.multiprogramacion)
        self.reset_btn.clicked.connect(self.reset)
   
        self.thread[1] = Thread(parent=None, index=1)
        self.thread[1].estado = 'activo'
        self.thread[2] = Thread(parent=None, index=2)
        self.thread[2].estado = 'activo'
        self.thread[3] = Thread(parent=None, index=3)
        self.thread[3].estado = 'activo'
        self.thread[4] = Thread(parent=None, index=4)
        self.thread[4].estado = 'activo'
        self.thread[5] = Thread(parent=None, index=5)
        self.thread[5].estado = 'activo'
        
        self.activo = True
    
    def iniciar (self, num_proceso, modo='boton'):
        if (num_proceso > 1) & (modo == 'lotes'):
            if (num_proceso <= 5)  & (self.thread[num_proceso-1].estado != 'cancelado'): 
                self.thread[num_proceso].start()
                self.thread[num_proceso].signal.connect(self.procesar)
                self.thread[num_proceso].finished.connect(lambda: self.iniciar(num_proceso+1, 'lotes'))
            else:
                self.activo = False
                
        elif modo == 'lotes':
            self.thread[num_proceso].start()
            self.thread[num_proceso].signal.connect(self.procesar)
            self.thread[num_proceso].finished.connect(lambda: self.iniciar(num_proceso+1, 'lotes'))
        else:
            self.thread[num_proceso].start()
            self.thread[num_proceso].signal.connect(self.procesar)
                
        if (num_proceso == 1) & (self.activo):
            self.iniciar_1.setEnabled(False)
            self.pausar_1.setEnabled(True)
            self.cancelar_1.setEnabled(True)            
        if (num_proceso == 2) & (self.activo):
            self.iniciar_2.setEnabled(False)
            self.pausar_2.setEnabled(True)
            self.cancelar_2.setEnabled(True)            
        if (num_proceso == 3) & (self.activo):
            self.iniciar_3.setEnabled(False)
            self.pausar_3.setEnabled(True)
            self.cancelar_3.setEnabled(True)       
        if (num_proceso == 4) & (self.activo):
            self.iniciar_4.setEnabled(False)
            self.pausar_4.setEnabled(True)
            self.cancelar_4.setEnabled(True)       
        if (num_proceso == 5) & (self.activo):
            self.iniciar_5.setEnabled(False)
            self.pausar_5.setEnabled(True)
            self.cancelar_5.setEnabled(True)       
    
    def pausar (self, num_proceso):
        self.thread[num_proceso].stop()   
        if num_proceso == 1:
            self.iniciar_1.setEnabled(True)
            self.pausar_1.setEnabled(False)
            self.cancelar_1.setEnabled(False)
        if num_proceso == 2:
            self.iniciar_2.setEnabled(True)
            self.pausar_2.setEnabled(False)
            self.cancelar_2.setEnabled(False)   
        if num_proceso == 3:
            self.iniciar_3.setEnabled(True)
            self.pausar_3.setEnabled(False)
            self.cancelar_3.setEnabled(False)   
        if num_proceso == 4:
            self.iniciar_4.setEnabled(True)
            self.pausar_4.setEnabled(False)
            self.cancelar_4.setEnabled(False)   
        if num_proceso == 5:
            self.iniciar_5.setEnabled(True)
            self.pausar_5.setEnabled(False)
            self.cancelar_5.setEnabled(False)
            self.reset_btn.setEnabled(True)
    
    def cancelar (self, num_proceso):
        self.thread[num_proceso].contador = 0
        self.thread[num_proceso].estado = 'cancelado'
        self.thread[num_proceso].terminate()
        
        if num_proceso == 1:
            self.progressBar_1.setValue(0)
            self.iniciar_1.setEnabled(True)
            self.pausar_1.setEnabled(False)
            self.cancelar_1.setEnabled(False)
        if num_proceso == 2:
            self.progressBar_2.setValue(0)
            self.iniciar_2.setEnabled(True)
            self.pausar_2.setEnabled(False)
            self.cancelar_2.setEnabled(False)
        if num_proceso == 3:
            self.progressBar_3.setValue(0)
            self.iniciar_3.setEnabled(True)
            self.pausar_3.setEnabled(False)
            self.cancelar_3.setEnabled(False)
        if num_proceso == 4:
            self.progressBar_4.setValue(0)
            self.iniciar_4.setEnabled(True)
            self.pausar_4.setEnabled(False)
            self.cancelar_4.setEnabled(False)
        if num_proceso == 5:
            self.progressBar_5.setValue(0)
            self.iniciar_5.setEnabled(True)
            self.pausar_5.setEnabled(False)
            self.cancelar_5.setEnabled(False)
    
    def procesar(self, contador):
        index = self.sender().index
        self.thread[index].progreso = contador
        if index==1:
            if self.thread[index].progreso == 101:
                self.pausar(index)
                self.iniciar_1.setEnabled(False)
            else:
                self.progressBar_1.setValue(self.thread[index].progreso)
        if index==2:
            if self.thread[index].progreso == 101:
                self.pausar(index)
                self.iniciar_2.setEnabled(False)
            else:
                self.progressBar_2.setValue(self.thread[index].progreso)
        if index==3:
            if self.thread[index].progreso == 101:
                self.pausar(index)
                self.iniciar_3.setEnabled(False)
            else:
                self.progressBar_3.setValue(self.thread[index].progreso)
        if index==4:
            if self.thread[index].progreso == 101:
                self.pausar(index)
                self.iniciar_4.setEnabled(False)               
            else:
                self.progressBar_4.setValue(self.thread[index].progreso)
        if index==5:
            if self.thread[index].progreso == 101:
                self.pausar(index)
                self.iniciar_5.setEnabled(False)
            else:
                self.progressBar_5.setValue(self.thread[index].progreso)  
    
    def multiprogramacion(self):
        self.reset_btn.setEnabled(False)
        self.iniciar(1, 'multi')
        self.iniciar(2, 'multi')
        self.iniciar(3, 'multi')
        self.iniciar(4, 'multi')
        self.iniciar(5, 'multi')
        
    def reset(self):
        self.progressBar_1.setValue(0)
        self.thread[1] = Thread(parent=None, index=1)
        self.iniciar_1.setEnabled(True)
        self.pausar_1.setEnabled(False)
        self.cancelar_1.setEnabled(False)   
        self.thread[1].estado = 'activo'
        
        self.progressBar_2.setValue(0)
        self.thread[2] = Thread(parent=None, index=2)
        self.iniciar_2.setEnabled(True)
        self.pausar_2.setEnabled(False)
        self.cancelar_2.setEnabled(False)   
        self.thread[2].estado = 'activo'
        
        self.progressBar_3.setValue(0)
        self.thread[3] = Thread(parent=None, index=3)
        self.iniciar_3.setEnabled(True)
        self.pausar_3.setEnabled(False)
        self.cancelar_3.setEnabled(False)   
        self.thread[3].estado = 'activo'
        
        self.progressBar_4.setValue(0)
        self.thread[4] = Thread(parent=None, index=4)
        self.iniciar_4.setEnabled(True)
        self.pausar_4.setEnabled(False)
        self.cancelar_4.setEnabled(False)   
        self.thread[4].estado = 'activo'
        
        self.progressBar_5.setValue(0)
        self.thread[5] = Thread(parent=None, index=5)
        self.iniciar_5.setEnabled(True)
        self.pausar_5.setEnabled(False)
        self.cancelar_5.setEnabled(False)   
        self.thread[5].estado = 'activo'
        
class Thread(QtCore.QThread):

    signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, index=0):
        super(Thread, self).__init__(parent)
        self.index = index
        self.is_running = True
        self.contador = 0
  
    def run(self):
        print('Iniciando proceso...', self.index)
        progreso = self.contador
        while (progreso <= 100):
            progreso += 1
            time.sleep(0.03)
            self.contador = progreso
            self.signal.emit(progreso)      
    
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