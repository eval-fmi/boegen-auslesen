import sys
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import numpy as np
from numpy import linalg as LA
import subprocess 
from tkinter import Label, Button, Canvas, StringVar, Tk, X, RIGHT, LEFT
import Levenshtein

from .evalFuns import oberer_punkt, unterer_punkt, linker_punkt, rechter_punkt
from .evalFuns import findRedTop, findRedBottom, findRedLeft, findRedRight
from .evalFuns import shakeDown, shakeLeft, shakeRight, shakeUp, shakeUp
from .evalFuns import shakeDownRGB, shakeLeftRGB, shakeRightRGB, shakeUpRGB, shakeUpRGB
from .evalFuns import searchBlack, searchRGBBlack
from .evalFuns import unterer_punkt, linker_punkt, rechter_punkt, oberer_punkt
from .evalFuns import findRedBottom, findRedLeft, findRedRight, findRedTop
from .evalFuns import item, paintItem


# wurde in boegen_vorbereiten übernommen
# def phase1(Questionnaire,leftborder=0,rightborder=0,topborder=0,bottomborder=0):
#     Fragebogen = Image.open(Questionnaire)
    
#     a,b = Fragebogen.size

#     Fragebogen = Fragebogen.convert('1', dither=Image.NONE)
#     FragebogenGefiltert=Fragebogen.filter(ImageFilter.MedianFilter(5))         
#     FB = FragebogenGefiltert.load()

#     sum = 0
#     stepx=5
#     stepy=10

#     for i in range(0,a,stepx):
#         for j in range (0,b,stepy):
#             sum += FB[i,j]

#     if sum*stepx*stepy/(a*b)>252:
#         sum=0
#         for i in range(0,a):
#             for j in range (0,b):
#                 sum += FB[i,j]
#         if sum/(a*b)>254:
#             return ["empty"]

#     Top=shakeRight(FB,a,b,shakeDown(FB,a,b,oberer_punkt(FB,a,b,topborder)))
#     Bottom=shakeRight(FB,a,b,shakeUp(FB,a,b,unterer_punkt(FB,a,b,bottomborder)))
#     Left=shakeDown(FB,a,b,shakeRight(FB,a,b,linker_punkt(FB,a,b,leftborder)))
#     Right=shakeDown(FB,a,b,shakeLeft(FB,a,b,rechter_punkt(FB,a,b,rightborder)))

#     TopA=np.array(Top)
#     BottomA=np.array(Bottom)
#     LeftA=np.array(Left)
#     RightA=np.array(Right)
    
#     TB=BottomA-TopA
#     TL=LeftA-TopA
#     TR=RightA-TopA
    
#     LB=BottomA-LeftA
#     LR=RightA-LeftA
#     LT=TopA-LeftA
    
#     BT=TopA-BottomA
#     BL=LeftA-BottomA
#     BR=RightA-BottomA
    
#     RB=BottomA-RightA
#     RL=LeftA-RightA
#     RT=TopA-RightA
    
#     cosTLB = np.dot(LT,LB)/LA.norm(LT)/LA.norm(LB)
#     cosRTL = np.dot(TL,TR)/LA.norm(TL)/LA.norm(TR)
#     cosBRT = np.dot(RB,RT)/LA.norm(RB)/LA.norm(RT)
#     cosLBR = np.dot(BL,BR)/LA.norm(BL)/LA.norm(BR)
#     cosRL_BT = np.dot(BT,RL)/LA.norm(BT)/LA.norm(RL)
    
#     winkelTLB = np.arccos(cosTLB)*360 / 2 / np.pi 
#     winkelRTL = np.arccos(cosRTL)*360 / 2 / np.pi 
#     winkelBRT = np.arccos(cosBRT)*360 / 2 / np.pi
#     winkelLBR = np.arccos(cosLBR)*360 / 2 / np.pi
#     winkelRL_BT = np.arccos(cosRL_BT)*360 / 2 / np.pi

#     if(abs(winkelRL_BT-90)>1): # gefundene Mittelstriche bilden kein Orthogonales Kreuz
#         if(abs(winkelTLB-69.5)<1): # Nehmen an Top, Left und Bottom richtig
#             RightA = LeftA+LT+LB
#             Right = RightA.tolist()
#         elif(abs(winkelBRT-69.5)<1): # Nehmen an Top, Right und Bottom richtig
#             LeftA = RightA+RT+RB
#             Left = LeftA.tolist()
#         elif(abs(winkelRTL-110.5)<1): # Nehmen an Right, Top, Left richtig
#             BottomA = TopA+TR+TL
#             Bottom = BottomA.tolist()
#         elif(abs(winkelLBR-110.5)<1): # Nehmen an Left, Bottom, Right richtig
#             TopA = BottomA+BR+BL
#             Top = TopA.tolist()
#         else: 
#             return ["help",Questionnaire]
    
