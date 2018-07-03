# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import numpy as np
import cv2
import requests

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')



TOKEN = 'NDYzNDYwMDA3MzcyMTI4MjY2.Dhwuhg.cnJJIiORZqd8ykFDwmqeCkoc86w'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('>hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(">repeat"):
        await client.send_message(message.channel, message.content[7:])
        
    if message.content.startswith(">detect"):
        cap = message.attachments
        print(cap)
        
        if len(cap) < 1:
            if message.content[8:].startswith('http'):
                url = message.content[8:]
                filename = url.split('/')[-1]
                r = requests.get(url, allow_redirects=True)
                open(filename, 'wb').write(r.content)

                cap = cv2.imread(filename)
                img = cap
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                print(faces)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = img[y:y+h, x:x+w]
        
                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    for (ex,ey,ew,eh) in eyes:
                        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,255),2)
                
                cv2.imwrite('img.jpg',img)
                if len(faces) <= 0:
                    msg = 'No Thots Detected'.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    msg = 'Thot(s) Detected'.format(message)
                    await client.send_message(message.channel, msg)
            
                await client.send_file(message.channel, "img.jpg")
                
               
            else:
                msg = 'That is not an image. Please try again.'.format(message)
                await client.send_message(message.channel, msg)
        else:
            url = cap[0]['url']
            filename = url.split('/')[-1]
            r = requests.get(url, allow_redirects=True)
            open(filename, 'wb').write(r.content)

            cap = cv2.imread(filename)
            img = cap
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            print(faces)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
        
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,255),2)
                
            cv2.imwrite('img.jpg',img)
            if len(faces) <= 0:
                msg = 'No Thots Detected'.format(message)
                await client.send_message(message.channel, msg)
            else:
                msg = str(len(faces)).format(message)
                await client.send_message(message.channel, msg)
                msg = 'Thot(s) Detected'.format(message)
                await client.send_message(message.channel, msg)
            
            await client.send_file(message.channel, "img.jpg")


    if message.content.startswith(">hey") and message.content.endswith("is a thot"):
        for user in message.mentions:
            msg = 'Destroyed thot {}'.format(user.mention)
            await client.send_message(message.channel, msg)


    if message.content.startswith(">john thicc"):
        msg = 'https://ifunny.co/fun/qUYtwnDq5'.format(message)
        await client.send_message(message.channel, msg)
        
    if message.content.startswith(">help"):
        msg = ''' Here is a list of my commands:

                >hello
                >repeat _text_
                >detect _image_
                >hey _name_ is a thot
                >john thicc
                >carsalesman (WIP)
                '''.format(message)
        await client.send_message(message.channel, msg)

        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='Use >help'))

client.run(TOKEN)
