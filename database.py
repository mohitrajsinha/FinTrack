import streamlit as st
from connections import DetaBaseConnection

# Create a connection to Deta Base using the provided data key
data_key = st.secrets["data_key"]
conn = st.experimental_connection("deta", type=DetaBaseConnection, _project_key=data_key)

# Create a reference to the Deta Base collection
db = conn._instance.Base("monthly-reports")  # Replace "monthly-reports" with your collection name


def insert_period(period, incomes, expenses, comment):
    """
    Insert a new period record into the Deta Base collection.

    Args:
        period (str): The period key (e.g., "2023_08") for which data is to be inserted.
        incomes (dict): A dictionary containing income categories and their respective values.
        expenses (dict): A dictionary containing expense categories and their respective values.
        comment (str): A comment associated with the period.

    Returns:
        None
    """
    db.put({"key": period, "income": incomes, "expenses": expenses, "comment": comment})


def fetch_all_periods():
    """
    Fetch all periods available in the Deta Base collection.

    Returns:
        list: A list of dictionaries containing information about all periods in the collection.
    """
    data_key = st.secrets["data_key"]
    conn = st.experimental_connection("deta", type=DetaBaseConnection, _project_key=data_key)

    db = conn._instance.Base("monthly-reports")  # Replace "monthly-reports" with your collection name
    response = db.fetch()
    return response.items


def get_period(period):
    """
    Fetch the data associated with a specific period from the Deta Base collection.

    Args:
        period (str): The period key (e.g., "2023_08") for which data is to be retrieved.

    Returns:
        dict or None: A dictionary containing information about the period if found, else None.
    """
    data_key = st.secrets["data_key"]
    conn = st.experimental_connection("deta", type=DetaBaseConnection, _project_key=data_key)

    db = conn._instance.Base("monthly-reports")  # Replace "monthly-reports" with your collection name
    period_data = db.get(period)  # Use the "get" method to fetch data using the period as the key
    return period_data
