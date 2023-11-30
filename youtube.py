from pytube import YouTube

def download(link,save_path):
    yt = YouTube(link)
    try:
        file_path = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').filter(resolution="1080p").first().download(save_path)
    except:
        try:
            file_path = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').filter(resolution="720p").first().download(save_path)
        except:
            return 0
    return 1
