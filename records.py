import streamlit as st 
import pandas as pd
import qrcode
import time
from PIL import Image
import os
from db import create_table,add_record,read_data,delete,filter_person,update,get_person
import numpy as np
import cv2
from pyzbar.pyzbar import decode
timestrf1=time.strftime("%Y%m%d-%H%M%S")
qr=qrcode.QRCode(version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,border=14)
st.header("Generate QR Code and decode QR code")
choice=st.sidebar.selectbox("Menu",['Select a Menu','Create','Read','Update','Delete','Decode'])
create_table()
if choice=='Create':
    st.subheader("Create a QR Code")
    col1,col2=st.columns(2)
    with col1:
        pn=st.text_input("Person name")
        ad=st.text_input("Address")
    with col2:
        cn=st.selectbox("Course",['python','data  science','django'])
        cdt=st.date_input("Course Date")
    if st.button("ADD"):
        add_record(pn,ad,cn,cdt)
        st.success("Record added successfully")
    raw_data={'person_name':pn,'course_name':cn}
    if st.button("QR Code generator"):
        qr.add_data(raw_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        img_filename = '{}{}.png'.format(pn, timestrf1) 
        st.success("Qr code generated successfully")
        path_for_images = os.path.join('qrimages', img_filename)
        img.save(path_for_images)
        final_image = Image.open(path_for_images)
        st.image(final_image)
    
    
elif choice=='Read':
    st.subheader("Reading a database")
    result=read_data()
    #st.write(result)
    df=pd.DataFrame(result,columns=['Person Name','Address','Course','Course Date'])
    with st.expander("View all records"):
        st.write(df)
    with st.expander("View course wise person count"):
        records=df['Course'].value_counts().to_frame()
        st.write(records)
elif choice=='Update':
    st.subheader("Update a database")
    result=read_data()
    #st.write(result)
    df=pd.DataFrame(result,columns=['Person-name','Address','Course','Course_Date'])
    with st.expander("View all records"):
        st.write(df)
    list_of_persons=filter_person()
    #st.write(list_of_persons)
    name_of_person=[i[0] for i in list_of_persons]
    #st.write(name_of_person)
    person=st.selectbox("Select a person name",name_of_person)
    #st.write(person)
    r=get_person(person)
    #st.write(r)
    for i in r:
        address=r[0][1]
        course_name=r[0][2]
        course_date=r[0][3]
    col1,col2=st.columns(2)
    with col1:
        pn=st.text_input("Person name",person)
        ad=st.text_input("Address",address)
    with col2:
        cn=st.selectbox("Course",['python','data  science','django'])
        cdt=st.date_input("Course Date",course_date)
    if st.button("Updated data"):
        update_data=update(ad,cn,cdt,pn)
        st.success(f"Record successfully updated {pn}")
    result=read_data()
    #st.write(result)
    df=pd.DataFrame(result,columns=['Person_name','Address','Course','Course_Date'])
    with st.expander("View all records"):
        st.write(df)
        
    
elif choice=='Delete':
    st.subheader("Delete a database")
    result=read_data()
    #st.write(result)
    df=pd.DataFrame(result,columns=['Person Name','Address','Course','Course Date'])
    with st.expander("View all records"):
        st.write(df)
    list_of_persons=filter_person()
    #st.write(list_of_persons)
    name_of_persons=[i[0]  for i in list_of_persons]
    #st.write(name_of_persons)
    name_of_person=st.selectbox("Select person name",name_of_persons)
    #st.write(name_of_person)
    delete(name_of_person)
    result1=read_data()
    #st.write(result)
    df=pd.DataFrame(result1,columns=['Person Name','Address','Course','Course Date'])
    with st.expander("View all records"):
        st.write(df)
    
    
elif choice=='Decode':
    st.subheader("Decode a database")
    qr_image=st.file_uploader("QR code image",type=['png','jpeg','jpg'])
    
    if qr_image is not None:
        file_bytes = np.asarray(bytearray(qr_image.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        c1, c2 = st.columns(2)
        with c1:
            st.image(opencv_image)
        with c2:
            st.info("Decoded QR Code")
            det = decode(opencv_image)
            #st.write(det)
            for i in det:
                st.write(i[0])
