import os

libname = 'IC.kicad_sym'

symbols_name = 'IC_temp.kicad_sym'

def file_write(file_name, content):
    try:
        f = open(libname, 'r+')
        fn = open('temp', 'w')
        lines = f.readlines()
        fn.writelines(lines[:-1])
        fn.write(LibAdd)
        fn.write(')')
        f.close()
        fn.close()
        os.remove(libname)
        os.rename('temp', libname)
    except:
        print("File not found " + file_name)


def file_read(file_name):
    try:
        f = open(file_name, 'r')
        result = f.read()
        f.close()
    except:
        print("File not found " + file_name)

    return result
    
if __name__ == "__main__":
    print ('Add New IC Symbol to Kican Lib,Please Input IC name:')
    NewIC = raw_input()
    #print(NewIC)
    Lib = file_read(symbols_name)
    LibAdd = Lib.replace("%%SYMBOL-NAME%%",NewIC)
    
    file_write(libname,LibAdd)