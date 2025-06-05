# import datetime
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from page.db import get_connection

# # Function to fetch data from the database
# def fetch_data(query, params):
#     connection = get_connection()
#     if not connection:
#         return None, "Failed to connect to the database."
    
#     try:
#         with connection.cursor(dictionary=True) as cursor:
#             cursor.execute(query, params)
#             result = cursor.fetchall()
#         return pd.DataFrame(result), None
#     except Exception as e:
#         return None, str(e)
#     finally:
#         connection.close()

# # SQL Queries
# QUERIES = {
#     "processing_tool_usage": """
#         SELECT OCR, COUNT(*) AS user_count
#         FROM managed_services
#         WHERE OCR IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY OCR
#         ORDER BY user_count DESC;
#     """,
#     "top_payers": """
#         SELECT payer, COUNT(*) AS payer_count
#         FROM managed_services
#         WHERE payer IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY payer
#         ORDER BY payer_count DESC
#         LIMIT 20;
#     """,
#     "emea_distribution": """
#         SELECT EMEA, COUNT(*) AS count
#         FROM managed_services
#         WHERE EMEA IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY EMEA
#         ORDER BY count DESC;
#     """,
#     "priority_distribution": """
#         SELECT priority, COUNT(*) AS count
#         FROM managed_services
#         WHERE priority IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY priority
#         ORDER BY count DESC;
#     """,
#     "top_languages": """
#         SELECT `foreign language` AS language, COUNT(*) AS count
#         FROM managed_services
#         WHERE `foreign language` IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY `foreign language`
#         ORDER BY count DESC
#         LIMIT 5;
#     """,
#     "implementation_dbr": """
#         SELECT TASK, COUNT(*) AS count 
#         FROM implementation_DBR
#         WHERE TASK IS NOT NULL AND timestamp BETWEEN %s AND %s
#         GROUP BY TASK
#         ORDER BY count DESC;
#     """

# }

# # Admin Dashboard
# def admin_dashboard():
#     st.title("Admin Dashboard")

#     # Tabs
#     tab1, tab2 ,tab3,tab4= st.tabs(["Managed Service", "Implementation DBR","Payee support","Payee Support Quality"])

#     with tab1:
#         st.subheader("Managed Service Dashboard")
#         today = datetime.datetime.now()
#         jan_1 = datetime.date(2020, 1, 1)
#         dec_31 = datetime.date(2028, 12, 31)

#         date_range = st.date_input("Enter Date Range", (jan_1, today.date()), jan_1, dec_31, format="MM.DD.YYYY")

#         if isinstance(date_range, tuple) and len(date_range) == 2:
#             start_date, end_date = date_range
#         else:
#             st.warning("Please select a valid date range.")
#             return

#         if start_date > end_date:
#             st.error("Start date cannot be after end date.")
#             return

#         # Colors
#         colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]
#         color_index = 0

#         data_fetchers = {
#             "OCR wise volume": ("processing_tool_usage", "OCR", "user_count"),
#             "Top Payers": ("top_payers", "payer", "payer_count"),
#             "EMEA Contribution": ("emea_distribution", "EMEA", "count"),
#             "Priority Distribution": ("priority_distribution", "priority", "count"),
#             "Top 5 Languages": ("top_languages", "language", "count"),
#         }

#         for section, (query_key, x_col, y_col) in data_fetchers.items():
#             df, error = fetch_data(QUERIES[query_key], (start_date, end_date))
#             if error:
#                 st.error(f"Error fetching {section.lower()} data: {error}")
#                 continue
            
#             if df.empty:
#                 continue

#             st.subheader(section)
#             color = colors[color_index % len(colors)]
#             color_index += 1

