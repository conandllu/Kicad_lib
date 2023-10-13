import os

libname = './symbols/IC.kicad_sym'

IC_TEMP = '  (symbol "%%SYMBOL-NAME%%" (in_bom yes) (on_board yes) \n \
    (property "Reference" "U" (at 0 6.35 0) \n \
        (effects (font (size 1.27 1.27))) \n \
    ) \n \
    (property "Value" "%%SYMBOL-NAME%%" (at 0 -6.35 0) \n \
      (effects (font (size 1.27 1.27))) \n \
    ) \n \
    (property "Footprint" " " (at 0 0 0) \n \
      (effects (font (size 1.27 1.27)) hide) \n \
    ) \n \
    (property "Datasheet" " " (at 0 0 0) \n \
      (effects (font (size 1.27 1.27)) hide) \n \
    ) \n \
    (property "SPEC" " " (at 0 0 0) \n \
      (effects (font (size 1.27 1.27)) hide) \n \
    ) \n \
    (property "Manufacturer" " " (at 0 0 0) \n \
      (effects (font (size 1.27 1.27)) hide) \n \
    )\n \
    (property "Part_Number" " " (at 0 0 0)\n \
      (effects (font (size 1.27 1.27)) hide)\n \
    )\n \
    (property "LCSC_Code" " " (at 0 0 0)\n \
      (effects (font (size 1.27 1.27)) hide)\n \
    )\n \
    (property "LCSC_LibSource" " " (at 0 0 0)\n \
      (effects (font (size 1.27 1.27)) hide)\n \
    )\n \
    (property "ki_description" " " (at 0 0 0)\n \
      (effects (font (size 1.27 1.27)) hide)\n \
    ) \n'
    
IC_TEMP_M0 = '    (symbol "%%SYMBOL-NAME%%_'
IC_TEMP_M1 = '_1" \n\
      (rectangle (start -1.27 1.27) (end 1.27 -1.27) \n\
        (stroke (width 0.254) (type default)) \n\
        (fill (type background)) \n\
      ) \n\
    ) \n'
    
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

def ic_gen(module_num):
    Lib = IC_TEMP
    for i in range(1,(module_num+1)):
        Lib = Lib + IC_TEMP_M0 + str(i) + IC_TEMP_M1
    Lib = Lib + '  ) \n'
    return Lib
    
def do_exit():
    raw_input('Press Any Key To Exit')
    exit(0)
        

if __name__ == "__main__":
    print ('Add New IC Symbol to Kican Lib,Please Input IC name:')
    NewICName = raw_input()
    #print ('Please Input IC SCH module Number:')
    try:
        NewICPart = int(raw_input('Please Input IC SCH module Number:'))
    except:
        print('Please input a number')
        do_exit()
    Check = raw_input('Make sure IC name:'+ NewICName + ',SCH module Number:' + str(NewICPart) + ' y or n:')
    if Check != 'y' :
        do_exit()
        
    #print(NewIC)
    Lib = ic_gen(NewICPart)
    LibAdd = Lib.replace("%%SYMBOL-NAME%%",NewICName)
    #print(LibAdd)
    file_write(libname,LibAdd)
    print('NewIC Add successful')
    do_exit()