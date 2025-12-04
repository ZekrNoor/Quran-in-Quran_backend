import streamlit as st


# Upload a file to a bucket
def upload_file(s3_client, bucket_name, file, file_name):
    try:
        s3_client.upload_fileobj(file, bucket_name, file_name)
        st.success(f"File '{file_name}' uploaded successfully.")
    except Exception as e:
        st.error(f"Error uploading file: {e}")


# Upload file section
def upload_file_section(s3_client, bucket_name):
    st.header("Upload File")
    bucket_name = st.text_input("Enter Bucket Name", value=bucket_name)
    uploaded_file = st.file_uploader("Choose a file to upload")
    if uploaded_file and st.button("Upload"):
        upload_file(s3_client, bucket_name, uploaded_file, uploaded_file.name)
