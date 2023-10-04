#!/usr/bin/python

import mysql.connector
import os, csv

def main():
    db_name = os.environ.get("DATABASE_NAME")
    db_root_pass = os.environ.get("MYSQL_ROOT_PASSWORD")
    db_ip_address = os.environ.get("MYSQL_EXTERNAL_IP")
    db_port = os.environ.get("MYSQL_EXTERNAL_PORT")
    csv_file = os.environ.get("CSV_FILE_NAME")
    csv_separator = ";"
    db_table_name =  os.environ.get("DB_TABLE_NAME")
    table_attributes_type = os.environ.get("COLUMN_TYPE")
    priv_key_col_index = int(os.environ.get("PRIM_KEY_COL_INDEX"))

    create_table_query = None
    insert_query = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader) 
        
        data = []
        
        for row in reader:
            record = {}
            
            for i, v in enumerate(row):       
                values = columns = columns_type = "("           
                for j, t in enumerate(headers[i].split(csv_separator)):
                    columns = f"{columns}, {t}"
                    if j == priv_key_col_index:                    
                        columns_type = f"{columns_type}, {t} {table_attributes_type} PRIMARY KEY"
                    else:         
                        columns_type = f"{columns_type}, {t} {table_attributes_type}"
                columns = f"{columns})".replace("(, ", "(")            
                columns_type = f"{columns_type})".replace("(, ", "(")     
                
                for t in v.split(csv_separator):
                    values = f"{values}, \"{t}\""
                values = f"{values})".replace("(, ", "(")

                if create_table_query is None:
                    create_table_query =f"CREATE TABLE IF NOT EXISTS {db_table_name} {columns_type}"

                insert_query.append(f"INSERT INTO {db_table_name} {columns} VALUES {values}")
                
    conn = mysql.connector.connect(
        host = db_ip_address,
        port = db_port, 
        user = "root",
        passwd = db_root_pass,
        database = db_name
    )

    cursor = conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()

    # Insert the lnes
    for c in insert_query:
        try:
            cursor.execute(c)
        except mysql.connector.Error as error:
            if error.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                print(f"Error: Duplicate primary key:\n{c}\n")
            else:
                print("Error: {}".format(error))

    conn.commit()
    conn.close()



if __name__ == "__main__":
    main()