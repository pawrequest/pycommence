import json
import struct

TFR = r'C:\Users\RYZEN\My Drive\WORKBENCH\amherst\commence install\COMMENCE TRANSFER.TFR'


def test_sfgljsd():
    with open(TFR, 'rb') as f:
        data = f.read()
    print(data[:1000])
    print(data[-1000:])


def hexdump(data, length=16):
    result = []
    for i in range(0, len(data), length):
        segment = data[i:i + length]
        hex_bytes = ' '.join(f'{b:02x}' for b in segment)
        ascii_bytes = ''.join(chr(b) if 32 <= b < 127 else '.' for b in segment)
        result.append(f'{i:08x}  {hex_bytes:<{length * 3}}  {ascii_bytes}')
    return '\n'.join(result)


def test_hexdump():
    with open(TFR, 'rb') as file:
        data = file.read()

    print(hexdump(data[:256]))  # Print the first 256 bytes for analysis
    print(hexdump(data[-256:]))  # Print the last 256 bytes for analysis


def parse_tfr_file()-> dict:
    with open(TFR, 'rb') as file:
        data = file.read()

    parsed_data = {}

    # Extract and decode header (first 10 bytes)
    header = data[:10]
    parsed_data['header'] = header.hex()

    # Example of extracting and decoding a section of 16 bytes after the header
    offset = 10
    block_size = 16

    # Extract block
    block = data[offset:offset + block_size]
    parsed_data['block_1'] = block.hex()

    # Decode block as a sequence of integers (for example)
    block_as_integers = struct.unpack_from('4I', block)
    parsed_data['block_1_integers'] = block_as_integers

    # More complex parsing logic would continue here
    offset += block_size
    blocks = []
    while offset < len(data):
        block = data[offset:offset + block_size]
        if len(block) < block_size:
            break
        block_as_integers = struct.unpack_from('4I', block)
        blocks.append(block_as_integers)
        offset += block_size

    parsed_data['blocks'] = blocks

    return parsed_data


def test_parse_tfr_file():
    parsed_output = parse_tfr_file()

    assert 'header' in parsed_output
    assert 'block_1' in parsed_output

    print(parsed_output['header'])

    # print(json.dumps(parsed_output, indent=4))
