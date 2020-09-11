from noscrypto import Utils

_ENCRYPTION_TABLE = [0x00, 0x20, 0x2D, 0x2E, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x0A, 0x00]
_DECRYPTION_TABLE = [0x00, 0x20, 0x2D, 0x2E, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0xFF, 0x00]

def LoginEncrypt(packet):
    output = []
    
    if packet[-1] != 0xA:
        packet += b'\n'
    
    for b in packet:
        v = b + 0xF
        output.append(v & 0xFF)
        
    return bytes(output)
    
def LoginDecrypt(packet):
    output = []
    
    for b in packet:
        v = (b - 0xF) ^ 0xC3
        output.append(v & 0xFF)
        
    return bytes(output)
    
def WorldEncrypt(packet):
    return Utils._Pack(packet, _ENCRYPTION_TABLE)
    
def WorldDecrypt(packet, session, is_first_packet = False):
    output = []
    
    if not is_first_packet:
        stype = (session >> 6) & 3
    else:
        stype = -1
    
    key = session & 0xFF
    
    for i in packet:
        if stype == 0:
            output.append((i - key - 0x40) & 0xFF)
            
        elif stype == 1:
            output.append((i + key + 0x40) & 0xFF)
            
        elif stype == 2:
            output.append(((i - key - 0x40) ^ 0xC3) & 0xFF)
            
        elif stype == 3:
            output.append(((i + key + 0x40) ^ 0xC3) & 0xFF)
            
        else:
            output.append((i - 0xF) & 0xFF)
            
    return Utils._Unpack(bytes(output), _DECRYPTION_TABLE)