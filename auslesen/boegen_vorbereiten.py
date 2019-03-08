""" in diesem Paket lassen sich alle Funktionen finden, die zur Vorbereitung
    der Eval-Bögen auf die Auswertung benötigt werdenself. """

import subprocess 

import numpy as np
from numpy import linalg as LA
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import auslesen.my_tesseract as tesseract

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
    """ gibt für einen RGB-Wert (Tripel) True zurück, wenn die Farbe rot ist"""
    return x[0]>240 and x[1]<15 and x[2] < 15

def isRGBBlack(x):
    """ gibt für einen RGB-Wert (Tripel) True zurück, wenn die Farbe schwarz ist"""
    return x[0]<15 and x[1]<15 and x[2]<15

def findRedTop(FB,a,b):
    """ findet bei der oberen Mittelmarkierung rote Punkte """
    for j in range(0,b):
        for i in range (3*a//8,5*a//8):
            if isRed(FB[i,j]):
                return (i,j)

def findRedBottom(FB,a,b):
    """ siehe findRedTop"""
    for j in range(b-1,0,-1):
        for i in range (3*a//8,5*a//8):
            if isRed(FB[i,j]):
                return (i,j)

def findRedLeft(FB,a,b):
    """ siehe findRedTop"""
    for i in range(0,a):
        for j in range (3*b//8,5*b//8):
            if isRed(FB[i,j]):
                return (i,j)

def findRedRight(FB,a,b):
    """ siehe findRedTop"""
    for i in range(a-1,0,-1):
        for j in range (3*b//8,5*b//8):
            if isRed(FB[i,j]):
                return (i,j)

def shakeRightRGB(FB,a,b,point):
    """
        findet den am weitesten rechtsliegenden schwarzen Punkt
        der sich in einer schwarzen Maße befindet??? Wenn dieser in 2er-Schritten
        vom Ursprungspunkt point erreichbar ist.
    """
    stop = False
    while not stop and point[0]in range (0,a):
        # rechts nebenliegender Punkt wird betrachtet, ob er noch schwarz ist
        if 0<=point[1]<b and isRGBBlack(FB[point[0]+1,point[1]]):
            point=(point[0]+1,point[1])
        # diagonal rechts oberer liegender Punkt wird betrachtet
        elif 0<=point[1]<b-1 and isRGBBlack(FB[point[0]+1,point[1]+1]):
            point=(point[0]+1,point[1]+1)
        # diagonal rechts unterer liegender Punkt wird betrachtet
        elif 0<point[1]<b and isRGBBlack(FB[point[0]+1,point[1]-1]):
            point=(point[0]+1,point[1]-1)
        
        # Das gleiche wie oben, nur das hier jetzt 2mal nach rechts gegangen wird
        elif point[0]<a-2 and 0<=point[1]<b and isRGBBlack(FB[point[0]+2,point[1]]):
            point=(point[0]+2,point[1])
        elif point[0]<a-2 and 0<=point[1]<b-1 and isRGBBlack(FB[point[0]+2,point[1]+1]):
            point=(point[0]+2,point[1]+1)
        elif point[0]<a-2 and 0<point[1]<b and isRGBBlack(FB[point[0]+2,point[1]-1]):
            point=(point[0]+2,point[1]-1)
        else:  # Es wurde kein Punkt in der näheren Umgebung gefunden
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
    """
        sucht im mit Durchmesser `diam` den nächsten schwarzen Punkt in der
        Umgebung, des Anfangspunktes `point`
    """
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


# diese Funktion wurde aus phase1 herausgenommen

### Hier kommen eigene Funktionen, die genutzt werden,
# um phase1 kleiner zu machen

def bild_ist_leer(FB, a, b):
    """
        überprüft, ob die Rückseite eines Fragebogens oder einfach ein lee
        leeres Blatt Papier eingelegt wurde. gibt entweder
        True oder False zurück
    """

    # stellt die Schrittweite ein, in der nach den Ecken gesucht wird
    sum = 0
    stepx = 5
    stepy = 10

    # gucken, ob der das Blatt leer ist und somit kein Fragebogen, sondern
    # die Rückseite eines Seminarbogens oder einfach mit reingerutscht ist

    # das Dokument wird durchgegangen und auf die Farbwerte überprüft 
    for i in range(0, a, stepx):
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
            return True

    return False

def bild_ist_vorbereitet(Fragebogen, leftborder=0, rightborder=0, topborder=0, bottomborder=0):
    """
        Das Bild wird für die spätere Bearbeitung vorbereitet.
        Dabei wird getestet, ob das Bild leer ist und ob ein orthogonales Kreuz
        vorliegt. Zudem, wird das Bild dann noch gedreht und
        die Mittelmarkierungen werden eingefärbt. wir erhalten ein
    """
    # glättet die Zeichen in dem Bild und entfernt problematische Überreste
    # des Kopiervorgangs.
    # (https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html?highlight=ImageFilter#PIL.ImageFilter.MedianFilter)
    a,b = Fragebogen.size
    FragebogenGefiltert=Fragebogen.filter(ImageFilter.MedianFilter(5))         
    
    # wandelt das Bild in ein PixelAccess-Objekt um, mit dem dann
    # weitergearbeitet wird
    FB = FragebogenGefiltert.load()
    
    if bild_ist_leer(FB, a, b):
        return ["empty"]

    ### überprüft, ob ein Kreuz vorliegt + Anfang des Drehens
    # Hier werden die Mittelstriche überprüft und es wird geguckt, ob die hinhauen
    # scheint die inneren Punkte (mit orientierung nach rechts unten ) der
    # Mittelstriche (nur der Mittelstriche) zu finden
    Top=shakeRight(FB,a,b,shakeDown(FB,a,b,oberer_punkt(FB,a,b,topborder)))
    Bottom=shakeRight(FB,a,b,shakeUp(FB,a,b,unterer_punkt(FB,a,b,bottomborder)))
    Left=shakeDown(FB,a,b,shakeRight(FB,a,b,linker_punkt(FB,a,b,leftborder)))
    Right=shakeDown(FB,a,b,shakeLeft(FB,a,b,rechter_punkt(FB,a,b,rightborder)))

    # erstellt numpy.arrays, damit mit diesen besser gearbeitet werden kann
    TopA=np.array(Top)
    BottomA=np.array(Bottom)
    LeftA=np.array(Left)
    RightA=np.array(Right)

    # berechnet die Differenzen zwischen den einzelnen Werten    
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
            return ["help"]
    
    # Das sollte eig. nicht passieren. Dass einer der Mittelstrich-Punkte aus
    # dem Bild herausfällt, aber wenn es kein Kreuz bildet, und die Punkte wie
    # oben berechnet werden, kann es trotzdem vorkommen
    if (Top[1]<0 or Bottom[1]>=b or Left[0]<0 or Right[0]>=a):
        return ["help"]
    
    ### Ab hier beginnt der Drehvorgang
    # erstellt rote Punkte in den Mittelstrichen, bei den vorher
    # berechneten Positionen des ungefilterten Fragebogens
    # Er war jedoch vorher schwarz-weiß und Graußstufen wurden entfernt
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

    # TODO: Welcher Winkel wird hier genau berechnet? Sollte der Winkel des
    #       verdrehten Kreuzes sein, welches auch bei winkelRL_BT betrachtet wird 
    LeftA=np.array(Left)
    RightA=np.array(Right)
    LR=RightA-LeftA
    e1=np.array((1,0))
    
    cosalpha = np.dot(LR,e1)/LA.norm(LR)/LA.norm(e1)
    alpha=np.arccos(cosalpha)*360 / 2 / np.pi

    # rotiert den Fragebogen
    rot=Fragebogen.rotate(alpha if Right[1]>Left[1] else -alpha, expand=1) 
    # vollständig Weißes Blatt, wird als als Maske verwendet
    fff = Image.new('RGBA',rot.size,(255,)*4)
    # erstellt aus dem gedrehten Bild un der weißen Maske ein fertiges Bild,
    # bei dem die vorher unklaren Stellen mit weißen Stellen ersetzt wurden
    Fragebogen = Image.composite(rot,fff,rot)

    return Fragebogen

def bogen_drehen(Fragebogen):
    """
        erhält einen Fragebogen von bild_ist_vorbereitet, indem die Mittelstriche
        mit roten Markierungen markiert wurden.
        Es werden jetzt die Ecken gesucht und über die Länge der unteren rechten
        Ecke herausgefunden, ob der Fragebogen richtig herum ist und 
        in die richtige Position gedreht. Am Ende wird ein richtig herum gedrehter
        Fragebogen und die Variablen Top, Bottom, Left, Right zurückgegeben.
    """

    a,b = Fragebogen.size
    FB = Fragebogen.load()

    # die vorher markierten roten Punkte bei den Mittelstrichen werden gesucht
    # und ausgehend von ihnen werden die innersten (nach rechts orientierten)
    # Pixel in den Mittelstrichen gesucht
    # Es muss erst in die innere Richtung (Top -> Down;Bottom -> Up,) gegangen
    # werden, damit ich auf schwarz Punkte treffe
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

    # Ausgehen von den berechneten Positionen der Ecken wird überprüft,
    # wo sich die Ecken befinden
    # ob das Blatt noch gedreht werden muss, bevor es ausgewertet werden kann
    if Top[0] < Bottom[0]: # linksneigung
        TopLeft = shakeLeftRGB(FB,a,b,shakeUpRGB(FB,a,b,searchRGBBlack(FB,a,b,TopLeft,40)))
        TopRight = shakeUpRGB(FB,a,b,shakeRightRGB(FB,a,b,searchRGBBlack(FB,a,b,TopRight,40)))
        BottomLeft = shakeDownRGB(FB,a,b,shakeLeftRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomLeft,40)))
        BottomRight = shakeRightRGB(FB,a,b,shakeDownRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomRight,40)))
    else: # rechtsneigung
        TopLeft = shakeUpRGB(FB,a,b,shakeLeftRGB(FB,a,b,searchRGBBlack(FB,a,b,TopLeft,40)))
        TopRight = shakeRightRGB(FB,a,b,shakeUpRGB(FB,a,b,searchRGBBlack(FB,a,b,TopRight,40)))
        BottomLeft = shakeLeftRGB(FB,a,b,shakeDownRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomLeft,40)))
        BottomRight = shakeDownRGB(FB,a,b,shakeRightRGB(FB,a,b,searchRGBBlack(FB,a,b,BottomRight,40)))

    # Wenn die Ecken nicht aus dem Bild herausfallen
    # werden die Längen der Ecken betrachtet, um die längste zu finden
    if TopLeft[0] in range(a) and TopLeft[1] in range(b):
        # Länge des Striches von der linken Ecke in y-Richtung
        lenTL = shakeDownRGB(FB,a,b,TopLeft)[1]-TopLeft[1]
    else: 
        lenTL = 0

    if TopRight[0] in range(a) and TopRight[1] in range(b):
        # siehe oben
        lenTR = shakeDownRGB(FB,a,b,TopRight)[1]-TopRight[1] 
    else:
        lenTR = 0

    if BottomLeft[0] in range(a) and BottomLeft[1] in range(b):  
        # siehe oben
        lenBL = BottomLeft[1]-shakeUpRGB(FB,a,b,BottomLeft)[1]
    else:
        lenBL = 0

    if BottomRight[0] in range(a) and BottomRight[1] in range(b):
        #siehe oben
        lenBR = BottomRight[1]-shakeUpRGB(FB,a,b,BottomRight)[1]
    else:
        lenBR = 0
    # Hier werden die Längen mit ihren Koordinaten gespeichert
    # TODO: Hier kann auf jeden Fall noch was verbessert werden
    # warum werden hier die Sachen mit ihren Werten als Schlüssel gespeihert
    corners = {lenTL : TopLeft, lenTR : TopRight, lenBL : BottomLeft, lenBR : BottomRight}
    m = max(lenTL,lenTR,lenBL,lenBR)
    M = set([lenTL,lenTR,lenBL,lenBR])

    # der größte Wert (die rechte untere Ecke ist immer die größte) wird entfernt
    # und es wird überprüft ob eine andere Länge noch ein Maximum darstellt
    # und ob die anderen Ecken überhaupt ein Länge haben
    # und nicht alle rausfallen
    # TODO: wird das verwendet, um festzustellen, ob der Fragebogen richtig ist?
    #       immerhin wissen wir, dass die größte Ecke rechts unten sein muss
    M.remove(m)
    FoundMax = True
    
    if(len(M) == 0):
        FoundMax=False
    else:
        for i in M:
            if i*1.5 >= m:
                FoundMax=False

    if not FoundMax:
        return ["help"]
    
    # Es werden jetzt die Koordinaten der rechten unteren Ecke festgelegt
    # sollte der Fragebogen nicht richtig gedreht sein, wird er jetzt
    # zurechtgedreht, in Abhängigkeit, wo die längste Ecke sich befindet
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
    else:
        pass  # Fragebogen ist in der richtigen Position
    
    # TODO: Das hier gefällt mir überhaupt nicht und muss nochmal geändert werden
    return [Fragebogen, Top, Bottom, Left, Right]

