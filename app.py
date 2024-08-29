import streamlit as st
import openai
from PIL import Image
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.Client()
print (client)

# Streamlit app title
st.title("Table to CSV Extractor")

# File uploader to upload the image
uploaded_file = st.file_uploader("Upload a table image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Provide information to the user
    st.write("The image will be analyzed based on the following prompt.")

    # Define the detailed prompt
    prompt = (
        "You are an AI assistant tasked with analyzing a table image and extracting its contents into a CSV format. "
        "The table is filled with information about people. Your goal is to understand the table structure, extract "
        "column names and their corresponding values, and output the data in CSV format. Pay close attention to "
        "preserving the table hierarchy and detecting handwritten English text.\n"
        "Do not give pretext, explanation, or any other text than CSV.\n"
        "I want all fields, even if blank. Only one row should be there.\n\n"
        "Here is the table image you need to analyze:\n"
        "<table_image>\n"
        "ATTACHED\n"
        "</table_image>\n\n"
        "Follow these steps to complete the task:\n\n"
        "Analyze the table structure:\n"
        "1. Identify the number of rows and columns in the table.\n"
        "2. Determine if there are any merged cells or nested structures.\n"
        "3. Look for any headers or subheaders that define the table's hierarchy.\n\n"
        "Extract column names:\n"
        "1. Identify all column names in the table, including any subcolumns.\n"
        "2. If there are multiple header rows, combine them to create full column names.\n"
        "3. Ensure that you capture all columns, even if some cells are empty.\n\n"
        "Extract cell values:\n"
        "1. For each row in the table, extract the values corresponding to each column.\n"
        "2. Pay special attention to detecting and accurately transcribing handwritten English text.\n"
        "3. If a cell is empty, represent it as an empty string in your output.\n\n"
        "Preserve table hierarchy:\n"
        "1. If the table has a hierarchical structure (e.g., main columns with subcolumns), reflect this in your column naming.\n"
        "2. Use dot notation to represent the hierarchy (e.g., 'Main Column.Subcolumn').\n\n"
        "Handle special cases:\n"
        "1. If you encounter merged cells, repeat the value for all affected rows/columns as appropriate.\n"
        "2. For any ambiguous or unclear content, make your best interpretation and note any uncertainties.\n\n"
        "Prepare CSV output:\n"
        "1. Create a header row with all the column names you've extracted.\n"
        "2. For each row of data, create a corresponding row in your CSV output.\n"
        "3. Ensure that the number of fields in each row matches the number of columns in the header.\n"
        "4. Use commas to separate fields and newlines to separate rows."
    )

    # Call the OpenAI API with the updated method for GPT-4o Mini
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Ensure this is the correct model name
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500  # Adjust based on your expected output length
    )

    # Extract the CSV output from the response
    csv_output = response.choices[0].message['content'].strip()

    # Display the CSV output in the app
    st.subheader("Extracted CSV Data")
    st.text(csv_output)

    # Provide download option for the CSV output
    st.download_button(
        label="Download CSV",
        data=csv_output,
        file_name="extracted_table.csv",
        mime="text/csv"
    )