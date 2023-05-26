from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError

# YouTube APIキーを設定します
API_KEY = 'your api key'

# YouTube Data APIのビルド
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 検索クエリとして使用するフィギュアスケートのキーワードを指定します
search_query = 'フィギュアスケート　シングル　演技'

try:
    # 検索リクエストを送信し、結果を取得します
    search_response = youtube.search().list(
        q=search_query,
        type='video',
        part='id,snippet',
        maxResults=1000  # 取得する動画の最大数を指定します
    ).execute()

    # 検索結果から動画の情報を取得し、保存します
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        try:
            # YouTubeの動画をダウンロードします
            youtube_video = YouTube(video_url)
            video = youtube_video.streams.filter(file_extension='mp4').first()
            video.download(output_path='result/')

            print(f'Downloaded video: {video.title}')
        except AgeRestrictedError:
            print(f'Skipping age-restricted video: {video_url}')

except HttpError as e:
    print(f'An HTTP error {e.resp.status} occurred: {e.content}')
