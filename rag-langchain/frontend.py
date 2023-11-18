import streamlit as st
import requests
st.title('Question Answering over Document')

# Upload PDF file
st.header('Upload Document in PDF format')
pdf_file = st.file_uploader('Upload a PDF file', type=['pdf'])

if pdf_file:
    api_endpoint = 'http://localhost:5000/upload'
    with open(f'data/uploaded_file.pdf', 'wb') as f:
            f.write(pdf_file.getvalue())

    response = requests.post(api_endpoint,json = {"file_path": 'data/uploaded_file.pdf'})
    if response.status_code == 200:
        st.success(f'Uploaded Succesfully!')
    else:
        st.error('Error: Unable to Upload.')


# Text area for entering questions
st.header('Enter your questions')
questions = st.text_area('Enter your questions separated by line breaks')

if st.button('Submit'):
    if questions:
        # Extract text from the uploaded PDF
        api_endpoint = 'http://localhost:5000/chat'
        response = requests.post(api_endpoint,json={'questions': questions})
        if response.status_code == 200:
            data = response.json()            
            st.markdown(f'<div style="color: green;">{data["quation_answer"]}</div>', unsafe_allow_html=True)

        else:
            st.error('Error: Unable to get Answer.')

       