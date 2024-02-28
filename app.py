import streamlit as st
from PIL import Image
import subprocess
import os

# .whlファイルのURL
whl_url = "https://github.com/VOICEVOX/voicevox_core/releases/download/0.14.3/voicevox_core-0.14.3+cpu-cp38-abi3-linux_x86_64.whl"
# ダウンロードする.whlファイルのファイル名
whl_file = "voicevox_core-0.14.3+cpu-cp38-abi3-linux_x86_64.whl"

# wgetを使用してファイルをダウンロード
subprocess.run(["wget", whl_url])

# pipを使用してダウンロードした.whlファイルをインストール
subprocess.run(["pip", "install", whl_file])

from main import main

# 画像を表示
image = Image.open("./images/tentative_logo_design.jpg")

image = "./images/tentative_logo_design.jpg"

def generate_video(input_text, detail_level, language, accuracy, painting_option):
    search_result, explanation, prompts, titles = main(input_text, detail_level, language, accuracy, painting_option)
    print(search_result)
    # セッション状態に返されたテキストを保存
    st.session_state["search_result"] = search_result
    st.session_state["explanation"] = explanation
    st.session_state["prompts"] = prompts
    st.session_state["titles"] = titles
    return search_result, explanation, prompts, titles
    
def main_page():
    # 以下をメインページに表示
    left_column, right_column = st.columns([2,5])
    left_column.image(image, width=200)
    right_column.title("One-Minute.ai")
    right_column.caption("One Minute Video to Grasp Anything")
    
    st.write("")
    st.write("")
    input_text = st.text_area(
        "Text to analyze",
        placeholder="Please enter a term you would like to know more about.",
        )

    # st.write(f'You wrote {len(input_text)} characters.')
    if st.button("Generate"):
        # セッション状態を更新
        st.session_state["input_text"] = input_text
        st.session_state["page"] = "video"
        painting_option = st.session_state.get("painting_option")
        detail_level = st.session_state.get("detail_level")
        language = st.session_state.get("language")
        accuracy = st.session_state.get("accuracy")
        generate_video(input_text, detail_level, language, accuracy, painting_option)
        st.experimental_rerun()
        


def sub_page():
    st.sidebar.header("Text options")
    MODEL = st.sidebar.selectbox("model", ["GPT-4", "歴史モデル（未実装）", "科学モデル（未実装）", "芸術モデル（未実装）"])
    DETAIL_LEVEL = st.sidebar.selectbox("detail level", ["初級（elementary）", "基礎（basic）", "中級（intermediate）", "上級（advanced）", "専門的（professional）"])
    ACCURACY = st.sidebar.slider("accuracy", 0, 10, 5)
    st.sidebar.caption("0: creative 10: accurate")
    language_options = ["日本語（Japanese）", "英語（English）（未実装）"]
    LANGUAGE = st.sidebar.selectbox("language", language_options)


    st.sidebar.header("Painting options")
    PAINTING_MODEL = st.sidebar.selectbox("model", ["DALL-E2", "DALL-E3"])
    # 技法の選択肢を追加し、'その他'オプションを含める
    techniques_options = ["水彩画（watercolor）", "油絵（oil painting）", "パステル画（pastel painting）", "鉛筆画（pencil drawing）", "デジタル画（digital painting）", "その他..."]
    PAINTING_TECHNIQUES = st.sidebar.selectbox("techniques", techniques_options)

    # 'その他'が選択された場合は、テキスト入力を表示
    if PAINTING_TECHNIQUES == "その他...":
        custom_technique = st.sidebar.text_input("Specify your technique")
        PAINTING_TECHNIQUES = custom_technique if custom_technique else PAINTING_TECHNIQUES

    # スタイルの選択肢を追加し、'その他'オプションを含める
    style_options = ["写実主義（realism）", "印象派（impressionism）", "シュルレアリスム（surrealism）", "抽象画（abstract）", "ポップアート（pop art）", "その他..."]
    PAINTING_STYLE = st.sidebar.selectbox("style", style_options)

    # 'その他'が選択された場合は、テキスト入力を表示
    if PAINTING_STYLE == "その他...":
        custom_style = st.sidebar.text_input("Specify your style")
        PAINTING_STYLE = custom_style if custom_style else PAINTING_STYLE

    # Optionをセッション状態に保存
    st.session_state["detail_level"] = DETAIL_LEVEL
    st.session_state["language"] = LANGUAGE
    st.session_state["accuracy"] = ACCURACY
    st.session_state["painting_option"] = {PAINTING_TECHNIQUES + "の" + PAINTING_STYLE}

