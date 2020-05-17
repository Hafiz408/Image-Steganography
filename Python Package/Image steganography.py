from PIL import Image
def encode():
    msg=input("ENCRYPTION\nEnter the encoded message:")
    binary=[]
    for x in msg:
        b=format(ord(x),'08b')
        binary.append(b)
    imgname=input("Enter the image with extension to be encoded:")
    img = Image.open(imgname)
    w,h=img.size
    pixel=img.load()
    x,y=0,1
    num=len(binary)
    pixel[0,0]=123
    for n in range(len(binary)):
        for i in range(8):
            if y==w:
                x=x+1
                y=0
            if binary[n][i]=='0':
                if pixel[x,y]%2!=0:
                    pixel[x,y]=pixel[x,y]-1
                y=y+1
            elif binary[n][i]=='1':
                if pixel[x,y]%2==0:
                    pixel[x,y]=pixel[x,y]-1
                y=y+1
        if y==w:
                x=x+1
                y=0
        if n<num-1:
            pixel[x,y]=100
            y=y+1
        elif n==num-1:
            pixel[x,y]=101
            y=y+1
    imgsave=input("What do you want to save the encoded image as-")
    img.save(imgsave)
    img.close()
    
def decode():
    decoded=""
    imgname=input("Enter the image with extension to be decoded:")
    img=Image.open(imgname)
    pixel=img.load()
    binary=""
    x,y=0,1
    if pixel[0,0]==123:
        while(True):
            if pixel[x,y]==100:
                z=int(binary,2)
                decoded=decoded + chr(z)
                del(binary)
                binary=""
                y=y+1
            elif pixel[x,y]==101:
                z=int(binary,2)
                decoded=decoded + chr(z)
                break
            elif pixel[x,y]%2==0:
                binary=binary + '0'
                y=y+1
            else:
                binary=binary + '1'
                y=y+1
    else:
         decoded="ERROR:No message encoded !!"
    return decoded       
    
    
while(True):   
    choice=int(input("IMAGE STEGANOGRAPHY\n\nMENU\n1.Encode\n2.Decode\nChoice-"))
    if choice==1:
        encode()
    elif choice==2:
        print("Encoded Message-",decode())
    else:
        print("Invalid entry")
    flag=input("Do you wanna continue?")
    if flag=='n':
        break