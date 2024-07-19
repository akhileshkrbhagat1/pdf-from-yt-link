!pip install opencv-python-headless
!pip install scikit-image
!pip install fpdf
!pip install yt-dlp
!pip install youtube_transcript_api
!apt-get install ffmpeg

import sys
import os
import tempfile
import re
from fpdf import FPDF
from PIL import Image
import yt_dlp
import cv2
from skimage.metrics import structural_similarity as compare_ssim
from youtube_transcript_api import YouTubeTranscriptApi
from google.colab import files

def download_video(url, output_file):
    if os.path.exists(output_file):
        os.remove(output_file)
    ydl_opts = {
        'outtmpl': output_file,
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def get_video_id(url):
    # Match YouTube Shorts URLs
    video_id_match = re.search(r"shorts\/(\w+)", url)
    if video_id_match:
        return video_id_match.group(1)

    # Match youtube.be shortened URLs
    video_id_match = re.search(r"youtu\.be\/([\w\-_]+)(\?.*)?", url)
    if video_id_match:
        return video_id_match.group(1)
               
    # Match regular YouTube URLs
    video_id_match = re.search(r"v=([\w\-_]+)", url)
    if video_id_match:
        return video_id_match.group(1)

    # Match YouTube live stream URLs
    video_id_match = re.search(r"live\/(\w+)", url)  
    if video_id_match:
        return video_id_match.group(1)

    return None

def get_playlist_videos(playlist_url):
    ydl_opts = {
        'ignoreerrors': True,
        'playlistend': 1000,  # Maximum number of videos to fetch
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        return [entry['url'] for entry in playlist_info['entries']]

def get_captions(video_id, lang='en'):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        captions = [(t['start'] * 1000, t['duration'] * 1000, t['text']) for t in transcript]
        return captions
    except Exception as e:
        print(f"Error fetching captions: {e}")
        return None

def extract_unique_frames(video_file, output_folder, n=3, ssim_threshold=0.8):
    cap = cv2.VideoCapture(video_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    last_frame = None
    saved_frame = None
    frame_number = 0
    last_saved_frame_number = -1
    timestamps = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_number % n == 0:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.resize(gray_frame, (128, 72))

            if last_frame is not None:
                similarity = compare_ssim(gray_frame, last_frame, data_range=gray_frame.max() - gray_frame.min())

                if similarity < ssim_threshold:
                    if saved_frame is not None and frame_number - last_saved_frame_number > fps:
                        frame_path = os.path.join(output_folder, f'frame{frame_number:04d}_{frame_number // fps}.png')
                        cv2.imwrite(frame_path, saved_frame)
                        timestamps.append((frame_number, frame_number // fps))

                    saved_frame = frame
                    last_saved_frame_number = frame_number
                else:
                    saved_frame = frame

            else:
                frame_path = os.path.join(output_folder, f'frame{frame_number:04d}_{frame_number // fps}.png')
                cv2.imwrite(frame_path, frame)
                timestamps.append((frame_number, frame_number // fps))
                last_saved_frame_number = frame_number

            last_frame = gray_frame

        frame_number += 1

    cap.release()
    return timestamps

def convert_frames_to_pdf(input_folder, output_file, timestamps):
    page_width = 1920
    page_height = 1080
    
    frame_files = sorted(os.listdir(input_folder), key=lambda x: int(x.split('_')[0].split('frame')[-1]))
    pdf = FPDF("L")
    pdf.set_auto_page_break(0)

    for i, (frame_file, (frame_number, timestamp_seconds)) in enumerate(zip(frame_files, timestamps)):
        frame_path = os.path.join(input_folder, frame_file)
        image = Image.open(frame_path)
        pdf.add_page()
        pdf.image(frame_path, x=0, y=0, w=pdf.w, h=pdf.h)

        timestamp = f"{timestamp_seconds // 3600:02d}:{(timestamp_seconds % 3600) // 60:02d}:{timestamp_seconds % 60:02d}"
        
        x, y, width, height = 5, 5, 60, 15
        region = image.crop((x, y, x + width, y + height)).convert("L")
        mean_pixel_value = region.resize((1, 1)).getpixel((0, 0))
        if mean_pixel_value < 64:
            pdf.set_text_color(255, 255, 255)
        else:
            pdf.set_text_color(0, 0, 0)

        pdf.set_xy(x, y)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 0, timestamp)

    pdf.output(output_file)

def create_transcripts_pdf(output_file, timestamps, captions):
    pdf = FPDF("P")
    pdf.set_auto_page_break(0)
    page_height = pdf.h

    caption_index = 0
    for i, (frame_number, timestamp_seconds) in enumerate(timestamps):
        pdf.add_page()

        timestamp = f"{timestamp_seconds // 3600:02d}:{(timestamp_seconds % 3600) // 60:02d}:{timestamp_seconds % 60:02d}"
        pdf.set_text_color(0, 0, 0)
        pdf.set_xy(10, 10)
        pdf.set_font("Arial", size=14)
        pdf.cell(0, 0, timestamp)

        if captions and caption_index < len(captions):
            transcript = ""
            start_time = 0 if i == 0 else timestamps[i - 1][1]
            end_time = timestamp_seconds

            while caption_index < len(captions) and start_time * 1000 <= captions[caption_index][0] < end_time * 1000:
                transcript += f"{captions[caption_index][2]}\n"
                caption_index += 1

            pdf.set_text_color(0, 0, 0)
            pdf.set_xy(10, 25)
            pdf.set_font("Arial", size=10)
            lines = transcript.split("\n")
            for line in lines:
                if pdf.get_y() + 10 > page_height:
                    pdf.add_page()
                    pdf.set_xy(10, 10)
                pdf.cell(0, 10, line)
                pdf.ln()

    pdf.output(output_file)

def get_video_title(url):
    ydl_opts = {
        'skip_download': True,
        'ignoreerrors': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(url, download=False)
        title = video_info['title'].replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('<', '-').replace('>', '-').replace('|', '-').replace('"', '-').strip('.')
        return title

        
def main(urls):
    video_urls = []
    for url in urls:
        if 'playlist?list=' in url:
            video_urls.extend(get_playlist_videos(url))
        else:
            video_urls.append(url)

    for video_url in video_urls:
        video_id = get_video_id(video_url)
        if not video_id:
            print(f"Invalid URL: {video_url}")
            continue

        video_title = get_video_title(video_url)
        video_file = f"video_{video_id}.mkv"  # Change this line if needed
        download_video(video_url, video_file)

        captions = get_captions(video_id)

        output_pdf_filename = f"{video_title}.pdf"
        transcript_pdf_filename = f"txt_{video_title}.pdf"

        with tempfile.TemporaryDirectory() as tmp_dir:
            frames_folder = os.path.join(tmp_dir, "frames")
            os.makedirs(frames_folder)

            timestamps = extract_unique_frames(video_file, frames_folder)
            convert_frames_to_pdf(frames_folder, output_pdf_filename, timestamps)
            create_transcripts_pdf(transcript_pdf_filename, timestamps, captions)

        print(f"Slides PDF: {output_pdf_filename}")
        print(f"Transcripts PDF: {transcript_pdf_filename}")
        files.download(output_pdf_filename)
        files.download(transcript_pdf_filename)
        

if __name__ == "__main__":
    urls = ["yt_link1","yt_link2]
    main(urls)
