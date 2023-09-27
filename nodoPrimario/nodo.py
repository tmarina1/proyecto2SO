import grpc
import time
import comunicacion_pb2
import comunicacion_pb2_grpc
import fragmentacion
from google.protobuf.json_format import MessageToDict

pool = [8080, 8081]
data = {}

def nodo():
  global data
  while True:
    print('Menú: ')
    print('1. enviar archivo')
    print('2. reconstruir archivo')
    opcion = int(input())
    if opcion == 1:
      peticion = 'recibirArchivo'
      print('Nombre del archivo: ')
      nombreArchivo = input()
      print('Número de particiones: ')
      numParticiones = int(input())
      fragmentos = fragmentacion.particionarArchivo(nombreArchivo, numParticiones)
      poolRespaldo = pool
      i = 0
      for fragmento in fragmentos:
        respuesta = gRPC(poolRespaldo[i % len(poolRespaldo)], peticion, fragmento, mandarArchivo(fragmento))
        if poolRespaldo[i % len(poolRespaldo)] not in data:
          data[poolRespaldo[i % len(poolRespaldo)]] = []
        data[poolRespaldo[i % len(poolRespaldo)]].append(fragmento)
        print(respuesta)
        i += 1
      print(data)
    elif opcion == 2:
      peticion = 'enviarArchivo'
      for clave, lista_valores in data.items():
        for valor in lista_valores:
          respuestaNodosSecundarios = gRPC1(int(clave), peticion)
          print('holi')
          almacenarArchivo(respuestaNodosSecundarios)
      fragmentacion.reconstruirArchivoParticionados()
      print('Archivo reconstruido satisfactoriamente')

def mandarArchivo(nombreArchivo):
  with open(f'archivosParticionados/{nombreArchivo}', 'rb') as file:
    archivo = file.read()
    return archivo

def almacenarArchivo(response):
  datos = response.archivo
  with open(f'archivosRecibidos/{response.nombreArchivo}', 'wb') as file:
    file.write(datos)
    print("Archivo recibido y guardado")

def gRPC(port, peticion, nombreArchivo, archivo):
  channel = grpc.insecure_channel(f'127.0.0.1:{port}')
  stub = comunicacion_pb2_grpc.messageServiceStub(channel)
  response = stub.message(comunicacion_pb2.instructionRequest(peticion = peticion, nombreArchivo = nombreArchivo, archivo = archivo))
  response  = MessageToDict(response)
  return response

def gRPC1(port, peticion):
  channel = grpc.insecure_channel(f'127.0.0.1:{port}')
  stub = comunicacion_pb2_grpc.messageServiceStub(channel)
  response = stub.message(comunicacion_pb2.instructionRequest(peticion = peticion))
  return response

if __name__ == '__main__':
  nodo()
