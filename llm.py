import os
import google.generativeai as genai
from dotenv import load_dotenv

from utilities import save_response_to_csv, merge_xml_files_to_string, read_previous_file, read_target_data

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
# Create the model
generation_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)


def compare_source_target():
    response_text = read_previous_file()
    target_data = read_target_data()
    source_data = merge_xml_files_to_string()

    query_text = (
        f"Compare target data: {target_data} with source data: {source_data}.\n"
        f"Prioritize target data. Generate a CSV report. Only output the CSV, no additional text."
        f"The report should have columns: 'Target Table', 'Target Field Name', 'Target Field Datatype', 'Target Key Indicator',"
        f"'Target Field DataType Transform', 'Source Table', 'Source Field Name', 'Source Field Datatype',  'One-to-One','Incremental Ind','Gen_Type', 'Mapping Logic'."
        f"Only include matching attributes. Follow these following conditions."
        f"1) Mark 'One-to-One' as 'YES' if an attribute matches in one source file, otherwise 'NO'. "
        f"2) 'Target Datatype Transforms' should show 'CHANGED' if datatype changes from source to target,  'NO CHANGE' if the data type remains same,and ' ' if source is empty. "
        f"3) 'Target Key Indicator' should be 'NO' if the primary key value of the file is 'na',' ','NULL' or blanks otherwise 'YES'. "
        f"4) 'Gen_Type' should be 'AI Generated' if there is a matching field otherwise put ''. "
        f"5) Leave the 'Incremental Ind' and 'Mapping Logic' field blank."
        f"Do not include column names in the output."
    )

    convo = model.start_chat()
    convo.send_message(query_text)
    response_text += convo.last.text

    save_response_to_csv(response_text=response_text, file_name="source_to_target_mapping")
    return response_text
