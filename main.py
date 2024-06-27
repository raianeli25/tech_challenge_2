from download_csv import download
from bucket_functions import handle_s3
import pandas as pd
from datetime import date

#download csv file from ibov site
download()

file_path = 'C:\\Users\\raiane.lima\\Downloads'
#convert file from csv to parquet
today = date.today()
today_str = today.strftime('%d-%m-%Y')
data = today_str[:-4]+today_str[-2:]
df = pd.read_csv(file_path+'\\IBOVDia_'+data+'.csv', index_col=False, skiprows=[0], sep=';', encoding='latin-1', engine= 'python')
df.drop(df.tail(2).index,inplace=True) 
df['date'] = today_str
df = df.rename(columns={"Setor":"setor_acao","Código": "cod_acao", "Ação": "nome_acao", "Qtde. Teórica": "qtd_acao", "Part. (%)": "part", "Part. (%)Acum.": "part_acum"})
print(df.head())
print(df.shape)
file_name = 'dados_ibov_'+data+'.parquet'
df.to_parquet(file_name)

#upload file on bucket s3
handle_s3(file_name,\
         'tech-challenge-2',\
         '',\
         '',\
         '',\
         'upload',\
         file_name,\
         'raw_data')
