import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.title("NHTSA Vehicle Complaints")

@st.cache_data
def load_makes():
    response = requests.get(
        f"{API_URL}/vehicles/makes"
    )
    response.raise_for_status()

    return response.json()


@st.cache_data
def load_models(make):
    response = requests.get(
        f"{API_URL}/vehicles/models/{make}"
    )
    response.raise_for_status()

    return response.json()

@st.cache_data
def load_years(make, model):
    response = requests.get(
        f"{API_URL}/vehicles/years/{make}/{model}"
    )
    
    if response.status_code == 404:
        return []

    response.raise_for_status()

    return response.json()


makes = load_makes()

make = st.selectbox(
    "Make",
    makes,
    index=makes.index("HONDA")
)

models = load_models(make)

default_model = (
    models.index("Civic")
    if "Civic" in models
    else 0
)

model = st.selectbox(
    "Model",
    models,
    index=default_model
)

years = load_years(make, model)

if not years:
    st.warning("No available years found for this vehicle.")
    st.stop()
    
year = st.selectbox(
    "Year",
    years
)

if st.button("Analyze"):
    url = (
        f"{API_URL}/vehicles/"
        f"{make}/{model}/{year}/complaints/ranking"
    )

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        st.header(
            f"{data['make']} {data['model']} — {data['year']}"
        )

        st.metric(
            "Total complaints",
            data["total_complaints"]
        )

        st.subheader("Severity")

        col1, col2, col3, col4 = st.columns(4)

        severity = data["severity"]

        col1.metric("Crashes", severity["crashes"])
        col2.metric("Fires", severity["fires"])
        col3.metric("Injuries", severity["injuries"])
        col4.metric("Deaths", severity["deaths"])

        st.subheader("Most reported components")

        st.dataframe(data["ranking"])

    elif response.status_code == 404:
        st.warning("No complaints found for this vehicle.")

    else:
        st.error("An error occurred.")