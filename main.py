# noinspection PyUnresolvedReferences
import streamlit as st
import requests

api_key = "API-KEY"

   #fetching Reviews
def fetch_reviews(api_key,place_id):
    reviews_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=review&key={api_key}"
    reviews_response = requests.get(reviews_url)
    reviews_json = reviews_response.json()
    print(reviews_json)
    '''
    reviews_all = reviews_json["result"]['reviews']

    for review in reviews_all:
        print("Author:", review["author_name"])
        print("Rating:", review["rating"])
        print("Text:", review["text"])
        print("\n")
    '''
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

    with st.spinner("Loading ..."):
        # Add a h1 reactivestreams run
        st.title("Customer Review Analysis")

        # Dark theme
        st.markdown("<style>body{background-color: #2e2e2e;color: white;}</style>", unsafe_allow_html=True)

        search_query = st.text_input("Enter Business Address:", key='query')

        # Show the user input
        st.write("Address:", search_query)

    address = search_query
    place_id = get_place_id(address)
    print("Place ID:", place_id)
    fetch_reviews(api_key,place_id)




if __name__ == '__main__':
    main()
