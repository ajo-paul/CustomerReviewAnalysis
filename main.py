# noinspection PyUnresolvedReferences
import streamlit as st
import requests
import pandas as pd
import time


api_key = "API-KEY"

import os
from google.cloud import sql_v1beta4


def update_cloudsql(data, project_id, instance_id, table_name, column_names):
    # Instantiate a client
    client = sql_v1beta4.SqlAdminClient()

    # Convert the data to a list of tuples
    values = [tuple(row.values()) for row in data]

    # Define the SQL statement
    sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES {values}"

    # Execute the SQL statement
    operation = client.execute_sql(
        project=project_id,
        instance=instance_id,
        sql=sql
    )
    operation.result()

    print("Update successful")


#fetching Reviews
def fetch_reviews(api_key,place_id):
    reviews_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=review&key={api_key}"
    reviews_response = requests.get(reviews_url)
    reviews_json = reviews_response.json()
    print(reviews_json)

    return

def get_place_id(address):
    endpoint = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

    params = {
        "input": address,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": api_key
    }

    response = requests.get(endpoint, params=params)
    data = response.json()
    if data['status'] == 'OK':
        return data['candidates'][0]['place_id']
    else:
        return None


def main():
    st.set_page_config(page_title="Customer Review Analysis", page_icon=":guardsman:", layout="wide")

    with st.spinner("Running ..."):
        # Add a h1 reactivestreams run
        st.title("Customer Review Analysis")

        # Dark theme
        st.markdown("<style>body{background-color: #2e2e2e;color: white;}</style>", unsafe_allow_html=True)

        # create a text input
        search_query = st.text_input("Enter Business Address:")

        # Show the user input
        st.write("Address:", search_query)

        if search_query:
            # display loading GIF
            with st.spinner("Loading... Please wait!"):
                time.sleep(5)  # simulate long running task
                df = pd.read_csv("https://people.sc.fsu.edu/~jburkardt/data/csv/addresses.csv")
            # display table
            st.write(df)

    address = search_query
    place_id = get_place_id(address)
    print("Place ID:", place_id)
    fetch_reviews(api_key,place_id)

    # Example usage:CloudSQL
    data = [
        {"column1": "value1", "column2": "value2"},
        {"column1": "value3", "column2": "value4"},
        # Add more data here
    ]
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    instance_id = "your-instance-id"
    table_name = "your_table"
    column_names = ["column1", "column2"]
    update_cloudsql(data, project_id, instance_id, table_name, column_names)


if __name__ == '__main__':
    main()
