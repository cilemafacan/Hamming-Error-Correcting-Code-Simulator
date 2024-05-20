def calculate_number_of_parity(data_length):
    """
    Calculate the number of parity bits needed for a given data length.
    """
    r = 0
    while 2 ** r < data_length + r + 1:
        r += 1
    return r

def xor(a, b):
    """
    XOR operation.
    """
    return a ^ b

def calculate_parity_bit_indexes(number_of_parity_bits):
    """
    Calculate the indexes of the parity bits.
    """
    indexes = []
    for i in range(number_of_parity_bits):
        indexes.append(2 ** i - 1)
    return indexes

def calculate_hamming_code(data, parity_bit_indexes):
    """
    Calculate the Hamming code for a given data.
    """
    hamming_code_length = len(data) + len(parity_bit_indexes)
    hamming_code = [0 for i in range(hamming_code_length)]

    data_indexes = [i for i in range(hamming_code_length) if i not in parity_bit_indexes]
    for i,data_index in enumerate(data_indexes):
        hamming_code[data_index] = data[i]

    for parity_bit_index in parity_bit_indexes:
        xor_result = 0
        for data_index in data_indexes:
            if (data_index + 1) & (parity_bit_index + 1): 
                xor_result = xor(xor_result, hamming_code[data_index])
        hamming_code[parity_bit_index] = xor_result
            
    return hamming_code

def calculate_error_syndrome(hamming_code, parity_bit_indexes):
    """
    Calculate the error syndrome for the given Hamming code.
    """
    error_syndrome = 0
    for parity_bit_index in parity_bit_indexes:
        xor_result = 0
        for i in range(len(hamming_code)):
            if (i + 1) & (parity_bit_index + 1):
                xor_result = xor(xor_result, hamming_code[i])
        if xor_result != 0:
            error_syndrome += parity_bit_index + 1
    return error_syndrome

def correct_error(hamming_code, error_syndrome):
    """
    Correct the error in the Hamming code based on the error syndrome.
    """
    if error_syndrome != 0:
        error_position = error_syndrome - 1
        hamming_code[error_position] = 0 if hamming_code[error_position] == 1 else 1
    return hamming_code