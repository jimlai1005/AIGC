import os

import openai
from flask import Flask, redirect, render_template, request, url_for
from io import BytesIO
from PIL import Image

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        subject = request.form.get("subject", "今天天氣真好")
        lang = request.form.get("lang", "繁體中文")
        words = request.form.get("words", "150字以內")
        style = request.form.get("style", "蔡康永")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(subject, lang, words, style),
            temperature=0.6,
            max_tokens = 3500
        )


        # # Read the image file from disk and resize it
        # image = Image.open("image.png")
        # width, height = 256, 256
        # image = image.resize((width, height))
        # Convert the image to a BytesIO object
        # byte_stream = BytesIO()
        # image.save(byte_stream, format='PNG')
        # byte_array = byte_stream.getvalue()
        # response = "今天聽到蔡康永老師的話，真的蠻鼓舞人心的：年輕人擁有自己的想法，老闆要有足夠的能力給予他們舞台，讓他們可以表現自己，並且聆聽他們的心聲，讓他們可以成長！"
        
        responseImg = openai.Image.create(
          # prompt="{}".format(response),
          prompt="{}".format(response.choices[0].text),
          # image=byte_array,
          n=1,
          size="512x512"
        )

        # try:
        #   openai.Image.create_variation(
        #     open("image.png", "rb"),
        #     n=1,
        #     size="1024x1024"
        #   )
        #   print(responseImg['data'][0]['url'])
        # except openai.error.OpenAIError as e:
        #   print(e.http_status)
        #   print(e.error)

        return redirect(url_for("index", result=response.choices[0].text, resultImg=responseImg['data'][0]['url']))
        # return redirect(url_for("index", result="123", resultImg=responseImg['data'][0]['url']))

    result = request.args.get("result")
    resultImg = request.args.get("resultImg")
    return render_template("index.html", result=result, resultImg=resultImg)


def generate_prompt(subject, lang, words, style):
    return """你是一個專業的社群貼文寫作專家, 
    請只回應我使用{lang}, 產出{words}的一篇主題為{subject}, 風格接近{style}的講話方式的貼文, 
    另外請再加上對應的hashtag, 並且確保貼文中的hashtag不被重複使用,
    最後, 請不要有任何多餘的說明文字, 謝謝

    如果是張旭的風格, 請根據下面這些文字, 來學習他的用詞與句法結構: 
    講得太好了！
    以前我能力還不夠時，確實會覺得年輕人太有自己的想法，現在我反而同意張琦老師所講，所以身為老闆的我們必須夠強大，夠能給舞台才有資格跟年輕人講話。
    不過呢，又有點不一樣，因為不是所有年輕人都那麼強。
    所以我覺得這段話是講給老闆們聽的，我個人覺得啦。


    """.format(
        subject=subject, lang=lang, words=words, style=style
    )

#     return """Suggest three names for an animal that is a superhero.

# Animal: Cat
# Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# Animal: Dog
# Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# Animal: {}
# Names:""".format(
#         subject.capitalize()
#     )
