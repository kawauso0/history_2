from text_processing import summarize_and_extract_prompts
from video_creator import create_video_from_images, generate_image_with_retry
from voicevox.speech_synthesis import create_sound_files_srt_files, concat_everything
from voicevox.voice import voicevox

def main(input_text, detail_level, language, accuracy, paint_style):
    print(input_text)
    search_result = "検索結果：" + input_text
    prompts = []
    # 読ませたいテキストをリストに格納
    section_lists = [['キリスト教は、紀元1世紀に中東の地で生まれた宗教です。', 'その起源は、イエス・キリストの教えにあります。'], ['キリスト教は、イエスの死後、急速に広がりました。', '彼の弟子たちが、地中海沿岸を中心に布教活動を行いました。'], ['しかし、キリスト教の歴史は平穏なものではありませんでした。', '異教徒からの迫害や、内部の分裂がありました。'], ['現在、キリスト教は世界で最も信者数が多い宗教の一つです。', '世界中に広がり、多様な形で信仰されています。']]
    titles = ['起', '承', '転', '結']

    # section_lists, prompts, titles = summarize_and_extract_prompts(input_text, detail_level, language, accuracy, paint_style)

    print(section_lists)
    print(prompts)
    print(titles)

    durations = []
    durations = create_sound_files_srt_files(section_lists, titles)

    # 1次元配列に変換
    flattened_durations = [item for sublist in durations for item in sublist]
    print(flattened_durations)
    
    # image_urls_with_durations = [(generate_image_with_retry(prompt), duration) for prompt, duration in zip(prompts, flattened_durations)]
    

    # create_video_from_images(image_urls_with_durations, "output.mp4")

    concat_everything(section_lists)



    return search_result, section_lists, prompts, titles
