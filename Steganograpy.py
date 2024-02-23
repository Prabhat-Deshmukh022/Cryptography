from PIL import Image

#Loading the image and taking its width and height
img1 = Image.open('img1.tiff')
enc = img1.load()
w,h = img1.size


def get_key():#Function to receive the hexa decimal key and assemble it
    key2=[];key3=[]
    key = input("Enter a 16-digit hexadecimal key(0-9; a-f): ")

    if len(key) != 16:
        print("Invalid")
    
    else:
        for i in key:
            #Restricting entry of any character after "f"
            if ord(i)>ord("f"):
                print("Inavlid")
                exit()
            #Obtaining and appending binary equivalent of the integers
            if i.isdigit():
                key2.append(bin(int(i)))
            else:
                key2.append(bin(int(i,16)))

        #Assembling the key as 4 bit string each
        for i in key2:
            if len(i)==3:
                j=i.replace('b',"")
                key3.append("00"+j)
            elif len(i)==4:
                j=i.replace('b',"")
                key3.append("0"+j)
            elif len(i)==5:
                j=i.replace('b',"")
                key3.append(j)
            elif len(i)==6:
                j=i.replace('b',"")
                k=j.replace("0","",1)
                key3.append(k)

        #Assembling the key in 4x4 matrix format
        m = [['0' for i in range(4)] for j in range(4)]
        for r in range(4):
            for c in range(4):
                m[r][c] = key3[r*4+c]
        
        key3 = m 
        return key3

#Converting decimal to binary-
def convert(value):
    n = ''
    while value>0:
        if value % 2 == 0:
            n += '0'
        else:
            n += '1'
        value = value//2
    rev = ''
    for i in range(-1,-len(n)-1,-1):
        rev += n[i]
    n = rev
    return n
    
#Getting an n-bit value-
def bit_n(value,n):
    if(len(value) < n):
        st = ''
        for i in range(n-len(value)):
            st += '0'
        for j in range(n+1-len(value), n+1):
            st += value[j+len(value)-n-1]
        value = st

    return value

#Taking 2 pixels(48 bits) at a time - Each pixel contains 3 bytes, each for R,G and B values
def parity_bit():
    L = []
    x=0
    while x<w-1:
        y=0
        while y<h-1:
            r1,g1,b1 = enc[x,y]
            r2,g2,b2 = enc[x+1,y+1]
            block = bit_n(convert(r1),8)+ bit_n(convert(g1),8) + bit_n(convert(b1),8) + bit_n(convert(r2), 8) + bit_n(convert(g2), 8) + bit_n(convert(b2),8)       

            i = 0
            nblock = ''
            while i < 48:
                s = block[i:i+6]
                c = s.count('1') % 4
            
                if c== 0:
                    nblock += (s + '00')
                elif c==1:
                      nblock += (s + '01')
                elif c== 2:
                    nblock += (s + '10')
                elif c==3:
                    nblock += (s + '11')
                i += 6

            y += 2
        L.append(nblock)
        x += 2
    return L

# print(get_key())
L = parity_bit()
print("Parity bit: ", L[0])

#Assembling the now 64 bit per element list into a 4x4 matrix-
def matrix(L):
    nL = []
    for i in L:
        m = [['0' for i in range(4)] for j in range(4)]
        l = []
        for j in range(0,64,4):
            l.append(i[j:j+4])
        
        for r in range(4):
            for c in range(4):
                m[r][c] = l[r*4+c]

        nL.append(m)
    return nL

#print(matrix(L)[0])

#Accessing the elements in the 4x4 matrix and left shift rotating the individual elements-
def lsr():
    blocks = matrix(L)
    print("Matrix: ", blocks[0])
    nb = []
    for block in blocks:
        nblock = []
        for r in block:
            #['0001','0011','0101','1100]
            nr = []
            for e in r:
                #e = '0001'
                ne = e[1] + e[2] + e[3] + e[0]
                nr.append(ne)
            nblock.append(nr)
        nb.append(nblock)

    blocks = nb
    return blocks

#print(lsr()[0])

def convert_decimal(st):
    d = 0
    for i in range(len(st)):
        d += 2**(len(st)-i-1)*(int(st[i]))
    return d

key = get_key()

def xor():
    blocks = lsr()
    print("Key:", key)
    print("LSR:", blocks[0]) #lsr
    nb = []

    for block in blocks:
        nblock = [[0 for i in range(4)] for j in range(4)]
        for r in range(4):
            for c in range(4):
                nblock[r][c] = bit_n(convert(convert_decimal(block[r][c]) ^ convert_decimal(key[r][c])), 4)
        nb.append(nblock)
    blocks = nb
    return blocks

#print(xor()[0])

def diffusion():
    blocks = xor()
    print("XOR: ", blocks[0])
    nb = []
    
    for block in blocks:
        nblock = []
        for r in block:
            #[0001,0101,1111,1001]
            nblock.append([r[1],r[2],r[3],r[0]])
        nb.append(nblock)

    b = []
    for block in nb:
        nblock = [[0 for i in range(4)] for j in range(4)]

        for r in range(4):
            for c in range(4):
                nblock[r][c] = block[c][r]
        b.append(nblock)
    
    print("AFter diffusion: ",b[0])
    blocks = b
    return blocks



