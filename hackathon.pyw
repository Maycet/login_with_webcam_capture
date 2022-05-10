import PIL
from PIL import Image,ImageTk
import pytesseract
import cv2
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

######################### Cargo la base de los usuarios #########################
with open('data.json') as json_file:
    users = json.load(json_file)

carreras = ['- Seleccione -','Derecho','Comunicación social y periodismo',\
            'Diseño digital','Publicidad internacional','Ingeniería industrial',\
            'Ingeniería ambiental','Ingeniería de sistemas y telecomunicaciones',\
            'Ingeniería electrónica','Matemáticas','Administración ambiental',\
            'Administración de negocios','Comercio internacional',\
            'Contaduría pública','Administración de empresas','Finanzas y comercio exterior',\
            'Marketing y negocios internacionales','Preuniversitario',\
            'Tecnología en administración agropecuaria','Tecnología en criminalística'\
            'Tecnología en dirección técnica de fútbol','Economía','Filosofía y humanidades',\
            'Licenciatura en filosofía y letras','Política y relaciones internacionales',\
            'Música','Teatro musical','Gestión deportiva','Psicología']

##### Funcion de camara web #####
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    added_image = cv2.addWeighted(frame[y:y+200,x:x+352,:],0.8,foreground[43:y+200,0:352,:],0.2,0)
    frame[y:y+200,x:x+352] = added_image
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

######################### Ventana inicial #########################
root = Tk()
root.title('Asistencia')
root.geometry('720x1280')
root.iconbitmap('maycet_icon_gray.ico')
root.config(bg='#00457C', padx=5, pady=50)
root.resizable(0, 0)

logo = PhotoImage(file='universidad-sergio-arboleda-35.png')
Label(root, image=logo, bg='#00457C').pack()

######################### Intruccion general #########################
inst = Label(root, text='Ingresa con tus datos', font=('bold',14))
inst.config(bg='#00457C', fg='white')
inst.pack(padx=10, pady=10)

######################### Frame 1 #########################
cuadro1 = Frame(root)
cuadro1.config(bg='#00457C', bd=5, relief='sunken')
cuadro1.pack(padx=10, pady=10)

######################### Formulario #########################

##### Instruccion carrera #####
carrera_inst = Label(cuadro1, text='Carrera', font=('bold',11))
carrera_inst.grid(row=1, column=0, padx=5, pady=10)
carrera_inst.config(bg='#00457C', fg='white')
##### Opciones carrera #####
carrera_ingreso = ttk.Combobox(cuadro1, state='readonly')
carrera_ingreso['values'] = carreras
carrera_ingreso.grid(row=1, column=1, padx=5, pady=10)
carrera_ingreso.current(0)
carrera_ingreso.config(font=('bold',11))

##### Instruccion ID #####
ID_inst = Label(cuadro1, text='N° Documento: ', font=('bold',11))
ID_inst.grid(row=2, column=0, padx=5, pady=11)
ID_inst.config(bg='#00457C', fg='white')
##### Cuadro ID #####
ID_ingreso = Entry(cuadro1)
ID_ingreso.grid(row=2, column=1, padx=5, pady=11)
ID_ingreso.config(bg='white', fg='#00457C', justify='center', font=('bold',11))

##### Instruccion nombre #####
nombre_inst = Label(cuadro1, text='Nombre completo: ', font=('bold',11))
nombre_inst.config(bg='#00457C', fg='white')
##### Cuadro nombre #####
nombre_ingreso = Entry(cuadro1)
nombre_ingreso.config(bg='white', fg='#00457C', justify='center', font=('bold',11))

##### Boton ingresar #####
def ingresar():
    if carrera_ingreso.get() == '- Seleccione -':
        messagebox.showinfo('Error de carrera','Debe seleccionar una carrera.')
    elif ID_ingreso.get() not in users.keys():
        messagebox.showinfo('Error de ID','Su número de identificación no está en los registros.')
    elif users[ID_ingreso.get()]['carrera'] != carrera_ingreso.get():
        messagebox.showinfo('Error de carrera','Verifique que la carrera sea la correcta.')
    else:
        inst.config(text='Manten tu rostro en\nel área delimitada')
        ingreso.pack_forget()
        registro.pack_forget()
        cuadro1.pack_forget()
        cuadro2.pack(padx=10, pady=10)
        lmain.pack()
        captura.pack(padx=10, pady=0)
        show_frame()

ingreso = Button(root, text='Ingresar', font=('bold',13), command=ingresar)
ingreso.config(bg='#00457C', fg='white')
ingreso.pack(padx=10, pady=0)

##### Boton registrar #####
def registrar():
    inst.config(text='Completa el registro con\nlos siguientes datos')
    ingreso.pack_forget()
    registro.pack_forget()
    nombre_inst.grid(row=3, column=0, padx=5, pady=11)
    nombre_ingreso.grid(row=3, column=1, padx=5, pady=11)
    validacion.pack(padx=10, pady=0)

registro = Button(root, text='Registrarse', font=('bold',11), command=registrar, borderwidth=0)
registro.config(bg='#00457C', fg='white')
registro.pack(padx=10, pady=0)

##### Boton validar #####
def validar():
    if carrera_ingreso.get() == '- Seleccione -':
        messagebox.showinfo('Error de registro','¡No ha seleccionado carrera!')
    elif ID_ingreso.get() == '':
        messagebox.showinfo('Error de registro','¡Debe poner un número de identificación!')
    elif nombre_ingreso.get() == '':
        messagebox.showinfo('Error de registro','¡Debe poner su nombre!')
    else:
        users[ID_ingreso.get()]={'nombre':nombre_ingreso.get(),'carrera':carrera_ingreso.get()}
        with open('data.json', 'w') as outfile:
            json.dump(users, outfile, indent=4)
        inst.config(text='Ingresa con tus datos')
        nombre_inst.grid_forget()
        nombre_ingreso.grid_forget()
        validacion.pack_forget()
        ingreso.pack(padx=10, pady=0)
        registro.pack(padx=10, pady=0)

validacion = Button(root, text='Validar', font=('bold',13), command=validar)
validacion.config(bg='#00457C', fg='white')

##### Boton capturar #####
def capturar():
    inst.config(text="¡Gracias!\nSi deseas ingresar con otra cuenta\ndale al botón 'Regresar'.")
    cuadro2.pack_forget()
    captura.pack_forget()
    regreso.pack(padx=10, pady=0)

captura = Button(root, text='Capturar', font=('bold',13), command=capturar)
captura.config(bg='#00457C', fg='white')

##### Boton regresar #####
def regresar():
    cuadro2.pack_forget()
    regreso.pack_forget()
    cuadro1.pack()
    inst.config(text='Ingresa con tus datos')
    ingreso.pack(padx=10, pady=0)
    registro.pack(padx=10, pady=10)

regreso = Button(root, text='Regresar', font=('bold',11), command=regresar, borderwidth=1)
regreso.config(bg='#00457C', fg='white')

######################### Formulario #########################
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
cont = True

######################### Frame 2 #########################
cuadro2 = Frame(root)
cuadro2.config(bg='#00457C', bd=5, relief='sunken')

lmain = Label(cuadro2)
foreground = cv2.imread('oval_t.png')
x,y = 0,43

######################### Mostrar #########################
root.mainloop()
