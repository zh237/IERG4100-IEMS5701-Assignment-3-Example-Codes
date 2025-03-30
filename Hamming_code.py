import numpy as np
import math
from functools import reduce
def Encode(data_bits, verbose=False):
    """Encode a binary array using standard Hamming code (SEC)."""
    m = len(data_bits)
    
    # Step 1: Find number of parity bits required (r)
    r = 0
    while (2 ** r) < (m + r + 1):
        r += 1
    n = m + r  # total encoded length

    # Step 2: Initialize array with parity placeholders (1-based index)
    encoded = [0] * (n + 1)  # index 0 is unused for simplicity
    j = 0  # data bit index

    for i in range(1, n + 1):
        if math.log2(i).is_integer():
            # parity bit position (placeholder, keep as 0 for now)
            encoded[i] = 0
        else:
            encoded[i] = data_bits[j]
            j += 1

    # Step 3: Calculate parity bits
    for i in range(r):
        parity_pos = 2 ** i
        parity = 0
        for j in range(1, n + 1):
            if j & parity_pos and j != parity_pos:
                parity ^= encoded[j]
        encoded[parity_pos] = parity

    # Step 4: Return encoded message (excluding index 0)
    result = encoded[1:]

    if verbose:
        print(f"Data bits: {data_bits}")
        print(f"Total bits (n): {n}, Parity bits (r): {r}")
        print(f"Encoded message: {result}")
    
    return result

def addErrorToCode(encoded, position):

    if position < 1 or position > len(encoded):
        print("Error: Position out of range (must be 1-based index within encoded length)")
        return encoded


    corrupted = encoded[:]  # make a copy
    corrupted[position - 1] ^= 1  # flip the bit (0 ↔ 1)
    return corrupted

def checkForError(received):

    n = len(received)
    r = 0
    while (2 ** r) <= n:
        r += 1

    error_pos = 0

    for i in range(r):
        parity_pos = 2 ** i
        parity = 0
        for j in range(1, n + 1):
            if j & parity_pos:
                parity ^= received[j - 1]
        if parity != 0:
            error_pos += parity_pos

    return error_pos  # 0 means no error

def recoverOriginalMessage(Corrected_code):
    # Remove parity bits to get original data
    n = len(Corrected_code)
    data_bits = []
    for i in range(1, n + 1):
        if not math.log2(i).is_integer():
            data_bits.append(Corrected_code[i - 1])

    return data_bits    

if __name__ == "__main__":
    #array = np.random.randint(0,2,20)
    array = np.array([1,1,0,1])
    Encoded_message = Encode(array, False)
    print("original code : ", array)
    print(f"Hamming code: {Encoded_message}")

    Received_code = addErrorToCode(Encoded_message, 7)
    print("received code: ", Received_code)

    error_position = checkForError(Received_code)
    if error_position == 0:
        print("No error detected.")
        Corrected_code = Received_code
    else:
        print(f"Error detected at position: {error_position}")
        Corrected_code = Received_code[:]
        Corrected_code[error_position - 1] = Received_code[error_position - 1] ^ 1

    Original_code = recoverOriginalMessage(Corrected_code)
    print("recovered code : ", Original_code)
        













