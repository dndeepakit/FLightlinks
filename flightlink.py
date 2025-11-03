import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Flight Search Assistant", layout="centered")

st.title("✈️ Flight Search Assistant")
st.write("Easily generate direct flight search links for major booking sites.")

# ---- Input Fields ----
col1, col2 = st.columns(2)
from_city = col1.text_input("From City (e.g. Delhi, Mumbai, Bangalore)")
to_city = col2.text_input("To City (e.g. Chennai, Pune, Kolkata)")

col3, col4 = st.columns(2)
departure_date = col3.date_input("Departure Date", value=date.today())
travellers = col4.number_input("Number of Travellers", min_value=1, max_value=9, value=1)

travel_class = st.selectbox("Class", ["Economy", "Premium Economy", "Business", "First"])
site = st.selectbox("Select Booking Site", [
    "MakeMyTrip",
    "Skyscanner",
    "EaseMyTrip",
    "Goibibo",
    "Cleartrip",
    "Yatra"
])

# ---- Function to generate URL ----
def generate_link(site, from_city, to_city, departure_date, travellers, travel_class):
    date_str = departure_date.strftime("%d/%m/%Y")
    from_code = from_city[:3].upper()
    to_code = to_city[:3].upper()
    
    if site == "MakeMyTrip":
        return f"https://www.makemytrip.com/flight/search?itinerary={from_code}-{to_code}-{date_str}&paxType=A-{travellers}_C-0_I-0&cabinClass={travel_class[0].upper()}"
    
    elif site == "EaseMyTrip":
        return f"https://www.easemytrip.com/flightresult/{from_code}-{to_code}/{date_str}/{travellers}/0/0/{travel_class[0].upper()}.html"
    
    elif site == "Goibibo":
        return f"https://www.goibibo.com/flights/air-{from_code}-{to_code}-{date_str}/?adults={travellers}&class={travel_class.lower()}"
    
    elif site == "Cleartrip":
        return f"https://www.cleartrip.com/flights/results?from={from_city}&to={to_city}&depart_date={date_str}&adults={travellers}&cabinClass={travel_class}"
    
    elif site == "Yatra":
        return f"https://flight.yatra.com/air-search-ui/dom2/trigger?type=O&origin={from_city}&destination={to_city}&flight_depart_date={date_str}&ADT={travellers}&CL={travel_class[0]}"
    
    elif site == "Skyscanner":
        return f"https://www.skyscanner.co.in/transport/flights/{from_code}/{to_code}/{departure_date.strftime('%y%m%d')}/?adults={travellers}&cabinclass={travel_class.lower()}"
    
    return None

# ---- Generate Button ----
if st.button("🔍 Generate Search Link"):
    if from_city and to_city:
        url = generate_link(site, from_city, to_city, departure_date, travellers, travel_class)
        st.success(f"Your {site} search link is ready!")
        st.markdown(f"[Click here to view flight options on {site}]({url})", unsafe_allow_html=True)
        
        # ---- Prepare Excel Download ----
        df = pd.DataFrame({
            "From City": [from_city],
            "To City": [to_city],
            "Departure Date": [departure_date.strftime("%d-%m-%Y")],
            "Travellers": [travellers],
            "Class": [travel_class],
            "Selected Site": [site],
            "Generated URL": [url]
        })
        
        excel_file = "flight_search.xlsx"
        df.to_excel(excel_file, index=False)
        with open(excel_file, "rb") as f:
            st.download_button("⬇️ Download Search Details (Excel)", f, file_name=excel_file)
    else:
        st.warning("Please enter both From and To cities.")
