import math

def _GetMaskPart(ch, charset):
    if ch == 0:
        return False
        
    return ch in charset
    
def _GetMask(packet, charset):
    output = []
    
    for ch in packet:
        if ch == 0x0:
            break
            
        output.append(_GetMaskPart(ch, charset))
        
        
    return output
    
def _CalcLenOfMask(start, mask, value):
    currentLen = 0
    for i in range(start, len(mask)):
        if mask[i] == value:
            currentLen += 1
        else:
            break
            
            
    return currentLen
    
    
def _Pack(packet, chars_to_pack):
    output = []
    mask = _GetMask(packet, chars_to_pack)
    pos = 0
    
    while len(mask) > pos:
        currentChunkLen = _CalcLenOfMask(pos, mask, False)
        
        for i in range(currentChunkLen):
            if pos > len(mask):
                break
                
            if i % 0x7E == 0:
                output.append(min(currentChunkLen - i, 0x7E))
                
            output.append(packet[pos] ^ 0xFF)
            pos += 1
                
        currentChunkLen = _CalcLenOfMask(pos, mask, True)

        for i in range(currentChunkLen):
            if pos > len(mask):
                break
                
            if i % 0x7E == 0:
                output.append(min(currentChunkLen - i, 0x7E) | 0x80)
            
            currentValue = chars_to_pack.index(packet[pos])
            
            if i % 2 == 0:
                output.append(currentValue << 4)
                
            else:
                output[-1] |= currentValue
                
            pos += 1
            
    output.append(0xFF)
    return bytes(output)
    
def _Unpack(packet, chars_to_unpack):
    output = []
    pos = 0
    
    while len(packet) > pos:
        if packet[pos] == 0xFF:
            break
    
        currentChunkLen = packet[pos] & 0x7F
        isPacked = packet[pos] & 0x80
        pos += 1
        
        
        if isPacked:
            for i in range(math.ceil(currentChunkLen / 2)):
                if pos >= len(packet):
                    break
                
                twoChars = packet[pos]
                pos += 1
                
                leftChar = twoChars >> 4
                output.append(chars_to_unpack[leftChar])
                
                rightChar = twoChars & 0xF
                if rightChar == 0:
                    break
                    
                output.append(chars_to_unpack[rightChar])
                
                
        else:
            for i in range(currentChunkLen):
                if pos >= len(packet):
                    break
                    
                output.append(packet[pos] ^ 0xFF)
                pos += 1
                
    return bytes(output)