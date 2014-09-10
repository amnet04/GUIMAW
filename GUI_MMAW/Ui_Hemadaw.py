# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/eudocio/Dropbox/programacion/python/GUI_MMAW/Hemadaw.ui'
#
# Created: Wed Sep 10 00:45:53 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore,  QtWidgets
import os, wave,  csv

'''
Se implementan las funciones que realizaran las operaciones sin intervención de la
platafroma gráfica
'''

# Esta función crea una tubla con nombres que contiene las propiedades del archivo
# y que puede ser usada por la función que escribe los datos al archivo csv
def propiedadesWav(archivo):
    from collections import namedtuple
    nombre=os.path.basename(archivo)
    ubicacion=os.path.dirname(archivo)
    tamanio=os.path.getsize(archivo)
    md5=suma_md5(archivo)
    w=wave.open(archivo,  'rb')
    framerate=w.getframerate()
    sampwidth=w.getsampwidth()
    nchannels=w.getnchannels()
    w.close()
    bitrate=framerate*sampwidth*nchannels
    duracion=str((tamanio-44)/bitrate).replace(".", ",")
    _parametros_wav=namedtuple('_parametros_wav','nombre ubicacion tamanio suma_md5 duracion nchannels sampwidth framerate bitrate')
    return(_parametros_wav(nombre, ubicacion,  tamanio, md5,  duracion,  nchannels, sampwidth, framerate,  bitrate))
    
#Función para  calcular sumas MD5 
def suma_md5(archivo):
     import hashlib
     f = open(archivo, "rb")
     hash=hashlib.md5()
     # Leemos cada linea del archivo
     # y vamos actualizando nuestro algoritmo
     for line in f.readlines():
         hash.update(line)
     f.close()
     # Mostramos la suma en formato de cadena simple
     return (hash.hexdigest())
     
# Esta función toma las variables de directorio de origen y del archivo
# en donde se van a escribir los datos.
# Abre o crea el archivo y el objeto de escritura csv
# como parametro para escribir las columnas utiliza la salida del la 
# función ordenar datos
def  datos_a_csv(directorio_origen,  archivo):
    # el archivo se debe guardar en txt para garantizar que se pueda escoger 
    # la codificación al abrirlo en excel.
    aspc=open(archivo,  "w") 
    # Nombré la variable aspc (archivo separado por comas), para que no se confunda
    # con el nombre de la clase CSV
    writer=csv.writer(aspc,  dialect="excel",  quoting=csv.QUOTE_ALL,  delimiter="\t")
    writer.writerows(ordenar_datos(directorio_origen))
    aspc.close()

# Esta función se encarga de buscar recursivamente los archivos wav en el directorio
# seleccionado y sus subcarpetas
def buscar_wav_recursivamente(directorio_origen):
    coincidencias = []
    for root, dirnames, filenames in os.walk(directorio_origen):
        for filename in filenames:
            if filename.endswith(('.wav')):
                coincidencias.append(os.path.join(root, filename))
    return coincidencias

# esta función examina los datos de cada archivo, extrae sus propiedades
# y las envía a un arreglo para que sean escritas en el archivo de datos
def ordenar_datos (directorio_origen):
    lista=buscar_wav_recursivamente(directorio_origen)
    rows=[["Nombre",  "Ubicacion",  "Tamaño",  "Suma_md5", "Duración",  "# Canales", "Profundidad de muestreo", "Frecuencia de muestreo", "Tasa de bits"]]
    for file in lista:
       rows.append(propiedadesWav(file))
    return (rows)

'''
Apartir de este lugar se implementa la plataforma gráfica
'''

