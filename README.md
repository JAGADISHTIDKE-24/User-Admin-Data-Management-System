# Data Management and Forecasting App

## Overview
This Streamlit-based web application enables users to upload CSV files, store them in a MySQL database, visualize data through dashboards, perform forecasting, and export data. The application supports user authentication with role-based access.

## Features
- **User Authentication**: Admins and users can log in with credentials stored in a MySQL database.
- **CSV Import**: Users can upload CSV files, which are stored in a database.
- **Data Visualization**: Interactive dashboards are available for data exploration.
- **Forecasting**: Predict future trends using uploaded data.
- **Audit Logs**: Tracks user activities such as logins and data uploads.
- **Data Export**: Users can export filtered data based on their preferences.

## Installation
### Prerequisites
- Python 3.8+
- MySQL Database
- Required Python packages:

```sh
pip install streamlit pandas mysql-connector-python
```

### Database Setup
1. Create a MySQL database and table structure.
2. Update `db.py` with your database connection details.

### Running the Application
```sh
streamlit run Home.py
```

## File Structure
```
📂 project-root/
├── 📂 page/
│   ├── db.py  # Database connection
│   ├── audit_logger.py  # Logs user activities
│   ├── admin.py  # Admin panel functionalities
│   ├── user.py  # User functionalities
├── Home.py  # Main Streamlit application
├── README.md  # Project documentation
```

## Troubleshooting
- **Connection Pool Exhausted**: Ensure all database connections are properly closed after use.
- **Login Issues**: Check if user credentials exist in the `employees` table.
- **File Upload Errors**: Ensure the uploaded file contains the required columns.

## Contributors
- **Jagadish Tidke**

## Contact
For any issues or contributions, contact: [jagadishtidke546@gmail.com](mailto:jagadishtidke546@gmail.com).

