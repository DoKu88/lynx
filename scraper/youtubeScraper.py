import yt_dlp
import hashlib
import os

# Download video from metadata using a specified output file format 
def download_video(video_metadata, output_path='../data'):
    url = video_metadata['url'] 
    names = video_metadata['names']
    video_id = video_metadata['id']

    video_path = os.path.join(output_path, 
                              f"{names[0].replace(' ','+')}_{names[1].replace(' ','+')}_%(id)s.%(ext)s")
    print("Downloading video to: ", video_path)

    ydl_opts = {
        'outtmpl': video_path,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print("Downloaded video to: ", video_path)

def download_videos(video_metadata_lst, output_path='../data'):
    # use map reduce to parallelize this
    for video_metadata in video_metadata_lst:
        download_video(video_metadata, output_path)

def get_channel_videos(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Don't download the videos, just retrieve metadata
        'force_generic_extractor': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(channel_url, download=False)
        return info_dict

# filter for specifically lex fridman channel videos
# his videos follow a specific format so we can filter for those
def lex_fridman_channel_videos(video_metadata, min_duration=600, max_duration=25200, delimiter=':', restrict_list=[], restrict_guests=[]):

    if video_metadata['title'] in restrict_list:
        return False
    if video_metadata['title'].find(delimiter) == -1:
        return False
    # We want shorter than 6 hours and longer than 10 minutes 
    if video_metadata['duration'] < min_duration or video_metadata['duration'] > max_duration:
        return False
    
    guest_name = video_metadata['title'].split(delimiter)[0]

    # Only want videos with a real guest, Lex structures his videos with the guest name first
    if not guest_name.replace(" ","").isalpha():
        return False
    if guest_name.lower() in restrict_guests:
        return False
    
    for name in restrict_guests:
        if name in guest_name.lower():
            return False

    video_metadata['names'] = ['lex fridman', guest_name.lower()]

    return True

def get_metadata_from_videos(channel_videos, channel_category):
    video_entries = channel_videos['entries'][0]['entries']
    print("Available Keys: ", video_entries[0].keys())

    video_metadata = []

    for video in video_entries:

        if channel_category == 'lex_fridman':
            if not lex_fridman_channel_videos(video, max_duration=3600, restrict_guests=['mit', 'ai', 'and']):
                continue
                
            video_metadata.append(video)

            print('Title: ', video['title'])
            print('Duration: ', video['duration'])
            print('Names: ', video['names'])
            print('URL: ', video['url'])
            print('id: ', video['id'])

    print('Total Videos: ', len(video_metadata))

    return video_metadata

if __name__ == '__main__':
    channel_videos = get_channel_videos('https://www.youtube.com/@lexfridman')
    video_metadata_lst = get_metadata_from_videos(channel_videos, 'lex_fridman')

    print(video_metadata_lst[0])
    import pdb; pdb.set_trace() # break point before we decide to actually download something

    download_videos(video_metadata_lst[:1], '../data/videoDownloads') # put [:1] to not use a ton of data

