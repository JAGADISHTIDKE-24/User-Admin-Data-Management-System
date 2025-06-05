# import streamlit as st
# import pandas as pd
# from page.db import get_connection

# # Function to fetch unique values for a specific column
# def fetch_unique_values(column_name):
#     connection = get_connection()
#     cursor = connection.cursor(dictionary=True)

#     try:
#         # Query to fetch distinct values
#         query = f"SELECT DISTINCT `{column_name}` FROM managed_services WHERE `{column_name}` IS NOT NULL"
#         cursor.execute(query)
#         results = cursor.fetchall()

#         # Extract values as a list
#         return [row[column_name] for row in results]
#     except Exception as e:
#         st.error(f"Error fetching unique values for {column_name}: {e}")
#         return []
#     finally:
#         cursor.close()
#         connection.close()

# # Function to fetch data based on dynamic filters
# def fetch_data_by_filters(email_address=None, OCRs=None, payers=None, start_date=None, end_date=None, bill_ref_code=None, track_id=None, annotation_id=None):
#     connection = get_connection()
#     cursor = connection.cursor(dictionary=True)

#     # Base query
#     query = "SELECT * FROM managed_services WHERE 1=1"
#     parameters = []

#     # Apply filters dynamically
#     if email_address:
#         query += " AND `Email Address` = %s"
#         parameters.append(email_address)
#     if OCRs:
#         query += " AND `OCR` IN (" + ",".join(["%s"] * len(OCRs)) + ")"
#         parameters.extend(OCRs)
#     if payers:
#         query += " AND `payer` IN (" + ",".join(["%s"] * len(payers)) + ")"
#         parameters.extend(payers)
#     if start_date and end_date:
#         query += " AND DATE(`Timestamp`) BETWEEN %s AND %s"
#         parameters.append(start_date.strftime('%Y-%m-%d'))
#         parameters.append(end_date.strftime('%Y-%m-%d'))
#     if bill_ref_code:
#         query += " AND `bill ref code` = %s"
#         parameters.append(bill_ref_code)
#     if track_id:
#         query += " AND `track id` = %s"
#         parameters.append(track_id)
#     if annotation_id:
#         query += " AND `annotation id` = %s"
#         parameters.append(annotation_id)

#     try:
#         # Execute query
#         cursor.execute(query, tuple(parameters))
#         results = cursor.fetchall()

#         return results
#     except Exception as e:
#         st.error(f"Error fetching data: {e}")
#         return []
#     finally:
#         cursor.close()
#         connection.close()

# # Export Data Page
# def admin_export_page():
#     st.title("Search and Export Data")

#     # Filters
#     email_address = st.selectbox("Email Address", options=[""] + fetch_unique_values("Email Address"))
#     OCRs = st.multiselect("OCR", options=fetch_unique_values("OCR"))
#     payers = st.multiselect("Payers", options=fetch_unique_values("payer"))
#     bill_ref_code = st.text_input("Bill Reference Code")
#     track_id = st.text_input("Track ID")
#     annotation_id = st.text_input("Annotation ID")
#     start_date = st.date_input("Start Date", value=None)
#     end_date = st.date_input("End Date", value=None)

#     # Add custom button style
#     st.markdown(
#         """
#         <style>
#             div.stButton > button:first-child {
#                 background-color: yellow !important;
#                 color: black !important;
#                 font-weight: bold;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#     # Initialize data
#     data = []
#     if st.button("Export Data"):
#         data = fetch_data_by_filters(
#             email_address=email_address if email_address else None, 
#             OCRs=OCRs if OCRs else None, 
#             payers=payers if payers else None, 
#             start_date=start_date, 
#             end_date=end_date,
#             bill_ref_code=bill_ref_code if bill_ref_code else None,
#             track_id=track_id if track_id else None,
#             annotation_id=annotation_id if annotation_id else None
#         )
#         if not (email_address or OCRs or payers or start_date or end_date or bill_ref_code or track_id or annotation_id):
#             st.warning("Select any one of the sections to filter data.")
#         else:
#             # Convert data to a DataFrame
#             df = pd.DataFrame(data)

#             # Display total count of filtered records
#             count_records = len(df)

#             # Reset index to start from 1 instead of 0
#             df.index = range(1, count_records + 1)

#             # Show the updated table
#             st.write("### Filter Data")
#             st.dataframe(df)

#             # Export the filtered data as CSV
#             csv = df.to_csv(index=True)  # Keep the new index in the CSV
#             st.download_button(
#                 label="Download Data",
#                 data=csv,
#                 file_name="admin_export_Data.csv",
#                 mime="text/csv"
#             )
#             # Display total count of filtered records
#             total_records = len(df)
#             st.success(f"Total Records Found: {total_records}")

# if __name__ == "__main__":
#     admin_export_page()

import streamlit as st
import pandas as pd
from page.db import get_connection

# --------------------------- Common Utilities ---------------------------

