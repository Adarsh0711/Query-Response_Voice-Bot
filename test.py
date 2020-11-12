from tkinter import *
import tkinter as tk
import wolframalpha
import wikipedia
import requests
import webbrowser
import speech_recognition as sr
from gtts import gTTS 
from playsound import playsound
import os
appId = 'E49Q54-Y8A9UHJ8LT'
client = wolframalpha.Client(appId)
root = Tk()
root.title('question page')
root.geometry("300x150")
pri = Text(root, height=3)
reswin = Tk()
reswin.title('answer page')
robo = Text(reswin)
def search_wiki(keyword=''):
  searchResults = wikipedia.search(keyword)
  if not searchResults:
    print("No result from Wikipedia")
    robo_print("No result from Wikipedia",robo)
  try:
    page = wikipedia.page(searchResults[0])
  except (wikipedia.DisambiguationError, err):
    page = wikipedia.page(err.options[0])
  wikiTitle = str(page.title.encode('utf-8'))
  wikiSummary = str(page.summary.encode('utf-8'))
  print(wikiSummary)
  robo_print(wikiSummary,robo)
def search(text=''):
  res = client.query(text)
  if res['@success'] == 'false':
     search_wiki(text)
  else:
    result = ''
    pod0 = res['pod'][0]
    pod1 = res['pod'][1]
    if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
      result = resolveListOrDict(pod1['subpod'])
      print(result)
      robo_print(result,robo)
      textspeech = gTTS(text = result, lang='en')
      textspeech.save('test.mp3')
      playsound('test.mp3')
      os.remove('test.mp3')
      question = resolveListOrDict(pod0['subpod'])
      question = removeBrackets(question)
      primaryImage(question)
    else:
      question = resolveListOrDict(pod0['subpod'])
      question = removeBrackets(question)
      search_wiki(question)
      primaryImage(question)
def removeBrackets(variable):
  return variable.split('(')[0]
def resolveListOrDict(variable):
  if isinstance(variable, list):
    return variable[0]['plaintext']
  else:
    return variable['plaintext']
def primaryImage(title=''):
    url = 'http://en.wikipedia.org/w/api.php'
    data = {'action':'query', 'prop':'pageimages','format':'json','piprop':'original','titles':title}
    try:
        res = requests.get(url, params=data)
        key = res.json()['query']['pages'].keys()[0]
        imageUrl = res.json()['query']['pages'][key]['original']['source']
        print(imageUrl)
        webbrowser.open(imageUrl)
    except (Exception, err):
        print('')
def main_function():
  flag = 0
  r = sr.Recognizer()
  
  with sr.Microphone() as source:
    print('say now')
    audio = r.listen(source)
  try:
    q=r.recognize_google(audio)
    flag=0
  except:
    robo_print('didnt understand, plese repeat your sentence',robo)
    human('sorry didnt understand',0)
    flag = 1
  if flag == 0:
    print(r.recognize_google(audio))
    human(r.recognize_google(audio),1)
    word = 'Anitha'
    qu = 'exit'
    if word in q.lower():
      matter='she is my AI teacher'
      textspeech = gTTS(text = matter, lang='en')
      robo_print(matter,robo)
      playsound('testos.mp3')
    if qu in q.lower():
      exit()
    else:
      search(q)
def wiki_print(reply):
  robo.delete('1.0',END)
  robo.insert(END,reply)
  robo.pack(side = LEFT, fill = X)
def robo_print(reply,robo):
      robo.delete('1.0',END)
      robo.insert(END,"Robo: \n"+reply)
      robo.pack(side = LEFT, fill = X)
def human(question,i):
  global pri
  pri.delete('1.0',END)
  pri.pack(side = RIGHT, fill = X)
  if i == 1:
    pri.insert(END,"User: "+question)
  else:
    pri.insert(END,"Sorry didnt understand your statement")
voice = Button(root, text="speak", width=40, bg="red", command = main_function)
voice.pack()
reswin.mainloop()
root.mainloop()
