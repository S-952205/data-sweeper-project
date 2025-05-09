import streamlit as st # Streamlit library web app banane ke liye use hoti hai.
import pandas as pd  # Pandas data ko manage aur analyze karne ke liye.
import os  
from io import BytesIO

# Page Configuration aur Title/Description Set Karna
st.set_page_config(page_title="💿 Data Sweeper", layout="wide") 
st.title("💿 Data Sweeper") # Web page ka title set karta hai.
st.write('Transform your files between CSV and Excel with built-in data cleaning and vitualization!') 


uploaded_files = st.file_uploader('Upload your files (CSV or Excel):', type=['csv', 'xlsx'], accept_multiple_files=True)

# Agar user ne koi file upload nahi ki, toh aage ka code run nahi hoga. Yeh condition ensure karti hai
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower() 

        if file_ext == '.csv':
            df = pd.read_csv(file) 
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f'Unspported file type: {file_ext}')
            continue 

        # Display info about the file
        st.write(f'**File Name:** {file.name}')
        st.write(f'**File Size:** {file.size/1024}')


        st.write('🔍 Preview the Head of the DataFrame')
        st.dataframe(df.head()) 

        # Options for Data Cleaning
        st.subheader('🧹 Data Cleaning Options')
        if st.checkbox(f'Clean Data for {file.name}'): 
            col1, col2 = st.columns(2) 

            with col1:
                if st.button(f'Remove Duplicates from {file.name}'):
                    df.drop_duplicates(inplace=True)
                    st.write('Duplicates Removed!')

            with col2:
                if st.button(f'Fill Missing Values for {file.name}'):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write('Missing Values Have been Filled!')

        # Choose Specific Columns to Keep or Convert User ko batana ke ab woh apne file ke data
        st.subheader('🎯 Select Columns to Convert')
        columns = st.multiselect(f'Choose Columns for {file.name}', df.columns, default=df.columns) 
        df = df[columns] 

        # Create Some Vitualizations
        st.subheader('📊 Data Visualization')
        if st.checkbox(f'Show Visualization for {file.name}:'):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        # Convert the File -> CSV to Excel
        st.subheader('🔁 Convertion Options')
        conversion_type = st.radio(f'Convert {file.name} to:', ['CSV', 'Excel'], key=file.name)
        if st.button(f'Convert {file.name}'):
            buffer = BytesIO() 
            if conversion_type == 'CSV':
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, '.csv') 
                mime_type = 'text/csv' 
            
            elif conversion_type == 'Excel':
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, '.xlsx')
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0) 
         

            
             # Download button se user directly converted file ko apne system par download kar sakta hai.
            st.download_button(
                label=f'🔽 Download {file.name} as {conversion_type}',
                data=buffer, 
                file_name=file_name, 
                mime = mime_type
              
            )
            st.success('All files processed!')