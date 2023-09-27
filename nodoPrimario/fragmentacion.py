import os

def particionarArchivo(archivoEntrada, numFragmentos):
  try:
    listaArchivos = []
    with open(f'archivosPruebas/{archivoEntrada}', 'rb') as archivoCompleto:
      datos = archivoCompleto.read()
      tamañoFragmento = len(datos) // numFragmentos
      inicio = 0
      contador = 0

      while contador < numFragmentos:
        fin = inicio + tamañoFragmento
        fragmento = datos[inicio:fin]
        nombre = f'parte_{contador}.bin'
        listaArchivos.append(nombre)
        nombreSalida = f'archivosParticionados/{nombre}'
        with open(nombreSalida, 'wb') as salida:
          salida.write(fragmento)
          inicio = fin
          contador += 1
    return listaArchivos
  except:
    print("Error")

def reconstruirArchivoParticionados():
  try:
    fragmentos = []
    for nombreFragmento in os.listdir('archivosParticionados'):
      fragmentos.append(nombreFragmento)
    fragmentos.sort()

    with open('archivoReconstruido.jpg', 'wb') as salida:
      for nombreFragmento in fragmentos:
        rutaFragmento = os.path.join('archivosParticionados', nombreFragmento)
        with open(rutaFragmento, 'rb') as fragmento:
          datos = fragmento.read()
          salida.write(datos)
  except:
    print("Error")

if __name__ == "__main__":
  reconstruirArchivoParticionados()
  #print(particionarArchivo('archivosPruebas/img.jpg', 2))