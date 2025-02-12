
import io
import zipfile

zip = zipfile.ZipFile("forest.zip", 'r')


def zip_arch(file):    
    data = zip.read(file)
    data_io = io.BytesIO(data)
    return data_io


def file_level_read(file):
    data = zip.read(file)
    return data




