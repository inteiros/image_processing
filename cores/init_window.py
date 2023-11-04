import tkinter as tk
from tkinter import filedialog
import tkinter.font
from PIL import Image, ImageTk
import os
import filtering
import color

class Window(tk.Tk):
  
    def __init__(self):
        super().__init__()    
        self.image = None #class attribute to store the input image
        self.image_copy = None
        self.resized_image = None
        self.tkimage = None #class attribute to store the display image   
        self.create_main_window()
        self.create_control_frame()
        self.create_image_canvas()       
        self.create_menubar()  

    def create_main_window(self):
        self.title('Filtragem de Imagem')
        self.width= self.winfo_screenwidth()               
        self.height= self.winfo_screenheight()   
        #set 80% of screen width and height            
        self.geometry("%dx%d" % (self.width*.8, self.height*.8))
        #maximize the window
        self.state('zoomed')

    def create_control_frame(self):
        self.controls = tk.Frame(self)
        self.controls.pack(side=tk.TOP,expand=True,pady=(0,10))

    def clear_control_frame(self):
        # destroy all widgets from frame
        for widget in self.controls.winfo_children():
            widget.destroy()

    def create_menubar(self): 
        self.menu_bar = tk.Menu(self, tearoff="off")
        self.config(menu=self.menu_bar)
        file_menu = tk.Menu(self.menu_bar, tearoff="off")
        self.menu_bar.add_cascade(label='Arquivo', menu=file_menu)
        file_menu.add_command(label='Abrir...', command=self.load_image)
        file_menu.add_separator()
        file_menu.add_command(label='Sair', command=self.quit)
        self.create_image_menu()
        self.create_color_menu()
        self.create_filter_menu()
        
    def create_image_menu(self):
        image_menu = tk.Menu(self, tearoff="off")
        self.menu_bar.add_cascade(label='Imagem', menu=image_menu, state='disabled')
        image_menu.add_command(label='Redimensionar', command=self.create_resize_image_controls)
        image_menu.add_command(label='Escala de Cinza', command=self.create_grayscale_controls)

    def create_color_menu(self):
        color_menu = tk.Menu(self, tearoff="off")
        self.menu_bar.add_cascade(label='Cores', menu=color_menu, state='disabled')
        color_menu.add_command(label='Negativo', command=self.create_negative_controls)
        brigh_contrast_menu = tk.Menu(self, tearoff="off")
        brigh_contrast_menu.add_command(label='Transformação Logarítmica', command=self.create_log_transform_controls)
        brigh_contrast_menu.add_command(label='Correção Gamma', command=self.create_gamma_correction_controls)
        brigh_contrast_menu.add_command(label='Ajuste de Contraste', command=self.create_contrast_stretch_controls)
        brigh_contrast_menu.add_command(label='Equalização de Histograma', command=self.create_histogram_equalization_controls)
        color_menu.add_command(label='Histograma', command=self.create_histogram_controls)
        color_menu.add_cascade(label='Brilho / Contraste',menu=brigh_contrast_menu)

    def create_filter_menu(self):
        filter_menu = tk.Menu(self, tearoff="off")
        self.menu_bar.add_cascade(label='Filtros', menu=filter_menu, state='disabled')
        smooth_menu = tk.Menu(self, tearoff="off")
        smooth_menu.add_command(label='Média', command=self.create_average_filter_controls)
        smooth_menu.add_command(label='Gaussiano', command=self.create_gaussian_filter_controls)
        smooth_menu.add_command(label='Mediana', command=self.create_median_filter_controls)
        sharpen_menu = tk.Menu(self, tearoff="off")
        sharpen_menu.add_command(label='Laplaciano', command=self.create_laplacian_filter_controls)
        sharpen_menu.add_command(label='High-boost', command=self.create_highboost_filter_controls)
        noise_menu = tk.Menu(self, tearoff="off")
        noise_menu.add_command(label='Sal e Pimenta', command=self.create_salt_and_pepper_noise_controls)
        filter_menu.add_cascade(label='Suavização',menu=smooth_menu)    
        filter_menu.add_cascade(label='Aguçamento',menu=sharpen_menu)
        filter_menu.add_cascade(label='Ruído',menu=noise_menu)      

    def create_image_canvas(self):
        image_frame = tk.Frame(self)
        image_frame.pack()
        yscrollbar = tk.Scrollbar(image_frame, orient = tk.VERTICAL)
        yscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        xscrollbar = tk.Scrollbar(image_frame, orient = tk.HORIZONTAL)
        xscrollbar.pack(side = tk.BOTTOM, fill = tk.X)
        self.image_canvas = tk.Canvas(image_frame, 
                                      width = self.width*.8, 
                                      height = self.height*.75,
                                      xscrollcommand = xscrollbar.set, 
                                      yscrollcommand = yscrollbar.set)
        self.image_canvas.pack()
        yscrollbar.config(command = self.image_canvas.yview)
        xscrollbar.config(command = self.image_canvas.xview)

    def activate_menus(self):
        self.menu_bar.entryconfig('Filtros',state='active')
        self.menu_bar.entryconfig('Imagem',state='active')
        self.menu_bar.entryconfig('Cores',state='active')

    def load_image(self):
        self.clear_control_frame()
        filename = filedialog.askopenfilename(initialdir=os.getcwd())
        if filename:
            img = filtering.read_image(filename=filename)
            self.image = img.copy() #stores a copy of the image to update the canvas
            self.image_copy = img.copy() #stores a copy of the image to remove applied filters
            self.resized_image = img.copy() #stores a copy of hte image to reset the original size
            self.display_image()
            self.activate_menus()

    def display_image(self):
        img = Image.fromarray(self.image)
        self.tkimage = ImageTk.PhotoImage(img)
        width,height = img.size
        self.image_canvas.config(scrollregion=(0,0,width,height))
        self.image_canvas.create_image(0,0,anchor="nw",image=self.tkimage)

    def create_resize_image_controls(self):
        self.clear_control_frame()
        width_label = tk.Label(self.controls,text='Largura: ', height=4)
        width_label.pack(side=tk.LEFT)
        font = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
        var = tk.IntVar()
        var.set(25) #default value
        self.width_spin = tk.Spinbox(self.controls, from_=1, to=200, textvariable=var, increment=1, font=font, width=4)
        self.width_spin.pack(side=tk.LEFT)
        perc_label1 = tk.Label(self.controls,text=' %', height=4)
        perc_label1.pack(side=tk.LEFT)
        heigth_label = tk.Label(self.controls,text='Altura: ', height=4)
        heigth_label.pack(side=tk.LEFT)
        self.height_spin = tk.Spinbox(self.controls, from_=1, to=200, textvariable=var, increment=1, font=font, width=4)
        self.height_spin.pack(side=tk.LEFT)
        perc_label2 = tk.Label(self.controls,text=' %', height=4)
        perc_label2.pack(side=tk.LEFT)
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_resize_image,width=20,height=1)
        button.pack(side=tk.LEFT) 
        self.reset_button = tk.Button(self.controls, text='Reset', command=self.reset_size,width=20,height=1)      

    def create_grayscale_controls(self):
        self.clear_control_frame()
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_grayscale,width=20,height=1)
        button.pack(side=tk.LEFT) 
        self.reset_button = tk.Button(self.controls, text='Reset', command=self.reset_image,width=20,height=1)
    
    def create_negative_controls(self):
        self.clear_control_frame()
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_negative,width=20,height=1)
        button.pack(side=tk.LEFT) 
        self.reset_button = tk.Button(self.controls, text='Reset', command=self.reset_image,width=20,height=1)

    def create_log_transform_controls(self):
        self.clear_control_frame()
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_log_transform,width=20,height=1)
        button.pack(side=tk.LEFT) 
        self.reset_button = tk.Button(self.controls, text='Reset', command=self.reset_image,width=20,height=1)

    def create_gamma_correction_controls(self):
        self.clear_control_frame()
        font = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
        const_var = tk.DoubleVar()
        const_var.set(1) #default value
        gamma_label = tk.Label(self.controls,text='Constante C: ', height=4)
        gamma_label.pack(side=tk.LEFT)
        self.gamma_spin = tk.Spinbox(self.controls, from_=0.1, to=3, textvariable=const_var, increment=0.1, font=font, width=3)
        self.gamma_spin.pack(side=tk.LEFT)
        slider = tk.Scale(self.controls,from_=0.1, to=3, variable=const_var,tickinterval=1, resolution=0.1,length= 300, orient="horizontal")
        slider.pack(side=tk.LEFT)
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_gamma_correction,width=20,height=1)
        button.pack(side=tk.LEFT) 
        self.reset_button = tk.Button(self.controls, text='Reset', command=self.reset_image,width=20,height=1)

    def create_contrast_stretch_controls(self):
        self.clear_control_frame()
        font = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
        const1_var = tk.IntVar()
        const1_var.set(255) #default value
        max_label = tk.Label(self.controls,text='Maior nível de intensidade: ', height=4)
        max_label.pack(side=tk.LEFT)
        self.max_spin = tk.Spinbox(self.controls, from_=128, to=255, textvariable=const1_var, increment=1, font=font, width=3)
        self.max_spin.pack(side=tk.LEFT)
        slider1 = tk.Scale(self.controls,from_=128, to=255, variable=const1_var,tickinterval=10, resolution=1,length= 300, orient="horizontal")
        slider1.pack(side=tk.LEFT)
        const2_var = tk.IntVar()
        const2_var.set(0) #default value
        min_label = tk.Label(self.controls,text='Menor nível de intensidade: ', height=4)
        min_label.pack(side=tk.LEFT)
        self.min_spin = tk.Spinbox(self.controls, from_=0, to=127, textvariable=const2_var, increment=1, font=font, width=3)
        self.min_spin.pack(side=tk.LEFT)
        slider2 = tk.Scale(self.controls,from_=0, to=127, variable=const2_var,tickinterval=10, resolution=1,length= 300, orient="horizontal")
        slider2.pack(side=tk.LEFT)
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_contrast_stretch,width=20,height=1)
        button.pack(side=tk.LEFT) 
        self.reset_button = tk.Button(self.controls, text='Reset', command=self.reset_image,width=20,height=1)

    def create_histogram_equalization_controls(self):
        self.clear_control_frame()
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_histogram_equalization,width=20,height=1)
        button.pack(side=tk.LEFT) 
        self.reset_button = tk.Button(self.controls, text='Reset', command=self.reset_image,width=20,height=1)


    def create_histogram_controls(self):
        self.clear_control_frame()
        color.show_histogram(self.image)

    def create_average_filter_controls(self):
        self.clear_control_frame()
        font = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
        var = tk.IntVar()
        var.set(3) #default value
        kernel_label = tk.Label(self.controls,text='Tamanho do kernel: ', height=4)
        kernel_label.pack(side=tk.LEFT)
        self.kernel_spin = tk.Spinbox(self.controls, from_=3, to=31, textvariable=var, increment=2, font=font, width=2)
        self.kernel_spin.pack(side=tk.LEFT)
        slider = tk.Scale(self.controls,from_=3, to=31, variable=var,tickinterval=2, resolution=2,length= 300, orient="horizontal")
        slider.pack(side=tk.LEFT)
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_average_filter,width=20,height=1)
        button.pack(side=tk.LEFT)
        self.remove_button = tk.Button(self.controls, text='Reset', command=self.reset_image,width=20,height=1)

    def create_gaussian_filter_controls(self):
        self.clear_control_frame()
        font = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
        var = tk.IntVar()
        var.set(3) #default value
        kernel_label = tk.Label(self.controls,text='Tamanho do kernel: ', height=4)
        kernel_label.pack(side=tk.LEFT)
        self.kernel_spin = tk.Spinbox(self.controls, from_=3, to=31, textvariable=var, increment=2, font=font, width=2)
        self.kernel_spin.pack(side=tk.LEFT)
        slider = tk.Scale(self.controls,from_=3, to=31, variable=var,tickinterval=2, resolution=2,length= 300, orient="horizontal")
        slider.pack(side=tk.LEFT)
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_gaussian_filter,width=20,height=1)
        button.pack(side=tk.LEFT) 
        self.remove_button = tk.Button(self.controls, text='Remover Filtros', command=self.reset_image,width=20,height=1)

    def create_median_filter_controls(self):
        self.clear_control_frame()
        font = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
        var = tk.IntVar()
        var.set(3) #default value
        kernel_label = tk.Label(self.controls,text='Tamanho do kernel: ', height=4)
        kernel_label.pack(side=tk.LEFT)
        self.kernel_spin = tk.Spinbox(self.controls, from_=3, to=31, textvariable=var, increment=2, font=font, width=2)
        self.kernel_spin.pack(side=tk.LEFT)
        slider = tk.Scale(self.controls,from_=3, to=31, variable=var,tickinterval=2, resolution=2,length= 300, orient="horizontal")
        slider.pack(side=tk.LEFT)
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_median_filter,width=20,height=1)
        button.pack(side=tk.LEFT) 
        self.remove_button = tk.Button(self.controls, text='Remover Filtros', command=self.reset_image,width=20,height=1)

    def create_salt_and_pepper_noise_controls(self):
        self.clear_control_frame()
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_salt_and_pepper_noise,width=20,height=1)
        button.pack(side=tk.LEFT) 
        self.remove_button = tk.Button(self.controls, text='Remover Filtros', command=self.reset_image,width=20,height=1)

    def create_highboost_filter_controls(self):
        self.clear_control_frame()
        font = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
        var = tk.DoubleVar()
        var.set(1) #default value
        factor_label = tk.Label(self.controls,text='Fator de amplificação: ', height=4)
        factor_label.pack(side=tk.LEFT)
        self.boost_spin = tk.Spinbox(self.controls, from_=1, to=3, textvariable=var, increment=0.1, font=font, width=3)
        self.boost_spin.pack(side=tk.LEFT)
        slider = tk.Scale(self.controls,from_=1, to=3, variable=var,tickinterval=1, resolution=0.1,length= 300, orient="horizontal")
        slider.pack(side=tk.LEFT)
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_highboost_filter,width=20,height=1)
        button.pack(side=tk.LEFT)
        self.remove_button = tk.Button(self.controls, text='Remover Filtros', command=self.reset_image,width=20,height=1) 

    def create_laplacian_filter_controls(self):
        self.clear_control_frame()
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_laplacian_filter,width=20,height=1)
        button.pack(side=tk.LEFT) 
        self.remove_button = tk.Button(self.controls, text='Remover Filtros', command=self.reset_image,width=20,height=1)

    def reset_image(self):
        self.image = self.resized_image.copy()
        self.display_image()    
          
    def reset_size(self):
        self.image = self.image_copy.copy()
        self.resized_image = self.image_copy.copy()
        self.display_image()

    def apply_resize_image(self):
        width = int(self.width_spin.get())
        height = int(self.height_spin.get())
        self.image = filtering.resize_image(self.image,width,height)
        self.resized_image = self.image.copy() #stores a copy of the resized image for reset option
        self.reset_button.pack(side=tk.LEFT,padx=5)
        self.display_image()

    def apply_grayscale(self):
        self.image = color.grayscale_image(self.image)
        self.reset_button.pack(side=tk.LEFT,padx=5)
        self.display_image()

    def apply_negative(self):
        self.image = color.negative_image(self.image)
        self.reset_button.pack(side=tk.LEFT,padx=5)
        self.display_image()

    def apply_log_transform(self):
        self.image = color.log_transform(self.image)
        self.reset_button.pack(side=tk.LEFT,padx=5)
        self.display_image() 

    def apply_gamma_correction(self):
        gamma = float(self.gamma_spin.get())
        self.image = color.gamma_correction(self.image,gamma)
        self.reset_button.pack(side=tk.LEFT,padx=5)
        self.display_image() 

    def apply_contrast_stretch(self):
        max = int(self.max_spin.get())
        min = int(self.min_spin.get())
        self.image = color.contrast_stretch(self.image,max,min)
        self.reset_button.pack(side=tk.LEFT,padx=5)
        self.display_image() 
    
    def apply_histogram_equalization(self):
        self.image = color.histogram_equalization(self.image)
        self.reset_button.pack(side=tk.LEFT,padx=5)
        self.display_image()

    def apply_average_filter(self):
        kernel_size = int(self.kernel_spin.get())
        self.image = filtering.average_filter(self.image,kernel_size)
        self.remove_button.pack(side=tk.LEFT,padx=5)
        self.display_image()

    def apply_gaussian_filter(self):
        kernel_size = int(self.kernel_spin.get())
        self.image = filtering.gaussian_filter(self.image,kernel_size)
        self.remove_button.pack(side=tk.LEFT,padx=5)
        self.display_image()  

    def apply_median_filter(self):
        kernel_size = int(self.kernel_spin.get())
        self.image = filtering.median_filter(self.image,kernel_size)
        self.remove_button.pack(side=tk.LEFT,padx=5)
        self.display_image()     

    def apply_salt_and_pepper_noise(self):
        self.image = filtering.salt_and_pepper_noise(self.image)
        self.remove_button.pack(side=tk.LEFT,padx=5)
        self.display_image()    

    def apply_highboost_filter(self):
        boost = float(self.boost_spin.get())
        self.image = filtering.highboost_filter(self.image,boost)
        self.remove_button.pack(side=tk.LEFT,padx=5)
        self.display_image()

    def apply_laplacian_filter(self):
        self.image = filtering.laplacian_filter(self.image)
        self.remove_button.pack(side=tk.LEFT,padx=5)
        self.display_image()             

if __name__== '__main__':
    app=Window()
    app.mainloop()