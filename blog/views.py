from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.views.generic.list import ListView
from .models import BlogPost, VersionPost, ReplyPost
from .forms import CreateBlogForm
from django.urls import reverse_lazy,reverse
from django.core.serializers import serialize
import uuid
import json

# Create your views here.
class CreateBlog(CreateView):
    model = BlogPost
    template_name = "create_blog.html"
    fields = '__all__'
    # success_url = reverse_lazy("update_blog",kwargs={"uuid":"c84eeaa3-f9ca-4835-b9e6-d5c4cfa6bb7b"})
    # def post(self,request,*args,**kwargs):
    #     if request.method == "POST":
    #         super().post(request,*args,**kwargs)
    #         x = BlogPost.objects.get(author=request.POST['author'])
    #         return redirect(reverse("update_blog",kwargs={'uuid':x.blog_id}))
    #     return HttpResponse("going to update you niga")

class HomeBlog(ListView):
    model = BlogPost 
    template_name = "home.html"
    context_object_name = "blogs"
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        blogs_list = BlogPost.objects.all()
        #lets map them together
        combined_list = []
        for blog in blogs_list:
            version = VersionPost.objects.filter(blog=blog).first()
            combined_list.append((blog,version))
        context["blog_version"] = combined_list
        return context

    

class UpdateBlog(UpdateView):
    model = BlogPost 
    template_name = "update_blog.html"
    context_object_name = "blogs"
    pk_url_kwarg = "uuid"
    fields = '__all__'
    success_url = reverse_lazy("home")

    def post(self,request,*args,**kwargs):
        if request.method == "POST":
            #get the versionPost 
            blogPost = BlogPost.objects.get(blog_id = kwargs['uuid'].value)
            versionPost = VersionPost.objects.filter(blog_id=blogPost.blog_id).first()
            versionList = request.POST['blog_content']
            if versionPost:
                if isinstance(versionPost.versions,list):
                    versionPost.versions.append(versionList)
                elif isinstance(versionPost.versions,str):
                    versionPost.versions = [versionPost.versions]
                    versionPost.versions.append(versionList)
                versionPost.save()
            else:
                VersionPost.objects.create(blog_id=kwargs['uuid'].value,name=blogPost.title,versions=[versionList])
        return super().post(request,*args,**kwargs)

class LookBlog(ListView):
    model = BlogPost
    template_name = "blog_detail.html"
    pk_url_kwarg = "uuid"
    
    # def fetchReplies(self, CommentID,margin_left,repliesData):
    #         #get the replyData
    #         #but first check it has reply or not
    #         replyData = ReplyPost.objects.filter(replyId = CommentID).first()
            
    #         repliesData.append(f'''
    #                         <div style='margin-left:{margin_left}' data-replyID={replyData.replyId} class="reply-container">
    #                             <div class="reply" contenteditable=false>{replyData.replyData}</div>
    #                             <button class='add-reply-btn' onClick="addReply()">Reply</button>
    #                             <button class='save-reply-btn' onClick="saveReply()">Save</button>
    #                             <button class='delete-reply-btn' onClick="deleteReply()">Delete</button>
    #                         </div>
    #                     ''')
    #         if replyData.hasReply == True:
    #             childrenReplyID = replyData.childrenReplyId
    #             if isinstance(childrenReplyID,list):
    #                 for replyID in childrenReplyID:
    #                     self.fetchReplies(replyID,margin_left+15,repliesData)
 
    def get_context_data(self, **kwargs):
        repliesData = []
        blog_id = self.kwargs['uuid'].value
        blog = BlogPost.objects.filter(blog_id = blog_id).first()
        version = VersionPost.objects.filter(blog = self.kwargs['uuid'] ).first()
        # replies = ReplyPost.objects.filter(parentId = blog_id)
        # for reply in replies:
        #     replyId = reply.replyId
        #     self.fetchReplies(replyId,15,repliesData)
        # lets map them together
        # return {"blog":blog,"version":version,"replies":repliesData}
        return {"blog":blog,"version":version}
        

class ReplyBlog(View):
    model = ReplyPost
    template_name = "reply.html"

    def updateParentReply(self,childId,parentId):
        #fetch the parentID
        parentReply = ReplyPost.objects.filter(replyId = parentId).first()
        if parentReply:
            #get the children list and make hasReply True
            parentReply.hasReply= True
            parentReply.childrenReplyId.append(childId)
            parentReply.save()

    def deleteChildrenReplies(self,parentReply):
        #get the childRepliesID
        if parentReply.hasReply == True:
            childrenId = parentReply.childrenReplyId
            for cid in childrenId:
                #get the id
                children = ReplyPost.objects.filter(replyId = cid).first()
                if children:
                    self.deleteChildrenReplies(children)
        parentReply.delete()

    def prepareRequestData(self,request):
        raw_data = request.body
        # Step 2: Decode the byte data to a string
        data_str = raw_data.decode('utf-8')
        # Step 3: Convert the string to a dictionary (assuming JSON format)
        data_dict = json.loads(data_str)
        return data_dict
    
    def fetchReplies(self, CommentID,repliesData):
            #get the replyData
            #but first check it has reply or not
            replyData = ReplyPost.objects.filter(replyId = CommentID).first()
            
            if replyData:
                repliesData.append(replyData)
                if replyData.hasReply == True:
                    childrenReplyID = replyData.childrenReplyId
                    if isinstance(childrenReplyID,list):
                        for replyID in childrenReplyID:
                            self.fetchReplies(replyID,repliesData)
                       
        

    def get(self,request,*args,**kwargs):
        blog_id = request.GET['blog_id']
        replies_data = []
        parentReplies = ReplyPost.objects.filter(parentId = blog_id)
        for reply in parentReplies:
            self.fetchReplies(reply.replyId,replies_data)
        data = serialize('json', replies_data)
        data = json.loads(data)
        return JsonResponse({"replyData":data})

    def post(self,request,*args,**kwargs):
        data = self.prepareRequestData(request)
        if data['type'] == "Create":
            replyData = data['replyData']
            parentId = data['parentId']
            upvote = data['upvote']
            downvote = data['downvote']
            parentId = data['parentId']
            replyId = uuid.uuid4().value
            #update the parentReply
            if not data['isComment']:
                self.updateParentReply(replyId,parentId)
            ReplyPost.objects.create(parentId=parentId,replyId=replyId,replyData=replyData,upvote=upvote,downvote=downvote)
            return JsonResponse({"replyId":replyId})
       


    # def update(self,request,*args,**kwargs):
    #     data = self.prepareRequestData(request)
    #     #do the stuff on 
    #     return HttpResponse({"msg":"[+] Data update Successfully.","updatedDate":reply['updateReplyDate']})


            

    def delete(self,request,*args,**kwargs):
        data = self.prepareRequestData(request)
        reply = ReplyPost.objects.filter(replyId = data['replyId']).first()
        self.deleteChildrenReplies(reply)
        return JsonResponse({"msg":"[+]Deleted all reply successfully"})