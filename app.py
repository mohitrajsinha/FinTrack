import streamlit as st
import plotly.graph_objects as go
import calendar
from datetime import datetime
from streamlit_option_menu import option_menu

import database as db

# SETTINGS
incomes = ["Salary", "Blog", "Other Income"]
expenses = ["Rent", "Utilities", "Groceries", "Car", "Other Expenses", "Savings"]
currency = "USD"
page_title = "FinTrack"
page_icon = "💰"
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

st.title(page_title + " " + page_icon)
st.subheader('Your Own Income and Expense Tracker')

# DROP DOWN VALUES FOR SELECTING THE PERIOD
years = [datetime.today().year, datetime.today().year - 1]
months = list(calendar.month_name[1:])


# DATABASE INTERFACE
def get_all_periods():
    """
    Fetch all periods from the database.

    Returns:
        list: List of available periods in the database.
    """
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods


# HIDE STREAMLIT STYLE
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# NAVIGATION
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization"],
    icons=["📝", "📊"],
    orientation="horizontal",
)


# INPUT AND SAVE PERIODS
if selected == "Data Entry":
    st.header(f"Data Entry in {currency}")
    with st.form("entry form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        col1.selectbox("Select Months", months, key="month")
        col2.selectbox("Select Years", years, key="year")

        st.markdown("""---""")
        with st.expander("Incomes"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
        with st.expander("Comment"):
            comment = st.text_area("", placeholder="Enter a Comment here...")

        st.markdown("""---""")
        submitted = st.form_submit_button("Submit")
        if submitted:
            # Prepare data for submission to the database
            period = f"{st.session_state['year']}_{st.session_state['month']}"
            incomes_data = {income: st.session_state[income] for income in incomes}
            expenses_data = {expense: st.session_state[expense] for expense in expenses}
            # Insert the data into the database
            db.insert_period(period, incomes_data, expenses_data, comment)
            st.write(f"incomes: {incomes_data}")
            st.write(f"expenses: {expenses_data}")
            st.success("Data Submitted Successfully!")

# ---- DISPLAY THE DATA ----

if selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("saved_periods"):
        period = st.selectbox("Select Period:", get_all_periods())
        submitted = st.form_submit_button("Plot Period")
        if submitted:
            # Get data from the database for the selected period
            period_data = db.get_period(period)
            if period_data:
                comment = period_data.get("comment")
                expenses_data = period_data.get("expenses")
                incomes_data = period_data.get("income")

                # Create metrics for data visualization
                total_income = sum(incomes_data.values())
                total_expense = sum(expenses_data.values())
                remaining_budget = total_income - total_expense
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Income", f"{total_income} {currency}")
                col2.metric("Total Expense", f"{total_expense} {currency}")
                col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
                st.text(f"Comment: {comment}")

                # Create sankey chart for data visualization
                label = list(incomes_data.keys()) + ["Total Income"] + list(expenses_data.keys())
                source = list(range(len(incomes_data))) + [len(incomes_data)] * len(expenses_data)
                target = [len(incomes_data)] * len(incomes_data) + [label.index(expense) for expense in expenses_data.keys()]
                value = list(incomes_data.values()) + list(expenses_data.values())

                # Data to dict, dict to sankey
                link = dict(source=source, target=target, value=value)
                node = dict(label=label, pad=20, thickness=30, color="#0384fc")
                data = go.Sankey(link=link, node=node)

                # Plot the sankey chart
                fig = go.Figure(data)
                fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Data for the selected period not found!")