#             if section == "Top Payers":
#                 df = df.sort_values(by=y_col, ascending=True)
#                 fig = px.bar(df, x=y_col, y=x_col, text=y_col, orientation="h", title=section, color_discrete_sequence=[color])
#                 fig.update_traces(textposition="inside")
#                 st.plotly_chart(fig)
#             elif section == "OCR wise volume":
#                 fig = px.bar(df, x=x_col, y=y_col, text=y_col, orientation="v", title=section, color_discrete_sequence=[color])
#                 fig.update_traces(textposition="outside")
#                 st.plotly_chart(fig)
#             elif section in ["EMEA Contribution", "Priority Distribution"]:
#                 df["percentage"] = (df[y_col] / df[y_col].sum()) * 100
#                 fig = px.pie(df, names=x_col, values="percentage", title=f"{section} in Percentage", color_discrete_sequence=[color])
#                 st.plotly_chart(fig)
#             elif section == "Top 5 Languages":
#                 df["percentage"] = (df[y_col] / df[y_col].sum()) * 100
#                 df.loc[len(df)] = ["Total", df[y_col].sum(), df["percentage"].sum()]
#                 df.index = range(1, len(df) + 1)
#                 st.write(df)

#     with tab2:
#         st.subheader("Implementation DBR Dashboard")

#         # Date Range Selection
#         date_range = st.date_input("Enter Date Range", (datetime.date(2022, 1, 1), datetime.datetime.now().date()), format="MM.DD.YYYY", key="dbr_date")
        
#         # Validate Date Range Selection
#         if len(date_range) != 2 or date_range[0] > date_range[1]:
#             st.error("Invalid date range. Please select a valid range.")
#         else:
#             start_date, end_date = date_range

#             # Convert to string format YYYY-MM-DD for SQL query
#             start_date_str = start_date.strftime("%Y-%m-%d")
#             end_date_str = end_date.strftime("%Y-%m-%d")

#             # Fetch Data
#             df, error = fetch_data(QUERIES["implementation_dbr"], (start_date_str, end_date_str))

#             if error:
#                 st.error(f"Error fetching Implementation DBR data: {error}")
#             elif df.empty:
#                 st.warning("No data found for the selected date range.")
#             else:
#                 # Task Distribution Chart
#                 st.subheader("Task Distribution")
#                 task_counts = df.groupby("TASK")["count"].sum().reset_index().sort_values(by="count", ascending=False)
                
#                 if not task_counts.empty:
#                     fig = px.bar(task_counts, x="TASK", y="count", title="Task Distribution", text="count",color_discrete_sequence=["#EF553B"])
#                     fig.update_traces(textposition="outside")
#                     st.plotly_chart(fig)
#                 else:
#                     st.warning("No task data available for the selected date range.")
#     with tab3:
#         st.subheader("Payee Support Dashboard")

#         # Date Range Selection
#         date_range = st.date_input("Enter Date Range", (datetime.date(2022, 1, 1), datetime.datetime.now().date()), format="MM.DD.YYYY", key="payee_date")
        
#         # Validate Date Range Selection
#         if len(date_range) != 2 or date_range[0] > date_range[1]:
#             st.error("Invalid date range. Please select a valid range.")
#         else:
#             start_date, end_date = date_range

#             # Convert to string format YYYY-MM-DD for SQL query
#             start_date_str = start_date.strftime("%Y-%m-%d")
#             end_date_str = end_date.strftime("%Y-%m-%d")

#             # Query for distinct count of Queue
#             queue_query = """
#             SELECT Queue, COUNT(DISTINCT `Ticket Link`) AS count
#             FROM payee_support
#             WHERE `Ticket Link` IS NOT NULL 
#             AND Queue IS NOT NULL 
#             AND TRIM(Queue) != '' 
#             AND timestamp BETWEEN %s AND %s
#             GROUP BY Queue
#             ORDER BY count DESC;


#             """

#             df, error = fetch_data(queue_query, (start_date_str, end_date_str))

#             if error:
#                 st.error(f"Error fetching Payee Support data: {error}")
#             elif df.empty:
#                 st.warning("No data found for the selected date range.")
#             else:
#                 st.subheader("Queue Distribution")
#                 fig = px.bar(df, x="Queue", y="count", text="count", title="Queue Count by Type", color_discrete_sequence=["#00CC96"])
#                 fig.update_traces(textposition="outside")
#                 st.plotly_chart(fig)

#     with tab4:
#         st.subheader("Payee Support Quality Dashboard")

#         # Date Range Selection
#         date_range = st.date_input("Enter Date Range", (datetime.date(2024, 1, 1), datetime.datetime.now().date()), format="MM.DD.YYYY", key="payee_quality_date")
        
#         # Validate Date Range Selection
#         if len(date_range) != 2 or date_range[0] > date_range[1]:
#             st.error("Invalid date range. Please select a valid range.")
#         else:
#             start_date, end_date = date_range

