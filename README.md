YouTube Video Frame Extraction and Transcript PDF Creator
=========================================================

This project allows you to download YouTube videos, extract unique frames from them, and create two PDF files:

*   A PDF of the extracted frames with timestamps.
    
*   A PDF of the video transcript with timestamps.
    

Requirements
------------

*   Python 3.x
    
*   Required Python packages:
    
    *   opencv-python-headless
        
    *   scikit-image
        
    *   fpdf
        
    *   yt-dlp
        
    *   youtube\_transcript\_api
        
    *   Pillow
        
    *   google-colab (for file downloads in Google Colab environments)
        

You can install the necessary packages using pip:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install opencv-python-headless scikit-image fpdf yt-dlp youtube_transcript_api pillow google-colab   `

For the ffmpeg dependency (for video processing), use:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   !apt-get install ffmpeg   `

Usage
-----

### Script Overview:

The script downloads YouTube videos, extracts unique frames based on their visual similarity, and creates two PDF files:

*   A PDF with the unique frames from the video.
    
*   A PDF containing the transcript of the video with timestamps aligned to the frames.
    

### Functionality:

*   download\_video(url, output\_file): Downloads a video from a given URL.
    
*   get\_video\_id(url): Extracts the video ID from a YouTube URL.
    
*   get\_playlist\_videos(playlist\_url): Retrieves video URLs from a YouTube playlist.
    
*   get\_captions(video\_id, lang='en'): Fetches subtitles/captions for a given video ID.
    
*   extract\_unique\_frames(video\_file, output\_folder, n=3, ssim\_threshold=0.8): Extracts unique frames from the video based on a similarity threshold.
    
*   convert\_frames\_to\_pdf(input\_folder, output\_file, timestamps): Converts extracted frames to a PDF file.
    
*   create\_transcripts\_pdf(output\_file, timestamps, captions): Creates a PDF with the transcript text aligned to the frames' timestamps.
    
*   get\_video\_title(url): Fetches the video title from a YouTube URL.
    
*   main(urls): Main function to handle the entire process for given YouTube URLs or playlists.
    

### Running the Script:

To run the script, provide a list of YouTube video URLs or playlist URLs:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   if __name__ == "__main__":      urls = ["yourlink1", "yourlink2"]      main(urls)   `

Replace the URL in the urls list with your desired YouTube video or playlist URL.

Output:
-------

*   **Slides PDF**: Contains the unique frames extracted from the video.
    
*   **Transcripts PDF**: Contains the transcript text aligned with the frames' timestamps.
    

The PDFs will be available for download via Google Colab or saved to your local environment if run locally.

Notes
-----

*   Ensure you have permissions to download and process the videos.
    
*   The script uses the yt-dlp library to download videos and extract information.
    
*   The cv2 library is used for frame extraction and image processing.
    
*   The FPDF library is used for generating PDF files.
    

Troubleshooting
---------------

*   If you encounter issues with missing packages or dependencies, ensure all required packages are installed.
    
*   If you get errors related to YouTube API or video downloading, check the URL format and availability.
    

Feel free to modify and extend the script as needed for your specific use case.
