from highlight import highlight
from youtube import download

LINK="https://www.youtube.com/watch?v=3ryID_SwU5E"

    
file_path = download(LINK,"temp")
highlight(file_path)