def typ_des_fbs(cropped_Questionnaire):
    """ 
        gibt den Typ des Fragebogens zurück, bisher wird deutsch ('deu') und
        englisch ('eng') als Sprachen unterstützt. Sollt der Fragebogen keiner
        der Fragen zugeordnet werden, wird ein leerer String zurückgegeben.
    """
    # Texterkennung tesseract wird auf Datei.crop angewendet mit Sprache Deutsch und Ergebnis an stdout geschickt
    # Das Tesseract-Modul muss wird genutzt, um den Typ der Veranstaltung zu bekommen
    s_deu = tesseract.image_to_string(cropped_Questionnaire, 'deu') 
    s_eng = tesseract.image_to_string(cropped_Questionnaire, 'eng')

    typ = ""
    # war bis auf "wurde" und "meetings" vorher auf 5
    # TODO: geht das auch so? oder muss ich es wieder hochstellen?
    erlaubte_fehler = 3
    
    for word in s_deu.split():
        if minimum_edit_distance(word,'Vorlesungen') < erlaubte_fehler:
            typ = "Vorlesung1"
            break
        elif not minimum_edit_distance(word,'Fragebogen')<erlaubte_fehler and (minimum_edit_distance(word,'Wurde')<3 or minimum_edit_distance(word,'Übungstermin')<erlaubte_fehler or minimum_edit_distance(word,'angeboten?')<erlaubte_fehler):
            typ = "Vorlesung2"
            break
        elif minimum_edit_distance(word,'Seminare')<erlaubte_fehler or minimum_edit_distance(word,'Praktika')<erlaubte_fehler:
            typ = "Seminar"
            break

    for word in s_eng.split():
        if minimum_edit_distance(word,'lectures')<erlaubte_fehler:
            typ = "Vorlesung1"
            break
        elif not minimum_edit_distance(word,'questionnaire')<erlaubte_fehler and (minimum_edit_distance(word,'exercise')<erlaubte_fehler or minimum_edit_distance(word,'meetings')<3 or minimum_edit_distance(word,'belonging')<erlaubte_fehler):
            typ = "Vorlesung2"
            break
        elif minimum_edit_distance(word,'seminars')<erlaubte_fehler or minimum_edit_distance(word,'practical')<erlaubte_fehler:
            typ = "Seminar"
            break

    return typ


