import lzma

def comprimirArchivos(archivoEntrada, archivoSalida):
    with open(archivoEntrada, 'rb') as archivoEntrada:
        with lzma.open(archivoSalida, 'wb', preset=9) as archivoSalidaComprimido:
            archivoSalidaComprimido.writelines(archivoEntrada)

def descomprimirArchivos(archivoComprimido, archivoSalida):
    with lzma.open(archivoComprimido, 'rb') as archivo:
        with open(archivoSalida, 'wb') as archivoDescomprimido:
            for linea in archivo:
                archivoDescomprimido.write(linea)

if __name__ == "__main__":
    #comprimirArchivos("archivosParticionados/parte_0.bin", "archivosComprimidos/archivo_comprimido.bin")
    #descomprimirArchivos('archivosComprimidos/archivo_comprimido.bin', 'archivoDescomprimido.bin')