import pandas as pd
import pdfplumber
import re

def parse(file_path: str) -> pd.DataFrame:
    """
    Parse SBI bank PDF/CSV file and return a pandas DataFrame.
    
    Parameters:
    file_path (str): Path to the PDF/CSV file.
    
    Returns:
    pd.DataFrame: A pandas DataFrame containing the parsed data.
    """
    
    # Check if file is a PDF or CSV
    if file_path.endswith('.pdf'):
        # Use pdfplumber to extract text from PDF
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        
        # Split text into lines
        lines = text.split('\n')
        
        # Remove empty lines
        lines = [line for line in lines if line.strip()]
        
        # Split lines into columns
        columns = []
        for line in lines:
            columns.append(re.split(r'\s{2,}', line))
        
        # Transpose columns
        columns = list(map(list, zip(*columns)))
        
        # Create DataFrame
        df = pd.DataFrame(columns)
        
    elif file_path.endswith(('.csv', '.txt')):
        # Use pandas to read CSV/Text file
        df = pd.read_csv(file_path)
    
    else:
        raise ValueError('Unsupported file format')
    
    # Handle repeated headers
    df.columns = df.columns.astype(str)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(r'\s+', ' ', regex=True)
    df.columns = df.columns.str.strip()
    
    # Remove empty rows
    df = df.dropna(how='all')
    
    # Replace NaN in numeric columns with 0.0
    df = df.apply(lambda x: x.fillna(0.0) if x.dtype in ['int64', 'float64'] else x)
    
    # Replace NaN in string columns with ""
    df = df.apply(lambda x: x.fillna("") if x.dtype == 'object' else x)
    
    return df