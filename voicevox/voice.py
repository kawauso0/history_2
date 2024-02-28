from pathlib import Path
from voicevox_core import AccelerationMode, VoicevoxCore
import pysrt
from pydub import AudioSegment
import wave

SPEAKER_ID = 3

open_jtalk_dict_dir = 'voicevox/open_jtalk_dic_utf_8-1.11'
# open_jtalk_dict_dir = Path('/Users/issei/Documents/GitHub/OneMinuteVideoMaker/webapp/voicevox/open_jtalk_dic_utf_8-1.11')

# text = 'I went to the store to buy some groceries.'
# out = Path('output.wav')
acceleration_mode = AccelerationMode.AUTO

def voicevox(text, path, speed=1.0):
    write_path = Path(path)
    core = VoicevoxCore(
        acceleration_mode=acceleration_mode, open_jtalk_dict_dir=open_jtalk_dict_dir
    )
    core.load_model(SPEAKER_ID)
    audio_query = core.audio_query(text, SPEAKER_ID) 
    audio_query.speed_scale = speed
    wav = core.synthesis(audio_query, SPEAKER_ID)
    write_path.write_bytes(wav)
    # playsound(path)
    with wave.open(path, mode='rb') as wf:
        time = float(wf.getnframes() / wf.getframerate())
    return time

def generate_adjusted_audio_from_srt(srt_file_path, output_path):
    subs = pysrt.open(srt_file_path)
    output_path = Path(output_path)
    combined_audio = AudioSegment.empty()
    sum_time = 0

    for sub in subs:
        text = sub.text_without_tags  # HTMLタグを除去したテキスト
        start_time = sub.start.ordinal / 1000  # 開始時間（ミリ秒を秒に変換）
        end_time = sub.end.ordinal / 1000  # 終了時間
        duration = end_time - start_time  # 表示期間
        sum_time += duration

        temp_audio_path = f"./temp/temp_audio_{sub.index}.wav"
        
        # テキストを音声に変換し、表示期間に合わせて速度を調整するための初期推定値を設定
        estimated_speed = 1.0  # 初期推定速度
        estimated_time = voicevox(text, temp_audio_path, estimated_speed)
        
        # 実際の表示期間に合わせて速度を調整
        speed_scale = estimated_time / duration
        adjusted_audio_path = f"./temp/adjusted_audio_{sub.index}.wav"
        voicevox(text, adjusted_audio_path, speed_scale)
        audio_segment = AudioSegment.from_wav(adjusted_audio_path)
        combined_audio += audio_segment

        # 不要になった一時ファイルの削除
        Path(temp_audio_path).unlink()
        Path(adjusted_audio_path).unlink()
    
    # すべての音声を結合
    combined_audio.export(output_path, format="wav")

    def sample():
        pass


if __name__ == "__main__":
    generate_adjusted_audio_from_srt("./srt/output.srt", "./temp/output_with_srt.wav")