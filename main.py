import pickle
import json
import numpy as np
import streamlit as st
import base64

__locations = None
__data_columns = None
__model = None


def get_locations():
    return __locations


def load_artifacts():
    global __data_columns
    global __locations
    global __model

    with open('model/columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]

    with open('model/home_model.pickle', 'rb') as f:
        __model = pickle.load(f)


def get_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def gui():
    main_bg = 'model/housebg.jpg'
    main_bg_ext = "jpg"

    html_temp = f"""
        <style>
        .reportview-container {{
        background-image: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
            background-size: cover
        }}
        </style>
        """
    st.markdown(html_temp, unsafe_allow_html=True)

    st.write('# Banglore Home Price Prediction')
    st.write('### Area (in sqft)')
    area = st.text_input('')
    select_bhk, select_bath = st.beta_columns([2, 2])
    bhkC, bathC = st.beta_columns([2, 2])
    select_bhk.subheader('Select BHK')
    bhk = bhkC.selectbox('', (1, 2, 3, 4, 5), key='bhk')
    select_bath.subheader('Select no of bathrooms')
    bath = bathC.selectbox('', (1, 2, 3, 4, 5), key='bath')
    st.subheader('Location')
    location = st.selectbox('', __locations)
    result = 0
    if st.button('Predict'):
        result = get_price(location, area, bhk, bath)
    price = round(result, 2)
    st.write('## Estimated price is (in lakhs) :  {}'.format(price))


if __name__ == '__main__':
    load_artifacts()
    gui()
