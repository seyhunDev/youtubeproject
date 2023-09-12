from flask import Flask, render_template, request
from googleapiclient.discovery import build
from datetime import datetime, timedelta

app = Flask(__name__)

# YouTube API anahtarını buraya ekleyin
API_KEY = 'AIzaSyDqmbXFB6a9UvucWz7sDdFHLI1hAGy5YFY'

def get_video_details(youtube, video_ids):
    video_details = youtube.videos().list(
        part='snippet,statistics',
        id=','.join(video_ids)
    ).execute()

    thumbnails = {}
    for video in video_details.get('items', []):
        thumbnails[video['id']] = video['snippet']['thumbnails']['maxres']['url']

    return video_details.get('items', []), thumbnails

@app.route('/', methods=['GET', 'POST'])
def index():
    # Kullanıcıdan gelen arama sorgusunu alın
    search_query = request.form.get('search_query', '')

    # YouTube API istemcisini oluşturun
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # 1 ay önceki tarihi hesaplayın ve ISO 8601 formatına dönüştürün
    one_month_ago = datetime.now() - timedelta(days=10)  # 1 ay 30 gündür
    published_after = one_month_ago.isoformat() + 'Z'

    # Arama sorgusunu yapın (ilk veri seti)
    search_response = youtube.search().list(
        q=search_query,
        type='video',
        part='id',
        maxResults=10,  # İlk 10 sonucu almak için
        order='viewCount',  # İzlenme sayısına göre sırala
        publishedAfter=published_after,  # Bu ay başından itibaren
    ).execute()

    # En çok izlenen videoların video ID'lerini alın (ilk veri seti)
    video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

    # Video detaylarını alın (ilk veri seti)
    video_details, thumbnails = get_video_details(youtube, video_ids)

    # Bugünün tarihini hesaplayın ve ISO 8601 formatına dönüştürün
    today = datetime.now() - timedelta(days=1)  # 1 ay 30 gündür
    published_after_two = today.isoformat() + 'Z'

    # İkinci veri seti sorgusu
    search_response_two = youtube.search().list(
        q=search_query,
        type='video',
        part='id',
        maxResults=10,
        order='viewCount',
        publishedAfter=published_after_two,
    ).execute()

    # En çok izlenen videoların video ID'lerini alın (ikinci veri seti)
    video_ids_two = [item['id']['videoId'] for item in search_response_two.get('items', [])]

    # Video detaylarını alın (ikinci veri seti)
    video_details_two, thumbnails_two = get_video_details(youtube, video_ids_two)
    




    mounth = datetime.now() - timedelta(days=30)  # 1 ay 30 gündür
    published_after_three = mounth.isoformat() + 'Z'

    # İkinci veri seti sorgusu
    search_response_three = youtube.search().list(
        q=search_query,
        type='video',
        part='id',
        maxResults=10,
        order='viewCount',
        publishedAfter=published_after_three,
    ).execute()

    # En çok izlenen videoların video ID'lerini alın (ikinci veri seti)
    video_ids_three = [item['id']['videoId'] for item in search_response_three.get('items', [])]

    # Video detaylarını alın (ikinci veri seti)
    video_details_three, thumbnails_three = get_video_details(youtube, video_ids_three)

    # HTML şablonunu kullanarak sayfayı görüntüle
    return render_template('index.html', search_query=search_query, video_details=video_details, thumbnails=thumbnails, video_details_two=video_details_two, thumbnails_two=thumbnails_two, video_details_three=video_details_three, thumbnails_three=thumbnails_three)



if __name__ == '__main__':
    app.run()
