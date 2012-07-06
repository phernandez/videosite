
from flask import Flask
from flaskext.mongoalchemy import MongoAlchemy
import video
import unittest
import os
from urllib import urlretrieve
import gridfs

from video.models import Video

class VideoTest(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config.from_object('video.settings')
            
    def test_video_save(self):
        vid = Video(embed_url="http://player.vimeo.com/video/41088675",
                    artist="Mirel Wagner",
                    url="http://pitchfork.com/tv/musicvideos/1983-joe/",
                    image="http://cdn3.pitchfork.com/video-archive/1983/medium.bb8aa5ef.jpg",
                    title="Joe")
        vid.save()
        saved = Video.query.get(vid.mongo_id)
        self.assertIsNotNone(saved, "Video not saved")
        self.assertIsNotNone(saved.source, "No video source set on save")
        self.assertIsNotNone(saved.image_gridfs, "No video gridfs image_gridfs")
        
    def test_video_img(self):
        vid = Video(embed_url="http://player.vimeo.com/video/41088675",
                    artist="Mirel Wagner",
                    url="http://pitchfork.com/tv/musicvideos/1983-joe/",
                    image="http://cdn3.pitchfork.com/video-archive/1983/medium.bb8aa5ef.jpg",
                    title="Joe")
        
        imgname = vid.image.split("/")[-1]
        filepath = os.path.join("/tmp/", imgname)
        urlretrieve(vid.image, filepath)
        
        vid_img = None
        fs = gridfs.GridFS(Video.query.session.db)
        with open(filepath,'rb') as ifile:
            vid_img = fs.put(ifile,filename=imgname)

        out = fs.get(vid_img)
        print out
        
if __name__ == '__main__':
    unittest.main()