#             # Convert to string format YYYY-MM-DD for SQL query
#             start_date_str = start_date.strftime("%Y-%m-%d")
#             end_date_str = end_date.strftime("%Y-%m-%d")

#             queue_query = {
#                 'Queue-wise ticket count': """
#                     SELECT Queue, COUNT(DISTINCT `Ticket Link`) AS count
#                     FROM payee_support_quality
#                     WHERE `Ticket Link` IS NOT NULL 
#                     AND Queue IS NOT NULL 
#                     AND TRIM(Queue) != '' 
#                     AND timestamp BETWEEN %s AND %s
#                     GROUP BY Queue
#                     ORDER BY count DESC;
#                 """,
                
#                 'Agent wise incorrect_info_count': """
#                     SELECT `Agent Name`, 
#                     COUNT(*) AS Incorrect_Info_Count
#                     FROM payee_support_quality
#                     WHERE `Incorrect Info` IS NOT NULL AND `Incorrect Info` != ''
#                     AND `Timestamp` BETWEEN %s AND %s
#                     GROUP BY `Agent Name`;
#                 """,
#                 'Agent wise incomplete_info_count': """
#                     SELECT `Agent Name`,
#                     COUNT(*) AS Incomplete_Info_Count
#                     FROM payee_support_quality
#                     WHERE `Incomplete Info` IS NOT NULL 
#                     AND `Incomplete Info` != ''
#                     AND `Timestamp` BETWEEN %s AND %s
#                     GROUP BY `Agent Name`
#                     ORDER BY Incomplete_Info_Count DESC;

#                 """
#             }


#             # Fetch Queue-wise ticket count
#             df_queue, error1 = fetch_data(queue_query['Queue-wise ticket count'], (start_date_str, end_date_str))

#             # Fetch Agent-wise incorrect info count
#             df_agent, error2 = fetch_data(queue_query['Agent wise incorrect_info_count'], (start_date_str, end_date_str))

#             # Fetch Agent-wise incorrect info count
#             df_incomplete, error3 = fetch_data(queue_query['Agent wise incomplete_info_count'], (start_date_str, end_date_str))

#             # Display chart for Queue-wise ticket count
#             if error1:
#                 st.error(f"Error fetching Queue data: {error1}")
#             elif df_queue.empty:
#                 st.warning("No queue data found for the selected date range.")
#             else:
#                 st.subheader("Queue Distribution")
#                 fig1 = px.bar(df_queue, x="Queue", y="count", text="count", title="Queue Count by Type", color_discrete_sequence=["#00CC96"])
#                 fig1.update_traces(textposition="outside")
#                 st.plotly_chart(fig1)

#             # Display chart for Agent-wise Incorrect Info Count
#             if error2:
#                 st.error(f"Error fetching Agent data: {error2}")
#             elif df_agent.empty:
#                 st.warning("No agent data found for the selected date range.")
#             else:
#                 st.subheader("Agent-wise Incorrect Info Count")
#                 fig2 = px.bar(df_agent, x="Agent Name", y="Incorrect_Info_Count", text="Incorrect_Info_Count",
#                             title="Incorrect Info Count by Agent", color_discrete_sequence=["#EF553B"])
#                 fig2.update_layout(xaxis_tickangle=-45)
#                 fig2.update_traces(textposition="outside")
#                 st.plotly_chart(fig2)

#             # Display chart for Agent-wise Incorrect Info Count
#             if error3:
#                 st.error(f"Error fetching Agent data: {error3}")
#             elif df_incomplete.empty:
#                 st.warning("No agent data found for the selected date range.")
#             else:
#                 st.subheader("Agent-wise Incomplete Info Count")
#                 fig3 = px.bar(df_incomplete, x="Agent Name", y="Incomplete_Info_Count", text="Incomplete_Info_Count",
#                 title="Incomplete Info Count by Agent", color_discrete_sequence=["#E2725B"])

#                 fig3.update_layout(xaxis_tickangle=-45)
#                 fig3.update_traces(textposition="outside")
#                 st.plotly_chart(fig3)

# if __name__ == "__main__":
#     admin_dashboard() 

import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from page.db import get_connection

