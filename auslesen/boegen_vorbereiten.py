""" in diesem Paket lassen sich alle Funktionen finden, die zur Vorbereitung
    der Eval-Bögen auf die Auswertung benötigt werdenself. """

import subprocess 

import numpy as np
from np import linalg as LA
from PIL import Image, ImageDraw, ImageFilter, ImageTk

def minimum_edit_distance(s1, s2):
    """ berechnet die Levenshteindistanz zwischen den beiden Strings s1 und s2 """
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distanzen = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        neue_distanzen = [index2+1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                neue_distanzen.append(distanzen[index1])
            else:
                neue_distanzen.append(1 + min((distanzen[index1],
                                             distanzen[index1+1],
                                             neue_distanzen[-1])))
        distanzen = neue_distanzen
    return distanzen[-1]

def ist_schwarz(x):
    """
    x stellt den Farbwert eines Pixels in einem PixelAccess-Object dar.
    Dabei ist 0 = Schwarz
    """
    return x < 15

# Suchen der Koordinaten der Mittelstriche
def oberer_punkt(FB,a,b,border=0):
    """gibt den obersten (kleinster y-Wert) schwarzen Punkt zurück"""
    for j in range(int(border*b/100),b):
        for i in range (3*a//8, 5*a//8):
            if ist_schwarz(FB[i,j]):
                return (i,j)

def unterer_punkt(FB,a,b,border=0):
    for j in range(b-1-int(border*b/100),0,-1):
        for i in range (3*a//8,5*a//8):
            if ist_schwarz(FB[i,j]):
                return (i,j)

def linker_punkt(FB,a,b,border=0):
    for i in range(int(border*a/100),a):
        for j in range (3*b//8,5*b//8):
            if ist_schwarz(FB[i,j]):
                return (i,j)

def rechter_punkt(FB,a,b,border=0):
    for i in range(a-1-int(border*a/100),0,-1):
        for j in range (3*b//8,5*b//8):
            if ist_schwarz(FB[i,j]):
                return (i,j)

                

#def wackeln(richtung, FB, a, b, point):
#    stop = False
#    while not stop and point[0] in range(0,a):
#        p
def shakeRight(FB,a,b,point):
    """
        sucht in einem Strich(Mittelpunkt), welcher durch den Pixel *point*
        *point* gegeben ist, den Pixel, der sich am weitesten rechts befindet
    """
    stop = False
    while(not stop and 0<=point[0]<a-1):
        if  0<=point[1]<b and ist_schwarz(FB[point[0]+1,point[1]]):
            point=(point[0]+1,point[1])
        elif 0<=point[1]<b-1 and ist_schwarz(FB[point[0]+1,point[1]+1]):
            point=(point[0]+1,point[1]+1)
        elif 0<point[1]<b and ist_schwarz(FB[point[0]+1,point[1]-1]):
            point=(point[0]+1,point[1]-1)
        elif point[0]<a-2 and 0<=point[1]<b and ist_schwarz(FB[point[0]+2,point[1]]):
            point=(point[0]+2,point[1])
        elif point[0]<a-2 and 0<=point[1]<b-1 and ist_schwarz(FB[point[0]+2,point[1]+1]):
            point=(point[0]+2,point[1]+1)
        elif point[0]<a-2 and 0<point[1]<b and ist_schwarz(FB[point[0]+2,point[1]-1]):
            point=(point[0]+2,point[1]-1)
        else:
            stop = True
    return (point)

def shakeLeft(FB,a,b,point):
    """siehe shakeRight"""
    stop = False
    while(not stop and point[0]>0):
        if   0<point[1]<b-1 and ist_schwarz(FB[point[0]-1,point[1]]):
            point=(point[0]-1,point[1])
        elif 0<point[1]<b-1 and ist_schwarz(FB[point[0]-1,point[1]+1]):
            point=(point[0]-1,point[1]+1)
        elif 0<point[1]<b-1 and ist_schwarz(FB[point[0]-1,point[1]-1]):
            point=(point[0]-1,point[1]-1)
        elif point[0]>1 and 0<point[1]<b-1 and ist_schwarz(FB[point[0]-2,point[1]]):
            point=(point[0]-2,point[1])
        elif point[0]>1 and 0<point[1]<b-1 and ist_schwarz(FB[point[0]-2,point[1]+1]):
            point=(point[0]-2,point[1]+1)
        elif point[0]>1 and 0<point[1]<b-1 and ist_schwarz(FB[point[0]-2,point[1]-1]):
            point=(point[0]-2,point[1]-1)
        else:
            stop = True
    return (point)

def shakeDown(FB,a,b,point):
    """ siehe shakeRight"""
    stop = False
    while(not stop and point[1]<b-1):
        if   0<point[0]<a-1 and ist_schwarz(FB[point[0],point[1]+1]):
            point=(point[0],point[1]+1)
        elif 0<point[0]<a-1 and ist_schwarz(FB[point[0]+1,point[1]+1]):
            point=(point[0]+1,point[1]+1)
        elif 0<point[0]<a-1 and ist_schwarz(FB[point[0]-1,point[1]+1]):
            point=(point[0]-1,point[1]+1)
        elif point[1]<b-2 and 0<point[0]<a-1 and ist_schwarz(FB[point[0],point[1]+2]):
            point=(point[0],point[1]+2)
        elif point[1]<b-2 and 0<point[0]<a-1 and ist_schwarz(FB[point[0]+1,point[1]+2]):
            point=(point[0]+1,point[1]+2)
        elif point[1]<b-2 and 0<point[0]<a-1 and ist_schwarz(FB[point[0]-1,point[1]+2]):
            point=(point[0]-1,point[1]+2)
        else:
            stop = True
    return (point)

def shakeUp(FB,a,b,point):
    """ siehe shakeRight"""
    stop = False
    while(not stop and point[1]>0):
        if   0<point[0]<a-1 and ist_schwarz(FB[point[0],point[1]-1]):
            point=(point[0],point[1]-1)
        elif 0<point[0]<a-1 and ist_schwarz(FB[point[0]+1,point[1]-1]):
            point=(point[0]+1,point[1]-1)
        elif 0<point[0]<a-1 and  ist_schwarz(FB[point[0]-1,point[1]-1]):
            point=(point[0]-1,point[1]-1)
        elif point[1]>1 and 0<point[0]<a-1 and ist_schwarz(FB[point[0],point[1]-2]):
            point=(point[0],point[1]-2)
        elif point[1]>1 and 0<point[0]<a-1 and ist_schwarz(FB[point[0]+1,point[1]-2]):
            point=(point[0]+1,point[1]-2)
        elif point[1]>1 and 0<point[0]<a-1 and  ist_schwarz(FB[point[0]-1,point[1]-2]):
            point=(point[0]-1,point[1]-2)
        else:
            stop = True
    return (point)

### Ab hier begintt die Arbeit mit dem RGB-Teil des Skriptes
def isRed(x):
    return x[0]>240 and x[1]<15 and x[2] < 15

def isRGBBlack(x):
    return x[0]<15 and x[1]<15 and x[2]<15

def findRedTop(FB,a,b):
    for j in range(0,b):
        for i in range (3*a//8,5*a//8):
            if isRed(FB[i,j]):
                return (i,j)

def findRedBottom(FB,a,b):
    for j in range(b-1,0,-1):
        for i in range (3*a//8,5*a//8):
            if isRed(FB[i,j]):
                return (i,j)

def findRedLeft(FB,a,b):
    for i in range(0,a):
        for j in range (3*b//8,5*b//8):
            if isRed(FB[i,j]):
                return (i,j)

def findRedRight(FB,a,b):
    for i in range(a-1,0,-1):
        for j in range (3*b//8,5*b//8):
            if isRed(FB[i,j]):
                return (i,j)

def shakeRightRGB(FB,a,b,point):
    stop = False
    while(not stop and 0<=point[0]<a-1):
        if 0<=point[1]<b and isRGBBlack(FB[point[0]+1,point[1]]):
            point=(point[0]+1,point[1])
        elif 0<=point[1]<b-1 and isRGBBlack(FB[point[0]+1,point[1]+1]):
            point=(point[0]+1,point[1]+1)
        elif 0<point[1]<b and isRGBBlack(FB[point[0]+1,point[1]-1]):
            point=(point[0]+1,point[1]-1)
        elif point[0]<a-2 and 0<=point[1]<b and isRGBBlack(FB[point[0]+2,point[1]]):
            point=(point[0]+2,point[1])
        elif point[0]<a-2 and 0<=point[1]<b-1 and isRGBBlack(FB[point[0]+2,point[1]+1]):
            point=(point[0]+2,point[1]+1)
        elif point[0]<a-2 and 0<point[1]<b and isRGBBlack(FB[point[0]+2,point[1]-1]):
            point=(point[0]+2,point[1]-1)
        else:
            stop = True
    return (point)

def shakeLeftRGB(FB,a,b,point):
    stop = False
    while(not stop and point[0]>0):
        if 0<point[1]<b-1 and isRGBBlack(FB[point[0]-1,point[1]]):
            point=(point[0]-1,point[1])
        elif 0<point[1]<b-1 and isRGBBlack(FB[point[0]-1,point[1]+1]):
            point=(point[0]-1,point[1]+1)
        elif 0<point[1]<b-1 and isRGBBlack(FB[point[0]-1,point[1]-1]):
            point=(point[0]-1,point[1]-1)
        elif point[0]>1 and 0<point[1]<b-1 and isRGBBlack(FB[point[0]-2,point[1]]):
            point=(point[0]-2,point[1])
        elif point[0]>1 and 0<point[1]<b-1 and isRGBBlack(FB[point[0]-2,point[1]+1]):
            point=(point[0]-2,point[1]+1)
        elif point[0]>1 and 0<point[1]<b-1 and isRGBBlack(FB[point[0]-2,point[1]-1]):
            point=(point[0]-2,point[1]-1)
        else:
            stop = True
    return (point)

def shakeDownRGB(FB,a,b,point):
    stop = False
    while(not stop and point[1]<b-1):
        if 0<point[0]<a-1 and isRGBBlack(FB[point[0],point[1]+1]):
            point=(point[0],point[1]+1)
        elif 0<point[0]<a-1 and isRGBBlack(FB[point[0]+1,point[1]+1]):
            point=(point[0]+1,point[1]+1)
        elif 0<point[0]<a-1 and isRGBBlack(FB[point[0]-1,point[1]+1]):
            point=(point[0]-1,point[1]+1)
        elif point[1]<b-2 and 0<point[0]<a-1 and isRGBBlack(FB[point[0],point[1]+2]):
            point=(point[0],point[1]+2)
        elif point[1]<b-2 and 0<point[0]<a-1 and isRGBBlack(FB[point[0]+1,point[1]+2]):
            point=(point[0]+1,point[1]+2)
        elif point[1]<b-2 and 0<point[0]<a-1 and isRGBBlack(FB[point[0]-1,point[1]+2]):
            point=(point[0]-1,point[1]+2)
        else:
            stop = True
    return (point)

def shakeUpRGB(FB,a,b,point):
    stop = False
    while(not stop and point[1]>0):
        if 0<point[0]<a-1 and isRGBBlack(FB[point[0],point[1]-1]):
            point=(point[0],point[1]-1)
        elif 0<point[0]<a-1 and isRGBBlack(FB[point[0]+1,point[1]-1]):
            point=(point[0]+1,point[1]-1)
        elif 0<point[0]<a-1 and  isRGBBlack(FB[point[0]-1,point[1]-1]):
            point=(point[0]-1,point[1]-1)
        elif point[1]>1 and 0<point[0]<a-1 and isRGBBlack(FB[point[0],point[1]-2]):
            point=(point[0],point[1]-2)
        elif point[1]>1 and 0<point[0]<a-1 and isRGBBlack(FB[point[0]+1,point[1]-2]):
            point=(point[0]+1,point[1]-2)
        elif point[1]>1 and 0<point[0]<a-1 and  isRGBBlack(FB[point[0]-1,point[1]-2]):
            point=(point[0]-1,point[1]-2)
        else:
            stop = True
    return (point)

def searchBlack(FB,a,b,point,diam):
    r=diam//2
    for i in range(0,r+1):
        for l in range(point[0]-i,point[0]+i):
            if 0<=l<a and 0<=point[1]-i<b and ist_schwarz(FB[l,point[1]-i]):
                return (l,point[1]-i)
            if 0<=l<a and 0<=point[1]+i<b and ist_schwarz(FB[l,point[1]+i]):
                return (l,point[1]+i)
        for l in range(point[1]-i,point[1]+i):
            if 0<=l<b and 0<=point[0]-i<a and ist_schwarz(FB[point[0]-i,l]):
                return (point[0]-i,l)
            if 0<=l<b and 0<=point[0]+i<a and ist_schwarz(FB[point[0]+i,l]):
                return (point[0]+i,l)
    return point

def searchRGBBlack(FB,a,b,point,diam):
    r=diam//2
    for i in range(0,r+1):
        for l in range(point[0]-i,point[0]+i):
            if 0<=l<a and 0<=point[1]-i<b and isRGBBlack(FB[l,point[1]-i]):
                return (l,point[1]-i)
            if 0<=l<a and 0<=point[1]+i<b and isRGBBlack(FB[l,point[1]+i]):
                return (l,point[1]+i)
        for l in range(point[1]-i,point[1]+i):
            if 0<=l<b and 0<=point[0]-i<a and isRGBBlack(FB[point[0]-i,l]):
                return (point[0]-i,l)
            if 0<=l<b and 0<=point[0]+i<a and isRGBBlack(FB[point[0]+i,l]):
                return (point[0]+i,l)
    return point


def phase1(Questionnaire,leftborder=0,rightborder=0,topborder=0,bottomborder=0):
    Fragebogen = Image.open(Questionnaire)
    
    a,b = im.size

    # wandelt das Bild in ein 2-Farbenbild (Schwarz, Weiß) um,
    # so das nur noch diese beiden Farben im Bild vorkommen
    # Dabei gilt 0=schwarz und 255=weiß. Es gibt nur diese beiden Werte
    # (https://pillow.readthedocs.io/en/stable/reference/Image.html?highlight=Image.convert#PIL.Image.Image.convert)
    Fragebogen = Fragebogen.convert('1', dither=Image.NONE)

    # glättet die Zeichen in dem Bild und entfernt problematische Überreste
    # des Kopiervorgangs.
    # (https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html?highlight=ImageFilter#PIL.ImageFilter.MedianFilter)
    FragebogenGefiltert=Fragebogen.filter(ImageFilter.MedianFilter(5))         
    
    # wandelt das Bild in ein PixelAccess-Objekt um, mit dem dann
    # weitergearbeitet wird
    FB = FragebogenGefiltert.load()

    # stellt die Schrittweite ein, in der nach den Ecken gesucht wird
    sum = 0
    stepx = 5
    stepy = 10

    # gucken, ob der das Blatt leer ist und somit kein Fragebogen, sondern
    # die Rückseite eines Seminarbogens oder einfach mit reingerutscht ist

    # das Dokument wird durchgegangen und auf die Farbwerte überprüft 
    for i in range(0,a,stepx):
        for j in range (0,b,stepy):
            sum += FB[i,j]
            
    # es wird geguckt, ob die Anzahl an Weiß sehr hoch ist
    
    # unklar, ob es leer ist, deshalb wird nochmal genauer geguckt
    if sum*stepx*stepy/(a*b)>252:  
        sum=0
        for i in range(0,a):
            for j in range (0,b):
                sum += FB[i,j]
        if sum/(a*b)>254:
            return ["empty"]

# bis hierher wurde der Fragebogen für das drehen und wackeln vorbereitet
# und geguckt, ob der Fragebogen leer ist
# -----------------------------

# Hier werden die Mittelstriche überprüft und es wird geguckt, ob die hinhauen
    # scheint die inneren Punkte (mit orientierung nach rechts unten ) zu finden
    Top=shakeRight(FB,a,b,shakeDown(FB,a,b,oberer_punkt(FB,a,b,topborder)))
    Bottom=shakeRight(FB,a,b,shakeUp(FB,a,b,unterer_punkt(FB,a,b,bottomborder)))
    Left=shakeDown(FB,a,b,shakeRight(FB,a,b,linker_punkt(FB,a,b,leftborder)))
    Right=shakeDown(FB,a,b,shakeLeft(FB,a,b,rechter_punkt(FB,a,b,rightborder)))


# erstellt numpy.arrays, damit mit diesen besser gearbeitet werden kann
    TopA=np.array(Top)
    BottomA=np.array(Bottom)
    LeftA=np.array(Left)
    RightA=np.array(Right)

# berechnte die Differenznen zwischen den einzelnen Werten    
    TB=BottomA-TopA
    TL=LeftA-TopA
    TR=RightA-TopA
    
    LB=BottomA-LeftA
    LR=RightA-LeftA
    LT=TopA-LeftA
    
    BT=TopA-BottomA
    BL=LeftA-BottomA
    BR=RightA-BottomA
    
    RB=BottomA-RightA
    RL=LeftA-RightA
    RT=TopA-RightA
  # Berechnet den Cosinus, zwischen der oben ergebenen Längen  
    cosTLB = np.dot(LT,LB)/LA.norm(LT)/LA.norm(LB)
    cosRTL = np.dot(TL,TR)/LA.norm(TL)/LA.norm(TR)
    cosBRT = np.dot(RB,RT)/LA.norm(RB)/LA.norm(RT)
    cosLBR = np.dot(BL,BR)/LA.norm(BL)/LA.norm(BR)
    cosRL_BT = np.dot(BT,RL)/LA.norm(BT)/LA.norm(RL)
    # berechnet die Winkel zwischen den einzelnen Strecken
    winkelTLB = np.arccos(cosTLB)*360 / 2 / np.pi 
    winkelRTL = np.arccos(cosRTL)*360 / 2 / np.pi 
    winkelBRT = np.arccos(cosBRT)*360 / 2 / np.pi
    winkelLBR = np.arccos(cosLBR)*360 / 2 / np.pi
    winkelRL_BT = np.arccos(cosRL_BT)*360 / 2 / np.pi ## Kreuz in der Mitte

    if(abs(winkelRL_BT-90)>1): # gefundene Mittelstriche bilden kein Orthogonales Kreuz
        if(abs(winkelTLB-69.5)<1): # Nehmen an Top, Left und Bottom richtig
            RightA = LeftA+LT+LB
            Right = RightA.tolist()
        elif(abs(winkelBRT-69.5)<1): # Nehmen an Top, Right und Bottom richtig
            LeftA = RightA+RT+RB
            Left = LeftA.tolist()
        elif(abs(winkelRTL-110.5)<1): # Nehmen an Right, Top, Left richtig
            BottomA = TopA+TR+TL
            Bottom = BottomA.tolist()
        elif(abs(winkelLBR-110.5)<1): # Nehmen an Left, Bottom, Right richtig
            TopA = BottomA+BR+BL
            Top = TopA.tolist()
        else: 
            return ["help",Questionnaire]
    # Das sollte eig. nicht passieren. Dass einer der Mittelstrich-Punkte aus
    # dem Bild herausfällt
    if (Top[1]<0 or Bottom[1]>=b or Left[0]<0 or Right[0]>=a):
        return ["help",Questionnaire]
    
    # TODO: Welcher Winkel wird hier genau berechnet? Sollte der Winkel des
    #       verdrehten Kreuzes sein, welches auch bei winkelRL_BT betrachtet wird 
    LR=RightA-LeftA
    e1=np.array((1,0))
    cosalpha = np.dot(LR,e1)/LA.norm(LR)/LA.norm(e1)
    alpha=np.arccos(cosalpha)*360 / 2 / np.pi

    # erstellt rote Punkte in den Mittelstrichen, bei den vorher berechneten
    # berechneten Positionen 
    Fragebogen = Fragebogen.convert('RGBA')
    FB = Fragebogen.load()
    FB[Top[0]-1,Top[1]]=(255,0,0,255)
    FB[Top[0],Top[1]]=(255,0,0,255)
    FB[Top[0]-1,Top[1]+1]=(255,0,0,255)
    FB[Top[0],Top[1]+1]=(255,0,0,255)
    FB[Bottom[0]-1,Bottom[1]]=(255,0,0,255)
    FB[Bottom[0],Bottom[1]]=(255,0,0,255)
    FB[Bottom[0]-1,Bottom[1]-1]=(255,0,0,255)
    FB[Bottom[0],Bottom[1]-1]=(255,0,0,255)
    FB[Left[0],Left[1]-1]=(255,0,0,255)
    FB[Left[0],Left[1]]=(255,0,0,255)
    FB[Left[0]+1,Left[1]-1]=(255,0,0,255)
    FB[Left[0]+1,Left[1]]=(255,0,0,255)
    FB[Right[0],Right[1]-1]=(255,0,0,255)
    FB[Right[0],Right[1]]=(255,0,0,255)
    FB[Right[0]-1,Right[1]-1]=(255,0,0,255)
    FB[Right[0]-1,Right[1]]=(255,0,0,255)


    rotiert den Fragebogen
    rot=Fragebogen.rotate(alpha if Right[1]>Left[1] else -alpha, expand=1) 
    # vollständig Weißes Blatt, wird als als Maske verwendet
    fff=Image.new('RGBA',rot.size,(255,)*4)
    # erstellt aus dem gedrehten Bild un der weißen Maske ein fertiges Bild,
    # bei dem die vorher unklaren Stellen mit weißen Stellen ersetzt wurden
    Fragebogen=Image.composite(rot,fff,rot)
    
    ### Hiermit ist unser Bild fertig gedreht und sollte in der richtigen
    # Position sein, um jetzt damit weiterzuarbeiten
    # --------------------------
    a,b=Fragebogen.size
    FB=Fragebogen.load()

    # die vorher markierten roten Punkte bei den Mittelstrichen werden gesucht
    # und ausgehend von ihnen werden die inneren (nach rechts orientierten)
    # Pixel in den Mittelstrichen gesucht
    Top = shakeRightRGB(FB,a,b,shakeDownRGB(FB,a,b,findRedTop(FB,a,b)))
    Bottom = shakeRightRGB(FB,a,b,shakeUpRGB(FB,a,b,findRedBottom(FB,a,b)))
    Left = shakeDownRGB(FB,a,b,shakeRightRGB(FB,a,b,findRedLeft(FB,a,b)))
    Right = shakeDownRGB(FB,a,b,shakeLeftRGB(FB,a,b,findRedRight(FB,a,b)))

    # sucht, wo die Ecken des Blattes eig. sein sollten, ausgehend
    # von den Enden der Mittelstriche
    TopLeft = (Left[0]+(Top[0]-Bottom[0])//2,Top[1]+(Left[1]-Right[1])//2)
    TopRight = (Right[0]+(Top[0]-Bottom[0])//2,Top[1]-(Left[1]-Right[1])//2)
    BottomLeft = (Left[0]-(Top[0]-Bottom[0])//2,Bottom[1]+(Left[1]-Right[1])//2)
    BottomRight = (Right[0]-(Top[0]-Bottom[0])//2,Bottom[1]-(Left[1]-Right[1])//2)

    # Ausgehen von den erechneten Positionen der Ecken wird überprüft,
    # wo sich die Ecken befinden
    # ob das Blatt noch gedreht wird muss, bevor es ausgewertet werden kann
    if Top[0]<Bottom[0]: # linksneigung
        TopLeft = shakeLeftRGB(FB,a,b,shakeUpRGB(FB,a,b,searchRGBBlack(FB,a,b,TopLeft,40)))
        TopRight = shakeUpRGB(FB,a,b,shakeRightRGB(FB,a,b,searchRGBBlack(FB,a,b,TopRight,40)))
        BottomLeft = shakeDownRGB(FB,a,b,shakeLeftRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomLeft,40)))
        BottomRight = shakeRightRGB(FB,a,b,shakeDownRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomRight,40)))
    else: # rechtsneigung
        TopLeft = shakeUpRGB(FB,a,b,shakeLeftRGB(FB,a,b,searchRGBBlack(FB,a,b,TopLeft,40)))
        TopRight = shakeRightRGB(FB,a,b,shakeUpRGB(FB,a,b,searchRGBBlack(FB,a,b,TopRight,40)))
        BottomLeft = shakeLeftRGB(FB,a,b,shakeDownRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomLeft,40)))
        BottomRight = shakeDownRGB(FB,a,b,shakeRightRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomRight,40)))

    if 0<=TopLeft[0]<a and 0<=TopLeft[1]<b:
        lenTL = shakeDownRGB(FB,a,b,TopLeft)[1]-TopLeft[1]
    else: 
        lenTL = 0

    if 0<=TopRight[0]<a and 0<=TopRight[1]<b:
        lenTR = shakeDownRGB(FB,a,b,TopRight)[1]-TopRight[1] 
    else:
        lenTR=0

    if 0<=BottomLeft[0]<a and 0<=BottomLeft[1]<b:  
        lenBL = BottomLeft[1]-shakeUpRGB(FB,a,b,BottomLeft)[1]
    else:
        lenBL = 0

    if 0<=BottomRight[0]<a and 0<=BottomRight[1]<b:
        lenBR = BottomRight[1]-shakeUpRGB(FB,a,b,BottomRight)[1]
    else:
        lenBR = 0

    corners = {lenTL : TopLeft, lenTR : TopRight, lenBL : BottomLeft, lenBR : BottomRight}
    m=max(lenTL,lenTR,lenBL,lenBR)
    M=set([lenTL,lenTR,lenBL,lenBR])

    M.remove(m)
    FoundMax=True
    
    if(len(M)==0):
        FoundMax=False
    else:
        for i in M:
            if i*1.5>=m:
                FoundMax=False

    if not FoundMax:
        return ["help",Questionnaire]
    
    RightLowerCorner = corners[max(lenTL,lenTR,lenBL,lenBR)]

    if(RightLowerCorner==TopLeft):
        Fragebogen=Fragebogen.rotate(180, expand=1)
        Top=(a-1-Top[0],b-1-Top[1])
        Bottom=(a-1-Bottom[0],b-1-Bottom[1])
        Left=(a-1-Left[0],b-1-Left[1])
        Right=(a-1-Right[0],b-1-Right[1])
        Top, Bottom, Left, Right = Bottom, Top, Right, Left
    elif (RightLowerCorner==TopRight):
        Fragebogen=Fragebogen.rotate(270, expand=1)
        Top=(b-1-Top[1],Top[0])
        Bottom=(b-1-Bottom[1],Bottom[0])
        Left=(b-1-Left[1],Left[0])
        Right=(b-1-Right[1],Right[0])
        Top, Bottom, Left, Right = Left, Right, Bottom, Top
        a,b = b,a
    elif (RightLowerCorner==BottomLeft):
        Fragebogen=Fragebogen.rotate(90, expand=1)
        Top=(Top[1],a-1-Top[0])
        Bottom=(Bottom[1],a-1-Bottom[0])
        Left=(Left[1],a-1-Left[0])
        Right=(Right[1],a-1-Right[0])
        Top, Bottom, Left, Right = Right, Left, Top, Bottom
        a,b = b,a

    FB = Fragebogen.load()

    height=.01*(Bottom[1]-Top[1])
    width=.01*(Right[0]-Left[0])

    origin = np.array((Left[0],Top[1]))
    
    box = (Left[0],int(Top[1]+(Left[1]-Top[1])/2.7),Top[0],int(Left[1]-(Left[1]-Top[1])/1.7))
    if(box[0]>=box[2] or box[1]>=box[3]):
        return ["help",Questionnaire]
    Fragebogen.crop(box).save(Questionnaire + ".crop", "PNG",optimize=True)
    # Texterkennung tesseract wird auf Datei.crop angewendet mit Sprache Deutsch und Ergebnis an stdout geschickt
    s_deu=subprocess.Popen(['tesseract '+Questionnaire+".crop"+' stdout -l deu'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].decode("utf-8") 
    s_eng=subprocess.Popen(['tesseract '+Questionnaire+".crop"+' stdout -l eng'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].decode("utf-8") 

    Fragebogen.save(Questionnaire + ".processed", "PNG",optimize=True)

    questions = []
    typ = ""

    for word in s_deu.split():
        if minimum_edit_distance(word,'Vorlesungen') < 5:
            typ = "Vorlesung1"
            break
        elif not minimum_edit_distance(word,'Fragebogen')<5 and (minimum_edit_distance(word,'Wurde')<3 or minimum_edit_distance(word,'Übungstermin')<5 or minimum_edit_distance(word,'angeboten?')<5):
            typ = "Vorlesung2"
            break
        elif minimum_edit_distance(word,'Seminare')<5 or minimum_edit_distance(word,'Praktika')<5:
            typ = "Seminar"
            break

    for word in s_eng.split():
        if minimum_edit_distance(word,'lectures')<5:
            typ = "Vorlesung1"
            break
        elif not minimum_edit_distance(word,'questionnaire')<5 and (minimum_edit_distance(word,'exercise')<5 or minimum_edit_distance(word,'meetings')<3 or minimum_edit_distance(word,'belonging')<5):
            typ = "Vorlesung2"
            break
        elif minimum_edit_distance(word,'seminars')<5 or minimum_edit_distance(word,'practical')<5:
            typ = "Seminar"
            break

    if typ=="":
        return ["help",Questionnaire]

    return [typ,Questionnaire+".processed",origin,width,height]

