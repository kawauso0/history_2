import re
import openai

def initialize_openai_api():
    openai.api_key = OPENAI_API_KEY

def summarize_and_extract_prompts(input_text, detail_level, language, accuracy, paint_style):
    initialize_openai_api()  # APIキーの初期化
    prompt = f"""起承転結の4段落で、{detail_level}レベルの詳しさで、ですます調で解説してください。各段落は2文からなり、段落ごとに100文字程度です。
                段落ごとに『』で囲い、その中の一文ごとに「」で囲んでください
                また、各段落ごとに起承転結以外のタイトルを付けて、【】で囲んでください"""
    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        max_tokens=1000,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text}
        ],
        temperature = (10 - accuracy) / 10,
        top_p=0,
    )

    response_text = response.choices[0].message['content']
    texts = [re.findall(r'「(.*?)」', section) for section in re.findall(r'『(.*?)』', response_text, re.DOTALL)]
    titles = re.findall(r'【(.*?)】', response_text)

    # プロンプト生成部分
    prompts = []
    flattenend_texts = [text for sublist in texts for text in sublist]
    for f_text in flattenend_texts:
        prompt = f"{input_text}に関連したこの文章を{paint_style}のスタイルで描写する絵をdalleで生成するためのプロンプトを英語で考えてください。"
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            max_tokens=1000,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f_text}
            ],
        )
        response_text = response.choices[0].message['content']
        prompts.append(response_text)

    return texts, prompts, titles