#     if (Top[1]<0 or Bottom[1]>=b or Left[0]<0 or Right[0]>=a):
#         return ["help",Questionnaire]
    
#     LR=RightA-LeftA

#     e1=np.array((1,0))

#     cosalpha = np.dot(LR,e1)/LA.norm(LR)/LA.norm(e1)
#     alpha=np.arccos(cosalpha)*360 / 2 / np.pi

#     Fragebogen = Fragebogen.convert('RGBA')
#     FB = Fragebogen.load()
#     FB[Top[0]-1,Top[1]]=(255,0,0,255)
#     FB[Top[0],Top[1]]=(255,0,0,255)
#     FB[Top[0]-1,Top[1]+1]=(255,0,0,255)
#     FB[Top[0],Top[1]+1]=(255,0,0,255)
#     FB[Bottom[0]-1,Bottom[1]]=(255,0,0,255)
#     FB[Bottom[0],Bottom[1]]=(255,0,0,255)
#     FB[Bottom[0]-1,Bottom[1]-1]=(255,0,0,255)
#     FB[Bottom[0],Bottom[1]-1]=(255,0,0,255)
#     FB[Left[0],Left[1]-1]=(255,0,0,255)
#     FB[Left[0],Left[1]]=(255,0,0,255)
#     FB[Left[0]+1,Left[1]-1]=(255,0,0,255)
#     FB[Left[0]+1,Left[1]]=(255,0,0,255)
#     FB[Right[0],Right[1]-1]=(255,0,0,255)
#     FB[Right[0],Right[1]]=(255,0,0,255)
#     FB[Right[0]-1,Right[1]-1]=(255,0,0,255)
#     FB[Right[0]-1,Right[1]]=(255,0,0,255)

#     rot=Fragebogen.rotate(alpha if Right[1]>Left[1] else -alpha, expand=1) 
#     fff=Image.new('RGBA',rot.size,(255,)*4)
#     Fragebogen=Image.composite(rot,fff,rot)
    
#     a,b=Fragebogen.size
#     FB=Fragebogen.load()

#     Top = shakeRightRGB(FB,a,b,shakeDownRGB(FB,a,b,findRedTop(FB,a,b)))
#     Bottom = shakeRightRGB(FB,a,b,shakeUpRGB(FB,a,b,findRedBottom(FB,a,b)))
#     Left = shakeDownRGB(FB,a,b,shakeRightRGB(FB,a,b,findRedLeft(FB,a,b)))
#     Right = shakeDownRGB(FB,a,b,shakeLeftRGB(FB,a,b,findRedRight(FB,a,b)))

#     TopLeft = (Left[0]+(Top[0]-Bottom[0])//2,Top[1]+(Left[1]-Right[1])//2)
#     TopRight = (Right[0]+(Top[0]-Bottom[0])//2,Top[1]-(Left[1]-Right[1])//2)
#     BottomLeft = (Left[0]-(Top[0]-Bottom[0])//2,Bottom[1]+(Left[1]-Right[1])//2)
#     BottomRight = (Right[0]-(Top[0]-Bottom[0])//2,Bottom[1]-(Left[1]-Right[1])//2)

#     if Top[0]<Bottom[0]: # linksneigung
#         TopLeft = shakeLeftRGB(FB,a,b,shakeUpRGB(FB,a,b,searchRGBBlack(FB,a,b,TopLeft,40)))
#         TopRight = shakeUpRGB(FB,a,b,shakeRightRGB(FB,a,b,searchRGBBlack(FB,a,b,TopRight,40)))
#         BottomLeft = shakeDownRGB(FB,a,b,shakeLeftRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomLeft,40)))
#         BottomRight = shakeRightRGB(FB,a,b,shakeDownRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomRight,40)))
#     else: # rechtsneigung
#         TopLeft = shakeUpRGB(FB,a,b,shakeLeftRGB(FB,a,b,searchRGBBlack(FB,a,b,TopLeft,40)))
#         TopRight = shakeRightRGB(FB,a,b,shakeUpRGB(FB,a,b,searchRGBBlack(FB,a,b,TopRight,40)))
#         BottomLeft = shakeLeftRGB(FB,a,b,shakeDownRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomLeft,40)))
#         BottomRight = shakeDownRGB(FB,a,b,shakeRightRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomRight,40)))

#     if 0<=TopLeft[0]<a and 0<=TopLeft[1]<b:
#         lenTL = shakeDownRGB(FB,a,b,TopLeft)[1]-TopLeft[1]
#     else: 
#         lenTL = 0

#     if 0<=TopRight[0]<a and 0<=TopRight[1]<b:
#         lenTR = shakeDownRGB(FB,a,b,TopRight)[1]-TopRight[1] 
#     else:
#         lenTR=0

