import socket

host = '127.0.0.1'
port = 12345

def cliente():
  clienteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  clienteSocket.connect((host, port))
  while True:
    peticion = clienteSocket.recv(1024).decode('utf-8')
    print(peticion)
    if peticion == 'solicitudArchivo':
      mandarArchivo(clienteSocket)
    elif peticion != '':
      print('aca')
      recibirArchivo(clienteSocket)
  clienteSocket.close(clienteSocket)

def recibirArchivo(clienteSocket):
  datos = []
  archivoRecibido = clienteSocket.recv(1024)
  datos.append(archivoRecibido)
  while len(archivoRecibido) != 0:
    archivoRecibido = clienteSocket.recv(1024)
    datos.append(archivoRecibido)
  datos = b''.join(datos)

  with open("archivo_recibido.jpg", 'wb') as file:
    file.write(datos)
    print("Archivo recibido y guardado")

def mandarArchivo(clientSocket):
  archivoParaMandar = ''
  rutaArchivo = os.path.join('', archivoParaMandar)
  try:
    with open(rutaArchivo, 'rb') as file:
      datos = file.read()
      clientSocket.send(datos)
      print(f"Archivo '{archivoParaMandar}' enviado a {clientAddress}")
  except FileNotFoundError:
    print(f"El archivo '{archivoParaMandar}' no se encontró")

if __name__ == "__main__":
  cliente()