from pytube import YouTube, Playlist 
from moviepy.editor import *

#params: playlist (youtube playlist to download from), videoDir (directory to save videos), audioDir (directory to save audio (song) files)
def downloadVideos(playlist = 'https://youtube.com/playlist?list=PLOi9Cf_JAyXLlJ9Hpph56NAYet_bp_I9g', videoDir="/Users/kylersaiki/Desktop/testFilter/videoDirectory", audioDir="/Users/kylersaiki/Desktop/testFilter/audioDirectory"):
    p = Playlist(playlist)
    videoLengths = []
    videoNames = []

    index = 0
    for url in p:
        YouTube(url).streams.filter(file_extension='mp4').first().download(output_path='/Users/kylersaiki/Desktop/testFilter/videoDirectory', filename=(str(index) + '.mp4'))

        videoLengths.append(YouTube(url).length)
        videoNames.append(YouTube(url).title)
        print(videoLengths[index])

        mp4_file = videoDir + '/' + str(index) + '.mp4' 
        mp3_file = audioDir + '/' + str(index) + '.mp3' 
        
        audioclip = VideoFileClip(mp4_file).audio
        os.remove(mp4_file)
        audioclip.write_audiofile(mp3_file)
        audioclip.close()
        
        index += 1
        return
downloadVideos()