import psycopg2
from dotenv import load_dotenv

load_dotenv()

import os
import pandas.io.sql as sqlio

# Criando uma conexão com o banco PostgreSQL usando a biblioteca psycopg2
connection = psycopg2.connect(
    user=os.getenv('PG_USER'),
    password=os.getenv('PG_PWD'),
    host=os.getenv('PG_HOST'),
    port=os.getenv('PG_PORT'),
    # database=os.getenv('PG_DATABASE')
)
cursor = connection.cursor()

df_messages = sqlio.read_sql_query(
    """
    select
        *
        , length(prompt) as prompt_length
        , length(response) as response_length
    from public.gpt_messages gm 
    order by gm."_id_message" desc
    """, connection
)

df_users = sqlio.read_sql_query(
    """
    select 
        * 
    from public.gpt_users
    """, connection
)

df_messages_images = sqlio.read_sql_query(
    """
    select
        *
        , length(prompt) as prompt_length
        , length(response) as response_length
        , prompt as image_link_to_google
    from public.gpt_messages gm 
    where type_input = 'image'
    order by gm."_id_message" desc
    """, connection
)

data_path = 'C:/Data/power_bi_data/luciana_dashboard'

df_messages.to_excel(f'{data_path}/gpt_messages_bi.xlsx', sheet_name='data', index=False)
df_users.to_excel(f'{data_path}/gpt_users_bi.xlsx', sheet_name='data', index=False)
df_messages_images.to_excel(f'{data_path}/gpt_messages_image_bi.xlsx', sheet_name='data', index=False)

print('Done!')