# Function to fetch data from the database
def fetch_data(query, params):
    connection = get_connection()
    if not connection:
        return None, "Failed to connect to the database."
    
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        return pd.DataFrame(result), None
    except Exception as e:
        return None, str(e)
    finally:
        connection.close()

# SQL Queries
QUERIES = {
    "processing_tool_usage": """
        SELECT OCR, COUNT(*) AS user_count
        FROM managed_services
        WHERE OCR IS NOT NULL AND timestamp BETWEEN %s AND %s
        GROUP BY OCR
        ORDER BY user_count DESC;
    """,
    "top_payers": """
        SELECT payer, COUNT(*) AS payer_count
        FROM managed_services
        WHERE payer IS NOT NULL AND timestamp BETWEEN %s AND %s
        GROUP BY payer
        ORDER BY payer_count DESC
        LIMIT 20;
    """,
    "emea_distribution": """
        SELECT EMEA, COUNT(*) AS count
        FROM managed_services
        WHERE EMEA IS NOT NULL AND timestamp BETWEEN %s AND %s
        GROUP BY EMEA
        ORDER BY count DESC;
    """,
    "priority_distribution": """
        SELECT priority, COUNT(*) AS count
        FROM managed_services
        WHERE priority IS NOT NULL AND timestamp BETWEEN %s AND %s
        GROUP BY priority
        ORDER BY count DESC;
    """,
    "top_languages": """
        SELECT `foreign language` AS language, COUNT(*) AS count
        FROM managed_services
        WHERE `foreign language` IS NOT NULL AND timestamp BETWEEN %s AND %s
        GROUP BY `foreign language`
        ORDER BY count DESC
        LIMIT 5;
    """,
    "implementation_dbr": """
        SELECT TASK, COUNT(*) AS count 
        FROM implementation_DBR
        WHERE TASK IS NOT NULL AND timestamp BETWEEN %s AND %s
        GROUP BY TASK
        ORDER BY count DESC;
    """

}

# Utility to get default date range for a table
def get_latest_timestamp(table_name):
    query = f"SELECT MAX(timestamp) AS latest FROM {table_name}"
    df, error = fetch_data(query, ())
    if error or df.empty or df['latest'][0] is None:
        return datetime.datetime.now().date()
    return df['latest'][0]


def get_default_range(table_name):
    latest_date = get_latest_timestamp(table_name)
    start_date = latest_date - datetime.timedelta(days=30)
    return start_date, latest_date

# Admin Dashboard
def admin_dashboard():
    st.title("Admin Dashboard")

    # Tabs
    tab1, tab2 ,tab3,tab4= st.tabs(["Managed Service", "Implementation DBR","Payee support","Payee Support Quality"])

    with tab1:
        st.subheader("Managed Service Dashboard")
        today = datetime.datetime.now()
        jan_1 = datetime.date(2020, 1, 1)
        dec_31 = datetime.date(2028, 12, 31)

#        date_range = st.date_input("Enter Date Range", (jan_1, today.date()), jan_1, dec_31, format="MM.DD.YYYY")

        default_start, default_end = get_default_range("managed_services")
        date_range = st.date_input("Enter Date Range", (default_start, default_end), format="MM.DD.YYYY")

        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
        else:
            st.warning("Please select a valid date range.")
            return

        if start_date > end_date:
            st.error("Start date cannot be after end date.")
            return

        # Colors
        colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]
        color_index = 0

        data_fetchers = {
            "OCR wise volume": ("processing_tool_usage", "OCR", "user_count"),
            "Top Payers": ("top_payers", "payer", "payer_count"),
            "EMEA Contribution": ("emea_distribution", "EMEA", "count"),
            "Priority Distribution": ("priority_distribution", "priority", "count"),
            "Top 5 Languages": ("top_languages", "language", "count"),
        }

        for section, (query_key, x_col, y_col) in data_fetchers.items():
            df, error = fetch_data(QUERIES[query_key], (start_date, end_date))
            if error:
                st.error(f"Error fetching {section.lower()} data: {error}")
                continue
            
            if df.empty:
                continue

            st.subheader(section)
            color = colors[color_index % len(colors)]
            color_index += 1

            if section == "Top Payers":
                df = df.sort_values(by=y_col, ascending=True)
                fig = px.bar(df, x=y_col, y=x_col, text=y_col, orientation="h", title=section, color_discrete_sequence=[color])
                fig.update_traces(textposition="inside")
                st.plotly_chart(fig)
            elif section == "OCR wise volume":
                fig = px.bar(df, x=x_col, y=y_col, text=y_col, orientation="v", title=section, color_discrete_sequence=[color])
                fig.update_traces(textposition="outside")
                st.plotly_chart(fig)
            elif section in ["EMEA Contribution", "Priority Distribution"]:
                df["percentage"] = (df[y_col] / df[y_col].sum()) * 100
                fig = px.pie(df, names=x_col, values="percentage", title=f"{section} in Percentage", color_discrete_sequence=[color])
                st.plotly_chart(fig)
            elif section == "Top 5 Languages":
                df["percentage"] = (df[y_col] / df[y_col].sum()) * 100
                df.loc[len(df)] = ["Total", df[y_col].sum(), df["percentage"].sum()]
                df.index = range(1, len(df) + 1)
                st.write(df)

    with tab2:
        st.subheader("Implementation DBR Dashboard")

        # Date Range Selection
