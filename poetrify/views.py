# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, render_to_response
from poetrify import models
import json
from math import *
# Create your views here.

def Home(request):
    return render_to_response('Home.html')

def Requests(request):
    print("")
    requestRows = models.Approval.objects.all()
    l = len(requestRows)
    wordsDict = {}
    for requestRow in requestRows:
        tempDict = {}
        tempDict['rhymes']=requestRow.rhymes
        tempDict['words']=requestRow.wordsList
        rId = requestRow.id
        wordsDict[rId] = tempDict
    data = {'wordsDict': wordsDict }
    print("-----------------------gr", data)
    return render_to_response('Requests.html', data)

def SeeAll(request):
    wordsRows = models.RhymeWords.objects.order_by('word').all()
    wordsDict = {}
    for row in wordsRows:
        a = row.alphabet
        w = row.word
        if a not in wordsDict:
            wordsDict[a] = [w]
        else:
            wordsDict[a].append(w)
    print(wordsDict)
    data = {'wordsDict': wordsDict}
    return render_to_response("SeeAll.html", data)

def GetRequest(request):
    rId = request.GET["requestId"]
    requestRow = models.Approval.objects.filter(id=rId).first()
    wList = requestRow.wordsList
    rhyme = requestRow.rhymes
    data = {'rhyme': rhyme, 'words': wList}
    return HttpResponse(json.dumps(data))

def RequestApproval(request):
    try:
        rId = request.GET["requestId"]
        add = request.GET["add"]
        print(add, type(add))
        requestRow = models.Approval.objects.filter(id=rId).first()
        rhyme = requestRow.rhymes
        words = requestRow.wordsList
        if add=='1':
            if rhyme==1:
                st = AddAsRhymeWords(words)
            else:
                st = AddAsNewWords(words)
        else:
            st = True
        if(st==True):
            requestRow.delete()
            return HttpResponse(1)
        else:
            return HttpResponse(0)
    except:
        return HttpResponse(0)

def GetNoOfRequests(request):
    noOfRequests = GetNumberOfRequests()
    return HttpResponse(json.dumps(noOfRequests))

def RhymesRequest(request):
    # w = request.word
    w = request.GET["word"]
    print("-----------------------rr", w)
    if CheckWord(w)==True:
        print("-----------------------word found")
        return HttpResponse(json.dumps(GetRhymes(w)))
    else:
        print("-----------------------word not found")
        AddRequest(w, 0)
    return HttpResponse('')

def AddNewRhymes(request):
    try:
        print("-----------------------anr")
        words = request.GET["words"]
        st = AddRequest(words, 1)
        print("-----------------------", st)
        if(st):
            return HttpResponse(1)
        return HttpResponse(0)
    except:
        return HttpResponse(0)

def AddNewWords(request):
    try:
        print("-----------------------anw")
        words = request.GET["words"]
        st = AddRequest(words, 0)
        if(st):
            return HttpResponse(1)
        return HttpResponse(0)
    except:
        return HttpResponse(0)

def AddRequest(words, rhymes):
    try:
        # words = words.replace(" ", "")
        st = models.Approval.objects.filter(wordsList=words).first()
        if(st!=None):
            return True
        wordsList = words.split(",")
        wordsStr = ''
        for w in wordsList:
            word = w.strip()
            if(word!=''):
                wordsStr += word+','
        print("-----------------------ar", wordsStr, rhymes)
        approvalRow = models.Approval()
        # totApprovals = GetNumberOfRequests()
        idApproval = GetIdForApprovals()
        approvalRow.id = idApproval
        approvalRow.wordsList = wordsStr[:-1]
        approvalRow.rhymes = rhymes
        approvalRow.save()
        return True
    except:
        return False

def GetIdForApprovals():
    totApprovals = GetNumberOfRequests()-1
    st = models.Approval.objects.filter(id__gt=totApprovals).first()
    if(st==None):
        print("-----------------------gifa", totApprovals+1)
        return totApprovals+1
    else:
        for i in range(totApprovals):
            print("-----------------------", i)
            st = models.Approval.objects.filter(id=i).first()
            if(st==None):
                print("-----------------------gifa", i)
                return i

