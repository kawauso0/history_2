# from voicevox.voice import voicevox, generate_adjusted_audio_from_srt
from voicevox.voice import pyopenjtalk_synthesize
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip, AudioFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
import budoux
from datetime import timedelta
import srt
import re


List = ["beginning", "development", "turn", "resolution"]
parser = budoux.load_default_japanese_parser()
entry_number = 1  # 字幕の番号

keywords = dict()
keywords["beginning"] = "キーワード: イエス・キリスト"
keywords["development"] = "キーワード: カトリック教会、プロテスタント教会、正教会"
keywords["turn"] = "キーワード: 旧約聖書、新約聖書、初代教会"
keywords["resolution"] = "キーワード: 礼拝、聖書、社会奉仕活動"

def create_sound_files_srt_files(Section_List, Keywords):
    start = 0
    srts = []
    keywords_srt = []
    time_segments = [[] for _ in range(len(Section_List))]
    end = 0
    sentence_start = 0
    sentence_end = 0
    for i, section in enumerate(Section_List):
        for j, sentence in enumerate(section):
            sentence = re.sub(r"\n", "", sentence)
            sentence = re.sub(r" ", "", sentence)
            sentence = re.sub(r"　", "", sentence)
            time = pyopenjtalk_synthesize(sentence, f"voicevox/sound/{i}_{j}.wav", speed=1.2)
            # 絶対パスで指定
            # time = voicevox(sentence, f"/Users/issei/Documents/GitHub/OneMinuteVideoMaker/webapp/voicevox/sound/{i}_{j}.wav", speed=1.2)
            end = start + time
            sentence_end = sentence_end + time
            srts.extend(split_text_and_write_srt(sentence, start, end, max_length=15))
            start = end
            time_segments[i].append(time)
        keywords_srt.append(create_keywords_srt(sentence_start, sentence_end, len(keywords_srt)+1, Keywords[i]))
        sentence_start = sentence_end
    
    
    with open("voicevox/srt/output.srt", "w") as f:
        f.write(srt.compose(srts))
        
    # with open("/Users/issei/Documents/GitHub/OneMinuteVideoMaker/webapp/voicevox/srt/output.srt", "w") as f:
    #     f.write(srt.compose(srts))
    
    with open("voicevox/srt/keywords.srt", "w") as f:
        f.write(srt.compose(keywords_srt))
        
    # with open("/Users/issei/Documents/GitHub/OneMinuteVideoMaker/webapp/voicevox/srt/keywords.srt", "w") as f:
    #     f.write(srt.compose(keywords_srt))
        
    return time_segments
        
# def create_sound_files_srt_files_oneminute():

#     start = 0
#     srts = []
#     keywords_srt = []
#     end = 0
#     for section in List:
#         file = f"./text/{section}.txt"
#         with open(file, "r") as f:
#             text = f.read()
#             text = re.sub(r"\n", "", text)
#             text = re.sub(r" ", "", text)
#             text = re.sub(r"　", "", text)
#         end = start + 15
#         srts.extend(split_text_and_write_srt(text, start, end, max_length=15))
#         keywords_srt.append(create_keywords_srt(start, end, len(keywords_srt)+1, keywords[section]))
#         start = end
    
#     with open("./srt/output.srt", "w") as f:
#         f.write(srt.compose(srts))
    
#     with open("./srt/keywords.srt", "w") as f:
#         f.write(srt.compose(keywords_srt))
    
#     generate_adjusted_audio_from_srt("./srt/output.srt", "./sound/output.wav")
        

def concat_sound_file(Section_List):

    ## 音声を結合する
    output = "voicevox/sound/output.wav"
    afes = []
    for i, section in enumerate(Section_List):
        for j, _ in enumerate(section):
            afes.append(AudioSegment.from_wav(f"voicevox/sound/{i}_{j}.wav"))
    output_sound = AudioSegment.empty()

    for afe in afes:
        output_sound += afe
    output_sound.export(output, format="wav")  

