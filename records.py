# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 12:42:04 2022

@author: Deepali
"""

import streamlit as st
import pandas as pd
import numpy as np
#mport matplotlib.pyplot as plt
from database import create_table,add_data,view_all_persons,delete,get_department,view_update,update
import qrcode
import os
import time
import cv2
#from pyzbar.pyzbar import decode
from PIL import Image
timestrf1=time.strftime("%Y%m%d-%H%M%S")
qr=qrcode.QRCode(version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,border=14)
#load image
def load_image(img):
    im=Image.open(img)
    return im
def main():
    st.title("QR GENERATION AND AUTHETICATION with Streamlite")
    menu=['Create','Read','Update','Delete','DecoderQR','About']
    choice=st.sidebar.selectbox("Menu",menu)
    create_table()
    if choice=='Create':
        st.subheader("Add Person records")
        col1,col2=st.columns(2)
        with col1:
            person_id=st.number_input("Person ID",1,100,1)
            person_name=st.text_input("Person Name")
        with col2:
            
            person_no=st.text_input("Person Phone No.",max_chars=10)
            #st.warning("Phone no.should be 10 digits")
            person_dept=st.selectbox("Department",['PYTHON','SQL','DATA SCIENCE'])
            person_record_date=st.date_input("Generator Date")
        if st.button("Add Record of Person"):
            add_data(person_id,person_name,person_no,person_dept,person_record_date)
            st.success("Successfully added record:{}{}{}{}{}".format(person_id,person_name,person_no,person_dept,person_record_date))                
            st.subheader("QR Generator")
                  
            
        #with st.form(key='myqr_form'):
        raw_text={'pd':person_id,'per_name':person_name,'person_no':person_no}              
        submit_button=st.button("Generate")
         #layout
        if submit_button:
             col1,col2=st.columns(2)
             with col1:
                qr.add_data(raw_text)
                qr.make(fit=True)
                img=qr.make_image(fill_color='black',back_color='white')
                #filename
                img_filename='generate_image_{}{}.png'.format(person_name,timestrf1)
                path_for_images=os.path.join('image_folder',img_filename)
                img.save(path_for_images)
                final_image=load_image(path_for_images)
                st.image(final_image)
             with col2:
                st.info("Original Text")
                st.write(raw_text)
    elif choice=='Read':
        st.subheader("View Records")
        result=view_all_persons()
        st.write(result)
        df=pd.DataFrame(result,columns=['person_id','person_name','person_no','Department','Date'])
        with st.expander("View all records"):
            st.dataframe(df)
        with st.expander("No.of Department"):
            counts=df['Department'].value_counts().to_frame()
            counts=counts.reset_index()
            st.dataframe(counts)
            #counts_array=np.array(counts)
            #p1=plt.pie(counts)
            #st.plt.show(p1)
    elif choice=='Update':
        st.subheader('Edit/Update Items')
        result=view_all_persons()
        
        df=pd.DataFrame(result,columns=['person_id','person_name','person_no','Department','Date'])
        with st.expander("Current data"):
            st.dataframe(df)
        #st.write(view_update())
        list_of_department=[i[0] for i in view_update()]
        #st.write(list_of_department)
        selected_dept=st.selectbox('Update Department', list_of_department)
        selected_result=get_department(selected_dept)
        #st.write(selected_result)
        if selected_result:
            person_id=selected_result[0][0]
            person_name=selected_result[0][1]
            person_no=selected_result[0][2]
            person_dept=selected_result[0][3]
            person_record_date=selected_result[0][4]
        col1,col2=st.columns(2)
        with col1:
            person_id=st.text_input("Person_id",person_id)
            person_name=st.text_input("Person_name",person_name)
        with col2:
            
        
            person_no=st.text_input("Person_Phone no.",person_no)
            new_person_dept=st.selectbox("Department",['PYTHON','SQL','DATA SCIENCE'])
            new_person_record_date=st.date_input("Person record date")
        if st.button("Updated data of Person"):
            update(new_person_dept,new_person_record_date,person_id)
            st.success("Successfully updated added record:{}::new_person_dept{}".format(person_dept,new_person_dept))         
        result2=view_all_persons()
        df2=pd.DataFrame(result2,columns=['person_id','person_name','person_no','Department','Date'])
        with st.expander("Updated data"):
            st.dataframe(df2)
    elif choice=='Delete':
        st.subheader('Delete the records')
        result=view_all_persons()
        df=pd.DataFrame(result,columns=['person_id','person_name','person_no','Department','Date'])
        with st.expander("current data"):
            st.dataframe(df)
        list_of_department=[i[0] for i in view_update()]
        selected_dept=st.selectbox('Update Department', list_of_department)
        st.warning("Do you want to delete{}".format(selected_dept))
        
        if st.button("Delete data"):
            delete(selected_dept)
            st.success("Data is deleted")
        new_result=view_all_persons()
        df3=pd.DataFrame(new_result,columns=['person_id','person_name','person_no','Department','Date'])
        with st.expander("current data"):
            st.dataframe(df3)
    
    elif choice=='DecoderQR':
        st.subheader("DecoderQR")
        image_file=st.file_uploader("Upload Image",type=['jpg','png','jpeg'])
        if image_file is not None:
            
               #img=load_image(image_file)
               #st.image(img)
               file_bytes=np.asarray(bytearray(image_file.read()),dtype=np.uint8)  
               opencv_image=cv2.imdecode(file_bytes,1)
               c1,c2=st.columns(2)
               with c1:
                   st.image(opencv_image)
               with c2:
                   st.info("Decoded QR Code")
                   det=cv2.QRCodeDetector()
                   retval,points,straight_qrcode=det.detectAndDecode(opencv_image)
                   st.write(retval)
                   st.write(points)
                   st.write(straight_qrcode)           
                    
    else:
        st.subheader('About')
        
if __name__=='__main__':
    main()