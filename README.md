YouTube Video Frame Extraction and Transcript PDF Creator
This project allows you to download YouTube videos, extract unique frames from them, and create two PDF files:

A PDF of the extracted frames with timestamps.
A PDF of the video transcript with timestamps.
Requirements
Python 3.x
Required Python packages:
opencv-python-headless
scikit-image
fpdf
yt-dlp
youtube_transcript_api
Pillow
google-colab (for file downloads in Google Colab environments)
You can install the necessary packages using pip:

bash
Copy code
pip install opencv-python-headless scikit-image fpdf yt-dlp youtube_transcript_api pillow google-colab
For the ffmpeg dependency (for video processing), use:

bash
Copy code
!apt-get install ffmpeg
Usage
Script Overview:

The script downloads YouTube videos, extracts unique frames based on their visual similarity, and creates two PDF files:

A PDF with the unique frames from the video.
A PDF containing the transcript of the video with timestamps aligned to the frames.
Functionality:

download_video(url, output_file): Downloads a video from a given URL.
get_video_id(url): Extracts the video ID from a YouTube URL.
get_playlist_videos(playlist_url): Retrieves video URLs from a YouTube playlist.
get_captions(video_id, lang='en'): Fetches subtitles/captions for a given video ID.
extract_unique_frames(video_file, output_folder, n=3, ssim_threshold=0.8): Extracts unique frames from the video based on a similarity threshold.
convert_frames_to_pdf(input_folder, output_file, timestamps): Converts extracted frames to a PDF file.
create_transcripts_pdf(output_file, timestamps, captions): Creates a PDF with the transcript text aligned to the frames' timestamps.
get_video_title(url): Fetches the video title from a YouTube URL.
main(urls): Main function to handle the entire process for given YouTube URLs or playlists.
Running the Script:

To run the script, provide a list of YouTube video URLs or playlist URLs:

python
Copy code
if __name__ == "__main__":
    urls = ["yourlink1","yourlink2"]
    main(urls)
Replace the URL in the urls list with your desired YouTube video or playlist URL.

Output:

Slides PDF: Contains the unique frames extracted from the video.
Transcripts PDF: Contains the transcript text aligned with the frames' timestamps.
The PDFs will be available for download via Google Colab or saved to your local environment if run locally.

Notes
Ensure you have permissions to download and process the videos.
The script uses the yt-dlp library to download videos and extract information.
The cv2 library is used for frame extraction and image processing.
The FPDF library is used for generating PDF files.
Troubleshooting
If you encounter issues with missing packages or dependencies, ensure all required packages are installed.
If you get errors related to YouTube API or video downloading, check the URL format and availability.
Feel free to modify and extend the script as needed for your specific use case.

Feel free to adjust or add any specific details as needed!
