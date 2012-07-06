'''
Created on May 8, 2012

@author: paul
'''
from bson.objectid import ObjectId
from flask import render_template, redirect, url_for, abort, request, current_app
from flask.wrappers import Response
from gridfs.errors import NoFile
from video import app
from video.models import Video
from werkzeug.wsgi import wrap_file
import gridfs
 
fs = gridfs.GridFS(Video.query.session.db)

@app.route('/videos')
@app.route('/videos/<int:page>')
def video_list(page=1):
    title = u'Video list'
    pagination = Video.query.paginate(page=page, per_page=5)
    return render_template('/video/video_list.html', pagination=pagination, title=title)

@app.route('/videos/show/<vid>')
def video_detail(vid):
    video = Video.query.get_or_404(vid)
    title = "{artist} - {title}".format(artist=video.artist, title=video.title)
    source = str(video.source).lower()
    return render_template('/video/video_{0}.html'.format(source), video=video, title=title)

@app.route('/videos/show/image/<vid>')
def video_image(vid):
    video = Video.query.get_or_404(vid)
    return gridfs_file(video.image_gridfs)

@app.route('/artists')
@app.route('/artists/<int:page>')
def artist_list(page=1):
    title = u'Artist list'
    pagination = Video.query.by_artist(page=page, per_page=5)
    return render_template('/video/artist_list.html', pagination=pagination, title=title)

def gridfs_file(oid):
    try:
        gfile = fs.get(oid)
        return Response(gfile, mimetype=gfile.content_type, direct_passthrough=True)
    except NoFile:
        abort(404)         