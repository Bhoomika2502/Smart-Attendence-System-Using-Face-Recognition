import streamlit as st
import pandas as pd
from datetime import datetime

# Get current date and timestamp
date = datetime.now().strftime("%d-%m-%Y")

# Define a function to read CSV data
def read_csv_data(date):
    try:
        df = pd.read_csv(f"Attendance/Attendance_{date}.csv")
        return df
    except FileNotFoundError:
        st.error(f"CSV file 'Attendance_{date}.csv' not found. Make sure the file exists.")
        return None
    except pd.errors.EmptyDataError:
        st.error(f"CSV file 'Attendance_{date}.csv' is empty.")
        return None
    except Exception as e:
        st.error(f"Error occurred while reading CSV: {str(e)}")
        return None

# Main Streamlit app layout with improved styling and embedded CSS
def main():
    st.set_page_config(
        page_title="Face Recognition Attendance System",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Define custom CSS for styling
    custom_css = """
    <style>
    .title-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: #333;
    }
    .subheader-text {
        font-size: 1.5rem;
        font-weight: bold;
        color: #555;
    }
    .timestamp {
        font-size: 1.2rem;
        color: #777;
    }
    .dataframe {
        border-collapse: collapse;
        width: 100%;
    }
    .dataframe th {
        background-color: #f2f2f2;
        text-align: left;
        padding: 8px;
    }
    .dataframe td {
        text-align: left;
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }
    .highlight {
        background-color: #ffffcc !important;
        font-weight: bold;
    }
    .alert {
        padding: 8px;
        margin-top: 10px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        border-radius: 4px;
    }
    .success {
        padding: 8px;
        margin-top: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        border-radius: 4px;
    }
    .info {
        padding: 8px;
        margin-top: 10px;
        background-color: #cce5ff;
        border: 1px solid #b8daff;
        color: #004085;
        border-radius: 4px;
    }
    .warning {
        padding: 8px;
        margin-top: 10px;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        border-radius: 4px;
    }
    .error {
        padding: 8px;
        margin-top: 10px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        border-radius: 4px;
    }
    </style>
    """

    # Display custom CSS using Markdown
    st.markdown(custom_css, unsafe_allow_html=True)

    st.title('Face Recognition Based Attendance System')
    st.markdown("---")
    
    # Display current timestamp
    st.subheader(f"Current Timestamp: {datetime.now().strftime('%H:%M:%S')}")

    # Read attendance data
    df = read_csv_data(date)
    
    # Display data if available
    if df is not None:
        st.subheader(f"Attendance Data for {date}")
        
        # Display DataFrame with additional USN column
        df_display = df.copy()  # Make a copy to avoid modifying the original DataFrame
        df_display['USN'] = [f"USN_{i+1}" for i in range(len(df))]  # Example: Replace with actual USN data
        st.dataframe(df_display.style.apply(lambda x: ['background: #ffffcc' if x.name == 'MAX' else '']))
    
    # Example of auto-refresh functionality
    count = st.session_state.get("fizzbuzzcounter", 0)
    count += 1
    st.session_state["fizzbuzzcounter"] = count
    
    st.markdown("---")
    st.subheader("Auto-refresh Example")
    
    if count == 0:
        st.error("Count is zero")
    elif count % 3 == 0 and count % 5 == 0:
        st.error("FizzBuzz")
    elif count % 3 == 0:
        st.warning("Fizz")
    elif count % 5 == 0:
        st.info("Buzz")
    else:
        st.success(f"Count: {count}")

if __name__ == '__main__':
    main()
