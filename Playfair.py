#Playfair cipher
def playfair():
    def encrypt():
        plain_text=input("Enter the plain text ")
        keyword=input("Enter the key ")

        or_str="abcdefghiklmnopqrstuvwxyz";list_plain=[];cipher_text=[];column=[]

        i=0
        while i<len(plain_text.lower())-1:
            a=plain_text.lower()[i];b=plain_text.lower()[i+1]
            if a!=b:
                list_plain.append(a+b)
                i=i+2
            elif i==len(plain_text)+1:
                list_plain.append(a+"z")
            else:
                list_plain.append(a+"x")
                i=i+1           

        q=len(plain_text)
        if q%2==0:
            list_plain=list_plain
        else:
            list_plain.append(plain_text.lower()[q-1]+'z')
        print(list_plain)

        matrix=[[] for i in range(5)]

        a=0;b=0

        for i in keyword:
            if i in or_str:
                matrix[a].append(i)
                or_str=or_str.replace(i,'')
                b=b+1
            if b>4:
                a=a+1
                b=0   

        for i in or_str:
            matrix[a].append(i)
            b=b+1
            if b>4:
                a=a+1
                b=0
        print(matrix)

        for i in list_plain:
            rule=False
            for j in matrix:
                if i[0] in j and i[1] in j:
                    j0=j.index(i[0]);j1=j.index(i[1])
                    s=j[(j0+1)%5]+j[(j1+1)%5]
                    cipher_text.append(s)
                    rule=True
            if rule:
                continue

            for j in range(5):
                col="".join([matrix[k][j] for k in range(5)])
                if i[0] in col and i[1] in col:
                    i0=col.index(i[0])
                    i1=col.index(i[1])

                    s=col[(i0+1)%5]+col[((i1+1)%5)]
                    cipher_text.append(s)
                    rule=True
            if rule:
                continue

            for j in range(5):
                row=matrix[j]
                if i[0] in row:
                    i0=j
                    j0=row.index(i[0])

                if i[1] in row:
                    i1=j
                    j1=row.index(i[1])

            cipher_text.append(matrix[i0][j1]+matrix[i1][j0])
            
        print(cipher_text)

    def decrypt():
        cipher_text=input("Enter the cipher text ")
        keyword=input("Enter the key ")

        or_str="abcdefghiklmnopqrstuvwxyz";list_cipher=[];plain_text=[];column=[]

        i=0
        while i<len(cipher_text.lower())-1:
            a=cipher_text.lower()[i];b=cipher_text.lower()[i+1]
            if a!=b:
                list_cipher.append(a+b)
                i=i+2
            elif i==len(plain_text)+1:
                list_cipher.append(a+"z")
            else:
                list_cipher.append(a+"x")
                i=i+1           

        q=len(cipher_text)
        if q%2==0:
            list_cipher=list_cipher
        else:
            list_cipher.append(cipher_text.lower()[q-1]+'z')
        print(list_cipher)

        matrix=[[] for i in range(5)]

        a=0;b=0

        for i in keyword:
            if i in or_str:
                matrix[a].append(i)
                or_str=or_str.replace(i,'')
                b=b+1
            if b>4:
                a=a+1
                b=0   

        for i in or_str:
            matrix[a].append(i)
            b=b+1
            if b>4:
                a=a+1
                b=0
        print(matrix)

        for i in list_cipher:
            rule=False
            for j in matrix:
                if i[0] in j and i[1] in j:
                    j0=j.index(i[0]);j1=j.index(i[1])
                    s=j[(j0-1)]+j[(j1-1)]
                    plain_text.append(s)
                    if j0-1<0 and j1-1<0:
                        j0=5
                        s=j[(j0-1)]
                        plain_text.append(s)
                    
                    rule=True
            if rule:
                continue

            for j in range(5):
                col="".join([matrix[k][j] for k in range(5)])
                if i[0] in col and i[1] in col:
                    i0=col.index(i[0])
                    i1=col.index(i[1])
                    s=col[(i0-1)]+col[(i1-1)]
                    plain_text.append(s)
                    if i0-1<0 and i1-1<0:
                        i0=5
                        s=col[(i0-1)]+col[(i1-1)]
                        plain_text.append(s)
                    rule=True
            if rule:
                continue

            for j in range(5):
                row=matrix[j]
                if i[0] in row:
                    i0=j
                    j0=row.index(i[0])

                if i[1] in row:
                    i1=j
                    j1=row.index(i[1])

            plain_text.append(matrix[i0][j1]+matrix[i1][j0])
            
        print(plain_text)
    
    n=input("Encrypt or Decrypt ")
    if n=="Encrypt":
        encrypt()
    elif n=="Decrypt":
        decrypt()
    else:
        print("Invalid")
playfair()
#End of Playfair cipher


