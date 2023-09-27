import os
import grpc
import comunicacion_pb2
import comunicacion_pb2_grpc
from concurrent import futures

class messageService(comunicacion_pb2_grpc.messageServiceServicer):
  def message(self, request, context):
    if request.peticion == 'recibirArchivo':
      almacenarArchivo(request)
      return comunicacion_pb2.messageResponse(respuesta = 'Recibido')
    elif request.peticion == 'enviarArchivo':
      archivosDisponibles = os.listdir('archivosRecibidos')
      if archivosDisponibles:
        nombreArchivo = archivosDisponibles[0]
        datosArchivo = mandarArchivo(nombreArchivo)
        os.remove(f'archivosRecibidos/{nombreArchivo}')
        return comunicacion_pb2.messageResponse(respuesta='Enviando archivo', nombreArchivo=nombreArchivo, archivo=datosArchivo)
      else:
        return comunicacion_pb2.messageResponse(respuesta='No hay archivos disponibles')

def almacenarArchivo(reponse):
  datos = reponse.archivo
  with open(f'archivosRecibidos/{reponse.nombreArchivo}', 'wb') as file:
    file.write(datos)
    print("Archivo recibido y guardado")

def mandarArchivo(archivo):
  with open(f'archivosRecibidos/{archivo}', 'rb') as file:
    archivoLeido = file.read()
    return archivoLeido

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  comunicacion_pb2_grpc.add_messageServiceServicer_to_server(messageService(), server)
  server.add_insecure_port('[::]:8080')
  server.start()
  server.wait_for_termination()

if __name__ == '__main__':
    serve()