#     if 0<=BottomLeft[0]<a and 0<=BottomLeft[1]<b:  
#         lenBL = BottomLeft[1]-shakeUpRGB(FB,a,b,BottomLeft)[1]
#     else:
#         lenBL = 0

#     if 0<=BottomRight[0]<a and 0<=BottomRight[1]<b:
#         lenBR = BottomRight[1]-shakeUpRGB(FB,a,b,BottomRight)[1]
#     else:
#         lenBR = 0

#     corners = {lenTL : TopLeft, lenTR : TopRight, lenBL : BottomLeft, lenBR : BottomRight}
#     m=max(lenTL,lenTR,lenBL,lenBR)
#     M=set([lenTL,lenTR,lenBL,lenBR])

#     M.remove(m)
#     FoundMax=True
    
#     if(len(M)==0):
#         FoundMax=False
#     else:
#         for i in M:
#             if i*1.5>=m:
#                 FoundMax=False

#     if not FoundMax:
#         return ["help",Questionnaire]
    
#     RightLowerCorner = corners[max(lenTL,lenTR,lenBL,lenBR)]

#     if(RightLowerCorner==TopLeft):
#         Fragebogen=Fragebogen.rotate(180, expand=1)
#         Top=(a-1-Top[0],b-1-Top[1])
#         Bottom=(a-1-Bottom[0],b-1-Bottom[1])
#         Left=(a-1-Left[0],b-1-Left[1])
#         Right=(a-1-Right[0],b-1-Right[1])
#         Top, Bottom, Left, Right = Bottom, Top, Right, Left
#     elif (RightLowerCorner==TopRight):
#         Fragebogen=Fragebogen.rotate(270, expand=1)
#         Top=(b-1-Top[1],Top[0])
#         Bottom=(b-1-Bottom[1],Bottom[0])
#         Left=(b-1-Left[1],Left[0])
#         Right=(b-1-Right[1],Right[0])
#         Top, Bottom, Left, Right = Left, Right, Bottom, Top
#         a,b = b,a
#     elif (RightLowerCorner==BottomLeft):
#         Fragebogen=Fragebogen.rotate(90, expand=1)
#         Top=(Top[1],a-1-Top[0])
#         Bottom=(Bottom[1],a-1-Bottom[0])
#         Left=(Left[1],a-1-Left[0])
#         Right=(Right[1],a-1-Right[0])
#         Top, Bottom, Left, Right = Right, Left, Top, Bottom
#         a,b = b,a

#     FB = Fragebogen.load()

#     height=.01*(Bottom[1]-Top[1])
#     width=.01*(Right[0]-Left[0])

#     origin = np.array((Left[0],Top[1]))
    
#     box = (Left[0],int(Top[1]+(Left[1]-Top[1])/2.7),Top[0],int(Left[1]-(Left[1]-Top[1])/1.7))
#     if(box[0]>=box[2] or box[1]>=box[3]):
#         return ["help",Questionnaire]
#     Fragebogen.crop(box).save(Questionnaire + ".crop", "PNG",optimize=True)
#     # Texterkennung tesseract wird auf Datei.crop angewendet mit Sprache Deutsch und Ergebnis an stdout geschickt
#     s_deu=subprocess.Popen(['tesseract '+Questionnaire+".crop"+' stdout -l deu'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].decode("utf-8") 
#     s_eng=subprocess.Popen(['tesseract '+Questionnaire+".crop"+' stdout -l eng'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].decode("utf-8") 

#     Fragebogen.save(Questionnaire + ".processed", "PNG",optimize=True)

#     questions = []
#     typ = ""

#     for word in s_deu.split():
#         if Levenshtein.distance(word,'Vorlesungen') < 5:
#             typ = "Vorlesung1"
#             break
#         elif not Levenshtein.distance(word,'Fragebogen')<5 and (Levenshtein.distance(word,'Wurde')<3 or Levenshtein.distance(word,'Übungstermin')<5 or Levenshtein.distance(word,'angeboten?')<5):
#             typ = "Vorlesung2"
#             break
#         elif Levenshtein.distance(word,'Seminare')<5 or Levenshtein.distance(word,'Praktika')<5:
#             typ = "Seminar"
#             break

#     for word in s_eng.split():
#         if Levenshtein.distance(word,'lectures')<5:
#             typ = "Vorlesung1"
#             break
#         elif not Levenshtein.distance(word,'questionnaire')<5 and (Levenshtein.distance(word,'exercise')<5 or Levenshtein.distance(word,'meetings')<3 or Levenshtein.distance(word,'belonging')<5):
#             typ = "Vorlesung2"
#             break
#         elif Levenshtein.distance(word,'seminars')<5 or Levenshtein.distance(word,'practical')<5:
#             typ = "Seminar"
#             break

#     if typ=="":
#         return ["help",Questionnaire]