def concat_sound_and_video():
    ## 動画と音声を結合する
    video = "voicevox/video/output.mp4"
    sound = "voicevox/sound/output.wav"
    output = "voicevox/result/output.mp4"

    video = VideoFileClip(video)
    audio = AudioFileClip(sound)
    video = video.set_audio(audio)
    video.write_videofile(output)

# max_length以下の文字数で分割
# 一文ごと渡すようにする。
def combine_elements_until_max_length(data, max_length, total_time):
    if not data:
        return [], []

    combined_list = []
    time_distribution = []
    current_string = ""
    total_length = sum(len(item) for item in data)  # 全テキストの合計文字数

    for item in data:
        if len(current_string + item) <= max_length:
            current_string += item
        else:
            combined_list.append(current_string)
            # 現在の文字列の長さに応じて時間を分割
            current_length = len(current_string)
            allocated_time = (current_length / total_length) * total_time
            time_distribution.append(allocated_time)
            current_string = item

    # 最後のcurrent_stringをリストに追加
    if current_string:
        combined_list.append(current_string)
        current_length = len(current_string)
        allocated_time = (current_length / total_length) * total_time
        time_distribution.append(allocated_time)

    return combined_list, time_distribution


def format_timedelta(td):
    """timedeltaオブジェクトをSRTファイル形式の時間文字列に変換する"""
    total_seconds = int(td.total_seconds())
    milliseconds = int(td.microseconds / 1000)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


# テキストを分割し、SRTファイルに書き込む関数
def split_text_and_write_srt(text, start, end, max_length=15):
    global entry_number
    words = parser.parse(text)
    duration = end - start
    segments, time_segments = combine_elements_until_max_length(words, max_length, duration)

    time_segments = [timedelta(seconds=ts) for ts in time_segments]
    
    start_time = timedelta(seconds=start)
    srt_entries = []
    
    for segment, time in zip(segments, time_segments):
        end_time = start_time + time
        srt_entries.append(srt.Subtitle(index=entry_number,
                                         start=start_time,
                                         end=end_time,
                                         content=segment))
        start_time = end_time
        entry_number += 1

    return srt_entries

def create_keywords_srt(start, end, index, keyword):
    start_time = timedelta(seconds=start)
    end_time = timedelta(seconds=end)
    return srt.Subtitle(index=index, start=start_time, end=end_time, content=keyword)



def combine_video_srt():
    video = VideoFileClip("voicevox/result/output.mp4")
    video = video.resize(width=640)  # 幅を720ピクセルに設定し、高さはアスペクト比を保持
    
    # 字幕テキストを表示するためのカスタム関数
    generator = lambda txt: TextClip(txt, font='/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc', fontsize=36, color='white', stroke_width=1, bg_color='#303030').set_opacity(0.8)

    
    generator_keywords = lambda txt: TextClip(txt, font='/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc', fontsize=36, color='white', stroke_width=1, bg_color='#303030').set_opacity(0.8)
    
    # SubtitlesClipを生成
    srt = SubtitlesClip("voicevox/srt/output.srt", make_textclip=generator)
    keywords_srt = SubtitlesClip("voicevox/srt/keywords.srt", make_textclip=generator_keywords)
    
    # 動画のサイズを取得
    w, h = video.size

    # CompositeVideoClipを使用して、動画と字幕を合成
    final_video = CompositeVideoClip([
        video,
        # 画面の下から40ピクセル上に字幕を配置
        srt.set_position(lambda t: ('center', h - 100)),
        # 画面の上から40ピクセル下にキーワード字幕を配置
        keywords_srt.set_position((20, 20))
    ])
    
    final_video.write_videofile("voicevox/result/output_with_srt.mp4", codec="libx264", fps=24)

def concat_everything(Section_List):
    concat_sound_file(Section_List)
    concat_sound_and_video()
    combine_video_srt()
