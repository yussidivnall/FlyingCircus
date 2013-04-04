Some playing with OpenCV

My Idea was to make an app which recognizes celebrities and make money, but google just released an app which does just that (http://www.theverge.com/2013/3/27/4153396/googles-knowledge-graph-expands-into-movies-on-android-tablets-thanks)
So I am dropping this project and putting it in the pool in the hope the code, which is in early development stages and is highly experimental and very messy might one day be usedful to anyone

There's a combination of scripts here.
In the root directory, are some scripts to preform several tasks of face recognition. and experementation.
On the WebServer directory there are some of those tasks automated to use a django webapp.

extract_faces.py -i <input_image> -o [output_directory] -c <cascade classifier (xml)> 
will output objects from input_image to output_directory using <cascade classifier> to match the object.

dump_faces_from_stream.sh <video_file> <output_directory>
Will dump all faces from a video file to an output directory, using a video.flv.frameNNNNN.png.faceM.png where M and N are integers.
It works by first extracting all frames using ffmpeg, and than extracting all faces by using extract_faces.py on all frames.

In the WebServer/ under test2 I implement some basic training using the imdb image database, this is done by some soup script which can easily be modified to use google images or any other imagewebpage.

TODO: This readme and the one under WebServer.