def AddAsRhymeWords(words):
    print("-----------------------anr")
    try:
        totWords = GetTotalWords()
        # words = request.GET["words"]
        wList = words.split(",")
        finalList = GetFinalList(wList)
        rhymeId = GetRhymeId(finalList)
        newWordsList = GetNewWords(finalList)
        # gotRhymeId = 1
        if rhymeId == -1:
            # gotRhymeId = 0
            rhymeId = GetNoOfRhymeGroups()
        rhymeWordsIds = ''
        i = 0
        for w in newWordsList:
            word = str(w)
            print("-----------------------loop", word, "saved")
            rowWords = models.RhymeWords()
            print("*****")
            rId = totWords + i
            print("*****")
            rowWords.id = rId
            print("*****")
            rhymeWordsIds += str(rId) + ","
            print("*****")
            rowWords.alphabet = word[0]
            print("*****")
            rowWords.word = word
            print("*****")
            rowWords.rhymingGroup = rhymeId
            print("*****")
            rowWords.save()
            print("*****")
            i += 1
        if len(newWordsList)!=0:
            rhymeGroupRow = models.RhymeGroups.objects.filter(id=rhymeId).first()
            if rhymeGroupRow==None:
                rowGroup = models.RhymeGroups()
                totGroups = GetNoOfRhymeGroups()
                rowGroup.id = totGroups
                rowGroup.words = rhymeWordsIds[:-1]
                rowGroup.save()
            else:
                rhymeGroupRow.words += ','+rhymeWordsIds[:-1]
                rhymeGroupRow.save()
        return True
    except:
        return False

def GetFinalList(wList):
    finalList = []
    for word in wList:
        w = word.strip()
        if w!='' and w not in finalList:
            finalList.append(w)
    print("-----------------------gfl", finalList)
    return finalList

def GetNewWords(finalList):
    newWordsList = []
    for word in finalList:
        if not CheckWord(word):
            newWordsList.append(word)
    print ("-----------------------gnw", newWordsList)
    return newWordsList

def GetRhymeId(finalList): #rhymeId of first word in db #needs change
    try:
        for word in finalList:
            st = models.RhymeWords.objects.filter(word=word).first()
            if st!=None:
                print("-----------------------gri", st.rhymingGroup)
                return int(st.rhymingGroup)
        print("-----------------------gri -1")
        return -1
    except:
        print("-----------------------gri -1")
        return -1

def AddAsNewWords(words):
    try:
        print("----------------------anw")
        # words = request.GET["words"]
        wList = words.split(",")
        finalList = GetFinalList(wList)
        newWordsList = GetNewWords(finalList)
        print("----------------------", wList)
        i = 0
        totGroups = GetNoOfRhymeGroups()
        totWords = GetTotalWords()
        print("totWords = ", totWords, "totGroups = ", totGroups)
        for word in newWordsList:
            rowWords = models.RhymeWords()
            rowWords.id = totWords + i
            rowWords.alphabet = str(word)[0]
            rowWords.word = word
            rowWords.rhymingGroup = totGroups + i
            rowWords.save()
            rowGroup = models.RhymeGroups()
            rowGroup.id = totGroups + i
            rowGroup.words = totWords + i
            rowGroup.save()
            i+=1
        return True
    except:
        return False

def CheckWord(w):
    print("-----------------------cw")
    st = models.RhymeWords.objects.filter(word=w).first()
    if st==None:
        return False
    else:
        return True

def GetRhymes(w):
    print("-----------------------gr")
    rhymingId = models.RhymeWords.objects.filter(word=w).first().rhymingGroup
    print("-----------------------rhyming id = ", rhymingId)
    idList = models.RhymeWords.objects.filter(rhymingGroup=rhymingId).all() #includes w
    rhymeList=[]
    for i in idList:
        rhymeList.append(i.word)
    print("-----------------------words are: ", rhymeList)
    return rhymeList

def GetTotalWords():
    tot = models.RhymeWords.objects.all().count()
    print("-----------------------gtw", tot)
    return tot

def GetNumberOfRhymeWords(w):
    rhymeId = models.RhymeWords.objects.filter(word=w).first().rhymingGroup
    noOfRhymes = models.RhymeWords.objects.filter(rhymingGroup=rhymeId).all().count()
    print("-----------------------gnorw", noOfRhymes)
    return noOfRhymes

def GetRhymeGroup(w):
    rhymeId = models.RhymeWords.objects.filter(word=w).first().rhymingGroup
    print("-----------------------grw", rhymeId)
    return rhymeId

def GetNoOfRhymeGroups():
    # totalGroups = models.RhymeWords.objects.aggregate(Max('rhymingGroup')).first().rhymingGroup
    totalGroups = models.RhymeGroups.objects.all().count()
    print("-----------------------gnorg", totalGroups)
    return totalGroups

def GetNumberOfRequests():
    totalRequests = models.Approval.objects.all().count()
    print("-----------------------gnor", totalRequests)
    return totalRequests

def Trial(request):
    return render_to_response("Trial.html")