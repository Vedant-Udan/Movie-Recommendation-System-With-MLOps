import streamlit as st
from src.config import Config
from src.data_loader import DataLoader
from getOutput import getRecommendation

loader = DataLoader(Config.DATA_PATH) 
data = loader.load_data()
preprocessed_data, data = loader.preprocess(data)

st.markdown("""

<style>

    .stButton > span {

        font-size: 30px;

    }

</style>

""", unsafe_allow_html=True)

st.write("# Hello Welcome To Movie Recommendation System")

st.write('### It recommend movie based on the movie you have watch earlier.')
movie = st.selectbox('Select Movie You Have Watched', list(data.index), )

if st.button('Recommend'):
    output = getRecommendation(movie)
    for  i in output['recommendations']:
        st.write(f'## {i}')
