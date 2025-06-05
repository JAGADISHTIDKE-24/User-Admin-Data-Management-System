#                                           sample code

import streamlit as st
import pandas as pd
from io import BytesIO
from page.db import get_connection

# Required Columns for Validation
REQUIRED_COLUMNS_MANAGED = ["Timestamp", "Email Address", "OCR", "Bill Ref Code", "Track ID", "Annotation ID", "Document Type",
    "Matched Payee ID", "Payer", "Review", "Bill Lines", "Payee Name", "Invoice", "Invoice Date",
    "Invoice Due Date", "Terms", "PO", "Tax Amt", "Total Amt", "Currency", "Foreign Language",
    "Quality Analyst", "Invoice Pages", "Multiple Payees", "Comments", "PST to IST", "US Date",
    "IND Date", "IND Time", "Team", "Agent", "Unique ID", "Priority", "Month", "Hour", "EMEA"]

REQUIRED_COLUMNS_IMPLEMENTATION = ["Timestamp", "Task", "QA Type", "Deal", "Request Type", "IM", "Rocketlane Name", "Location", "Go Live Date",
    "Received Date", "QA_Status", "Errors", "QA_Comments", "Instance_Opportunity", "Instance_Payer",
    "Instance_Status", "Currency", "Instance_Comments", "Addon Entity", "Addon_Payer", "Addon_Status",
    "Addon_Comments", "GC_Payer", "GC_EMail", "GC+Status", "Defects", "Email Address", "Salesforce Name",
    "OCR Vendor", "Deal Type"]

REQUIRED_COLUMNS_PAYEE_SUPPORT = [
    "Timestamp", "Email Address","Unique_ID", "Auxes", "Queue", "Ticket Link", "Payer", "Payee", "Ticket Origin Timestamp", "Assigned Ticket Status", "Query", "Ticket History", "Aphub Status", "Payer Ticket",
    "Account Located", "Managed By", "Zendesk User", "DBR Timestamp", "Agent", "Ticket Link 2", "Accuracy",
    "Observations", "PST to IST", "US Date", "IND Date", "IND Time", "Agent", "Month", "Week", "Hourly"
]
REQUIRED_COLUMNS_PAYEE_SUPPORT_quality= ["Timestamp","Email Address","Unique_ID","Agent Name","Payer","Ticket Link", "Queue","Assigned Ticket Status","Agent Solved","Solved Opportunity",
 	"Incorrect Info","Incomplete Info","FCR","DBR Tagging","Grammatical Errors","Apology / Sympathy",
    "Opening / Closing","Fatal","Fatal Parameters","Query","Comments"
]

TABLE_MANAGED = "managed_services"
TABLE_IMPLEMENTATION = "implementation_DBR"
TABLE_PAYEE_SUPPORT = "payee_support"
TABLE_PAYEE_SUPPORT_quality="payee_support_quality"
COLUMN_DATA_TYPES = {
    "Invoice Date": "datetime64",
    "Invoice Due Date": "datetime64",
    "Total Amt": "float64",
    "Unique ID": "str"
}

# Column Data Type Mapping
COLUMN_DATA_TYPES = {
    "Timestamp": "datetime64",
    "Email Address": "string",
    "OCR": "string",
    "Bill Ref Code": "string",
    "Track ID": "string",
    "Annotation ID": "string",
    "Document Type": "string",
    "Matched Payee ID": "string",
    "Payer": "string",
    "Review": "string",
    "Bill Lines": "Int64",
    "Payee Name": "string",
    "Invoice": "Int64",
    "Invoice Date": "string",
    "Invoice Due Date": "string",
    "Terms": "string",
    "PO": "string",
    "Tax Amt": "float64",
    "Total Amt": "float64",
    "Currency": "string",
    "Foreign Language": "string",
    "Quality Analyst": "string",
    "Invoice Pages": "Int64",
    "Multiple Payees": "string",
    "Comments": "string",
    "PST to IST": "string",
    "US Date": "datetime64",
    "IND Date": "datetime64",
    "IND Time": "datetime64",
    "Team": "string",
    "Agent": "string",
    "Unique ID": "string",
    "Priority": "string",
    "Month": "string",
    "Hour": "Int64",
    "EMEA": "string",
    "Go Live Date":"datetime64",
    "Received Date":"datetime64",
    "Auxes":"string",
    "Queue":"string",
    "Ticket Link":"string",
    "payee":"string",
    "Ticket Origin Timestamp":"string",
    "Assigned Ticket Status":"string",
    "Query":"string",
    "Ticket History":"string",
    "Aphub Status":"string",
    "Payer Ticket":"string",
    "Account Located":"string",
    "Managed By":"string",
    "Zendesk User":"string",
    "DBR Timestamp":"string",
    "Agent":"string",
    "Ticket Link 2":"string",
    "Accuracy":"string",
    "Observations":"string",
    "Agent 2":"string",
    "Week":"Int64",
    "Hourly":"Int64",
    "Unique_ID":"string",
    "Agent Name":"string",
    "Payer":"string",
    "Ticket Link":"string",
    "Queue":"string",
    "Assigned Ticket Status":"string",
    "Agent Solved":"string",
    "Solved Opportunity":"Int64",
    "Incorrect Info":"Int64",
    "Incomplete Info":"Int64",
    "FCR":"Int64",
    "DBR Tagging":"Int64",
    "Grammatical Errors":"Int64",
    "Apology / Sympathy":"Int64",
    "Opening / Closing":"Int64",
    "Fatal":"string",
    "Fatal Parameters":"string",
    "Query":"string",
    "Unique_ID" : "string"
}

