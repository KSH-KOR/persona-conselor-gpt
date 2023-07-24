import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# prompt_with_system = "너는 심리 전문 상담가야. 환자의 질문에 대해서 친절하고 친근한 말투로 답변해줘." 

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        on_question = request.form["on-question"]
        if len(on_question) > 0:
            response = openai.Completion.create(
                model= "curie:ft-personal-2023-07-21-03-37-01", #"davinci:ft-personal:ammmar-hangouts-chatbot-2022-04-30-01-23-28", #"text-davinci-001",
                prompt= on_question.capitalize() + '\n',
                temperature=0.8,
                max_tokens=257,
                stop=["\n ##end##"],
            )
            on_response = response.choices[0].text
            return redirect(url_for("index", on_prompt=on_question, on_result=on_response))

    return render_template("index.html", 
        on_prompt=request.args.get("on_prompt"),
        on_result=request.args.get("on_result"),  
        )

if __name__ == "__main__":
    app.run()

    