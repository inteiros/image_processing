import tkinter as tk
from tkinter import filedialog
import tkinter.font
from PIL import Image, ImageTk
import numpy as np
from matplotlib import pyplot as plt
import os
import colorsys
import filtering
import color
import segmentation


class Window(tk.Tk):
  
    def __init__(self):
        super().__init__() 
        self.image = None #class attribute to store the input image
        self.image_copy = None
        self.resized_image = None
        self.tkimage = None #class attribute to store the display image
        self.rgb_color = (255,0,0) #attribute to store a RGB color (default=red)
        self.create_main_window()
        self.create_control_frame()
        self.create_image_canvas()       
        self.create_menubar()  
        #set a protocol to close all windows when main window is closed
        self.protocol('WM_DELETE_WINDOW', self.close_all_windows)

    def close_all_windows(self):
        plt.close('all')
        self.destroy()    
    
    def create_main_window(self):
        self.title('Filtragem de Imagem')
        self.width= self.winfo_screenwidth()               
        self.height= self.winfo_screenheight()   
        #set 80% of screen width and height            
        self.geometry("%dx%d" % (self.width*.8, self.height*.8))
        #maximize the window
        #self.state('zoomed')

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
        file_menu.add_command(label='Sair', command=self.close_all_windows)
        self.create_image_menu()
        self.create_color_menu()
        self.create_filter_menu()
        self.create_segmentation_menu()
        
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

    def create_segmentation_menu(self):
        segmentation_menu = tk.Menu(self, tearoff="off")
        self.menu_bar.add_cascade(label='Segmentação', menu=segmentation_menu, state='disabled')
        segmentation_menu.add_command(label='Cor', command=self.create_color_segmentation_controls)
        segmentation_menu.add_command(label='Limiarização', command=self.create_threshold_controls)      
        segmentation_menu.add_command(label='Limiarização Otsu', command=self.create_otsu_threshold_controls)      
        segmentation_menu.add_command(label='Detecção de bordas (Canny)', command=self.create_canny_controls)      

    def create_image_canvas(self):
        image_frame = tk.Frame(self)
        image_frame.pack()
        yscrollbar = tk.Scrollbar(image_frame, orient = tk.VERTICAL)
        yscrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        xscrollbar = tk.Scrollbar(image_frame, orient = tk.HORIZONTAL)
        xscrollbar.pack(side = tk.BOTTOM, fill = tk.X)
        self.image_canvas = tk.Canvas(image_frame, 
                                      width = self.width, 
                                      height = self.height,
                                      xscrollcommand = xscrollbar.set, 
                                      yscrollcommand = yscrollbar.set)
        self.image_canvas.bind("<Button-1>", self.get_color)
        self.image_canvas.pack()
        yscrollbar.config(command = self.image_canvas.yview)
        xscrollbar.config(command = self.image_canvas.xview)

    def activate_menus(self):
        self.menu_bar.entryconfig('Filtros',state='active')
        self.menu_bar.entryconfig('Imagem',state='active')
        self.menu_bar.entryconfig('Cores',state='active')
        self.menu_bar.entryconfig('Segmentação',state='active')

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

    def get_color(self, event):
        if (np.ndim(self.image) > 2): #if more than 2 dimensions then it is a color image
            x,y = event.x,event.y
            #print(f'clicked at: {x,y}')
            h,w = self.image.shape[:2]
            #print(w,h)
            if(x < w and y < h):
                img = Image.fromarray(self.image)
                self.rgb_color = img.getpixel((x,y))
                self.update_segmentation_controls()

    def update_segmentation_controls(self):
        r,g,b = self.rgb_color[0],self.rgb_color[1],self.rgb_color[2]
        h,s,v = self.convert_rgb2hsv_values(r,g,b)
        h_lower = max(0, min(h-10, 179)) #clamp the result of the subtraction between 0 and 179
        h_upper = max(0, min(h+10, 179)) #clamp the result of the sum between 0 and 179
        try: #if the variables below exists
            self.low_h.set(h_lower)
            self.high_h.set(h_upper)
        except AttributeError: #otherwise do nothing
            None

    def convert_rgb2hsv_values(self,r,g,b):
        #in colorsys the coordinates are all between 0 and 1.
        r,g,b = r/255,g/255,b/255
        h,s,v = colorsys.rgb_to_hsv(r,g,b)
        #OpenCV uses HSV ranges between (0-179, 0-255, 0-255)
        h,s,v = int(h*179),int(s*255),int(v*255)
        #print(h,s,v)
        return h,s,v
    
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
    
    def create_color_segmentation_controls(self):
        self.clear_control_frame()
        font = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
        low_label = tk.Label(self.controls,text='Menor nível de: H ', height=4)
        low_label.pack(side=tk.LEFT)
        self.low_h = tk.IntVar()
        self.low_s = tk.IntVar()
        self.low_v = tk.IntVar()
        self.low_h.set(160) #default value
        self.low_s.set(50) #default value
        self.low_v.set(50) #default value
        low_hue_spin = tk.Spinbox(self.controls, from_=0, to=179, textvariable=self.low_h, increment=1, font=font, width=3)
        low_hue_spin.pack(side=tk.LEFT)
        low_label0 = tk.Label(self.controls,text='S ', height=4)
        low_label0.pack(side=tk.LEFT)
        low_saturation_spin = tk.Spinbox(self.controls, from_=0, to=255, textvariable=self.low_s, increment=1, font=font, width=3)
        low_saturation_spin.pack(side=tk.LEFT)
        low_label1 = tk.Label(self.controls,text='V ', height=4)
        low_label1.pack(side=tk.LEFT)
        low_value_spin = tk.Spinbox(self.controls, from_=0, to=255, textvariable=self.low_v, increment=1, font=font, width=3)
        low_value_spin.pack(side=tk.LEFT)
        high_label = tk.Label(self.controls,text='Maior nível de: H ', height=4)
        high_label.pack(side=tk.LEFT)
        self.high_h = tk.IntVar()
        self.high_s = tk.IntVar()
        self.high_v = tk.IntVar()
        self.high_h.set(179) #default value
        self.high_s.set(255) #default value
        self.high_v.set(255) #default value
        high_hue_spin = tk.Spinbox(self.controls, from_=0, to=179, textvariable=self.high_h, increment=1, font=font, width=3)
        high_hue_spin.pack(side=tk.LEFT)
        high_label0 = tk.Label(self.controls,text='S ', height=4)
        high_label0.pack(side=tk.LEFT)
        high_saturation_spin = tk.Spinbox(self.controls, from_=0, to=255, textvariable=self.high_s, increment=1, font=font, width=3)
        high_saturation_spin.pack(side=tk.LEFT)
        high_label1 = tk.Label(self.controls,text='V ', height=4)
        high_label1.pack(side=tk.LEFT)
        high_value_spin = tk.Spinbox(self.controls, from_=0, to=255, textvariable=self.high_v, increment=1, font=font, width=3)
        high_value_spin.pack(side=tk.LEFT)
        button = tk.Button(self.controls, text='Segmentar', command=self.apply_color_segmentation,width=20,height=1)
        button.pack(side=tk.LEFT) 

    def create_threshold_controls(self):
        self.clear_control_frame()
        font = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
        self.threshold = tk.IntVar()
        self.threshold.set(127) #default value
        factor_label = tk.Label(self.controls,text='Limiar: ', height=4)
        factor_label.pack(side=tk.LEFT)
        thresh_spin = tk.Spinbox(self.controls, from_=0, to=255, textvariable=self.threshold, increment=1, font=font, width=3)
        thresh_spin.pack(side=tk.LEFT)
        slider = tk.Scale(self.controls,from_=0, to=255, variable=self.threshold,tickinterval=20, resolution=1,length= 300, orient="horizontal")
        slider.pack(side=tk.LEFT)
        button = tk.Button(self.controls, text='Segmentar', command=self.apply_threshold,width=20,height=1)
        button.pack(side=tk.LEFT)

    def create_otsu_threshold_controls(self):
        self.clear_control_frame()
        button = tk.Button(self.controls, text='Aplicar', command=self.apply_otsu_threshold,width=20,height=1)
        button.pack(side=tk.LEFT)      

    def create_canny_controls(self):
        self.clear_control_frame()
        font = tkinter.font.Font(family='Helvetica', size=12, weight='bold')
        self.lower_thresh_rate = tk.DoubleVar()
        self.lower_thresh_rate.set(0.5) #default value
        thresh_label = tk.Label(self.controls,text='Percentual do Limiar Inferior em relação ao Limiar Superior: ', height=4)
        thresh_label.pack(side=tk.LEFT)
        thresh_spin = tk.Spinbox(self.controls, from_=0, to=1, textvariable=self.lower_thresh_rate, increment=0.1, font=font, width=3)
        thresh_spin.pack(side=tk.LEFT)
        slider = tk.Scale(self.controls,from_=0, to=1, variable=self.lower_thresh_rate,tickinterval=0.1, resolution=0.1,length= 300, orient="horizontal")
        slider.pack(side=tk.LEFT)
        button = tk.Button(self.controls, text='Segmentar', command=self.apply_canny,width=20,height=1)
        button.pack(side=tk.LEFT)

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

    def apply_color_segmentation(self):
        if (np.ndim(self.image) > 2): #if more than 2 dimensions then it is a color image
            lower_range = np.array([self.low_h.get(), self.low_s.get(), self.low_v.get()])
            upper_range = np.array([self.high_h.get(), self.high_s.get(), self.high_v.get()])
            t1,m,t2,r = segmentation.color_segmentation(self.image,lower_range,upper_range)
            self.create_update_pyplot_window(t1,m,t2,r)      
        else:
            tkinter.messagebox.showinfo(title='', message='A imagem deve ser colorida!')

    def apply_threshold(self):
        t1,m,t2,r = segmentation.threshold(self.image,self.threshold.get())
        self.create_update_pyplot_window(t1,m,t2,r)   

    def apply_otsu_threshold(self):
        t1,m,t2,r = segmentation.otsu_threshold(self.image)
        self.create_update_pyplot_window(t1,m,t2,r)

    def apply_canny(self):
        t1,m,t2,r = segmentation.canny(self.image,self.lower_thresh_rate.get())
        self.create_update_pyplot_window(t1,m,t2,r)

    def create_update_pyplot_window(self,title1, mask, title2, result):
        plt.close('all')
        plt.figure(figsize=[9,4]) #pyplot window to show segmentation result
        plt.subplot(121)
        plt.title(title1,fontdict={'fontsize': 14})
        plt.imshow(mask, cmap='gray')
        plt.axis('off')
        plt.subplot(122)
        plt.title(title2,fontdict={'fontsize': 14})
        if (np.ndim(result) > 2): #entao a imagem possui 3 canais (colorida)    
            plt.imshow(result)
        else:
            plt.imshow(result, cmap='gray')
        plt.axis('off')
        plt.show()              

if __name__== '__main__':
    app=Window()
    app.mainloop()