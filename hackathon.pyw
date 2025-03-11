import time
import PIL
from PIL import  ImageTk
import cv2
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import constants

class WebcamApp:
	def __init__(self, root):
		self.root = root
		self.video_capture = None
		# self.stop_webcam = False
		self.users = self.load_users_data()
		self.setup_ui()
	
	def log_message(self, message):
		with open('app_log.txt', 'a') as log_file:
			log_file.write(f"{message}\n")

	def load_users_data(self):
		try:
			with open('users_data.json') as json_file:
				return json.load(json_file)
		except Exception as exception:
			self.log_message(exception)
			messagebox.showerror("Error", "No se pudo leer la información de los usuarios. Verifique la ruta del archivo.")

	def init_webcam(self):
		try:
			self.foreground = cv2.imread('oval1.png')
		except Exception as exception:
			self.log_message(exception)
		
		self.video_capture = cv2.VideoCapture(0)
		self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
		self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

	def show_webcam_frame(self):
		if self.video_capture is None:
			self.init_webcam()

		# if self.stop_webcam:
		# 	if self.video_capture is not None:
		# 		self.video_capture.release()
		# 		self.video_capture = None
		# 	return

		if self.video_capture is None or not self.video_capture.isOpened():
			messagebox.showerror("Error", "No se pudo inicializar la cámara. Verifique la conexión.")
			return
		
		_, frame = self.video_capture.read()
		frame = cv2.flip(frame, 1)
		
		if self.foreground is not None:
			foreground_height, foreground_width = self.foreground.shape[:2]
			frame = cv2.resize(frame, (foreground_width, foreground_height))
			added_image = cv2.addWeighted(frame, 0.9, self.foreground, 0.1, 0)
			frame = added_image

		cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
		img = PIL.Image.fromarray(cv2image)
		imgtk = ImageTk.PhotoImage(image=img)
		self.lmain.imgtk = imgtk
		self.lmain.configure(image=imgtk)
		self.lmain.after(10, self.show_webcam_frame)

	def login_command(self):
		if self.career_combobox.get() == '- Seleccione -':
			messagebox.showinfo('Error de carrera', 'Debe seleccionar una carrera.')
		elif self.id_number_input.get() not in self.users.keys():
			messagebox.showinfo('Error de ID', 'Su número de identificación no está en los registros.')
		elif self.users[self.id_number_input.get()]['carrera'] != self.career_combobox.get():
			messagebox.showinfo('Error de carrera', 'Verifique que la carrera sea la correcta.')
		else:
			self.login_button.pack_forget()
			self.registration_button.pack_forget()
			self.form_container.pack_forget()
			
			time.sleep(0.5)
			self.info_label.config(text='Manten tu rostro en\nel área delimitada')
			self.cuadro2.pack(padx=10, pady=10)
			self.lmain.pack()
			self.snapshot_button.pack(padx=10, pady=0)
			self.show_webcam_frame()

	def registration_command(self):
		self.info_label.config(text='Completa el registro con\nlos siguientes datos')
		self.login_button.pack_forget()
		self.registration_button.pack_forget()
		self.full_name_label.grid(row=3, column=0, padx=5, pady=11)
		self.full_name_input.grid(row=3, column=1, padx=5, pady=11)
		self.validate_button.pack(padx=10, pady=0)
		self.return_button.pack(padx=10, pady=0)

	def validate_registration(self):
		if self.career_combobox.get() == '- Seleccione -':
			messagebox.showinfo('Error de registro', '¡No ha seleccionado carrera!')
		elif self.id_number_input.get() == '':
			messagebox.showinfo('Error de registro', '¡Debe poner un número de identificación!')
		elif self.full_name_input.get() == '':
			messagebox.showinfo('Error de registro', '¡Debe poner su nombre!')
		else:
			self.users[self.id_number_input.get()] = {'nombre': self.full_name_input.get(), 'carrera': self.career_combobox.get()}
			with open('data.json', 'w') as outfile:
				json.dump(self.users, outfile, indent=4)
			self.info_label.config(text='Ingresa con tus datos')
			self.full_name_label.grid_forget()
			self.full_name_input.grid_forget()
			self.validate_button.pack_forget()
			self.login_button.pack(padx=10, pady=0)
			self.registration_button.pack(padx=10, pady=0)

	def snapshot_command(self):
		self.info_label.config(text="¡Gracias!\nSi deseas ingresar con otra cuenta\ndale al botón 'Regresar'.")
		self.cuadro2.pack_forget()
		self.snapshot_button.pack_forget()
		self.return_button.pack(padx=10, pady=0)

	def return_command(self):
		self.lmain.pack_forget()
		self.cuadro2.pack_forget()
		self.return_button.pack_forget()
		self.validate_button.pack_forget()
		self.full_name_label.grid_forget()
		self.full_name_input.grid_forget()
		self.form_container.pack()
		self.info_label.config(text='Ingresa con tus datos')
		self.login_button.pack(padx=10, pady=0)
		self.registration_button.pack(padx=10, pady=10)
		# self.stop_webcam = True

	def setup_ui(self):
		self.root.title('Asistencia')
		self.root.geometry('720x1280')
		self.root.iconbitmap('maycet_icon_gray.ico')
		self.root.config(bg=constants.main_color, padx=5, pady=50)
		self.root.resizable(0, 0)

		# Load the image using PIL and ImageTk
		logo_image = PIL.Image.open('universidad-sergio-arboleda-35.png')
		logo = ImageTk.PhotoImage(logo_image)
		Label(self.root, image=logo, bg=constants.main_color).pack()
		self.root.logo = logo

		# Information label
		self.info_label = Label(self.root, text='Ingresa con tus datos', font=('bold', 14))
		self.info_label.config(bg=constants.main_color, fg=constants.secondary_color)
		self.info_label.pack(padx=10, pady=10)

		self.setup_form()
		self.setup_buttons()

		# Webcam container frame
		self.cuadro2 = Frame(self.root)
		self.cuadro2.config(bg=constants.main_color, bd=5, relief='sunken')
		self.lmain = Label(self.cuadro2)
	
	def setup_form(self):
		#  Form container frame
		self.form_container = Frame(self.root, bg=constants.main_color, bd=5, relief='sunken')
		self.form_container.pack(padx=10, pady=10)

		# Carreer label
		career_label = Label(self.form_container, text='Carrera', font=('bold', 11))
		career_label.grid(row=1, column=0, padx=5, pady=10)
		career_label.config(bg=constants.main_color, fg=constants.secondary_color)

		# Carreers combobox
		self.career_combobox = ttk.Combobox(self.form_container, state='readonly')
		self.career_combobox['values'] = constants.courses
		self.career_combobox.grid(row=1, column=1, padx=5, pady=10)
		self.career_combobox.current(0)
		self.career_combobox.config(font=('bold', 11))

		# ID number label
		id_number_label = Label(self.form_container, text='N° Documento: ', font=('bold', 11))
		id_number_label.grid(row=2, column=0, padx=5, pady=11)
		id_number_label.config(bg=constants.main_color, fg=constants.secondary_color)

		# ID entry
		self.id_number_input = Entry(self.form_container)
		self.id_number_input.grid(row=2, column=1, padx=5, pady=11)
		self.id_number_input.config(bg=constants.secondary_color, fg=constants.main_color, justify='center', font=('bold', 11))

		# Name label
		self.full_name_label = Label(self.form_container, text='Nombre completo: ', font=('bold', 11))
		self.full_name_label.config(bg=constants.main_color, fg=constants.secondary_color)

		# Name entry
		self.full_name_input = Entry(self.form_container)
		self.full_name_input.config(bg=constants.secondary_color, fg=constants.main_color, justify='center', font=('bold', 11))

	def setup_buttons(self):
		# Login button
		self.login_button = Button(self.root, text='Ingresar', font=('bold', 13), command=self.login_command)
		self.login_button.config(bg=constants.main_color, fg=constants.secondary_color)
		self.login_button.pack(padx=10, pady=0)

		# Register button
		self.registration_button = Button(self.root, text='Registrarse', font=('bold', 11), command=self.registration_command, borderwidth=0)
		self.registration_button.config(bg=constants.main_color, fg=constants.secondary_color)
		self.registration_button.pack(padx=10, pady=0)

		# Validation button
		self.validate_button = Button(self.root, text='Validar', font=('bold', 13), command=self.validate_registration)
		self.validate_button.config(bg=constants.main_color, fg=constants.secondary_color)

		# Capture button
		self.snapshot_button = Button(self.root, text='Capturar', font=('bold', 13), command=self.snapshot_command)
		self.snapshot_button.config(bg=constants.main_color, fg=constants.secondary_color)

		# Return button
		self.return_button = Button(self.root, text='Regresar', font=('bold', 11), command=self.return_command, borderwidth=1)
		self.return_button.config(bg=constants.main_color, fg=constants.secondary_color)

def main():
	root = Tk()
	WebcamApp(root)
	root.mainloop()

if __name__ == "__main__":
	main()