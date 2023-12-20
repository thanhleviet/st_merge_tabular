import streamlit as st
import pandas as pd
import os
import tempfile

# Define a function to merge TSV files and add a filename column
def merge_and_add_filename(files):
    merged_data = pd.DataFrame()
    for file in files:
        # Create a temporary file and save the uploaded content to it
        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix=".tsv")
        temp_file.write(file.read())
        temp_file.close()

        # Read the header (6th line after removing '#') as column names
        with open(temp_file.name, 'r') as f:
            header = next(line for i, line in enumerate(f) if i == 5).lstrip('#')
            header = header.strip().split('\t')

        # Read the data, skipping comment lines
        df = pd.read_csv(temp_file.name, sep='\t', skiprows=lambda x: x < 5)
        df.columns = header  # Set column names

        # df['Filename'] = os.path.basename(file.name).split(".")[0]
        # Add "Filename" column as the first column
        df.insert(0, "Filename", os.path.basename(file.name).split(".")[0])
        merged_data = pd.concat([merged_data, df], ignore_index=True)
        os.remove(temp_file.name)  # Remove the temporary file

    return merged_data

# Streamlit app
def main():
    st.title("Merge TSV Files with Comments and Add Filename Column")

    # Allow users to upload TSV files
    uploaded_files = st.file_uploader("Upload TSV files", type=["tsv", "txt", "tabular"], accept_multiple_files=True)

    if uploaded_files:
        st.write("Uploaded Files:")
        for file in uploaded_files:
            st.write(file.name)

        # Merge and add filename column when a button is clicked
        if st.button("Merge and Add Filename Column"):
            merged_df = merge_and_add_filename(uploaded_files)

            # Display the merged data
            st.write("Merged Data:")
            st.write(merged_df)

            # Download the merged file as a CSV
            csv_data = merged_df.to_csv(index=False)
            st.download_button(
                label="Download Merged Data as CSV",
                data=csv_data,
                file_name="merged_data.csv",
                key="download_csv",
            )

if __name__ == "__main__":
    main()