# Clean Column Names
def clean_column_names(columns):
    return [col.strip().replace("\xa0", " ") for col in columns]

# Generate a CSV Template
def generate_csv_template(columns):
    df_template = pd.DataFrame(columns=columns)
    buffer = BytesIO()
    df_template.to_csv(buffer, index=False, encoding="utf-8-sig")
    buffer.seek(0)
    return buffer

# Check if Table Exists
def table_exists(connection, table_name):
    with connection.cursor() as cursor:
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        return cursor.fetchone() is not None
def enforce_data_types(df, table_name):
    if table_name in [TABLE_MANAGED, TABLE_IMPLEMENTATION,TABLE_PAYEE_SUPPORT_quality]:
        # For TABLE_MANAGED and TABLE_IMPLEMENTATION
        for column, dtype in COLUMN_DATA_TYPES.items():
            if column in df.columns:
                try:
                    if dtype.startswith("datetime64"):
                        df[column] = pd.to_datetime(df[column], errors="coerce")

                        # Safely convert datetime to string
                        df[column] = df[column].apply(
                            lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else None
                        )
                    elif dtype == "float64":
                        df[column] = pd.to_numeric(df[column], errors="coerce")
                    elif dtype == "Int64":
                        df[column] = pd.to_numeric(df[column], errors="coerce", downcast="integer")
                    else:
                        df[column] = df[column].astype(str).str.strip()
                except Exception as e:
                    st.warning(f"Could not convert column {column} to {dtype}: {e}")

    elif table_name == TABLE_PAYEE_SUPPORT:
        # For TABLE_PAYEE_SUPPORT
        for column, dtype in COLUMN_DATA_TYPES.items():
            if column in df.columns:
                try:
                    if dtype.startswith("datetime64"):
                        df[column] = df[column].astype(str).str.strip()
                        df[column] = pd.to_datetime(df[column], format="%d-%m-%Y %H:%M", errors="coerce")
                        df[column] = df[column].dt.strftime('%Y-%m-%d %H:%M:%S')
                    elif dtype == "float64":
                        df[column] = pd.to_numeric(df[column], errors="coerce")
                    elif dtype == "Int64":
                        df[column] = pd.to_numeric(df[column], errors="coerce", downcast="integer")
                    else:
                        df[column] = df[column].astype(str).str.strip()
                except Exception as e:
                    st.warning(f"Could not convert column {column} to {dtype}: {e}")



    return df

# Insert Data in Batches
def insert_data_in_batches(connection, df, table_name, batch_size=2000):
    insert_query = f"INSERT INTO {table_name} ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({', '.join(['%s'] * len(df.columns))})"
    
    with connection.cursor() as cursor:
        for i in range(0, len(df), batch_size):
            batch_data = [tuple(row.where(pd.notna(row), None)) for _, row in df.iloc[i:i + batch_size].iterrows()]
            cursor.executemany(insert_query, batch_data)
            connection.commit()

def insert_unique_data(connection, df, table_name):
    df.columns = clean_column_names(df.columns)

    # Define primary key based on table
    if table_name == TABLE_MANAGED:
        primary_key_col = "Unique ID"

    elif table_name == TABLE_PAYEE_SUPPORT:
        primary_key_col = "Unique_ID"  # Always compare using "Unique_id"
    
    elif table_name == TABLE_IMPLEMENTATION:
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM `{table_name}`")
            connection.commit()
        insert_data_in_batches(connection, df, table_name)
        st.success(f"Existing records deleted, and new records inserted into {table_name}.")
        return

    else:
        st.error(f"Unique insertion is not supported for table: {table_name}")
        return

    # Validate primary key column exists
    if primary_key_col not in df.columns:
        st.error(f"Missing primary key column: {primary_key_col}")
        return

    # Clean up dataframe
    df.dropna(subset=[primary_key_col], inplace=True)
    df.drop_duplicates(subset=[primary_key_col], inplace=True)

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT `{primary_key_col}` FROM `{table_name}`")
        existing_ids = {row[0] for row in cursor.fetchall()}

    # Filter new records based on existing ones
    new_records = df[~df[primary_key_col].isin(existing_ids)]

    if new_records.empty:
        st.warning(f"No new unique records found for {table_name}.")
        return

    insert_data_in_batches(connection, new_records, table_name)
    st.success(f"{len(new_records)} unique records uploaded successfully to {table_name}.")

