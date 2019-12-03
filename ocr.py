import tkinter
import pytesseract
from pytesseract import image_to_string
from PIL import ImageTk,Image
import tkinter.filedialog
import cv2
import os


root = tkinter.Tk()
root.geometry("600x300") 
load = Image.open("D:/1.Wardrobe/Walls/490725.png")
render = tkinter.PhotoImage(file="D:/1.Wardrobe/Walls/490725.png")
browseText = 'Browse Image'
actionText = 'Convert'
def display_image():
    global f
    f = tkinter.filedialog.askopenfilename(
        parent=root, initialdir='C:/Tutorial',
        title='Choose file',
        filetypes=[('png images', '.png'),
                   ('gif images', '.gif')]
        )
    #print(f)
    
    load = Image.open(f)
    load = load.resize((150, 150), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)

    img = tkinter.Label(root,image=render)
    img.image = render
    img.place(x=60,y=60)

def convert():
    global theText
    image = cv2.imread(f)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    #The pre-processing starts
    image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    image = cv2.medianBlur(image, 3)
    image = cv2.bilateralFilter(image,9,75,75)
    #The pre-processing ends
    if( preprocess.get() == "Thresh"):
        gray = cv2.threshold(gray, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    elif preprocess.get() == "Blur":
        gray = cv2.medianBlur(gray, 3)
    
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    
    pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
    theText = pytesseract.image_to_string(Image.open(filename),lang=language.get())
    os.remove(filename)
    print(theText)
    ent = tkinter.Entry(root, state='readonly', readonlybackground='white', fg='black')
    var = tkinter.StringVar()
    var.set(theText)
    ent.config(textvariable=var, relief='flat')
    ent.pack(ipadx=30,ipady=30,side=tkinter.RIGHT,padx=25, pady=50)
    
browseButton = tkinter.Button(root, text=browseText, command=display_image)
browseButton.place(y=40)
browseButton.pack()

preprocess = tkinter.StringVar(root)
preprocess.set("--Select Preprocess--")
preprocessButton = tkinter.OptionMenu(root,preprocess,"Blur","Thresh")
preprocessButton.place(relx = 5, rely = 5, anchor = "center")
preprocessButton.pack()

language = tkinter.StringVar(root)
language.set("--Select Language--")
languageButton = tkinter.OptionMenu(root,language,"eng","kan")
languageButton.place(relx = 5, rely = 5, anchor = "center")
languageButton.pack()

actionButton = tkinter.Button(root, text="Convert", command=convert)
actionButton.place(x=350,y=350)
actionButton.pack(ipadx=10,ipady=10,padx=15,pady=5)

root.mainloop()