def main_video_page():
    search_result = st.session_state.get("search_result")
    title = st.session_state.get("titles")

    left_column, right_column = st.columns([1,6])

    with left_column:
        # 画像を小さくして表示
        st.image(image, caption='Tentative logo', width=100)

    with right_column:
        # HTMLを使用してタイトルとキャプションのフォントサイズを調整
        st.markdown("<h1 style='font-size: 24px;'>One minute to find out anything</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 18px;'>Learn the barrier to entry of any field in one minute.</p>", unsafe_allow_html=True)
    
    
    st.title(search_result)
    _, container, _ = st.columns([1, 5, 1])
    video_path = "./voicevox/result/output_with_srt.mp4"
    container.video(video_path)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Beginning", "Development", "Turn", "Resolution"])
    with tab1:
        st.subheader(f"{title[0]}")
        content = "\n\n".join(st.session_state.get("explanation")[0])
        print(content)
        st.write(content)
    
    with tab2:
        st.subheader(f"{title[1]}")
        content = "\n\n".join(st.session_state.get("explanation")[1])
        st.write(content)
    
    with tab3:
        st.subheader(f"{title[2]}")
        content = "\n\n".join(st.session_state.get("explanation")[2])
        st.write(content)
    
    with tab4:
        st.subheader(f"{title[3]}")
        content = "\n\n".join(st.session_state.get("explanation")[3])
        st.write(content)
    
    if st.button("Go Back"):
        st.session_state["page"] = "main"
        st.experimental_rerun()

def sub_video_page():
    st.sidebar.header("Text options")
    MODEL = st.sidebar.selectbox("model", ["GPT-4", "歴史モデル（未実装）", "科学モデル（未実装）", "芸術モデル（未実装）"])
    DETAIL_LEVEL = st.sidebar.selectbox("detail level", ["初級（elementary）", "基礎（basic）", "中級（intermediate）", "上級（advanced）", "専門的（professional）"])
    ACCURACY = st.sidebar.slider("accuracy", 0, 10, 5)
    st.sidebar.caption("0: creative 10: accurate")
    language_options = ["日本語（Japanese）", "英語（English）（未実装）"]
    LANGUAGE = st.sidebar.selectbox("language", language_options)


    st.sidebar.header("Painting options")
    PAINTING_MODEL = st.sidebar.selectbox("model", ["DALL-E2", "DALL-E3"])
    # 技法の選択肢を追加し、'その他'オプションを含める
    techniques_options = ["水彩画（watercolor）", "油絵（oil painting）", "パステル画（pastel painting）", "鉛筆画（pencil drawing）", "デジタル画（digital painting）", "その他..."]
    PAINTING_TECHNIQUES = st.sidebar.selectbox("techniques", techniques_options)

    # 'その他'が選択された場合は、テキスト入力を表示
    if PAINTING_TECHNIQUES == "その他...":
        custom_technique = st.sidebar.text_input("Specify your technique")
        PAINTING_TECHNIQUES = custom_technique if custom_technique else PAINTING_TECHNIQUES

    # スタイルの選択肢を追加し、'その他'オプションを含める
    style_options = ["写実主義（realism）", "印象派（impressionism）", "シュルレアリスム（surrealism）", "抽象画（abstract）", "ポップアート（pop art）", "その他..."]
    PAINTING_STYLE = st.sidebar.selectbox("style", style_options)

    # 'その他'が選択された場合は、テキスト入力を表示
    if PAINTING_STYLE == "その他...":
        custom_style = st.sidebar.text_input("Specify your style")
        PAINTING_STYLE = custom_style if custom_style else PAINTING_STYLE

    # Optionをセッション状態に保存
    st.session_state["detail_level"] = DETAIL_LEVEL
    st.session_state["language"] = LANGUAGE
    st.session_state["accuracy"] = ACCURACY
    st.session_state["painting_option"] = {PAINTING_TECHNIQUES + "の" + PAINTING_STYLE}

    tab1, tab2 = st.sidebar.tabs(["Options", "Generation"])

    with tab2:

        tab2.write("")
        tab2.write("")
        txt = tab2.text_area(
            "Text to analyze",
            placeholder="Please enter a term you would like to know more about.",
            )

        tab2.write(f'You wrote {len(txt)} characters.')

        if st.button("Generate"):
            # セッション状態を更新
            st.session_state["input_text"] = txt
            detail_level = st.session_state.get("detail_level")
            accuracy = st.session_state.get("accuracy")
            painting_option = st.session_state.get("painting_option")
            generate_video(txt, detail_level, LANGUAGE, accuracy, painting_option)
            st.session_state["page"] = "video"
            st.experimental_rerun()

def webpages():
    main_page()
    sub_page()

def video_webpages():
    main_video_page()
    sub_video_page()

    
# セッション状態の初期化
if "page" not in st.session_state:
    st.session_state["page"] = "main"

# 現在のページに基づいて表示を切り替え
if st.session_state["page"] == "main":
    webpages()
elif st.session_state["page"] == "video":
    video_webpages()
