import streamlit as st
import pandas as pd
from page.db import get_connection

# Function to fetch unique values for a specific column
def fetch_unique_values(column_name):
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

def fetch_data_by_filters(email_address=None, payers=None, start_date=None, end_date=None, ticket_link=None):
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

# Export Data Page
def payee_support_quality_page():
    st.title("Search and Export Data")

    # Sidebar user profile
    st.sidebar.title("User Profile")
    st.sidebar.info(f"""
    **Name:** {st.session_state.get("username", "Not Available")}  
    **Email:** {st.session_state.get("email", "Not Available")}  
    **Department:** {st.session_state.get("department", "Not Available")}  
    """)

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # Filters
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    email_address = st.selectbox("Email Address", options=[""] + fetch_unique_values("Email Address"))
    payers = st.multiselect("Payers", options=fetch_unique_values("Payer"))
    ticket_link = st.text_input("Ticket Link")


    st.markdown("""
        <style>
            div.stButton > button:first-child {
                background-color: yellow !important;
                color: black !important;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    data = []
    if st.button("Export Data"):
        if not (email_address or payers or start_date or end_date or ticket_link):
            st.warning("Select at least one filter.")
        else:
            data = fetch_data_by_filters(
                email_address=email_address if email_address else None,
                payers=payers if payers else None,
                start_date=start_date,
                end_date=end_date,
                ticket_link=ticket_link if ticket_link else None
            )
            df = pd.DataFrame(data)
            if not df.empty:
                df.index = range(1, len(df) + 1)
                st.write("### Filtered Data")
                st.dataframe(df)
                csv = df.to_csv(index=True)
                st.download_button("Download Data", data=csv, file_name="exported_data.csv", mime="text/csv")
                st.success(f"Total Records Found: {len(df)}")
            else:
                st.warning("No records found.")

if __name__ == "__main__":
    payee_support_quality_page()