# Creación del formulario    
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(447, 190)

        # Botón para seleccionar el directorio
        self.seleccionarDirectorio = QtWidgets.QPushButton(Form)
        self.seleccionarDirectorio.setGeometry(QtCore.QRect(20, 10, 411, 40))
        self.seleccionarDirectorio.setObjectName("seleccionarDirectorio")
        '''''
        En la siguiente línea se conecta el botón con la función que guarda el
        nombre del directorio que el usuario a elegido
        '''''
        self.seleccionarDirectorio.clicked.connect(self.seleccionDeDirectorio)
        
        # Rótulo que mostrará el directorio seleccionado
        self.rotuloDirectorio = QtWidgets.QLabel(Form)
        self.rotuloDirectorio.setGeometry(QtCore.QRect(20, 50, 411, 20))
        self.rotuloDirectorio.setObjectName("rotuloDirectorio")
        
        #Botón para seleccionar el archivo csv donde se guarda la info
        self.seleccionarCSV = QtWidgets.QPushButton(Form)
        self.seleccionarCSV.setGeometry(QtCore.QRect(20, 70, 411, 40))
        self.seleccionarCSV.setObjectName("seleccionarCSV")
        '''''
        En la siguiente línea se conecta el botón con la función que guarda el
        nombre del archivo csv que el usuario a elegido
        '''''
        self.seleccionarCSV.clicked.connect(self.seleccionDeCSV)  
        
        # Rótulo que mostrará el archivo seleccionado
        self.rotuloArchivo = QtWidgets.QLabel(Form)     
        self.rotuloArchivo.setGeometry(QtCore.QRect(20, 110, 411, 20))
        self.rotuloArchivo.setObjectName("rotuloArchivo")
        
        # Botón para iniciar el proceso de revisión de los wav
        self.iniciarRegistro = QtWidgets.QPushButton(Form)
        self.iniciarRegistro.setGeometry(QtCore.QRect(20, 145, 191, 40))
        self.iniciarRegistro.setObjectName("iniciarRegistro")
        '''''
        En la siguiente línea se conecta el botón con la función que guarda el
        nombre del archivo csv que el usuario a elegido
        '''''
        self.iniciarRegistro.clicked.connect(self.preProcesar)
        
        # Boton para cerrar la ventana
        self.cerrarScript = QtWidgets.QPushButton(Form)
        self.cerrarScript.setGeometry(QtCore.QRect(220, 145, 211, 40))
        self.cerrarScript.setObjectName("cerrarScript")
        
        # Dialogo de alerta
        self.alerta=QtWidgets.QMessageBox()
        self.alerta.setIcon(QtWidgets.QMessageBox.Warning)
 
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    # Función que crea los elementos de texto del formulario
    # (Nombres de botones, contenido de rótulos, etc)
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Herramienta para extracción masiva de datos wav"))
        self.seleccionarDirectorio.setText(_translate("Form", "Selecciona el directorio en el que residen los wav"))
        self.rotuloDirectorio.setText(_translate("Form","No se ha seleccionado ningún directorio"))
        self.seleccionarCSV.setText(_translate("Form", "Seleccionar el archivo csv que almacenará los datos técnicos"))
        self.rotuloArchivo.setText(_translate("Form","No se ha seleccionado ningún archivo para almacenar los datos"))
        self.iniciarRegistro.setText(_translate("Form", "Iniciar registro"))
        self.cerrarScript.setText(_translate("Form", "Cerrar el script"))

    #Función que almacena el nombre del directorio y la muestra en el rótulo respectivo
    def seleccionDeDirectorio(self):
        directorioSeleccionado=QtWidgets.QFileDialog.getExistingDirectory()
        if (directorioSeleccionado!=""):
            self.rotuloDirectorio.setText(directorioSeleccionado)
        else:
            self.rotuloDirectorio.setText("No se ha seleccionado ningún directorio")
        self.Directorio=directorioSeleccionado
    
    #Función que almacena el nombre del archivo csv y la muestra en el rótulo respectivo    
    def seleccionDeCSV(self):
        padreVacio=QtWidgets.QWidget()
        archivoCSV=QtWidgets.QFileDialog.getSaveFileName(padreVacio, '','', '*.txt')
        if (archivoCSV[0]!=""):
            self.rotuloArchivo.setText(archivoCSV[0])
        else:
            self.rotuloArchivo.setText("No se ha seleccionado ningún archivo para almacenar los datos")
        self.Archivo=archivoCSV[0]
      
    
    # Atributos del objeto que recogen los valores arrojados por la selección de
    # directorio y archivo csv
    Directorio=""
    Archivo=""
    
    # Funcion de preprocesamiento, se encarga de revisar si se seleccionaron el
    # Directorio de trabajo y el archivo donde se guardará la información
    def preProcesar(self):
        if (self.Directorio==""):
            self.alerta.setText("No se ha seleccionado ningún directorio")
            self.alerta.show()
        elif (self.Archivo==""):
            self.alerta.setText("No se ha seleccionado ningún archivo txt")
            self.alerta.show()
        else:
            datos_a_csv(self.Directorio,  self.Archivo)
            self.alerta.setText("La operación ha terminado")
            self.alerta.show()
            
    
    
    
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    '''''
    En la siguiente línea se conecta el botón cerrarScript 
    con la función que cierra la ventana
    '''''
    ui.cerrarScript.clicked.connect(Form.close) 
    sys.exit(app.exec_())

