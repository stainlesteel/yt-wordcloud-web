from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled, VideoUnavailable
from wordcloud import WordCloud
import base64
from io import BytesIO
from PIL import Image

app = FastAPI()
temps = Jinja2Templates(directory='templates')

@app.post("/entry")
def entry(url: Annotated[str, Form()], request: Request):

    try:
        langs = ['en', 'en-US', 'en-GB', 'en-auto']
        if "v=" in url:
              id_start = "v="
              if "&" in url:
                     cat_id = url.split(id_start, 1)[1]
                     qwe_id = cat_id.split('&')
                     res_id = qwe_id[0]
                     print(f"id is: {res_id}")
              else:    
                     res_id = url.split(id_start, 1)[1]
                     print(f"id is: {res_id}")
        else:
             res_id = url
             print(f"id is {res_id}")

        api = YouTubeTranscriptApi()
        data = api.fetch(res_id, langs)
        segs = [item.text for item in data]
        txt = " ".join(segs)
        txt2 = txt.replace('""', '')
        txt3 = txt2.replace('.', '')
        wc = WordCloud()
        wc.generate(txt2)
        byts = BytesIO()
        nump = wc.to_array()
        pil = Image.fromarray(nump)
        pil.save(byts, format='PNG')
        byts.seek(0)
        mango = byts.read()
        wc_64 = base64.b64encode(mango)
        wc_78 = wc_64.decode('utf-8').strip()
        return temps.TemplateResponse('index.html', {'request': request, "wordcloud": wc_78})
    except NoTranscriptFound:
             return temps.TemplateResponse('index.html', {'request': request, "error_mesg": "No english transcript found for this video."})
    except TranscriptsDisabled:
             return temps.TemplateResponse('index.html', {'request': request, "error_mesg": "This video does not allow subtitles."})
    except VideoUnavailable:
             return temps.TemplateResponse('index.html', {'request': request, "error_mesg": "Video unavailable, don't use the youtu.be link and remove the t=s20s from your link."})
    

@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    return temps.TemplateResponse('index.html', {'request': request})
