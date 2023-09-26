import socket
import os
import particionar_archivo as particionar
#import comprimir_archivos_bin as comprimir

host = '0.0.0.0'
puerto = 12345
mandarArchivos = True
solicitarArchivos = False

directorioArchivos = "archivosParticionados"

def archivoParaMandar():
  global directorioArchivos
  archivos = os.listdir(directorioArchivos)
  if archivos:
    archivoSeleccionado = archivos.pop(0)
    return archivoSeleccionado
  else:
    return None

def servidor():
  global mandarArchivos
  global solicitarArchivos
  serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serverSocket.bind((host, puerto))
  serverSocket.listen(2)

  print(f"Nodo 1 (Servidor) escuchando en {host}:{puerto}")

  while True:
    print("Esperando conexiones entrantes")
    clientSocket, clientAddress = serverSocket.accept()
    print(f"Conexión entrante desde {clientAddress}")

    if mandarArchivos:
      particionar = particinarArchivo('img.jpg', 2)
      archivo = archivoParaMandar()
      solicitud = "envioArchivo"
      clientSocket.send(solicitud.encode())
      mandarArchivo(clientSocket, archivo)
      mandarArchivos = False
      solicitarArchivos = True
    
    if solicitarArchivos:
      solicitud = "solicitudArchivo"
      clientSocket.send(solicitud.encode())
      recibirArchivos(clientSocket)

    clientSocket.close()

def particinarArchivo(rutaArchivo, numFragmentos):
  particionar.particionarArchivo(rutaArchivo, numFragmentos)

'''def comprimirArchivos(archivoEntrada, archivoSalida):
  comprimir.comprimirArchivos(archivoEntrada, archivoSalida)'''

def mandarArchivo(clientSocket, archivoParaMandar):
  global directorioArchivos
  if archivoParaMandar:
    rutaArchivo = os.path.join(directorioArchivos, archivoParaMandar)
    try:
      with open(rutaArchivo, 'rb') as file:
        datos = file.read()
        clientSocket.send(datos)
        print(f"Archivo '{archivoParaMandar}'")
    except FileNotFoundError:
        print(f"El archivo '{archivoParaMandar}' no se encontró")
  else:
    print("No hay más archivos disponibles para enviar.")

def recibirArchivos(clientSocket):
  global directorioArchivos
  datos = []
  archivoRecibido = clientSocket.recv(1024)
  while len(archivoRecibido) != 0:
    datos.append(archivoRecibido)
    archivoRecibido = clientSocket.recv(1024)
  datos = b''.join(datos)
  nombreSalida = os.path.join(directorioArchivos, "archivo_recibido.jpg")

  with open(nombreSalida, 'wb') as file:
    file.write(datos)

  print(f"Archivo '{nombreSalida}' recibido y guardado")

if __name__ == "__main__":
  servidor()
