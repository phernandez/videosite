'''
Created on Dec 30, 2011

@author: paul
'''
from selenium import webdriver
from tutorial.spiders.pitchfork import parse_detail_with_selenium
import unittest

class Test(unittest.TestCase):

    vimeo_vid_url = 'http://pitchfork.com/tv/musicvideos/1513-possession'
    youtube_vid_url = 'http://pitchfork.com/tv/musicvideos/1606-benefits/'
    
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()
        
    def test_pitchfork_vimeo(self):
        result = parse_detail_with_selenium(self.driver, self.vimeo_vid_url)
        self.assertEqual('http://player.vimeo.com/video/30273829?title=0&byline=0&portrait=0', result)

    def test_pitchfork_youtube(self):
        result = parse_detail_with_selenium(self.driver, self.youtube_vid_url)
        self.assertEqual('http://www.youtube.com/v/vjhX6h5Httk?version=3&feature=oembed', result)

    def test_youtube_iframe(self):
        result = parse_detail_with_selenium(self.driver, 'http://pitchfork.com/tv/musicvideos/1707-motivate-to-be-rich-ft-dallas-tha-kid/')
        self.assertEqual('http://www.youtube.com/embed/5nCxdYgkFCE?fs=1&feature=oembed', result)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_pitchfork_selenium']
    unittest.main()