def get_ls_bits(value, n):
    value = value << (8 - n)
    value = value % 256
    return value >> 8 - n

def rem_ls_bits(value, n):
    value = value >> n 
    return value << n

def get_ms_bits(value, n):
    return value >> 8 - n

def shift(value, n):
    return value << 8 - n

def make(data, res):
    image = Image.new("RGB", res)
    image.putdata(data)
    return image


def encrypt():
    blocks = diffusion()
    bits = ''
    
    for block in blocks:
        for r in block:
            for e in r:
                bits += e
    
    L = []
    for i in range(0,len(bits),8):
        L.append(bits[i:i+8])
    
    bits = L

    img2 = Image.open("img2.tiff")
    original = img2.load()
    wo,ho = img2.size

    L = []
    x=0
    while x<wo-1:
        y=0
        while y<ho-1:
            r1,g1,b1 = original[x,y]
            r2,g2,b2 = original[x+1,y+1]
            block = bit_n(convert(r1),8)+ bit_n(convert(g1),8) + bit_n(convert(b1),8) + bit_n(convert(r2), 8) + bit_n(convert(g2), 8) + bit_n(convert(b2),8)       
            L.append(block)
            y += 2 
        x += 2      

    original_bits = ''

    for i in L:
        original_bits += i
    
    l = []
    for i in range(0,len(original_bits),6):
        l.append(original_bits[i:i+6])
    
    original_bits = l

    new = []
    for i in range(len(bits)):
        ni = bit_n(convert(rem_ls_bits(convert_decimal(original_bits[i]),2)), 6)
        msb = bit_n(convert(get_ms_bits(convert_decimal(bits[i]),2)), 6)
        new.append(bit_n(ni + msb, 6))
    
    nst = ''
    for i in new:
        nst += i
    
    nl = []
    for i in range(0,len(nst),24):
        nl.append((int(convert_decimal(nst[i:i+8])), int(convert_decimal(nst[i+8:i+16])), int(convert_decimal(nst[i+16:i+24]))))
    
    new = nl
    return make(new, img2.size)


def decrypt(cipher,key):
    width, height = cipher.size
    encoded_image = cipher.load()

    data = []

    for y in range(height):
        for x in range(width):

            r_encoded, g_encoded, b_encoded = encoded_image[x,y]

            r_encoded = get_ls_bits(r_encoded, 2)
            g_encoded = get_ls_bits(g_encoded, 2)
            b_encoded = get_ls_bits(b_encoded, 2)

            r_encoded = shift(r_encoded, 2)
            g_encoded = shift(g_encoded, 2)
            b_encoded = shift(b_encoded, 2)

            data.append((r_encoded, g_encoded, b_encoded))

    nd=[]
    for t in data:
        nt=(bit_n(convert(t[0]),8)+bit_n(convert(t[1]),8)+bit_n(convert(t[2]),8))
        nd.append(nt)
    
    nst=''
    for i in nd:
        for j in i:
            nst=nst+j

    bits=[]
    for i in range(0,len(nst),64):
        bits.append(nst[i:i+64])
            
    blocks=matrix(bits)

    nb=[]

    for block in blocks:
        nblock=[]
        for r in block:
            nblock.append([r[3]+r[0]+r[1]+r[2]])
        nb.append(nblock)

    blocks=nb
    for block in blocks:
        nblock = [[0 for i in range(4)] for j in range(4)]
        for r in range(4):
            for c in range(4):
                nblock[r][c] = bit_n(convert(convert_decimal(block[r][c]) ^ convert_decimal(key[r][c])), 4)
        nb.append(nblock)
    blocks = nb

    blocks = matrix(L)
    for block in blocks:
        nblock = []
        for r in block:
            nr = []
            for e in r:
                ne = e[3] + e[0] + e[1] + e[2]
                nr.append(ne)
            nblock.append(nr)
        nb.append(nblock)

    blocks = []
    for block in nb:
        nblock=''
        for r in block:
            for e in r:
                nblock+=e
        blocks.append(nblock)

    nb=[]
    for block in blocks:
        for i in range(0,len(block),8):
            nblock=nblock[i:i+6]
        nb.append(nblock)
    blocks=nb

    L=[]
    for block in blocks:
        for i in range(0,len(block),24):
            L.append((convert_decimal(block[i:i+8])),convert_decimal(block[i+8:i+16]),convert_decimal(block[i+16:i+24]))

    data=L
    return make(data, cipher.size)


if "_main_":
    # hidden = "./hidden.png"
    # original = "./original.png"
    encoded = "./encoded.tiff"
    decoded = "./decoded.tiff"
    n = 2

    # hidden = Image.open(hidden)
    # original = Image.open(original)

    while True:
        ch = input("Encode(e) or decode(d)? ")
        if ch == 'e':
            encrypt().save(encoded)

        elif ch == 'd':
            cipher = Image.open(encoded)
            decrypt(cipher,key).save(decoded)
        else:
            break