#        date_range = st.date_input("Enter Date Range", (datetime.date(2022, 1, 1), datetime.datetime.now().date()), format="MM.DD.YYYY", key="dbr_date")

        default_start, default_end = get_default_range("implementation_DBR")
        date_range = st.date_input("Enter Date Range", (default_start, default_end), format="MM.DD.YYYY", key="dbr_date")

        # Validate Date Range Selection
        if len(date_range) != 2 or date_range[0] > date_range[1]:
            st.error("Invalid date range. Please select a valid range.")
        else:
            start_date, end_date = date_range

            # Convert to string format YYYY-MM-DD for SQL query
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")

            # Fetch Data
            df, error = fetch_data(QUERIES["implementation_dbr"], (start_date_str, end_date_str))

            if error:
                st.error(f"Error fetching Implementation DBR data: {error}")
            elif df.empty:
                st.warning("No data found for the selected date range.")
            else:
                # Task Distribution Chart
                st.subheader("Task Distribution")
                task_counts = df.groupby("TASK")["count"].sum().reset_index().sort_values(by="count", ascending=False)
                
                if not task_counts.empty:
                    fig = px.bar(task_counts, x="TASK", y="count", title="Task Distribution", text="count",color_discrete_sequence=["#EF553B"])
                    fig.update_traces(textposition="outside")
                    st.plotly_chart(fig)
                else:
                    st.warning("No task data available for the selected date range.")
    with tab3:
        st.subheader("Payee Support Dashboard")

        # Date Range Selection
 #       date_range = st.date_input("Enter Date Range", (datetime.date(2022, 1, 1), datetime.datetime.now().date()), format="MM.DD.YYYY", key="payee_date")
        default_start, default_end = get_default_range("payee_support")
        date_range = st.date_input("Enter Date Range", (default_start, default_end), format="MM.DD.YYYY", key="payee_date")

        
        # Validate Date Range Selection
        if len(date_range) != 2 or date_range[0] > date_range[1]:
            st.error("Invalid date range. Please select a valid range.")
        else:
            start_date, end_date = date_range

            # Convert to string format YYYY-MM-DD for SQL query
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")

            # Query for distinct count of Queue
            queue_query = """
            SELECT Queue, COUNT(DISTINCT `Ticket Link`) AS count
            FROM payee_support
            WHERE `Ticket Link` IS NOT NULL 
            AND Queue IS NOT NULL 
            AND TRIM(Queue) != '' 
            AND timestamp BETWEEN %s AND %s
            GROUP BY Queue
            ORDER BY count DESC;


            """

            df, error = fetch_data(queue_query, (start_date_str, end_date_str))

            if error:
                st.error(f"Error fetching Payee Support data: {error}")
            elif df.empty:
                st.warning("No data found for the selected date range.")
            else:
                st.subheader("Queue Distribution")
                fig = px.bar(df, x="Queue", y="count", text="count", title="Queue Count by Type", color_discrete_sequence=["#00CC96"])
                fig.update_traces(textposition="outside")
                st.plotly_chart(fig)

    with tab4:
        st.subheader("Payee Support Quality Dashboard")

        # Date Range Selection
