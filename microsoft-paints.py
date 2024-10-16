from cmu_graphics import *
'''
Bonus Feature: Pou Option
Link to Video: https://drive.google.com/drive/folders/1xRACoLNpb6jzXSBkntXzX3uyqkpipCnr?usp=sharing
'''

class Rect:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

class Line:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

class Polygon:
    def __init__(self, points):
        self.points = points
        
    def addPoint(self, point):
        self.points.append(point)
        
    def removeTuples(self):
        pointsList = []
        for coord in self.points:
            x, y = coord
            pointsList.append(x)
            pointsList.append(y)
        return pointsList

class FreeLine:
    def __init__(self, lines = []):
        self.lines = lines
        
    def addLine(self, line):
        if self.lines == []:
            self.lines = [line]
        else:
            if self.lines[-1] != line:
                self.lines.append(line)
                
class Pou:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height    
    
class PaintCanvas:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        
    def __repr__(self):
        return f'Canvas with left: {self.left}, top: {self.top}, width: {self.width}, height: {self.height}'

class Sidebar:
    def __init__(self, top, width, height):
        self.left = 0
        self.top = top
        self.width = width
        self.height = height
        
def onAppStart(app):
    app.width = 700
    app.height = 450
    app.canvas = PaintCanvas(75, 50, app.width - 95, app.height - 70)
    app.sidebar = Sidebar(app.canvas.top, app.canvas.left, app.height - app.canvas.top)
    app.colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'black', 'gray']
    app.options = ['rect', 'circle', 'line', 'polygon', 'freeLine', 'pou']
    
    #Current options
    app.currShape = 'polygon'
    app.currShapeIndex = None
    app.currOutline = None
    app.currColor = app.colors[0] #Default: red
    app.clickCoord = None
    app.releaseCoord = None
    
    app.shapesOnCanvas = []
    app.shapeMemory = []
    
    ##Free Line attributes
    app.currLines = []

    ##Polygon Coordinates
    app.polygonCoords = []
    
def onKeyPress(app, key):
    if key == 'z' and len(app.shapesOnCanvas) != 0:
        app.shapesOnCanvas = app.shapesOnCanvas[:-1]
    elif key == 'y' and len(app.shapesOnCanvas) < len(app.shapeMemory):
        shapeIndex = len(app.shapesOnCanvas)
        redoShape = app.shapeMemory[shapeIndex]
        app.shapesOnCanvas = app.shapesOnCanvas + [redoShape]
    
def onMousePress(app, mouseX, mouseY):
    if legalPaintingLocation(app, mouseX, mouseY) and app.currShapeIndex != None:
        app.clickCoord = (mouseX, mouseY)
        if app.currShape == 'polygon':
            app.currOutline = Polygon(app.polygonCoords)
            if hitsStartPoint(app, mouseX, mouseY): ##Checks if user hits green X
                if len(app.polygonCoords) >= 3: ##Checks if valid Python
                    shape, color = app.currOutline, app.currColor
                    app.shapesOnCanvas.append((shape, color))
                    app.shapeMemory = app.shapesOnCanvas
                    app.clickCoord = None
                app.currOutline = None
                app.polygonCoords = []
            else:
                updateOutlinePolygon(app, mouseX, mouseY)
                app.polygonCoords = app.currOutline.points
    else:
        if clickedShapeOption(app, mouseX, mouseY):
            app.clickCoord = None
            app.currOutline = None
            app.polygonCoords = []
        elif clickedColorOption(app, mouseX, mouseY):
            return
        elif clickedUndoOption(app, mouseX, mouseY):
            return
        elif clickedRedoOption(app, mouseX, mouseY):
            return
            
            
def onMouseDrag(app, mouseX, mouseY):
    if app.clickCoord != None:
        clickX, clickY = app.clickCoord
        if app.currShape == 'rect': ###Updates outline of Rectangle
            releaseX, releaseY = mouseX, mouseY
            if ((clickX) != releaseX and (clickY != releaseY)) and legalPaintingLocation(app, mouseX, mouseY):
                updateOutlineRect(app, mouseX, mouseY)
                app.releaseCoord = (mouseX, mouseY)
        elif app.currShape == 'circle': ###Updates outline of Circle
            r = distance(clickX, clickY, mouseX, mouseY)
            if r != 0 and legalPaintingLocation(app, mouseX, mouseY):
                updateOutlineCircle(app, r)
                app.releaseCoord = (mouseX, mouseY)
        elif app.currShape == 'line': ###Updates outline of Line
            if (mouseX,mouseY) != (clickX, clickY) and legalPaintingLocation(app, mouseX, mouseY):
                updateOutlineLine(app, mouseX, mouseY)
                app.releaseCoord = (mouseX, mouseY)
        elif app.currShape == 'freeLine': ###Updates outline of Free Line
            if legalPaintingLocation(app, mouseX, mouseY):
                app.currOutline = FreeLine(app.currLines)
                updateOutlineFreeLine(app, mouseX, mouseY)
                app.currLines = app.currOutline.lines
                app.releaseCoord = (mouseX, mouseY)
        elif app.currShape == 'pou':
            releaseX, releaseY = mouseX, mouseY
            if ((clickX) != releaseX and (clickY != releaseY)) and legalPaintingLocation(app, mouseX, mouseY):
                updateOutlinePou(app, mouseX, mouseY)####################
                app.releaseCoord = (mouseX, mouseY)

        
