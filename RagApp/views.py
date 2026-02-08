from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import pymysql
from django.core.files.storage import FileSystemStorage
from datetime import date
from transformers import AutoTokenizer, RagRetriever, RagSequenceForGeneration, RagTokenForGeneration
import torch
import numpy as np
from numpy import dot
from numpy.linalg import norm
import os
import boto3

global uname, tokenizer, retriever, model
tokenizer = AutoTokenizer.from_pretrained("facebook/rag-sequence-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-sequence-nq", index_name="exact", use_dummy_dataset=True)
model = RagSequenceForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

def GenerationAction(request):
    if request.method == 'POST':
        query = request.POST.get('t1', False)
        inputs = tokenizer(query, return_tensors="pt")
        input_ids = inputs["input_ids"]
        question_hidden_states = model.question_encoder(input_ids)[0]
        docs_dict = retriever(input_ids.numpy(), question_hidden_states.detach().numpy(), return_tensors="pt")
        doc_scores = torch.bmm(question_hidden_states.unsqueeze(1), docs_dict["retrieved_doc_embeds"].float().transpose(1, 2)).squeeze(1)
        generated = model.generate(context_input_ids=docs_dict["context_input_ids"], context_attention_mask=docs_dict["context_attention_mask"], doc_scores=doc_scores)
        generated_string = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
        context= {'data': "Input Text = "+query+"<br/><br/>Generated Text = "+str(generated_string)}
        return render(request, 'Generation.html', context) 

def Generation(request):
    if request.method == 'GET':
       return render(request, 'Generation.html', {})

def Retrieval(request):
    if request.method == 'GET':
       return render(request, 'Retrieval.html', {})

def DownloadFile(request):
    if request.method == 'GET':
        name = request.GET.get('name', False)
        with open('RagApp/static/files/'+name, "rb") as file:
            data = file.read()
        file.close()
        response = HttpResponse(data,content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+name
        return response         

def RetrievalAction(request):
    if request.method == 'POST':
        query = request.POST.get('t1', False)
        query = query.strip().lower()
        documents = []
        names = []
        search = []
        rag = []
        for root, dirs, directory in os.walk('RagApp/static/files'):
            for j in range(len(directory)):
                with open(root+"/"+directory[j], "rb") as file:
                    data = file.read()
                file.close()
                print(data.decode())
                names.append(directory[j])
                data = data.decode()
                if len(data) > 2500:
                    data = data[0:2500]
                data = data.strip('\n').strip().lower()    
                inputs = tokenizer(data, return_tensors="pt")
                input_ids = inputs["input_ids"]
                question_hidden_states = model.question_encoder(input_ids)[0]
                question_hidden_states = question_hidden_states.detach().numpy().ravel()
                rag.append(question_hidden_states)
        rag = np.asarray(rag)
        inputs = tokenizer(query, return_tensors="pt")
        input_ids = inputs["input_ids"]
        query = model.question_encoder(input_ids)[0]
        query = query.detach().numpy().ravel()
        for i in range(len(rag)):
            predict_score = dot(rag[i], query)/(norm(rag[i])*norm(query))
            if predict_score > 0.50:
                search.append([names[i], predict_score])
        search.sort(key = lambda x : x[1], reverse=True)
        result = "<table border=1 align=center><tr><th>Searched File Name</th><th>Retrieval Accuracy</th><th>Download File</th></tr>"
        for i in range(0, len(search)):
            out = search[i]
            result += "<tr><td><font size=3 color=black>"+out[0]+"</font></td><td><font size=3 color=black>"+str(out[1])+"</font></td>"
            result += '<td><a href=\'DownloadFile?name='+out[0]+'\'><font size=3 color=black>Download File</font></a></td></tr>'            
        result += "</table><br/><br/><br/><br/>"
        context= {'data': result}
        return render(request, 'UserScreen.html', context)                

def UploadDocumentAction(request):
    if request.method == 'POST':
        global uname
        myfile = request.FILES['t1'].read()
        fname = request.FILES['t1'].name
        if os.path.exists("RagApp/static/files/"+fname):
            os.remove("RagApp/static/files/"+fname)
        with open("RagApp/static/files/"+fname, "wb") as file:
            file.write(myfile)
        file.close()
        status = "Error in loading document"
        current_date = str(date.today())
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'rag',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO documents VALUES('"+uname+"','"+fname+"','"+current_date+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        s3 = boto3.client(
    's3',
    region_name='ap-south-1'
)
        s3 = session.resource('s3')
        bucket = s3.Bucket('ragcloud')
        bucket.upload_file("RagApp/static/files/"+fname, fname)
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            status = "Document successfully uploaded"
        context= {'data': '<font size="3" color="blue">'+status+'</font>'}
        return render(request, 'UploadDocument.html', context)        

def UploadDocument(request):
    if request.method == 'GET':
       return render(request, 'UploadDocument.html', {})  

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})    

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def Aboutus(request):
    if request.method == 'GET':
       return render(request, 'Aboutus.html', {})    

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})   

def Contactus(request):
    if request.method == 'GET':
        name = "Ameerpet"
        output = '<iframe width="625" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q='+name+'&amp;ie=UTF8&amp;&amp;output=embed"></iframe><br/>'
        context= {'data1':output}
        return render(request, 'Contactus.html', context)

def RegisterAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        status = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'rag',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    status = "Username already exists"
                    break
        if status == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'rag',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = "Signup process completed"
        context= {'data': '<font size="3" color="blue">'+status+'</font>'}
        return render(request, 'Register.html', context)

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'rag',charset='utf8')
        with con:    
            cur = con.cursor()
            cur.execute("select username, password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1]:
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)  


    
        
