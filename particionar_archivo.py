import os
import json

def crearJson(nombreArchivo, nombreFragmento, destino):
  data[nombreArchivo].append({'Nombre fragmento' : nombreFragmento,
                              'Destino': destino})

def particionarArchivo(archivoEntrada, numFragmentos):
  try:
    with open(archivoEntrada, 'rb') as archivoCompleto:
      datos = archivoCompleto.read()
      tamañoFragmento = len(datos) // numFragmentos
      inicio = 0
      contador = 0

      while contador < numFragmentos:
        fin = inicio + tamañoFragmento
        fragmento = datos[inicio:fin]
        nombre_salida = f'archivosParticionados/parte_{contador}.bin'
        with open(nombre_salida, 'wb') as salida:
          salida.write(fragmento)
          inicio = fin
          contador += 1
  except:
    print("Error")

def reconstruirArchivoParticionados():
  try:
    fragmentos = []
    for nombreFragmento in os.listdir('archivosParticionados'):
      fragmentos.append(nombreFragmento)
    fragmentos.sort()

    with open('archivoRecontruido.jpg', 'wb') as salida:
      for nombreFragmento in fragmentos:
        rutaFragmento = os.path.join('archivosParticionados', nombreFragmento)
        with open(rutaFragmento, 'rb') as fragmento:
          datos = fragmento.read()
          salida.write(datos)
  except:
    print("Error")

if __name__ == "__main__":
  #reconstruirArchivoParticionados()
  #particionarArchivo('img.jpg', 3)

  data = {}
  data['img.jpg'] = []
  crearJson('img.jpg', 'archivosParticionados/parte_0.bin', 1)
  with open('data.json', 'a') as file:
    json.dump(data, file, indent = 4)