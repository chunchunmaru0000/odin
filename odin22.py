try:
    import struct
except ImportError:
    print('cant imagine that')


def writing(file, structure, data: []):
    try:
        file.write(structure.pack(*data))
    except Exception as thrown_error:
        print(f'Error is occurred while writing, the error is {thrown_error}')

try:
    data_structure = struct.Struct('if16s')
except Exception as thrown_error:
    print(f'Error is occurred, {thrown_error}')

with open('odin22.bin', 'wb') as file_for_writing:
    writing(file_for_writing, data_structure, (123, float(123.321), b'Baikal'.ljust(16)))
    writing(file_for_writing, data_structure, (4321, float(123.1234), b'Yarilo'.ljust(16)))
    writing(file_for_writing, data_structure, (4312, float(1234.321), b'Svarog'.ljust(16)))
    print('you are given chance to write some binary data on your own')
    try:
        writing(file_for_writing, data_structure, (int(input('integer variable: ')),
                                                    float(input('float variable: ')),
                                                    input('string variable: ').ljust(16)[:16].encode('utf-8')))
    except Exception as thrown_error:
        print(f'Error is occurred while proceeding writing, the error is {thrown_error}')
    print('successfully written odin22.bin')

# файл весит байта согласно дано (16+4+4)*количество записей

with open('odin22.bin', 'rb') as file_for_writing:
    while True:
        try:
            data = file_for_writing.read(data_structure.size)
            if not data:
                break
            data = data_structure.unpack(data)
            print(data)
        except Exception as thrown_error:
            print(f'there was an error while reading odin22 and its {thrown_error}')