#        date_range = st.date_input("Enter Date Range", (datetime.date(2024, 1, 1), datetime.datetime.now().date()), format="MM.DD.YYYY", key="payee_quality_date")

        default_start, default_end = get_default_range("payee_support_quality")
        date_range = st.date_input("Enter Date Range", (default_start, default_end), format="MM.DD.YYYY", key="payee_quality_date")

        # Validate Date Range Selection
        if len(date_range) != 2 or date_range[0] > date_range[1]:
            st.error("Invalid date range. Please select a valid range.")
        else:
            start_date, end_date = date_range

            # Convert to string format YYYY-MM-DD for SQL query
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")


            # """
            queue_query = {
                'Queue-wise ticket count': """
                    SELECT Queue, COUNT(DISTINCT `Ticket Link`) AS count
                    FROM payee_support_quality
                    WHERE `Ticket Link` IS NOT NULL 
                    AND Queue IS NOT NULL 
                    AND TRIM(Queue) != '' 
                    AND timestamp BETWEEN %s AND %s
                    GROUP BY Queue
                    ORDER BY count DESC;
                """,
                
                'Agent wise incorrect_info_count': """
                    SELECT `Agent Name`, 
                    COUNT(*) AS Incorrect_Info_Count
                    FROM payee_support_quality
                    WHERE `Incorrect Info` IS NOT NULL AND `Incorrect Info` != ''
                    AND `Timestamp` BETWEEN %s AND %s
                    GROUP BY `Agent Name`;
                """,
                'Agent wise incomplete_info_count': """
                    SELECT `Agent Name`,
                    COUNT(*) AS Incomplete_Info_Count
                    FROM payee_support_quality
                    WHERE `Incomplete Info` IS NOT NULL 
                    AND `Incomplete Info` != ''
                    AND `Timestamp` BETWEEN %s AND %s
                    GROUP BY `Agent Name`
                    ORDER BY Incomplete_Info_Count DESC;

                """
            }

            # Fetch Queue-wise ticket count
            df_queue, error1 = fetch_data(queue_query['Queue-wise ticket count'], (start_date_str, end_date_str))

            # Fetch Agent-wise incorrect info count
            df_agent, error2 = fetch_data(queue_query['Agent wise incorrect_info_count'], (start_date_str, end_date_str))

            # Fetch Agent-wise incorrect info count
            df_incomplete, error3 = fetch_data(queue_query['Agent wise incomplete_info_count'], (start_date_str, end_date_str))

            # Display chart for Queue-wise ticket count
            if error1:
                st.error(f"Error fetching Queue data: {error1}")
            elif df_queue.empty:
                st.warning("No queue data found for the selected date range.")
            else:
                st.subheader("Queue Distribution")
                fig1 = px.bar(df_queue, x="Queue", y="count", text="count", title="Queue Count by Type", color_discrete_sequence=["#00CC96"])
                fig1.update_traces(textposition="outside")
                st.plotly_chart(fig1)

            # Display chart for Agent-wise Incorrect Info Count
            if error2:
                st.error(f"Error fetching Agent data: {error2}")
            elif df_agent.empty:
                st.warning("No agent data found for the selected date range.")
            else:
                st.subheader("Agent-wise Incorrect Info Count")
                fig2 = px.bar(df_agent, x="Agent Name", y="Incorrect_Info_Count", text="Incorrect_Info_Count",
                            title="Incorrect Info Count by Agent", color_discrete_sequence=["#EF553B"])
                fig2.update_layout(xaxis_tickangle=-45)
                fig2.update_traces(textposition="outside")
                st.plotly_chart(fig2)

            # Display chart for Agent-wise Incorrect Info Count
            if error3:
                st.error(f"Error fetching Agent data: {error3}")
            elif df_incomplete.empty:
                st.warning("No agent data found for the selected date range.")
            else:
                st.subheader("Agent-wise Incomplete Info Count")
                fig3 = px.bar(df_incomplete, x="Agent Name", y="Incomplete_Info_Count", text="Incomplete_Info_Count",
                title="Incomplete Info Count by Agent", color_discrete_sequence=["#E2725B"])

                fig3.update_layout(xaxis_tickangle=-45)
                fig3.update_traces(textposition="outside")
                st.plotly_chart(fig3)

if __name__ == "__main__":
    admin_dashboard()
