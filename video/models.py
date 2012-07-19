# -*- coding: utf-8 -*-
'''
Created on May 8, 2012

@author: paul
'''
from __future__ import unicode_literals
import re
from unidecode import unidecode
import os
from urllib import urlretrieve
import gridfs
from flaskext.mongoalchemy import BaseQuery

from video import db

class VideoQuery(BaseQuery):

    def by_artist(self, **kwargs):
        return self.filter().ascending(self.type.artist).paginate(**kwargs)

    def by_title(self, **kwargs):
        return self.filter().ascending(self.type.title).paginate(**kwargs)
    

class Video(db.Document):
    
    query_class = VideoQuery

    #patterns to extract video ids from embedded video types
    embed_types = (
        ('youtube', r'youtube\.com\/embed\/([A-Za-z0-9._%-]+)'),
        ('vimeo', r'player\.vimeo\.com\/video\/([A-Za-z0-9._%-]+)'),
        ('pitchfork',''),
    )
    embeds = [e[0] for e in embed_types]
    
    # mongo collection name
    config_collection_name = 'videos'

    url = db.StringField()
    artist = db.StringField()
    artist_slug = db.StringField(required=False)
    title = db.StringField()
    title_slug = db.StringField(required=False)
    image = db.StringField()
    embed_url = db.StringField(required=False, default=None, allow_none=True)
    source = db.EnumField(db.StringField(), *embeds, required=False, default=None, allow_none=True)    
    source_id = db.StringField(required=False)
    image_gridfs = db.ObjectIdField(required=False)
        
        
    def save(self, safe=None):
        
        self.artist_slug = slugify(self.artist)
        self.title_slug = slugify(self.title)
        
        if self.embed_url:
            self._set_video_source_info()
        
        if self.image:
            self._save_img()
            
        return db.Document.save(self, safe)
    
    def _set_video_source_info(self):
        for val,pattern in self.embed_types:
            if val in self.embed_url:
                self.source = val
                self.source_id = re.findall(pattern,self.embed_url)[0]
                break
        
        if not self.source:
            print "No source for %s" % self
            #print 'No source from {1} found in embed_url {2}.'.format(self.embed_types, self.embed_url)
    
    def _save_img(self):
        imgname = self.image.split("/")[-1]
        
        if not imgname:
            return
        
        filepath = os.path.join("/tmp/", imgname)
        urlretrieve(self.image, filepath)
        
        try:
            fs = gridfs.GridFS(Video.query.session.db)
            with open(filepath,'rb') as ifile:
                self.image_gridfs = fs.put(ifile,filename=imgname)
        except Exception as e:
            print e
            print 'Error saving image to GridFS for {1}'.format(self)

            
###########################
# Other functions
###########################

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).split())
    return unicode(delim.join(result))
