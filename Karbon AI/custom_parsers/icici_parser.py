import pandas as pd
import pdfplumber
import re

def parse(file_path: str) -> pd.DataFrame:
    """
    Parse ICICI Bank PDF/CSV file and return a pandas DataFrame.
    
    Parameters:
    file_path (str): Path to the PDF/CSV file.
    
    Returns:
    pd.DataFrame: Parsed DataFrame.
    """
    
    # Check if file is a PDF or CSV
    if file_path.endswith('.pdf'):
        # Extract text from PDF using pdfplumber
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        
        # Split text into lines
        lines = text.split('\n')
        
        # Remove empty lines
        lines = [line for line in lines if line.strip()]
        
        # Split lines into columns
        columns = re.split('\s{2,}', lines[0])
        data = []
        for line in lines[1:]:
            values = re.split('\s{2,}', line)
            if len(values) == len(columns):
                data.append(values)
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=columns)
        
    elif file_path.endswith('.csv'):
        # Read CSV file directly
        df = pd.read_csv(file_path)
    
    else:
        raise ValueError("Unsupported file format. Only PDF and CSV are supported.")
    
    # Handle repeated headers
    if df.columns.nunique() != len(df.columns):
        df = df.loc[:, df.columns.duplicated().cumsum().eq(0)]
    
    # Remove empty rows
    df = df.dropna(how='all')
    
    # Replace NaN in numeric columns with 0.0, and strings with ""
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0.0)
        else:
            df[col] = df[col].fillna("")
    
    return df