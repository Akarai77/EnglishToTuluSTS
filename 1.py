import pandas as pd

# Define file paths
path = r'C:\Users\Akarsh\Downloads\archive (5)'

eng = f'{path}\\en.txt'
kan = f'{path}\\kn.txt'

# Read text files
with open(eng, 'r') as en:
    entext = en.read()

with open(kan, 'r', encoding='utf-8') as kn:
    kntext = kn.read()

# Split lines and ensure equal length
en_word = [line.strip() for line in entext.split('\n')]
kn_word = [line.strip() for line in kntext.split('\n')]

# Align lengths by padding with empty strings if necessary
max_length = max(len(en_word), len(kn_word))
en_word.extend([''] * (max_length - len(en_word)))
kn_word.extend([''] * (max_length - len(kn_word)))

# Create DataFrame for new data
data_to_append = {
    'English': en_word,
    'Kannada': kn_word
}

df_new = pd.DataFrame(data_to_append)

# Define maximum rows per sheet
chunk_size = 1_048_576

# Split the DataFrame into chunks
chunks = [df_new[i:i + chunk_size] for i in range(0, len(df_new), chunk_size)]

# Write chunks to Excel in multiple sheets
with pd.ExcelWriter('./en-kn.xlsx', engine='openpyxl') as writer:
    # Iterate through chunks and write to separate sheets
    for i, chunk in enumerate(chunks):
        sheet_name = f'Sheet{i + 1}'  # Create unique sheet names
        chunk.to_excel(writer, sheet_name=sheet_name, index=False)
