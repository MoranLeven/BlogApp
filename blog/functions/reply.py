import json
import uuid


reply = {
            'content': "I'm a small reply", 
            'hasReply': True, 
            'reply': {
                'content': "i'm a reply to another reply", 
                'hasReply': True, 
                'reply': {
                    'content': "i'm the last reply",
                    'hasReply': True,
                    'reply': {
                        'content': "I'm last one 😅", 
                        'hasReply': True, 
                        'reply': {
                            'content': 'REPLY NO 1 ', 
                            'hasReply': True, 
                            'reply': {
                                'content': 'REPLY NO 2 ', 
                                'hasReply': True, 
                                'reply': {
                                    'content': 'REPLY NO 3 ', 
                                    'hasReply': True, 
                                    'reply': {
                                        'content': 
                                        'REPLY NO 4 ', 
                                        'hasReply': False, 
                                        'reply': None
                                        }
                                    }

                                }
                            }
                        }
                    }
                }
            }

update_reply = {
                    "ParentReplyID":uuid.uuid4().value,
                    "ReplyID":uuid.uuid4().value,
                    "upvote":0,
                    "downvote":0,
                    "ChildrenReplyID":[uuid.uuid4().value],
                    "hasReply":True,
                    "visited":"",
                    "replyContent":"I'm a small reply."
                } 

displayData = []
def displayReplies(CommentID,margin_left):
    #get the replyData
    #but first check it has reply or not
    replyData = Reply.objects.filter(replyID = CommentID).first()
    displayData.append(f'''
                    <div style='margin-left:{margin_left}' data-replyID={replyData['replyID']} class="reply-container">
                        <div class="reply" contenteditable=false>{replyData['replyContent']}</div>
                        <button class='add-reply-btn' onClick="addReply()">Reply</button>
                        <button class='save-reply-btn' onClick="saveReply()">Save</button>
                        <button class='delete-reply-btn' onClick="deleteReply()">Delete</button>
                    </div>
                   ''')
    if replyData['hasReply'] == True:
        childrenReplyID = replyData['childrenReplyID']
        if isinstance(childrenReplyID,list):
            for replyID in replyData['childrenReplyID']:
                displayReplies(replyID,margin_left+50)


                


        

def fetchReplies(reply):
    all_replies = []
    while(True):
        if reply['hasReply']:
            all_replies.append(reply['content'])
        else:
            all_replies.append(reply['content'])
            break
        reply = reply['reply']
    return all_replies

def saveReplies(reply,content):
    if  reply['hasReply'] == True:
        saveReplies(reply['reply'],content)

    if reply['hasReply'] == False:
        reply['hasReply'] = True
        reply['reply'] ={
            "content":content,
            "hasReply":False,
            "reply":None
        }
    return reply


reply = saveReplies(reply,"I'm last one 😅")
reply = saveReplies(reply,"REPLY NO 1 ")
reply = saveReplies(reply,"REPLY NO 2 ")
reply = saveReplies(reply,"REPLY NO 3 ")
reply = saveReplies(reply,"REPLY NO 4 ")
print(json.loads(json.dumps(reply)))
print(fetchReplies(reply))


print(ReplyPost.objects.all())