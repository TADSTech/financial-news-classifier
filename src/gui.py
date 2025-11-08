import gradio as gr
from core.infer import predict
from core.rss import fetch_rss

def classify_text(text):
    sentiment, conf = predict(text)
    return f"{sentiment} ({conf:.2f})"

def classify_rss(url):
    headlines = fetch_rss(url)
    results = [predict(h)[0] for h in headlines]
    return dict(zip(headlines, results))

def launch_gui():
    with gr.Blocks(title="Financial News Classifier") as demo:
        gr.Markdown("## 🧠 Financial News Classifier\nClassify financial text, files, or RSS feeds locally.")

        with gr.Tab("Text"):
            txt = gr.Textbox(label="Enter headline or text")
            out = gr.Textbox(label="Predicted Sentiment")
            txt.submit(classify_text, inputs=txt, outputs=out)

        with gr.Tab("RSS"):
            rss_in = gr.Textbox(label="RSS Feed URL")
            rss_out = gr.JSON(label="Results")
            rss_in.submit(classify_rss, inputs=rss_in, outputs=rss_out)

    demo.launch()