def onMouseRelease(app, mouseX, mouseY):
    if app.currShape != 'polygon' and app.clickCoord != None and app.clickCoord != (mouseX, mouseY):
        shape, color = app.currOutline, app.currColor
        app.shapesOnCanvas.append((shape, color))
        app.shapeMemory = app.shapesOnCanvas
        app.clickCoord = None
        app.releaseCoord = None
        app.currOutline = None
        app.currLines = [] 
    

def redrawAll(app):
    drawBackground(app)
    drawHeader(app)
    drawCanvas(app)
    drawSidebar(app)
    drawSidebarBoxes(app)
    drawShapesOnCanvas(app)
    drawOutline(app)

#### Draw Functions
def drawBackground(app):
    drawRect(0, 0, app.width, app.height, fill= 'gainsboro')

def drawHeader(app):
    drawRect(0, 0, app.width, app.canvas.top, fill= 'gainsboro', border= 'black')
    drawLabel('Microsoft Paints', 350, 25, font='caveat', size=30)

def drawCanvas(app):
    drawRect(app.canvas.left, app.canvas.top, app.canvas.width, app.canvas.height, fill='white', border= 'black')

    
def drawSidebar(app):
    drawRect(app.sidebar.left, app.sidebar.top, app.sidebar.width, app.sidebar.height, fill='gainsboro', border='black')
    drawLabel('Fill Options', 37, 275, size=13, italic=True)
    
def drawSidebarBoxes(app):
    drawShapeBoxes(app)
    drawUndoBoxes(app)
    drawColorBoxes(app)
        
def drawShapeBoxes(app): #Helper Function to draw Sidebar boxes
    boxWidth = 30
    boxHeight = 30
    i = 0
    k = 0
    dy = 60
    while i < len(app.options):
        shape = app.options[i]
        dx = 5 + 35 * k
        if dx >= app.canvas.left:
            k = 0
            dx = 5
            dy += 40
        if app.currShapeIndex == i:
            borderColor = 'limeGreen'
        else:
            borderColor = 'black'
        drawRect(dx, dy, boxWidth, boxHeight, fill= None, border=borderColor)
        drawShapeIcons(app, shape)
        k += 1
        i += 1

def drawShapeIcons(app, shape):
    if shape == 'rect':
        drawRect(10, 65, 20, 20, fill='darkGray', border='dimGray')
    elif shape == 'circle':
        drawCircle(55, 75, 10, fill='darkGray', border='dimGray')
    elif shape == 'line':
        drawLine(12, 123, 28, 107, fill='dimGray')
    elif shape == 'polygon':
        drawPolygon(45, 110, 62, 105, 59, 125, 50, 120, fill='darkGray', border='dimGray')
    elif shape == 'freeLine':
        # pencilSymbol = chr(0x1f589)
        # drawLabel(pencilSymbol, 20, 155, size=20, fill='dimGray', font='symbols')
        drawLabel("Pencil", 20, 155, fill='red', size= 8, bold=True)
    elif shape == 'pou':
        pouPic = 'https://tr.rbxcdn.com/26f663eead6a4bf8e7b64131e9d808db/420/420/Hat/Png'
        drawImage(pouPic, 55, 155, align='center', width = 20, height=20)


