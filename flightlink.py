import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

st.set_page_config(page_title="Flight Search Link Generator", layout="centered")

st.title("✈️ Flight Search Link Generator")
st.write("Generate ready-to-click flight search links across multiple travel sites.")

# --- Inputs ---
col1, col2 = st.columns(2)
from_city = col1.text_input("From City (e.g., Delhi, Mumbai, Bangalore)")
to_city = col2.text_input("To City (e.g., Chennai, Pune, Kolkata)")

col3, col4 = st.columns(2)
departure_date = col3.date_input("Departure Date", value=date.today())
travellers = col4.number_input("No. of Travellers", min_value=1, max_value=9, value=1)

travel_class = st.selectbox("Class", ["Economy", "Premium Economy", "Business", "First"])

sites = st.multiselect(
    "Select Booking Sites",
    ["MakeMyTrip", "Skyscanner", "EaseMyTrip", "Goibibo", "Cleartrip", "Yatra"],
    default=["MakeMyTrip", "Skyscanner"]
)

# --- Link generator ---
def generate_link(site, from_city, to_city, departure_date, travellers, travel_class):
    d = departure_date
    date_str = d.strftime("%d/%m/%Y")
    date_str_dash = d.strftime("%d-%m-%Y")
    ymd = d.strftime("%y%m%d")
    from_code = from_city[:3].upper()
    to_code = to_city[:3].upper()

    if site == "MakeMyTrip":
        return f"https://www.makemytrip.com/flight/search?itinerary={from_code}-{to_code}-{date_str}&paxType=A-{travellers}_C-0_I-0&cabinClass={travel_class[0].upper()}"
    if site == "EaseMyTrip":
        return f"https://www.easemytrip.com/flightresult/{from_code}-{to_code}/{date_str}/{travellers}/0/0/{travel_class[0].upper()}.html"
    if site == "Goibibo":
        return f"https://www.goibibo.com/flights/air-{from_code}-{to_code}-{date_str_dash}/?adults={travellers}&class={travel_class.lower()}"
    if site == "Cleartrip":
        return f"https://www.cleartrip.com/flights/results?from={from_city}&to={to_city}&depart_date={date_str_dash}&adults={travellers}&cabinClass={travel_class}"
    if site == "Yatra":
        return f"https://flight.yatra.com/air-search-ui/dom2/trigger?type=O&origin={from_city}&destination={to_city}&flight_depart_date={date_str_dash}&ADT={travellers}&CL={travel_class[0]}"
    if site == "Skyscanner":
        return f"https://www.skyscanner.co.in/transport/flights/{from_code}/{to_code}/{ymd}/?adults={travellers}&cabinclass={travel_class.lower()}"
    return ""

# --- Generate Output ---
if st.button("Generate Links"):
    if not from_city or not to_city:
        st.warning("Please enter both From and To cities.")
    else:
        links_data = []
        for s in sites:
            url = generate_link(s, from_city, to_city, departure_date, travellers, travel_class)
            links_data.append({
                "Booking Site": s,
                "From": from_city,
                "To": to_city,
                "Departure Date": departure_date.strftime("%d-%b-%Y"),
                "Travellers": travellers,
                "Class": travel_class,
                "Search Link": url
            })
        df = pd.DataFrame(links_data)

        st.subheader("Generated Flight Search Links")
        for _, row in df.iterrows():
            st.markdown(f"🔗 **{row['Booking Site']}** → [Open Link]({row['Search Link']})")

        st.dataframe(df.drop(columns=["Search Link"]), use_container_width=True)

        # --- Excel Download ---
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Flight Links")
        st.download_button(
            label="📥 Download Excel File",
            data=output.getvalue(),
            file_name=f"Flight_Links_{from_city}_{to_city}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
