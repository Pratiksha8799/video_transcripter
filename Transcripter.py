# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 11:26:04 2024

@author: user
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import regex as re
import os

from youtube_transcript_api import YouTubeTranscriptApi

class YT_transcript():
    def __init__(self,name):
        self.name = name
    @staticmethod    
    def get_youtube_transcript(video_id):
        try:
            # Retrieves the language code.
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            for transcript in transcript_list:
                print(f"Language code: {transcript.language_code}, Language: {transcript.language}")
            code = transcript.language_code
            
            # Fetch the transcript for a particular language code.
            transcript = YouTubeTranscriptApi.get_transcript(video_id,languages=[code])
    
            # Combine transcript into a single string
            transcript_text = "\n".join([entry['text'] for entry in transcript])
    
            return transcript_text
        except Exception as e:
            return str(e)   
    

    def save_transcript_to_file(self, video_id, transcript_text):
        # Create a directory for transcripts if it doesn't exist
        if not os.path.exists('transcripts'):
            os.makedirs('transcripts')
        
        # Define the file name with video ID
        file_name = f'transcripts/{video_id}_transcript.txt'
        
        # Save the transcript text to the file
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(transcript_text)
        
        print(f"Transcript saved to {file_name}")
        
    def yt_interraction(self):
        driver = webdriver.Chrome()
        driver.get('https://www.youtube.com')
        time.sleep(2)
        search = driver.find_element(By.NAME,'search_query')
        search.send_keys(self.name)
        search.send_keys(Keys.ENTER)
        time.sleep(1)
        video_links = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
        time.sleep(2)
        ids =[]

        # Extract and print the href attribute (URL) of each video link
        for i, link in enumerate(video_links[:2]):  # Limit to the first 5 results
            l = link.get_attribute('href')
            time.sleep(1)
            try:
                print(type(l))
                l = re.findall('(?<=v=).*', l)[0]
                print(type(l))
            except Exception as e:
                print("error: ",e)
            ids.append(l)
            time.sleep(1)
        for l in ids:
            text = self.get_youtube_transcript(l)
            self.save_transcript_to_file(l,text)
    
if __name__ == '__main__':
    name = "21 notes in english episode 1"
    obj = YT_transcript(name)
    obj.yt_interraction()
    
    