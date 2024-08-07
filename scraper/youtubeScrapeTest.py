import yt_dlp

def download_video(url, output_path='../data'):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    video_url = 'https://www.youtube.com/shorts/EAiP4R6_q_4'
    download_video(video_url)

