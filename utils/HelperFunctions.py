from bs4 import BeautifulSoup

def get_audio_ques(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    audio_text_id = soup.find(id="transcript")
    print(audio_text_id.get_text())
    return audio_text_id.get_text()