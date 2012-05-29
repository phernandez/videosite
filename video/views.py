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
def list_videos(page=1):
    title = u'Video list'
    pagination = Video.query.paginate(page=page, per_page=5)
    return render_template('/video/video_list.html', pagination=pagination, title=title)

@app.route('/videos/show/<id>')
def video_detail(id):
    video = Video.query.get_or_404(id)
    title = "{artist} - {title}".format(artist=video.artist, title=video.title)
    source = str(video.source).lower()
    return render_template('/video/video_{0}.html'.format(source), video=video, title=title)

@app.route('/videos/show/image/<id>')
def video_image(id):
    video = Video.query.get_or_404(id)
    return gridfs_file(video.image_gridfs)

def gridfs_file(oid):
    try:
        file = fs.get(oid)
        return Response(file, mimetype=file.content_type, direct_passthrough=True)
    except NoFile:
        abort(404)         