def phase1(Questionnaire,leftborder=0,rightborder=0,topborder=0,bottomborder=0):
    
    Fragebogen = Image.open(Questionnaire)
    
    # wandelt das Bild in ein 2-Farbenbild (Schwarz, Weiß) um,
    # so das nur noch diese beiden Farben im Bild vorkommen
    # Dabei gilt 0=schwarz und 255=weiß. Es gibt nur diese beiden Werte
    # (https://pillow.readthedocs.io/en/stable/reference/Image.html?highlight=Image.convert#PIL.Image.Image.convert)
    Fragebogen = Fragebogen.convert('1', dither=Image.NONE)
    
    # Ein vorbereitetes Bild wird erstellt
    Fragebogen = bild_ist_vorbereitet(
        Fragebogen, 
        leftborder,
        rightborder,
        topborder,
        bottomborder)
    
    # überprüfe, ob ein Fehler aufgetreten ist, bei der Bearbeitung
    if type(Fragebogen) is list:
        if Fragebogen == ["empty"]:
            return ["empty"]
        elif Fragebogen == ["help"]:
            return ["help", Questionnaire]
        else:
            raise TypeError

# start die weiter bearbeitung und die Suche nach den Ecken
    
    gedrehte_liste = bogen_drehen(Fragebogen)
    Fragebogen = gedrehte_liste[0]
    Top = gedrehte_liste[1]
    Bottom = gedrehte_liste[2]
    Left = gedrehte_liste[3]
    Right = gedrehte_liste[4]

    if Fragebogen == ["help"]:
        # Es ist ein Problem aufgetreten
        return ["help", Questionnaire]

    # TODO: Wie wird das weiterverwendet height, width, origin
    height = .01*(Bottom[1]-Top[1])
    width = .01*(Right[0]-Left[0])

    origin = np.array((Left[0],Top[1]))
    
    # Die Box gibt an, welcher Bereich ausgewählt werden muss, um dann
    # um dann dort zu gucken, zu welchem Typ der Fragebogen gehört 
    box = (Left[0],int(Top[1]+(Left[1]-Top[1])/2.7),Top[0],int(Left[1]-(Left[1]-Top[1])/1.7))
    # ist der linke/obere x/y-Wert größer als der rechte/obere, wird ein Fehler
    # zurückgegeben
    if(box[0]>=box[2] or box[1]>=box[3]):
        return ["help",Questionnaire]
    # der zu untersuchende Bereich wird gespeichert
    Fragebogen.crop(box).save(str(Questionnaire) + ".crop", "PNG",optimize=True)

    typ = typ_des_fbs(str(Questionnaire) + ".crop")

    # TODO: bisher gibt es keinen guten Grund, dass diese Datei existiert,
    #       aha der Ort wird zurückgegeben
    Fragebogen.save(str(Questionnaire) + ".processed", "PNG",optimize=True)
    
    # Wenn ein leerer String als Typ zurückgegeben wird
    if not typ:
        return ["help",Questionnaire]

    return [typ,str(Questionnaire)+".processed",origin,width,height]