def drawUndoBoxes(app): #Helper Function to draw Sidebar boxes
    boxWidth = 30
    boxHeight = 30
    b1X, b1Y = 5, 180
    b2X, b2Y = 40, 180
    drawRect(b1X, b1Y, boxWidth, boxHeight, fill= None, border='black') ###Draws Undo Box
    leftArrow = chr(0x1f808)                                                ##
    # drawLabel(leftArrow, 20, 195, font='symbols', fill='dimGray', size=20)  ##Labels in Box
    drawLabel("Undo", 20, 195, fill='red', size= 9, bold=True)
    drawLabel('z', 11, 204, size=10, fill='dimGray')                        ##
    drawRect(b2X, b2Y, boxWidth, boxHeight, fill= None, border='black') ##Draws Redo Box
    rightArrow = chr(0x1f80a)                                               ##
    # drawLabel(rightArrow, 55, 195, font='symbols', fill='dimGray', size=20) ##Labels in Box
    drawLabel("Redo", 55, 195, fill='red', size= 9, bold=True)

    drawLabel('y', 46, 204, size=10, fill='dimGray')                        ##

    
def drawColorBoxes(app):
    boxWidth = 30
    boxHeight = 30
    i = 0
    k = 0
    dy = 290
    while i < len(app.colors):
        borderColor = 'black'
        color = app.colors[i]
        dx = 5 + 35 * k
        if dx >= app.canvas.left:
            k = 0
            dx = 5
            dy += 40
        if app.currColor == color:
            borderColor = 'limeGreen'
        drawRect(dx, dy, boxWidth, boxHeight, fill= color, border=borderColor)
        k += 1
        i += 1
    
def drawOutline(app):
    if app.clickCoord != None and app.releaseCoord != None:
        if app.currShape == 'rect':
            left = app.currOutline.left
            top = app.currOutline.top
            width = app.currOutline.width
            height = app.currOutline.height
            drawRect(left, top, width, height, border= app.currColor, fill=None)
        elif app.currShape == 'circle':
            cx = app.currOutline.x
            cy = app.currOutline.y
            cr = app.currOutline.r
            drawCircle(cx, cy, cr, border= app.currColor, fill=None)
        elif app.currShape == 'line':
            x0 = app.currOutline.x0
            y0 = app.currOutline.y0
            x1 = app.currOutline.x1
            y1 = app.currOutline.y1
            drawLine(x0, y0, x1, y1, fill= app.currColor)
        elif app.currShape == 'freeLine':
            lines = app.currOutline.lines
            for line in lines:
                x0, y0, x1, y1 = line
                drawLine(x0, y0, x1, y1, fill= app.currColor)
        elif app.currShape == 'pou':
            left = app.currOutline.left
            top = app.currOutline.top
            width = app.currOutline.width
            height = app.currOutline.height
            drawRect(left, top, width, height, border='burlyWood', fill=None)
    elif app.currShape == 'polygon' and app.clickCoord != None and app.currOutline != None:
        points = app.currOutline.points
        for i in range(len(points)):
            coord = points[i]
            x = coord[0]
            y = coord[1]
            if i == 0:
                color = 'green'
            else:
                color = 'red'
            drawLabel('X', x, y, fill= color)
            
def drawShapesOnCanvas(app):
    for shape, color in app.shapesOnCanvas:
        if isinstance(shape, Rect):
            left = shape.left
            top = shape.top
            width = shape.width
            height = shape.height
            drawRect(left, top, width, height, fill= color)
        elif isinstance(shape, Circle):
            cx = shape.x
            cy = shape.y
            cr = shape.r
            drawCircle(cx, cy, cr, fill= color)
        elif isinstance(shape, Line):
            x0 = shape.x0
            y0 = shape.y0
            x1 = shape.x1
            y1 = shape.y1
            drawLine(x0, y0, x1, y1, fill= color)
        elif isinstance(shape, FreeLine):
            for line in shape.lines:
                x0, y0, x1, y1 = line
                drawLine(x0, y0, x1, y1, fill= color)
        elif isinstance(shape, Polygon):
            pointsTuple = shape.points
            pointsList = shape.removeTuples()
            drawPolygon(*pointsList, fill= color)
        elif isinstance(shape, Pou):
            left = shape.left
            top = shape.top
            pouWidth = shape.width
            pouHeight = shape.height
            pouPic = 'https://tr.rbxcdn.com/26f663eead6a4bf8e7b64131e9d808db/420/420/Hat/Png'
            drawImage(pouPic, left, top, width= pouWidth, height= pouHeight)

##
#### End of Draw Functions

######Other Functions

def legalPaintingLocation(app, x, y):
    return ((x > app.canvas.left) and (x < (app.canvas.width + app.canvas.left)) and
        (y > app.canvas.top) and (y < app.canvas.height + app.canvas.top))
        
