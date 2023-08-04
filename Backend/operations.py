
import pandas as pd 
def add_new_row_to_table(df, table_name, conn,index):
     # Create a DataFrame for the new row data
   
     new_row_df = pd.DataFrame(df, index=[index])  # Assuming the new index is 2

     # Append the new row DataFrame to the 'periodLog' table in the database
     new_row_df.to_sql(table_name, conn, if_exists='append', index_label='id', index=True)






