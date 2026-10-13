"""Run with: python app.py"""
from pathlib import Path
from uuid import uuid4
import os

os.environ.setdefault('GRADIO_ANALYTICS_ENABLED', 'False')

import gradio as gr
from groq import APIError, AuthenticationError, RateLimitError

from agent import generate_blog


def run(topic, audience, tone, words, progress=gr.Progress()):
    try:
        blog, outline, review = generate_blog(
            topic, audience, tone, words,
            progress=lambda label: progress(0, desc=label),
        )
        folder = Path(__file__).parent / 'blogs'
        folder.mkdir(exist_ok=True)
        path = folder / f'blog-{uuid4().hex[:12]}.md'
        path.write_text(blog, encoding='utf-8')
        status = 'Revised once' if review['needs_revision'] else 'Accepted without revision'
        return blog, outline, f'{status}\n\n{review["feedback"]}', str(path)
    except AuthenticationError:
        raise gr.Error('Groq rejected the API key. Check your local .env file.') from None
    except RateLimitError:
        raise gr.Error('Groq’s usage limit was reached. Wait and try again, or check your account limits.') from None
    except APIError:
        raise gr.Error('Could not complete the Groq request. Check your connection and model availability.') from None
    except ValueError as error:
        raise gr.Error(str(error)) from None


with gr.Blocks(title='Blog Studio') as demo:
    gr.Markdown('# ✍️ Blog Studio\nTurn an idea into a draft with an outline and editorial review.')
    with gr.Row():
        with gr.Column(scale=1):
            topic = gr.Textbox(label='What would you like to write about?', placeholder='How to start learning Python', lines=3)
            audience = gr.Textbox(label='Audience', value='Complete beginners')
            tone = gr.Dropdown(['Friendly', 'Professional', 'Conversational', 'Educational'], value='Friendly', label='Tone')
            words = gr.Slider(300, 1000, value=600, step=100, label='Approximate word count')
            button = gr.Button('Generate blog', variant='primary')
        with gr.Column(scale=2):
            blog = gr.Markdown('Your blog will appear here.')
            download = gr.File(label='Download Markdown', interactive=False)
    with gr.Accordion('See the outline and editorial review', open=False):
        outline = gr.Markdown()
        review = gr.Markdown()
    gr.Markdown('Up to four model calls per blog. Editorial review does not verify facts. Drafts are saved locally in blogs/.')
    button.click(run, [topic, audience, tone, words], [blog, outline, review, download], concurrency_limit=1)

if __name__ == '__main__':
    demo.queue().launch(inbrowser=True, server_name='127.0.0.1')