def quality_unique_data(connection, df, table_name):
    cursor = connection.cursor()

    # Clean the Unique_ID column in the dataframe
    if "Unique_ID" not in df.columns:
        st.error("Missing 'Unique_ID' column in the uploaded file.")
        return

    df["Unique_ID"] = df["Unique_ID"].astype(str).str.strip().str.lower()
    df["Unique_ID"] = df["Unique_ID"].str.extract(r'(\d+)', expand=False)
    df = df[df["Unique_ID"].notna() & (df["Unique_ID"] != "")]

    # Fetch Unique_IDs from the table
    cursor.execute(f"SELECT `Unique_ID` FROM `{table_name}`")
    existing_ids = cursor.fetchall()
    existing_ids_set = {
        str(row[0]).strip().lower().split()[0] for row in existing_ids if row[0] is not None
    }

    # Filter new records
    new_records = df[~df["Unique_ID"].isin(existing_ids_set)]

    if new_records.empty:
        st.warning("All records already exist in the table. No new data to insert.")
        return

    # Insert only new unique records
    placeholders = ", ".join(["%s"] * len(new_records.columns))
    columns = ", ".join([f"`{col}`" for col in new_records.columns])
    insert_query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"

    cursor.executemany(insert_query, new_records.values.tolist())
    connection.commit()
    cursor.close()

    st.success(f"{len(new_records)} unique records inserted successfully.")
def import_csv_process(table_name, required_columns, truncate=False):
    uploaded_file = st.file_uploader("Choose a file to upload", type=["csv", "xlsx", "json"], key=table_name)
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, dtype=str, low_memory=False)
            df.fillna("", inplace=True)
            df.columns = clean_column_names(df.columns)
            df = enforce_data_types(df, table_name)

            # Check for missing required columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"Invalid file: Missing required columns - {', '.join(missing_columns)}")
                return

            st.write(f"Total records in uploaded file: {len(df)}")
            st.success("File loaded successfully!")

            df.index = df.index + 1  # Start index from 1
            st.dataframe(df)

            if st.button("Upload Data", key=f"upload_{table_name}"):
                connection = get_connection()
                if connection:
                    if table_exists(connection, table_name):
                        if table_name in [TABLE_MANAGED, TABLE_PAYEE_SUPPORT, TABLE_IMPLEMENTATION]:
                            insert_unique_data(connection, df, table_name)
                        elif table_name in [TABLE_PAYEE_SUPPORT_quality]:
                            quality_unique_data(connection, df, table_name)
                        else:
                            insert_data_in_batches(connection, df, table_name)
                            st.success(f"Data uploaded successfully to {table_name}")
                    else:
                        st.error(f"Table {table_name} does not exist. Please create it manually in the database.")
                    connection.close()
                else:
                    st.error("Could not connect to the database.")
        except Exception as e:
            st.error(f"Error loading file: {e}")
    else:
        st.warning("Please upload a file.")

# Streamlit UI
def import_csv_page():
    st.title("Import CSV Data")
    tab1, tab2,tab3,tab4= st.tabs(["Managed Services", "Implementation DBR", "Payee Support","Payee support quality"])
    
    with tab1:
        st.subheader("Import Managed Services Data")
        st.download_button("Download CSV Template", data=generate_csv_template(REQUIRED_COLUMNS_MANAGED), file_name="managed_services.csv", mime="text/csv")
        import_csv_process(TABLE_MANAGED, REQUIRED_COLUMNS_MANAGED)
    
    with tab2:
        st.subheader("Import Implementation DBR Data")
        st.download_button("Download CSV Template", data=generate_csv_template(REQUIRED_COLUMNS_IMPLEMENTATION), file_name="implementation_DBR.csv", mime="text/csv")
        import_csv_process(TABLE_IMPLEMENTATION, REQUIRED_COLUMNS_IMPLEMENTATION, truncate=True)
    
    with tab3:
        st.subheader("Import Payee Support Data")
        st.download_button("Download CSV Template", data=generate_csv_template(REQUIRED_COLUMNS_PAYEE_SUPPORT), file_name="payee_support.csv", mime="text/csv")
        import_csv_process(TABLE_PAYEE_SUPPORT, REQUIRED_COLUMNS_PAYEE_SUPPORT)
    with tab4:
        st.subheader("Import Payee Support Desk Data")
        st.download_button("Download CSV Template", data=generate_csv_template(REQUIRED_COLUMNS_PAYEE_SUPPORT_quality), file_name="payee_support_desk.csv", mime="text/csv")
        import_csv_process(TABLE_PAYEE_SUPPORT_quality, REQUIRED_COLUMNS_PAYEE_SUPPORT_quality)

if __name__ == "__main__":
    import_csv_page()