#     return [typ,Questionnaire+".processed",origin,width,height]

def phase1M(Questionnaire,anzahl): # laesst den Benutzer manuell den Fragebogen drehen und Ecken markieren
    gedreht = False
    Fragebogen = Image.open(Questionnaire)
    Fragebogen = Fragebogen.convert('1', dither=Image.NONE)
    while(not gedreht):
        if(Fragebogen.size[0]<Fragebogen.size[1]):
            b=600
            a=b*Fragebogen.size[0]//Fragebogen.size[1]
        else:
            a=800
            b=a*Fragebogen.size[1]//Fragebogen.size[0]

        window = Tk()
        image = Fragebogen.resize((a,b), Image.ANTIALIAS)

        message = "Drehe bitte manuell den Fragebogen in die korrekte Position (noch "+str(anzahl)+")."

        Label
        label = Label(window,text=message)
        label.pack()

        canvas = Canvas(window, width=image.size[0], height=image.size[1])
        canvas.pack()

        image_tk = ImageTk.PhotoImage(image)
        canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)

        def turn90():
            nonlocal Fragebogen
            Fragebogen=Fragebogen.rotate(90, expand=1)
            window.destroy()
        def turn180():
            nonlocal Fragebogen
            Fragebogen=Fragebogen.rotate(180, expand=1)
            window.destroy()
        def turn270():
            nonlocal Fragebogen
            Fragebogen=Fragebogen.rotate(270, expand=1)
            window.destroy()
        def fertig():
            nonlocal gedreht
            gedreht = True
            window.destroy()
        
        buttonDone = Button(window,text="Fertig",command=fertig).pack(side=RIGHT)
        button90 = Button(window,text="Drehe 90 Grad",command=turn90).pack(side=LEFT)
        button180 = Button(window,text="Drehe 180 Grad",command=turn180).pack(side=LEFT)
        button270 = Button(window,text="Drehe 270 Grad",command=turn270).pack(side=LEFT)
        
        window.mainloop()
    
    possible = True
    window = Tk()
    image = Fragebogen.resize((a,b), Image.ANTIALIAS)

    message = "Bitte klicke moeglichst praezise auf 3 sichtbare Markierungen, die ueber Eck liegen (Ecke + 2 Mittelmarkierungen)."
    
    label = Label(window,text=message)
    label.pack(fill=X)

    canvas = Canvas(window, width=image.size[0], height=image.size[1])
    canvas.pack()

    clicks = {"counter" : 0, 0: (0,0), 1: (0,0), 2:(0,0)}

    def imp():
        nonlocal possible
        possible = False
        clicks = {"counter" : 0, 0: (0,0), 1: (0,0), 2:(0,0)}
        window.destroy()

    buttonImp = Button(window,text="Unmoeglich",command=imp)
    buttonImp.pack(side=RIGHT)


    v0 = StringVar()
    v1 = StringVar()
    v2 = StringVar()
    v0.set(str(clicks[0]))
    v1.set(str(clicks[1]))
    v2.set(str(clicks[2]))

    label1 = Label(window,text="Punkt 1: ")
    label2 = Label(window,text="Punkt 2: ")
    label3 = Label(window,text="Punkt 3: ")
    labelP1 = Label(window,textvariable=v0)
    labelP2 = Label(window,textvariable=v1)
    labelP3 = Label(window,textvariable=v2)
    label1.pack(side=LEFT)
    labelP1.pack(side=LEFT)
    label2.pack(side=LEFT)
    labelP2.pack(side=LEFT)
    label3.pack(side=LEFT)
    labelP3.pack(side=LEFT)

    buttonDone = Button(window,text="Fertig",command=window.destroy)

    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)

    wi = Fragebogen.size[0]
    he = Fragebogen.size[1]

    wi2 = image.size[0]
    he2 = image.size[1]

    def callback(event):
        x = event.x
        y = event.y

        if clicks["counter"]%3==0:
            clicks[0] = (int(x*wi/wi2), int(y*wi/wi2))
            clicks["counter"] += 1
            v0.set(str(clicks[0]))

        elif clicks["counter"]%3==1:
            clicks[1] = (int(x*wi/wi2), int(y*wi/wi2))
            clicks["counter"] += 1
            v1.set(str(clicks[1]))

        elif clicks["counter"]%3==2:
            clicks[2] = (int(x*wi/wi2), int(y*wi/wi2))
            clicks["counter"] += 1
            v2.set(str(clicks[2]))
            buttonDone.pack(side=RIGHT)

    canvas.bind("<Button-1>", callback)

    window.mainloop()

    if not possible:
        return []

    a = clicks[0]
    b = clicks[1]
    c = clicks[2]

    a_ar = np.array(a)
    b_ar = np.array(b)
    c_ar = np.array(c)

    u = a_ar-b_ar
    v = a_ar-c_ar
    w = b_ar-c_ar

    cosalpha = np.dot(u,v)/LA.norm(u)/LA.norm(v)
    cosbeta  = np.dot(u,w)/LA.norm(u)/LA.norm(w)
    cosgamma = np.dot(v,w)/LA.norm(v)/LA.norm(w)

    m = min(abs(cosalpha),abs(cosbeta),abs(cosgamma))


    if abs(cosalpha)==m: # rechter Winkel zwischen u und v => a ist Ecke
        ecke = a
        if LA.norm(u) > LA.norm(v): # |a-b|>|a-c|
            horiMitte = b
            vertiMitte = c
        else:
            horiMitte = c
            vertiMitte = b
    if abs(cosbeta)==m:# rechter Winkel zwischen u und w => b ist Ecke
        ecke = b
        if LA.norm(u) > LA.norm(w): # |a-b|>|b-c|
            horiMitte = a
            vertiMitte = c
        else:
            horiMitte = c
            vertiMitte = a
    if abs(cosgamma)==m: # rechter Winkel zwischen v und w => c ist Ecke
        ecke = c
        if LA.norm(v) > LA.norm(w): # |a-c|>|b-c|
            horiMitte = a
            vertiMitte = b
        else:
            horiMitte = b
            vertiMitte = a

    FB=Fragebogen.load()



    if ecke[0] < wi/2: # linke Ecke
        if ecke[1] < he/2: # obere Ecke
            TopLeft = shakeUp(FB,wi,he,searchBlack(FB,wi,he,ecke,40))
            tl1 = shakeLeft(FB,wi,he,TopLeft)
            tl2 = shakeDown(FB,wi,he,tl1)
            ar1 = np.array(TopLeft)
            ar2 = np.array(tl1)
            ar3 = np.array(tl2)
            if (LA.norm(ar1-ar2) < 2*LA.norm(ar2-ar3)): # linksrotiert
                TopLeft = tl1
            Left = shakeRight(FB,wi,he,searchBlack(FB,wi,he,vertiMitte,40))
            Top = shakeDown(FB,wi,he,searchBlack(FB,wi,he,horiMitte,40))
            Fragebogen = Fragebogen.convert('RGBA')
            FB = Fragebogen.load()
            FB[Top[0]-1,Top[1]]=(255,0,0,255)
            FB[Top[0],Top[1]]=(255,0,0,255)
            FB[Top[0]-1,Top[1]+1]=(255,0,0,255)
            FB[Top[0],Top[1]+1]=(255,0,0,255)
            FB[TopLeft[0]-1,TopLeft[1]]=(255,0,0,255)
            FB[TopLeft[0],TopLeft[1]]=(255,0,0,255)
            FB[TopLeft[0]-1,TopLeft[1]-1]=(255,0,0,255)
            FB[TopLeft[0],TopLeft[1]-1]=(255,0,0,255)
            FB[Left[0],Left[1]-1]=(255,0,0,255)
            FB[Left[0],Left[1]]=(255,0,0,255)
            FB[Left[0]+1,Left[1]-1]=(255,0,0,255)
            FB[Left[0]+1,Left[1]]=(255,0,0,255)

            TopA=np.array(Top)
            TopLeftA=np.array(TopLeft)
            LeftA=np.array(Left)

            u=TopA-TopLeftA
            e1=np.array((1,0))

            cosalpha = np.dot(u,e1)/LA.norm(u)/LA.norm(e1)
            alpha=np.arccos(cosalpha)*360 / 2 / np.pi

            rot=Fragebogen.rotate(alpha if Top[1]>TopLeft[1] else -alpha, expand=1) 
            fff=Image.new('RGBA',rot.size,(255,)*4)
            Fragebogen=Image.composite(rot,fff,rot)

            FB = Fragebogen.load()
            Top = findRedTop(FB,Fragebogen.size[0],Fragebogen.size[1])
            Left = findRedLeft(FB,Fragebogen.size[0],Fragebogen.size[1])
            Bottom = (Top[0],2*Left[1]-Top[1])
            Bottom = shakeUpRGB(FB,wi,he,searchRGBBlack(FB,wi,he,Bottom,40))
            Right = (2*Top[0]-Left[0],Left[1])
            Right = shakeLeftRGB(FB,wi,he,searchRGBBlack(FB,wi,he,Right,40))


        else:   # untere Ecke
            BottomLeft = shakeDown(FB,wi,he,searchBlack(FB,wi,he,ecke,40))
            bl1 = shakeLeft(FB,wi,he,BottomLeft)
            bl2 = shakeUp(FB,wi,he,bl1)
            ar1 = np.array(BottomLeft)
            ar2 = np.array(bl1)
            ar3 = np.array(bl2)
            if (LA.norm(ar1-ar2) < 2*LA.norm(ar2-ar3)): # linksrotiert
                BottomLeft = bl1
            Left = shakeRight(FB,wi,he,searchBlack(FB,wi,he,vertiMitte,40))
            Bottom = shakeUp(FB,wi,he,searchBlack(FB,wi,he,horiMitte,40))
            Fragebogen = Fragebogen.convert('RGBA')
            FB = Fragebogen.load()
            FB[Bottom[0]-1,Bottom[1]]=(255,0,0,255)
            FB[Bottom[0],Bottom[1]]=(255,0,0,255)
            FB[Bottom[0]-1,Bottom[1]+1]=(255,0,0,255)
            FB[Bottom[0],Bottom[1]+1]=(255,0,0,255)
            FB[BottomLeft[0]-1,BottomLeft[1]]=(255,0,0,255)
            FB[BottomLeft[0],BottomLeft[1]]=(255,0,0,255)
            FB[BottomLeft[0]-1,BottomLeft[1]-1]=(255,0,0,255)
            FB[BottomLeft[0],BottomLeft[1]-1]=(255,0,0,255)
            FB[Left[0],Left[1]-1]=(255,0,0,255)
            FB[Left[0],Left[1]]=(255,0,0,255)
            FB[Left[0]+1,Left[1]-1]=(255,0,0,255)
            FB[Left[0]+1,Left[1]]=(255,0,0,255)

            BottomA=np.array(Bottom)
            BottomLeftA=np.array(BottomLeft)
            LeftA=np.array(Left)

            u=BottomA-BottomLeftA
            e1=np.array((1,0))

            cosalpha = np.dot(u,e1)/LA.norm(u)/LA.norm(e1)
            alpha=np.arccos(cosalpha)*360 / 2 / np.pi

            rot=Fragebogen.rotate(alpha if Bottom[1]>BottomLeft[1] else -alpha, expand=1) 
            fff=Image.new('RGBA',rot.size,(255,)*4)
            Fragebogen=Image.composite(rot,fff,rot)

            FB = Fragebogen.load()
            Bottom = findRedBottom(FB,Fragebogen.size[0],Fragebogen.size[1])
            Left = findRedLeft(FB,Fragebogen.size[0],Fragebogen.size[1])
            Top = (Bottom[0],2*Left[1]-Bottom[1])
            Top = shakeDownRGB(FB,wi,he,searchRGBBlack(FB,wi,he,Top,40))
            Right = (2*Top[0]-Left[0],Left[1])
            Right = shakeLeftRGB(FB,wi,he,searchRGBBlack(FB,wi,he,Right,40))

    else: # rechte Ecke
        if ecke[1] < he/2: #obere Ecke
            TopRight = shakeUp(FB,wi,he,searchBlack(FB,wi,he,ecke,40))
            tr1 = shakeRight(FB,wi,he,TopRight)
            tr2 = shakeDown(FB,wi,he,tr1)
            ar1 = np.array(TopRight)
            ar2 = np.array(tr1)
            ar3 = np.array(tr2)
            if (LA.norm(ar1-ar2) < 2*LA.norm(ar2-ar3)): # linksrotiert
                TopRight = tr1
            Right = shakeLeft(FB,wi,he,searchBlack(FB,wi,he,vertiMitte,40))
            Top = shakeDown(FB,wi,he,searchBlack(FB,wi,he,horiMitte,40))
            Fragebogen = Fragebogen.convert('RGBA')
            FB = Fragebogen.load()
            FB[Top[0]-1,Top[1]]=(255,0,0,255)
            FB[Top[0],Top[1]]=(255,0,0,255)
            FB[Top[0]-1,Top[1]+1]=(255,0,0,255)
            FB[Top[0],Top[1]+1]=(255,0,0,255)
            FB[TopRight[0]-1,TopRight[1]]=(255,0,0,255)
            FB[TopRight[0],TopRight[1]]=(255,0,0,255)
            FB[TopRight[0]-1,TopRight[1]-1]=(255,0,0,255)
            FB[TopRight[0],TopRight[1]-1]=(255,0,0,255)
            FB[Right[0],Right[1]-1]=(255,0,0,255)
            FB[Right[0],Right[1]]=(255,0,0,255)
            FB[Right[0]+1,Right[1]-1]=(255,0,0,255)
            FB[Right[0]+1,Right[1]]=(255,0,0,255)

            TopA=np.array(Top)
            TopRightA=np.array(TopRight)
            RightA=np.array(Right)

            u=TopRightA-TopA
            e1=np.array((1,0))

            cosalpha = np.dot(u,e1)/LA.norm(u)/LA.norm(e1)
            alpha=np.arccos(cosalpha)*360 / 2 / np.pi

            rot=Fragebogen.rotate(alpha if TopRight[1]>Top[1] else -alpha, expand=1) 
            fff=Image.new('RGBA',rot.size,(255,)*4)
            Fragebogen=Image.composite(rot,fff,rot)

            FB = Fragebogen.load()
            Top = findRedTop(FB,Fragebogen.size[0],Fragebogen.size[1])
            Right = findRedRight(FB,Fragebogen.size[0],Fragebogen.size[1])
            Left = (2*Top[0]-Right[0],Right[1])
            Left = shakeRightRGB(FB,wi,he,searchRGBBlack(FB,wi,he,Left,40))            
            Bottom = (Top[0],2*Left[1]-Top[1])
            Bottom = shakeUpRGB(FB,wi,he,searchRGBBlack(FB,wi,he,Bottom,40))

        else: # untere Ecke
            BottomRight = shakeDown(FB,wi,he,searchBlack(FB,wi,he,ecke,40))
            br1 = shakeRight(FB,wi,he,BottomRight)
            br2 = shakeUp(FB,wi,he,br1)
            ar1 = np.array(BottomRight)
            ar2 = np.array(br1)
            ar3 = np.array(br2)
            if (LA.norm(ar1-ar2) < 2*LA.norm(ar2-ar3)): # linksrotiert
                BottomRight = br1
            Right = shakeLeft(FB,wi,he,searchBlack(FB,wi,he,vertiMitte,40))
            Bottom = shakeUp(FB,wi,he,searchBlack(FB,wi,he,horiMitte,40))
            Fragebogen = Fragebogen.convert('RGBA')
            FB = Fragebogen.load()
            FB[Bottom[0]-1,Bottom[1]]=(255,0,0,255)
            FB[Bottom[0],Bottom[1]]=(255,0,0,255)
            FB[Bottom[0]-1,Bottom[1]+1]=(255,0,0,255)
            FB[Bottom[0],Bottom[1]+1]=(255,0,0,255)
            FB[BottomRight[0]-1,BottomRight[1]]=(255,0,0,255)
            FB[BottomRight[0],BottomRight[1]]=(255,0,0,255)
            FB[BottomRight[0]-1,BottomRight[1]-1]=(255,0,0,255)
            FB[BottomRight[0],BottomRight[1]-1]=(255,0,0,255)
            FB[Right[0],Right[1]-1]=(255,0,0,255)
            FB[Right[0],Right[1]]=(255,0,0,255)
            FB[Right[0]+1,Right[1]-1]=(255,0,0,255)
            FB[Right[0]+1,Right[1]]=(255,0,0,255)

            BottomA=np.array(Bottom)
            BottomRightA=np.array(BottomRight)
            RightA=np.array(Right)

            u=BottomRightA-BottomA
            e1=np.array((1,0))

            cosalpha = np.dot(u,e1)/LA.norm(u)/LA.norm(e1)
            alpha=np.arccos(cosalpha)*360 / 2 / np.pi

            rot=Fragebogen.rotate(alpha if BottomRight[1]>Bottom[1] else -alpha, expand=1) 
            fff=Image.new('RGBA',rot.size,(255,)*4)
            Fragebogen=Image.composite(rot,fff,rot)

            FB = Fragebogen.load()
            Bottom = findRedBottom(FB,Fragebogen.size[0],Fragebogen.size[1])
            Right = findRedRight(FB,Fragebogen.size[0],Fragebogen.size[1])
            Top = (Bottom[0],2*Right[1]-Bottom[1])
            Top = shakeDownRGB(FB,wi,he,searchRGBBlack(FB,wi,he,Top,40))
            Left = (2*Top[0]-Right[0],Right[1])
            Left = shakeRightRGB(FB,wi,he,searchRGBBlack(FB,wi,he,Left,40)) 


    Fragebogen.convert("1", dither=Image.NONE).save(Questionnaire+".processed","PNG",optimize=True)

    height=.01*(Bottom[1]-Top[1])
    width=.01*(Right[0]-Left[0])

    origin = np.array((Left[0],Top[1]))
    box = (Left[0],int(Top[1]+(Left[1]-Top[1])/2.7),Top[0],int(Left[1]-(Left[1]-Top[1])/1.7))
    Fragebogen.crop(box).save(Questionnaire+".crop", "PNG",optimize=True)
    s=subprocess.Popen(['tesseract '+Questionnaire+".crop"+' stdout -l deu'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].decode("utf-8") 


    questions = []
    typ = ""

    for word in s.split():
        if Levenshtein.distance(word,'Vorlesungen')<5:
            typ = "Vorlesung1"
            break
        elif not Levenshtein.distance(word,'Fragebogen')<5 and (Levenshtein.distance(word,'Wurde')<3 or Levenshtein.distance(word,'Übungstermin')<5 or Levenshtein.distance(word,'angeboten?')<5):
            typ = "Vorlesung2"
            break
        elif Levenshtein.distance(word,'Seminare')<5 or Levenshtein.distance(word,'Praktika')<5:
            typ = "Seminar"
            break

    if typ=="":
        return ["unknown",Questionnaire+".processed",origin,width,height]

    return [typ,Questionnaire+".processed",origin,width,height]

    

def phase2(typ,Questionnaire,origin,width,height):
    Fragebogen = Image.open(Questionnaire)
    Fragebogen = Fragebogen.convert('RGBA')
    FB = Fragebogen.load()

    if typ == "Vorlesung1":
        questions = list(range(1,39))
    if typ == "Vorlesung2":
        questions = list(range(39,63))
    if typ == "Seminar":
        questions = list(range(1,17))+list(range(117,121))

    questions=list(questions)

    if 28 in questions: # Tafel
        if not 1 in item(FB,28,origin,width,height)[0]:
            questions.remove(29)
            questions.remove(30)
            questions.remove(31)
            questions.remove(32)

    if 33 in questions: # Beamer
        if not 1 in item(FB,33,origin,width,height)[0]:
            questions.remove(34)
            questions.remove(35)
            questions.remove(36)
            questions.remove(37)
            questions.remove(38)

    if 39 in questions: # Skript
        if not 1 in item(FB,39,origin,width,height)[0]:
            questions.remove(40)
            questions.remove(41)
            questions.remove(42)
            questions.remove(43)

    if 44 in questions: # Uebungstermin angeboten
        if not 1 in item(FB,44,origin,width,height)[0]:
            questions.remove(45)
            questions.remove(46)
            questions.remove(47)
            questions.remove(48)
            questions.remove(49)
            questions.remove(50)
            questions.remove(51)
            questions.remove(52)
            questions.remove(53)
            questions.remove(54)

    if 46 in questions: # Uebungstermin angeboten
        if 3 in item(FB,46,origin,width,height)[0]:
            questions.remove(47)
            questions.remove(48)
            questions.remove(49)
            questions.remove(50)
            questions.remove(51)
            questions.remove(52)
            questions.remove(53)
            questions.remove(54)

    if 55 in questions: # Uebungstermin angeboten
        if not 1 in item(FB,55,origin,width,height)[0]:
            questions.remove(56)
            questions.remove(57)
            questions.remove(58)
            questions.remove(59)
            questions.remove(60)
            questions.remove(61)
            questions.remove(62)

    if 56 in questions: # Uebungstermin angeboten
        if 3 in item(FB,56,origin,width,height)[0]:
            questions.remove(57)
            questions.remove(58)
            questions.remove(59)
            questions.remove(60)
            questions.remove(61)
            questions.remove(62)

    res = []
    NoCrossCounter = 0
    for i in questions:
        s=str(i)
        itemerg = item(FB,i,origin,width,height)
        d = itemerg[0]
        if(itemerg[1]): # Falls kein Kreuz gesetz wurde
            NoCrossCounter+=1
        for key in d:
            paintItem(FB,d[key],origin,width,height)
            s=s+","+str(key)
        res=res+[s]


    Fragebogen.save(Questionnaire, "PNG",optimize=True)

    return res
    #file.close()
    #Fragebogen.show()
    #return ""


def phase2M(Questionnaire,anzahl):

    Fragebogen = Image.open(Questionnaire[0])
    Fragebogen = Fragebogen.convert('1', dither=Image.NONE)

    if(Fragebogen.size[0]<Fragebogen.size[1]):
        b=600
        a=b*Fragebogen.size[0]//Fragebogen.size[1]
    else:
        a=800
        b=a*Fragebogen.size[1]//Fragebogen.size[0]

    window = Tk()
    image = Fragebogen.resize((a,b), Image.ANTIALIAS)

    message = "Bitte hilf bei der Erkennung des Fragebogentyps (noch "+str(anzahl)+")."

    label = Label(window,text=message)
    label.pack(fill=X)

    canvas = Canvas(window, width=image.size[0], height=image.size[1])
    canvas.pack()

    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)

    typ = ""

    def VL1():
        nonlocal typ
        typ="Vorlesung1"
        window.destroy()
    def VL2():
        nonlocal typ
        typ="Vorlesung2"
        window.destroy()
    def Sem():
        nonlocal typ
        typ="Seminar"
        window.destroy()
    def fertig():
        window.destroy()


    button1 = Button(window,text="Vorlesung front ",command=VL1).pack(side=LEFT)
    button2 = Button(window,text="Vorlesung rueck ",command=VL2).pack(side=LEFT)
    button3 = Button(window,text="Seminar",command=Sem).pack(side=LEFT)
    buttonDone = Button(window,text="Unmoeglich",command=window.destroy)

    window.mainloop()

    if typ == "":
        return []

    return [typ,Questionnaire[0],Questionnaire[1],Questionnaire[2],Questionnaire[3]]