def updateOutlineRect(app, mouseX, mouseY): ##Updates rectangle measurement values
    clickX, clickY = app.clickCoord
    releaseX, releaseY = mouseX, mouseY
    
    width = abs(clickX - releaseX)
    height = abs(clickY - releaseY)
    
    if releaseX < clickX:
        left = releaseX
    else:
        left = clickX
    if releaseY < clickY:
        top = releaseY
    else:
        top = clickY
    app.currOutline = Rect(left, top, width, height)

def updateOutlineCircle(app, r): ##Updates Circle measurement values
    clickX, clickY = app.clickCoord
    if ((legalPaintingLocation(app, clickX + r, clickY + r)) and
        (legalPaintingLocation(app, clickX - r, clickY - r))):
        app.currOutline = Circle(clickX, clickY, r)

def updateOutlineLine(app, mouseX, mouseY): ##Updates Line Coordinates
    clickX, clickY = app.clickCoord
    app.currOutline = Line(clickX, clickY, mouseX, mouseY)
    
def updateOutlineFreeLine(app, mouseX, mouseY): ##Updates Free Line
    clickX, clickY = app.clickCoord
    if app.currLines == []:
        line = (clickX, clickY, mouseX, mouseY)
    else:
        x0, y0, x1, y1 = app.currLines[-1]
        line = (x1, y1, mouseX, mouseY)
    app.currOutline.addLine(line)

def updateOutlinePolygon(app, mouseX, mouseY): ##Updates Polygon points
    point = (mouseX, mouseY)
    app.currOutline.addPoint(point)

def updateOutlinePou(app, mouseX, mouseY):
    clickX, clickY = app.clickCoord
    releaseX, releaseY = mouseX, mouseY
    
    width = abs(clickX - releaseX)
    height = abs(clickY - releaseY)
    
    if releaseX < clickX:
        left = releaseX
    else:
        left = clickX
    if releaseY < clickY:
        top = releaseY
    else:
        top = clickY
    app.currOutline = Pou(left, top, width, height)
    
def hitsStartPoint(app, mouseX, mouseY): #Checks whether User clicked start of Polygon point
    if len(app.polygonCoords) < 1:
        return False
    x, y = app.currOutline.points[0]
    if distance(x, y, mouseX, mouseY) < 5:
        return True
    else:
        return False
        
def clickedShapeOption(app, mouseX, mouseY): ##Changes shape according to which box user clicks
    boxWidth = 30
    boxHeight = 30
    i = 0
    k = 0
    dy = 60
    while i < len(app.options):
        dx = 5 + 35 * k
        if dx >= app.canvas.left:
            k = 0
            dx = 5
            dy += 40
        if ((mouseX >= dx and mouseX <= dx+boxWidth) and
            (mouseY >= dy and mouseY <= dy+boxHeight)):
            if app.currShapeIndex == i:
                app.currShapeIndex = None
            else:
                app.currShapeIndex = i
            app.currShape = app.options[i]
            return True
        k += 1
        i += 1

def clickedColorOption(app, mouseX, mouseY): ###Changes Color based on where User Clicks
    boxWidth = 30
    boxHeight = 30
    i = 0
    k = 0
    dy = 290
    while i < len(app.colors):
        color = app.colors[i]
        dx = 5 + 35 * k
        if dx >= app.canvas.left:
            k = 0
            dx = 5
            dy += 40
        if ((mouseX >= dx and mouseX <= dx+boxWidth) and
            (mouseY >= dy and mouseY <= dy+boxHeight)):
            app.currColor = color
        k += 1
        i += 1

def clickedUndoOption(app, mouseX, mouseY):
    boxWidth = 30
    boxHeight = 30
    b1X, b1Y = 5, 180
    if ((mouseX >= b1X and mouseX <= b1X+boxWidth) and
        (mouseY >= b1Y and mouseY <= b1Y+boxHeight) and
        (len(app.shapesOnCanvas) != 0)):
        app.shapesOnCanvas = app.shapesOnCanvas[:-1]

def clickedRedoOption(app, mouseX, mouseY):
    boxWidth = 30
    boxHeight = 30
    b2X, b2Y = 40, 180
    if ((mouseX >= b2X and mouseX <= b2X+boxWidth) and
        (mouseY >= b2Y and mouseY <= b2Y+boxHeight) and
        (len(app.shapesOnCanvas) < len(app.shapeMemory))):
        shapeIndex = len(app.shapesOnCanvas)
        redoShape = app.shapeMemory[shapeIndex]
        app.shapesOnCanvas = app.shapesOnCanvas + [redoShape]

def distance(x0, y0, x1, y1):
    return (((x1 - x0)**2 + (y1 - y0)**2)**0.5)




def main():
    runApp()
main()