def fetch_unique_values(column_name, table):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = f"SELECT DISTINCT `{column_name}` FROM {table} WHERE `{column_name}` IS NOT NULL"
        cursor.execute(query)
        results = cursor.fetchall()
        return [row[column_name] for row in results]
    except Exception as e:
        st.error(f"Error fetching unique values for {column_name}: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# --------------------------- Managed Services ---------------------------

def fetch_managed_services(email_address=None, OCRs=None, payers=None, start_date=None, end_date=None, bill_ref_code=None, track_id=None, annotation_id=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM managed_services WHERE 1=1"
    parameters = []

    if email_address:
        query += " AND `Email Address` = %s"
        parameters.append(email_address)
    if OCRs:
        query += " AND `OCR` IN (" + ",".join(["%s"] * len(OCRs)) + ")"
        parameters.extend(OCRs)
    if payers:
        query += " AND `payer` IN (" + ",".join(["%s"] * len(payers)) + ")"
        parameters.extend(payers)
    if start_date and end_date:
        query += " AND DATE(`Timestamp`) BETWEEN %s AND %s"
        parameters.append(start_date.strftime('%Y-%m-%d'))
        parameters.append(end_date.strftime('%Y-%m-%d'))
    if bill_ref_code:
        query += " AND `bill ref code` = %s"
        parameters.append(bill_ref_code)
    if track_id:
        query += " AND `track id` = %s"
        parameters.append(track_id)
    if annotation_id:
        query += " AND `annotation id` = %s"
        parameters.append(annotation_id)

    try:
        cursor.execute(query, tuple(parameters))
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# --------------------------- Implementation DBR ---------------------------

def fetch_implementation_data(rocketlane_name=None, task=None, start_date=None, end_date=None, unique_data=False):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM implementation_DBR WHERE 1=1"
    parameters = []

    if start_date and end_date:
        query += " AND DATE(`Timestamp`) BETWEEN %s AND %s"
        parameters.append(start_date.strftime('%Y-%m-%d'))
        parameters.append(end_date.strftime('%Y-%m-%d'))
    if task:
        query += " AND `Task` = %s"
        parameters.append(task)
    if rocketlane_name:
        query += " AND `Rocketlane Name` = %s"
        parameters.append(rocketlane_name)

    try:
        cursor.execute(query, tuple(parameters))
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# --------------------------- Payee Support ---------------------------

def fetch_payee_support_data(email_address=None, payers=None, start_date=None, end_date=None, ticket_link=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM payee_support WHERE 1=1"
    parameters = []

    if email_address:
        query += " AND `Email Address` = %s"
        parameters.append(email_address)
    if payers:
        query += " AND `Payer` IN (" + ",".join(["%s"] * len(payers)) + ")"
        parameters.extend(payers)
        query += " AND `Payee` IN (" + ",".join(["%s"] * len(payers)) + ")"
        parameters.extend(payers)
    if start_date and end_date:
        query += " AND DATE(`Timestamp`) BETWEEN %s AND %s"
        parameters.append(start_date.strftime('%Y-%m-%d'))
        parameters.append(end_date.strftime('%Y-%m-%d'))
    if ticket_link:
        query += " AND `Ticket Link` = %s"
        parameters.append(ticket_link)

    try:
        cursor.execute(query, tuple(parameters))
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []
    finally:
        cursor.close()
        connection.close()


# Add this below the other fetch_unique_values for isolation
def fetch_unique_values_psq(column_name):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = f"SELECT DISTINCT `{column_name}` FROM payee_support_quality WHERE `{column_name}` IS NOT NULL"
        cursor.execute(query)
        results = cursor.fetchall()
        return [row[column_name] for row in results]
    except Exception as e:
        st.error(f"Error fetching unique values for {column_name}: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def fetch_payee_support_quality_data(email_address=None, payers=None, start_date=None, end_date=None, ticket_link=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM payee_support_quality WHERE 1=1"
    parameters = []

    if email_address:
        query += " AND `Email Address` = %s"
        parameters.append(email_address)
    if payers:
        query += " AND `Payer` IN (" + ",".join(["%s"] * len(payers)) + ")"
        parameters.extend(payers)
    if start_date and end_date:
        query += " AND DATE(`Timestamp`) BETWEEN %s AND %s"
        parameters.append(start_date.strftime('%Y-%m-%d'))
        parameters.append(end_date.strftime('%Y-%m-%d'))
    if ticket_link:
        query += " AND `Ticket Link` = %s"
        parameters.append(ticket_link.strip())

    try:
        cursor.execute(query, tuple(parameters))
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []
    finally:
        cursor.close()
        connection.close()


# --------------------------- Main Page ---------------------------

def admin_export_page():
    st.title("Search and Export Data")

    tab1, tab2, tab3,tab4 = st.tabs(["Managed Services", "Implementation DBR", "Payee Support","Payee Support Quality"])

    # Tab 1: Managed Services
    with tab1:
        st.header("Managed Services Export")
        start_date = st.date_input("Start Date", key="ms_start")
        end_date = st.date_input("End Date", key="ms_end")
        email_address = st.selectbox("Email Address", options=[""] + fetch_unique_values("Email Address", "managed_services"))
        OCRs = st.multiselect("OCR", options=fetch_unique_values("OCR", "managed_services"))
        payers = st.multiselect("Payers", options=fetch_unique_values("payer", "managed_services"))
        bill_ref_code = st.text_input("Bill Reference Code")
        track_id = st.text_input("Track ID")
        annotation_id = st.text_input("Annotation ID")

        if st.button("Export Data", key="export_managed_services"):
            if not (email_address or OCRs or payers or start_date or end_date or bill_ref_code or track_id or annotation_id):
                st.warning("Select any one of the sections to filter data.")
            else:
                data = fetch_managed_services(email_address, OCRs, payers, start_date, end_date, bill_ref_code, track_id, annotation_id)
                df = pd.DataFrame(data)
                df.index = range(1, len(df) + 1)
                st.write("### Filter Data")
                st.dataframe(df)
                csv = df.to_csv(index=True)
                st.download_button("Download Data", data=csv, file_name="Managed_service_Data.csv", mime="text/csv")
                st.success(f"Total Records Found: {len(df)}")

    # Tab 2: Implementation DBR
    with tab2:
        st.header("Implementation DBR Export")
        start_date = st.date_input("Start Date", key="dbr_start")
        end_date = st.date_input("End Date", key="dbr_end")
        task = st.selectbox("Task", options=[""] + fetch_unique_values("Task", "implementation_DBR"))
        unique_selection = st.radio("Select Data Type:", ("All Data", "Unique Data"), key="dbr_unique")
        unique_data = unique_selection == "Unique Data"
        rocketlane_name = st.selectbox("Rocketlane Name", options=[""] + fetch_unique_values("Rocketlane Name", "implementation_DBR"))

        if st.button("Export Data", key="export_implementation_dbr"):
            if not (task or start_date or end_date or rocketlane_name):
                st.warning("Select at least one filter to retrieve data.")
            else:
                data = fetch_implementation_data(rocketlane_name, task, start_date, end_date, unique_data)
                df = pd.DataFrame(data)
                if unique_data:
                    df.dropna(axis=1, how='all', inplace=True)
                    df = df.loc[:, (df != "").any()]
                df.index = range(1, len(df) + 1)
                if df.empty:
                    st.warning("No valid data found after applying filters.")
                else:
                    st.write("### Filtered Data")
                    st.dataframe(df)
                    csv = df.to_csv(index=False)
                    st.download_button("Download Data", data=csv, file_name="Implementation DBR_export.csv", mime="text/csv")
                    st.success(f"Total Records Found: {len(df)}")

    # Tab 3: Payee Support
    with tab3:
        st.header("Payee Support Export")
        start_date = st.date_input("Start Date", key="payee_start")
        end_date = st.date_input("End Date", key="payee_end")
        email_address = st.selectbox("Email Address", options=[""] + fetch_unique_values("Email Address", "payee_support"))
        payers = st.multiselect("Payers", options=fetch_unique_values("Payer", "payee_support"))
        ticket_link = st.text_input("Ticket Link")

        if st.button("Export Data", key="export_payee_support"):
            if not (email_address or payers or start_date or end_date or ticket_link):
                st.warning("Select at least one filter.")
            else:
                data = fetch_payee_support_data(email_address, payers, start_date, end_date, ticket_link)
                df = pd.DataFrame(data)
                if not df.empty:
                    df.index = range(1, len(df) + 1)
                    st.write("### Filtered Data")
                    st.dataframe(df)
                    csv = df.to_csv(index=True)
                    st.download_button("Download Data", data=csv, file_name="Payee_Support.csv", mime="text/csv")
                    st.success(f"Total Records Found: {len(df)}")
                else:
                    st.warning("No records found.") 

    # Tab 4: Payee Support Quality
    with tab4:
        st.header("Payee Support Quality Export")
        start_date = st.date_input("Start Date", key="psq_start")
        end_date = st.date_input("End Date", key="psq_end")
        email_address = st.selectbox("Email Address", options=[""] + fetch_unique_values_psq("Email Address"), key="psq_email")
        payers = st.multiselect("Payers", options=fetch_unique_values_psq("Payer"))
        ticket_link = st.text_input("Ticket Link", key="psq_ticket")

        if st.button("Export Data", key="export_payee_support_quality"):
            if not (email_address or payers or start_date or end_date or ticket_link):
                st.warning("Select at least one filter.")
            else:
                data = fetch_payee_support_quality_data(email_address, payers, start_date, end_date, ticket_link)
                df = pd.DataFrame(data)
                if not df.empty:
                    df.index = range(1, len(df) + 1)
                    st.write("### Filtered Data")
                    st.dataframe(df)
                    csv = df.to_csv(index=True)
                    st.download_button("Download Data", data=csv, file_name="payee_support_quality_data.csv", mime="text/csv")
                    st.success(f"Total Records Found: {len(df)}")
                else:
                    st.warning("No records found.")


if __name__ == "__main__":
    admin_export_page()
