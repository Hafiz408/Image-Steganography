import streamlit as st
from PIL import Image
from io import BytesIO

buf = BytesIO()

def encode(msg, image):
    binary=[]
    for x in msg:
        b=format(ord(x),'08b')
        binary.append(b)
    img = Image.open(image)
    name,extension = image.name.rsplit('.', 1)
    img.save(name+'.gif')
    img = Image.open(name+'.gif')
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
    img.save(buf, format='gif')
    byte_im = buf.getvalue()
    return byte_im
    
def decode(image):
    decoded=""
    img=Image.open(image)
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
        return False
    return decoded       

col1,col2 = st.sidebar.columns([4,3])
col1.image("giphy.webp", width=120)
col2.write("")
col2.write("")
col2.write("""# SPY """)   
st.sidebar.write("")
st.sidebar.write("")

cols = st.sidebar.columns([1,1,1])
choice = cols[1].radio("Menu",['Encode','Decode'])

cols = st.columns([3,4,3])
cols[1].image("giphy.webp", width=250)
cols = st.columns([1,2,1])
cols[1].title("|........  SPY  ........|")
st.write("")

if choice == 'Encode':
    cols = st.columns([1,2,1])
    cols[1].write("""#### Encrypt message into an image""")
    st.write("")

    cols = st.columns([1,3,1])
    msg = cols[1].text_area('Enter message to encode:')
    img = cols[1].file_uploader('Upload an image to encode the message:')
    if img:
        encoded_img = encode(msg,img)
        st.write("")
        cols = st.columns([1,1,1])
        cols[1].download_button(
                                label="Download image",
                                data=encoded_img,
                                file_name='Encoded_' + img.name,
                                mime="image/png")

else:
    cols = st.columns([1,2,1])
    cols[1].write("""#### Decrypt message from an image""")
    st.write("")

    cols = st.columns([1,3,1])
    img = cols[1].file_uploader('Upload the image to decode the message:')
    if img:
        decoded_msg = decode(img)
        cols[1].write('### Decoded message:')
        if decoded_msg:
            cols[1].code(decoded_msg)
        else:
            cols[1].warning('No encoded message.')


