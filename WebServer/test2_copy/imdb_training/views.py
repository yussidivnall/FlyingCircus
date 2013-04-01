from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django import forms

import imdb_utils
import face_utils
def start_page(request):
    return render_to_response('imdb_training/start_page.html')
def search_page(request):
    return render_to_response('imdb_training/search_page.html')
def results_page(request):
    mutils=imdb_utils.imdb_utils()
    if 'q' in request.GET and request.GET['q']:
        actor_list=mutils.search(request.GET['q'])
        #In case imdb redirect to actor's page
        if ( 'status' in actor_list[0]  and  actor_list[0]['status']=='found'):
            #UGLY, not loose coupling!!!
            return HttpResponseRedirect('/imdb_training/actor/?imdb_id='+actor_list[0]['id'])
        #In case no one was found
        if actor_list=='nothing':
            return HttpResponse('nothing found')
        #TODO handle other exceptions (like special charecters) 

        #return render_to_response('imdb_training/results_page.html')
        return render_to_response('imdb_training/results_page.html',{'actors':actor_list,})
    else:
        return HttpResponse('Please submit a search term.')

def actor_page(request):    
    mimdb_utils=imdb_utils.imdb_utils()
    mface_utils=face_utils.face_utils()
    if 'imdb_id' in request.GET and request.GET['imdb_id']:
        mimdb_utils.set_temp_path('/home/volcan/Desktop/development/FlyingCircus/WebServer/media/actors/') #Should come from some static_root
        mface_utils.set_temp_path('/home/volcan/Desktop/development/FlyingCircus/WebServer/media/actors/') #Should come from some static_root
        imdb_id=request.GET['imdb_id']
        picture_index=mimdb_utils.download_all_images(imdb_id) #Populate with original images
        picture_index=mface_utils.extract_from_index(picture_index) # Populate with faces images
        return render_to_response("imdb_training/actor_page.html",{'images_index':picture_index,'imdb_id':imdb_id,}, context_instance = RequestContext(request))
    else: return HttpResponse("could not render this, are we missing ?imdb_id=...")
    #return HttpResponse("Actor...")

#TODO This can only add to positives, not remove, fix in face_utils.set_positives
def update_positives(request):
    if request.method=='POST':
        imdb_id=request.POST['imdb_id']
        mface_utils=face_utils.face_utils()
        mface_utils.set_temp_path('/home/volcan/Desktop/development/FlyingCircus/WebServer/media/actors/') #Should come from some static_root
        picture_index=mface_utils.image_indices_from_imdb_id(imdb_id)
        selected=[]
        for i in request.POST:
            if i.startswith("face"): 
                selected.append(request.POST[i])
        picture_index=mface_utils.set_positives(picture_index,selected)
        mface_utils.save_image_indices(picture_index,imdb_id)
        
        #model=mface_utils.lbph_train(picture_index,selected)
        #picture_index=mface_utils.label_confidence(model,picture_index)
        return render_to_response("imdb_training/update_positives_page.html",{'images_index':picture_index,'imdb_id':imdb_id,'selected':selected}, context_instance = RequestContext(request))
#        html=[]
#        for i in request.POST:
#            html.append(i+"  -  "+request.POST[i]+"<br/>")
#        return HttpResponse('%s' % '\n'.join(html))
    else:
        return HttpResponse("Not a post...")

def train_lbph_page(request):
    if 'imdb_id' in request.GET and request.GET['imdb_id']:
        imdb_id=request.GET['imdb_id']
        mface_utils=face_utils.face_utils()
        mface_utils.set_temp_path('/home/volcan/Desktop/development/FlyingCircus/WebServer/media/actors/') #Should come from some static_root
        picture_index=mface_utils.image_indices_from_imdb_id(imdb_id)
        mface_utils.train_lbph()
        picture_index=mface_utils.predict_lbph_labels(picture_index)
        return render_to_response("imdb_training/training_result_page.html",{'images_index':picture_index,'imdb_id':imdb_id},context_instance = RequestContext(request))
    else: return HttpResponse("could not render this, are we missing ?imdb_id=...")

def train_all_page(request):
    if 'imdb_id' in request.GET and request.GET['imdb_id']:
        imdb_id=request.GET['imdb_id']
        mface_utils=face_utils.face_utils()
        mface_utils.set_temp_path('/home/volcan/Desktop/development/FlyingCircus/WebServer/media/actors/') #Should come from some static_root
        picture_index=mface_utils.image_indices_from_imdb_id(imdb_id)
        mface_utils.train_all()
        picture_index=mface_utils.predict_all_labels(picture_index)
        return render_to_response("imdb_training/training_result_page.html",{'images_index':picture_index,'imdb_id':imdb_id},context_instance = RequestContext(request))
    else: return HttpResponse("could not render this, are we missing ?imdb_id=...")


def test_image(request):
    if request.method=='POST':
        form=upload_file_form(request.POST,request.FILES)
        #Do something with file... (request.FILES[])
        HttpResponse("done...")
    else: 
        form=upload_file_form()
    return render_to_response('imdb_training/upload_form.html',{'form':form})

class upload_file_form(forms.Form):
    title=forms.CharField(max_length=50)
    file =forms.FileField()
