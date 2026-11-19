# streamlit run main.py

from bs4 import BeautifulSoup
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from googletrans import Translator
import asyncio
import altair as alt
import streamlit as st


# メタスコアサイトからレビュー情報を取得
def get_review(url_metacritic):
    dummy_user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
    res = requests.get(url_metacritic, headers={"User-Agent": dummy_user_agent})
    soup = BeautifulSoup(res.text, 'html.parser')
    review_content = soup.find('div', {'data-testid': 'product-reviews'})
    review_list = review_content.find_all('div', {'data-testid': 'review-card'})

    data_review = []
    for review in review_list:
        data = {}
        data['date'] = review.find('div', {'data-testid': 'review-card-date'}).text
        data['header'] = review.find('a', {'data-testid': 'review-card-header'}).text
        data['text'] = review.find('div', {'data-testid': 'review-card-quote-block'}).text
        header_arr = data['header'].split(' ')
        data['score'] = header_arr[0]
        data['user'] = header_arr[1]
        data_review.append(data)
    return data_review

# google日本語翻訳APIから結果を取得
async def translate_bulk(data_review):
    trans_src = []
    for data in data_review:
        trans_src.append(data['text'])
    result = []
    async with Translator(service_urls=['translate.googleapis.com']) as translator:
        translations = await translator.translate(trans_src, dest='ja')
        for translation in translations:
            #print(translation.origin, ' -> ', translation.text)
            result.append(translation.text)
    return result


# レビューリストの出力
def output_review(review_list):
    for data in review_list:
        with st.container():
            col1, col2, col3 = st.columns(3)
            col1.badge(data['score'], icon=":material/star:", color="yellow")
            col2.write(data['date'])
            col3.write(data['user'])
            st.write(data['trans_txt'])
            with st.expander("原文"):
                st.write(data['text'])
            st.divider()


st.sidebar.subheader('メタスコアレビュー表示アプリ')
st.sidebar.write("""
選択したタイトルの
metacritic.comの
レビューコメントを
表示します
""")
pages = ["ENDER MAGNOLIA", "ENDER LILIES", "Brigandine Abyss"]
page = st.sidebar.radio("title", pages)

if page == "ENDER MAGNOLIA":
    url_metacritic = 'https://www.metacritic.com/game/ender-magnolia-bloom-in-the-mist/user-reviews/?platform=pc'
elif page == "ENDER LILIES":
    url_metacritic = 'https://www.metacritic.com/game/ender-lilies-quietus-of-the-knights/user-reviews/?platform=pc'
else:
    url_metacritic = 'https://www.metacritic.com/game/brigandine-abyss/user-reviews/?platform=nintendo-switch-2'

st.header(page)
st.divider()
with st.spinner("Loading...", show_time=False):
    # metacriticからメタスコア情報を取得
    data_review = get_review(url_metacritic)
    # レビュー本文を日本語翻訳する
    trans_dest = asyncio.run(translate_bulk(data_review))
    for i, trans_txt in enumerate(trans_dest):
        data_review[i]['trans_txt'] = trans_txt

# 出力
output_review(data_review)












