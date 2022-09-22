from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
import sys, time, os

#Nuestra clase para la main window llamada Admin
class Admin(QtWidgets.QMainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        ui_path = os.path.dirname(os.path.abspath(__file__))
        self.ui = uic.loadUi(os.path.join(ui_path, 'admin_procesos.ui'), self)
       
        #Inicializamos el atributo hilo que contendrá los hilos declarados posteriormente
        self.thread={}
        
        #variables para FCFS y RR
        self.quantum.setText("0")
        self.orden_1.setText("1")
        self.orden_2.setText("2")
        self.orden_3.setText("3")
        self.orden_4.setText("4")
        self.orden_5.setText("5")
        
        self.quantum_value = int(self.quantum.text())
        self.get_order()

        
        #Inicializamos las señales de boton presionado con una funcion lambda para pasar argumentos
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
        
        self.rr_btn.clicked.connect(self.round_robin)
        self.fcfs_btn.clicked.connect(self.fcfs)
        
        self.threads_init()
        #activo se utiliza para hacer toggle del estado de los botones
        self.activo = True
        
    def threads_init (self):
        #Inicializamos un hilo para cada proceso y se le pone 'activo' como estado
        self.thread[self.ord_1] = Thread(parent=None, index=self.ord_1)
        self.thread[self.ord_1].estado = 'activo'
        self.thread[self.ord_2] = Thread(parent=None, index=self.ord_2)
        self.thread[self.ord_2].estado = 'activo'
        self.thread[self.ord_3] = Thread(parent=None, index=self.ord_3)
        self.thread[self.ord_3].estado = 'activo'
        self.thread[self.ord_4] = Thread(parent=None, index=self.ord_4)
        self.thread[self.ord_4].estado = 'activo'
        self.thread[self.ord_5] = Thread(parent=None, index=self.ord_5)
        self.thread[self.ord_5].estado = 'activo'
        
    #La función iniciar recibe el numero del proceso que se va a iniciar y el modo que
    #determina la manera en la que se inicia cada proceso
    def iniciar (self, num_proceso, modo='boton'):
        #En caso de que el modo sea lotes, iniciaremos el siguiente hilo en cuanto termine de procesarse el actual
        if (num_proceso > 1) & (modo == 'lotes'):
            #Si el proceso anterior no está marcado como candelado, iniciamos el proceso siguiente en cuanto termine el actual
            if (num_proceso <= 5)  & (self.thread[num_proceso-1].estado != 'cancelado'): 
                self.thread[num_proceso].start()
                self.thread[num_proceso].signal.connect(self.procesar)
                self.thread[num_proceso].finished.connect(lambda: self.iniciar(num_proceso+1, 'lotes'))
            else:
                self.activo = False
                
       #Si el ya no es el primer proceso lo validamos solo con el modo para que los botones no se desactiven cuando no deben         
        elif modo == 'lotes':
            self.thread[num_proceso].start()
            self.thread[num_proceso].signal.connect(self.procesar)
            self.thread[num_proceso].finished.connect(lambda: self.iniciar(num_proceso+1, 'lotes'))
        else:
            #Este caso es para cuando no se está ejecutando por lotes, no se detecta la señal de finished
            self.thread[num_proceso].start()
            self.thread[num_proceso].signal.connect(self.procesar)
        
        #Aqui se hace una validación para reactivar los botones de cada proceso
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
    
    #la función de pausar se usa para detener el hilo, esta usa la funcion terminate() por lo que los mata también
    def pausar (self, num_proceso):
        #detiene el hilo y togglea el estado de los botones 
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
        #En el caso de canelar un proceso, lo terminamos inmediatamente,
        #reseteamos el contador de progreso y le ponemos el estado de cancelado
        self.thread[num_proceso].contador = 0
        self.thread[num_proceso].estado = 'cancelado'
        self.thread[num_proceso].terminate()
        
        #Se togglea el estado de cada botón dependiendo de cual proceso se cancela
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
    
    #Procesar es la función a la que se conecta el hilo, esta recibe la variable que emite el hilo y la procesa
    #para cada barra de progreso
    def procesar(self, contador):
        #El íncide del proceso es el indice del remitente de la señal (cada proceso)
        index = self.sender().index
        
        #Contador es el argumento que recibe la señal que emite el hilo
        self.thread[index].progreso = contador
        
        #Dependiendo del index del remitente es la barra de progreso a la que se le aumenta el valor
        if index==self.ord_1:
            if self.thread[index].progreso == 101:
                self.pausar(index)
                self.iniciar_1.setEnabled(False)
            else:
                self.progressBar_1.setValue(self.thread[index].progreso)
        if index==self.ord_2:
            if self.thread[index].progreso == 101:
                self.pausar(index)
                self.iniciar_2.setEnabled(False)
            else:
                self.progressBar_2.setValue(self.thread[index].progreso)
        if index==self.ord_3:
            if self.thread[index].progreso == 101:
                self.pausar(index)
                self.iniciar_3.setEnabled(False)
            else:
                self.progressBar_3.setValue(self.thread[index].progreso)
        if index==self.ord_4:
            if self.thread[index].progreso == 101:
                self.pausar(index)
                self.iniciar_4.setEnabled(False)               
            else:
                self.progressBar_4.setValue(self.thread[index].progreso)
        if index==self.ord_5:
            if self.thread[index].progreso == 101:
                self.pausar(index)
                self.iniciar_5.setEnabled(False)
            else:
                self.progressBar_5.setValue(self.thread[index].progreso)  
    
    #El método de multiprogramación ejecuta todos los hilos sumultáneamente con un modo distinto a lotes
    def multiprogramacion(self):
        self.reset_btn.setEnabled(False)
        self.iniciar(1, 'multi')
        self.iniciar(2, 'multi')
        self.iniciar(3, 'multi')
        self.iniciar(4, 'multi')
        self.iniciar(5, 'multi')
    
    #Reset es para reiniciar todos los procesos en 0 para probar distintos casos en el administrador
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
        
    def get_order(self):
        self.ord_1 = int(self.orden_1.text())
        self.ord_2 = int(self.orden_2.text())
        self.ord_3 = int(self.orden_3.text())
        self.ord_4 = int(self.orden_4.text())
        self.ord_5 = int(self.orden_5.text())

    def round_robin(self):
        print(self.quantum_value)
    
    def fcfs(self):
        self.get_order()

        self.threads_init()
        
        self.reset_btn.setEnabled(False)
        
        self.iniciar(1, 'lotes')
        print(self.quantum_value)

#La clase Thread extiende de los QThread de QTCore lo que nos permite hacer override de sus funciones
class Thread(QtCore.QThread):

    #declaramos la señal a emitir de tipo entero
    #la cual será la que aumente el progreso de las barras
    signal = QtCore.pyqtSignal(int)

    #Se declara el constructor de la clase
    def __init__(self, parent=None, index=0):
        super(Thread, self).__init__(parent)
        self.index = index
        self.is_running = True
        self.contador = 0
  
    #Run es el método que inicia el proceso del hilo,
    #Aumentando el contador de la barra de progreso y transmitiendolo
    #a la función de procesar
    def run(self):
        print('Iniciando proceso...', self.index)
        progreso = self.contador
        while (progreso <= 100):
            progreso += 1
            time.sleep(0.03)
            self.contador = progreso
            self.signal.emit(progreso)      
    
    #Stop termina el proceso y cambia el estado del hilo
    def stop(self):
        self.is_running = False
        print('Deteniendo proceso...', self.index)
        self.terminate()

#Nuestro main que inicializa un objeto de Admin, muestra el mainwindow y ejecuta la app
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = Admin()
	mainWindow.resize(810, 880)
	mainWindow.show()
	sys.exit(app.exec_())