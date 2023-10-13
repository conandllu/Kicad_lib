# coding=utf-8

import xlrd
import datetime

lib_name = 'example.xls'
symbols_name = './template.kicad_sym'
output_folder = './symbols/'

# Debug functions


def info(text):
    print("[INFO] " + text)


def warning(text):
    print("[WARNING] " + text)


def error(text):
    print("[ERROR] " + text)
    print("Terminate script")
    exit()


# File read and write functions


def file_write(file_name, content):
    try:
        f = open(output_folder + '/' + file_name, 'w', encoding='utf-8')
        f.write(content)
        f.close()
    except FileNotFoundError:
        error("File not found" + file_name)


def file_read(file_name):
    try:
        f = open(file_name, 'r')
        result = f.read()
        f.close()
    except FileNotFoundError:
        error("File not found " + file_name)

    return result


# Open workbook
info("Try to open workbook - " + lib_name)
try:
    wb = xlrd.open_workbook(lib_name,encoding_override="utf-8")
except FileNotFoundError:
    error("File not found" + lib_name)

# Try to open symbol data
info("Try to open symbol data - " + symbols_name)
symbol_data = file_read(symbols_name)

# Go through sheets
for ws in wb.sheets():
    info("  Read sheet - " + ws.name)

    if ws.name == "Footprint" : #跳过封装sheet
        continue
    # Get file names
    lib_name = ws.name + '.kicad_sym'

    # Init DCM and LIB and create header
    info("    Add lib and dcm header to the files - " + ws.name)
    lib = 'EESchema-LIBRARY Version 2.4\n#encoding utf-8\n'
    now = datetime.datetime.now()
    now = now.strftime("%Y%m%d_%H:%M:%S")
    lib = "(kicad_symbol_lib (version 20211014) (generator conandllu_kicad_symbol_generator_"+ now + ")\n"
    #dcm = 'EESchema-DOCLIB  Version 2.0\n#\n'

    # Get headers
    info("    Get headers")
    headers = {}

    for col_idx in range(0, ws.ncols):
        header = str(ws.cell(0, col_idx).value)
        header = header.upper()
        header = header.replace(' ', '-')
        header = '%%' + header + '%%'
        # info("    Header " + header + " found in positon " + str(col_idx))
        headers[header] = col_idx
    # Check if schematic symbol present
    if "%%SCHEMATIC%%" not in headers.keys():
        error("%%SCHEMATIC%% header not found!")

    # Go through items
    for row_idx in range(1, ws.nrows):
        symbol = ws.cell(row_idx, headers["%%SCHEMATIC%%"]).value
        type = ws.cell(row_idx, headers["%%TYPE%%"]).value

        info("    Look for schematic symbol - " + symbol)
        if symbol_data.find("---" + symbol + "-" + type + "---") == -1:
            error("Symbol not found - " + symbol)

        sym_data = symbol_data[symbol_data.find("---" + symbol + "-" + type + "---")+len("---" + symbol + "-" + type + "---"):]
        sym_data = sym_data[:sym_data.find("---" + symbol + "-" + type + "-END---")] + "\n"
        #sym_data = sym_data.replace(symbol, "%%SYMBOL-NAME%%")

        #info("      Init DCM data")
        #dcm_data = "$CMP %%SYMBOL-NAME%%\nD %%DESCRIPTION%%\nK %%KEYWORDS%%\nF %%DATASHEET%%\n$ENDCMP\n#\n"

        info("      Substitute parameters")
        for header in headers.items():
            key = header[0]
            value = str(ws.cell(row_idx, int(header[1])).value)
            info("      " + key + " = " + value)
            sym_data = sym_data.replace(key, value)
            #dcm_data = dcm_data.replace(key, value)
        info("      Add lib and dcm content to the files - " + ws.name)
        lib += sym_data
        #dcm += dcm_data

    # Create footer
    info("    Add lib and dcm footer to the files - " + ws.name)
    lib += '\n)\n'
    #dcm += '#End Doc Library\n'

    # Write dcm
    info("    Write files - " + ws.name)
    file_write(lib_name, lib)
    #file_write(dcm_name, dcm)