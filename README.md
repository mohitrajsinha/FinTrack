# FinTrack - Your Income and Expense Tracker



FinTrack is a web application built with Streamlit that allows you to track your income and expenses easily. It provides a simple and intuitive interface to record your financial data and visualize it in various formats.

## Features

- Data Entry: Easily enter your income and expense details for different periods.
- Data Visualization: Visualize your financial data using interactive charts and graphs.
- Monthly Reports: View and manage your income and expenses for different months.
- Data Persistence: All data is stored securely using Deta Base.

 Check Out the live app at: https://fintrack-python.streamlit.app



## Installation

1. Clone the repository:

```
https://github.com/mohitrajsinha/FinTrack.git
```
2.Install the required packages:
```
cd fintrack
pip install -r requirements.txt
```
3.Set up your Deta Base credentials:
- Obtain your Deta Base project key from https://deta.sh
- Create a `secrets.toml` file in the `.streamlit` folder of your root directory of the project.
- Insert `data_key=YOUR_PROJECT_KEY`
  
3.To run the FinTrack app, simply execute the following command:
```
streamlit run app.py

```

