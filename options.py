try:
    import Tkinter as tkinter
except ImportError:
    import tkinter

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import pygrid_support
import matplotlib as mpl
from collections import OrderedDict



class GeneralOptionBox(object):

    root = None

    def __init__(self, config):
        """
        Create the CoastOptionBox
        """        
        self.config=config
        
        tki = tkinter
        self.top = tki.Toplevel(NeiOptionBox.root)
        self.top.geometry("400x500+650+250")
        self.top.title("General Options")
        self.top.configure(highlightcolor="black")

        self.frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        self.frm.pack(fill='both', expand=True)

        rh = 0.055
        rw = 0.85
        rw2 = 0.4 
        rw3 = 0.33       
        sh = 0.06
        ry = 0.01
                    
        self.smode=tki.StringVar()

        
        label(self.frm,0.075,ry,rh,rw,'''Default Axis Selection''')
        ry += sh
        rbutton(self.frm,0.05,ry,rh,rw3,'''-180,180''',
                self.smode, 'NEGE')
        rbutton(self.frm,0.35,ry,rh,rw3,'''0,360''',
                self.smode, 'POSE')
        rbutton(self.frm,0.65,ry,rh,rw3,'''Custom''',
                self.smode, 'CUSTOM')
        self.smode.set(self.config['gen']['axis'])
                
        ry += sh        
        ry += sh        
        label(self.frm,0.075,ry,rh,rw,'''Define Axis For Custom''')
        
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Lon. Min.''')
        self.e1=entry(self.frm,0.5,ry,rh,rw2,self.config['gen']['clonmin'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Lon. Max.''')
        self.e2=entry(self.frm,0.5,ry,rh,rw2,self.config['gen']['clonmax'])

        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Lat. Min.''')
        self.e3=entry(self.frm,0.5,ry,rh,rw2,self.config['gen']['clatmin'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Lat. Max.''')
        self.e4=entry(self.frm,0.5,ry,rh,rw2,self.config['gen']['clatmax'])
               
       

        ################################################################
        #Save close apply buttons
        ################################################################
        self.b_save=button(self.frm,.01+sh*0.1,.925,rh,rw3*.95,'''Save''',self.saveConfig)
        self.b_cancel=button(self.frm,.01+rw3*.95+sh*.25,.925,rh,rw3*.95,'''Close''',self.top.destroy)
        self.b_submit=button(self.frm,.01+rw3*2*.95+sh*.4,.925,rh,rw3*.95,'''Apply''',self.setConfig)


    def setConfig(self):
        
        e1=self.e1.get() 
        if self.config['gen']['clonmin']!=e1:
            self.config['gen']['clonmin']=e1
        e2=self.e2.get() 
        if self.config['gen']['clonmax']!=e2:
            self.config['gen']['clonmax']=e2
        e3=self.e3.get() 
        if self.config['gen']['clatmin']!=e3:
            self.config['gen']['clatmin']=e3
        e4=self.e4.get() 
        if self.config['gen']['clatmax']!=e4:
            self.config['gen']['clatnmax']=e4


        self.config['gen']['axis']=self.smode.get()
        atype=self.smode.get()
        
        if atype=='NEGE':
            self.config['gen']['dlonmin']=-180  
            self.config['gen']['dlonmax']=180  
            self.config['gen']['dlatmin']=-90  
            self.config['gen']['dlatmax']=90 
        if atype=='POSE':
            self.config['gen']['dlonmin']=0  
            self.config['gen']['dlonmax']=360  
            self.config['gen']['dlatmin']=-90  
            self.config['gen']['dlatmax']=90 
        if atype=='CUSTOM':
            self.config['gen']['dlonmin']=self.config['gen']['clonmin'] 
            self.config['gen']['dlonmax']=self.config['gen']['clonmax']  
            self.config['gen']['dlatmin']=self.config['gen']['clatmin']  
            self.config['gen']['dlatmax']=self.config['gen']['clatmax']  

    
    def saveConfig(self):
        '''Set and save the config file'''  
        
        self.setConfig()        
        saveConfigFile(self.config)   


class CoastOptionBox(object):

    root = None

    def __init__(self, config):
        """
        Create the CoastOptionBox
        """        
        self.config=config
        
        tki = tkinter
        self.top = tki.Toplevel(NeiOptionBox.root)
        self.top.geometry("400x500+650+250")
        self.top.title("Coastline Plot Options")
        self.top.configure(highlightcolor="black")

        self.frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        self.frm.pack(fill='both', expand=True)

        rh = 0.055
        rw = 0.85
        rw2 = 0.4 
        rw3 = 0.33       
        sh = 0.06
        ry = 0.01
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Fill''')
        self.fillMenuVar = tki.StringVar(self.root)
        self.fillChoices={'True','False'}
        self.fillMenuVar.set(self.config['coast']['fill'])
        self.fillMenu = tki.OptionMenu(self.frm,self.fillMenuVar,*self.fillChoices)
        self.fillMenu.place(relx=0.50, rely=ry, relheight=rh, relwidth=rw2)
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Facecolor''')
        self.e1=entry(self.frm,0.5,ry,rh,rw2,self.config['coast']['facecolor'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Edgecolor''')
        self.e2=entry(self.frm,0.5,ry,rh,rw2,self.config['coast']['edgecolor'])

        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Linewidth''')
        self.e3=entry(self.frm,0.5,ry,rh,rw2,self.config['coast']['linewidth'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Linestyle''')
        self.e4=entry(self.frm,0.5,ry,rh,rw2,self.config['coast']['linestyle'])
               
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Zorder''')
        self.e5=entry(self.frm,0.5,ry,rh,rw2,self.config['coast']['zorder'])
        

        ################################################################
        #Save close apply buttons
        ################################################################
        self.b_save=button(self.frm,.01+sh*0.1,.925,rh,rw3*.95,'''Save''',self.saveConfig)
        self.b_cancel=button(self.frm,.01+rw3*.95+sh*.25,.925,rh,rw3*.95,'''Close''',self.top.destroy)
        self.b_submit=button(self.frm,.01+rw3*2*.95+sh*.4,.925,rh,rw3*.95,'''Apply''',self.setConfig)



    def setConfig(self):
        replot=False  
              
        e0=self.fillMenuVar.get() 
        if self.config['coast']['fill']!=e0:
            self.config['coast']['fill']=e0
            replot=True
        e1=self.e1.get() 
        if self.config['coast']['facecolor']!=e1:
            self.config['coast']['facecolor']=e1
            replot=True
        e2=self.e2.get() 
        if self.config['coast']['edgecolor']!=e2:
            self.config['coast']['edgecolor']=e2
            replot=True
        e3=self.e3.get() 
        if self.config['coast']['linewidth']!=e3:
            self.config['coast']['linewidth']=e3
            replot=True
        e4=self.e4.get() 
        if self.config['coast']['linestyle']!=e4:
            self.config['coast']['linestyle']=e4
            replot=True
        e5=self.e5.get() 
        if self.config['coast']['zorder']!=e5:
            self.config['coast']['zorder']=e5
            replot=True
        
        if replot:
            pygrid_support.TODO 
    
    def saveConfig(self):
        '''Set and save the config file'''  
        
        self.setConfig()        
        saveConfigFile(self.config)   
        
        
class SegOptionBox(object):

    root = None

    def __init__(self, config):
        """
        Create the NeiOptionBox
        """        
        self.config=config
        
        tki = tkinter
        self.top = tki.Toplevel(NeiOptionBox.root)
        self.top.geometry("400x500+650+250")
        self.top.title("Seg Plot Options")
        self.top.configure(highlightcolor="black")

        self.frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        self.frm.pack(fill='both', expand=True)

        rh = 0.055
        rw = 0.85
        rw2 = 0.4 
        rw3 = 0.33       
        sh = 0.06
        ry = 0.01
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Markersize''')
        self.e1=entry(self.frm,0.5,ry,rh,rw2,self.config['seg']['markersize'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Markercolor''')
        self.e2=entry(self.frm,0.5,ry,rh,rw2,self.config['seg']['markercolor'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Linecolor''')
        self.e3=entry(self.frm,0.5,ry,rh,rw2,self.config['seg']['linecolor'])

        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Linewidth''')
        self.e4=entry(self.frm,0.5,ry,rh,rw2,self.config['seg']['linewidth'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''LineDotSize''')
        self.e5=entry(self.frm,0.5,ry,rh,rw2,self.config['seg']['linedotsize'])
               
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Zorder''')
        self.e6=entry(self.frm,0.5,ry,rh,rw2,self.config['seg']['zorder'])


        ################################################################
        #Save close apply buttons
        ################################################################
        self.b_save=button(self.frm,.01+sh*0.1,.925,rh,rw3*.95,'''Save''',self.saveConfig)
        self.b_cancel=button(self.frm,.01+rw3*.95+sh*.25,.925,rh,rw3*.95,'''Close''',self.top.destroy)
        self.b_submit=button(self.frm,.01+rw3*2*.95+sh*.4,.925,rh,rw3*.95,'''Apply''',self.setConfig)


    def setConfig(self):
        replot=False  
              
        e1=self.e1.get() 
        if self.config['seg']['markersize']!=e1:
            self.config['seg']['markersize']=e1
            replot=True
        e2=self.e2.get() 
        if self.config['seg']['markercolor']!=e2:
            self.config['seg']['markercolor']=e2
            replot=True
        e3=self.e3.get() 
        if self.config['seg']['linecolor']!=e3:
            self.config['seg']['linecolor']=e3
            replot=True
        e4=self.e4.get() 
        if self.config['seg']['linewidth']!=e4:
            self.config['seg']['linewidth']=e4
            replot=True
        e5=self.e5.get() 
        if self.config['seg']['linedotsize']!=e5:
            self.config['seg']['linedotsize']=e5
            replot=True
        e6=self.e6.get() 
        if self.config['seg']['zorder']!=e6:
            self.config['seg']['zorder']=e6
            replot=True
        
        if replot:
            pygrid_support._plot_segfile() 
    
    def saveConfig(self):
        '''Set and save the config file'''  
        
        self.setConfig()        
        saveConfigFile(self.config)   

class NeiOptionBox(object):

    root = None

    def __init__(self, config):
        """
        Create the NeiOptionBox
        """        
        self.config=config
        
        tki = tkinter
        self.top = tki.Toplevel(NeiOptionBox.root)
        self.top.geometry("400x500+650+250")
        self.top.title("Nei Plot Options")
        self.top.configure(highlightcolor="black")

        self.frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        self.frm.pack(fill='both', expand=True)

        rh = 0.055
        rw = 0.85
        rw2 = 0.4 
        rw3 = 0.33       
        sh = 0.06
        ry = 0.01
        
        label(self.frm,0.650,ry,rh,rw3,'''Override''')

        ry += sh
        label(self.frm,0.0,ry,rh,rw3,'''Colormap''')

        self.CMMenuVar = tki.StringVar(self.root)
        self.CMChoices={'viridis','jet','seismic'}
        self.CMMenuVar.set(self.config['nei']['colormap'])
        self.CMMenu = tki.OptionMenu(self.frm,self.CMMenuVar,*self.CMChoices)
        self.CMMenu.place(relx=0.2850, rely=ry, relheight=rh, relwidth=rw3)
        
        self.e1=entry(self.frm,0.65,ry,rh,rw3,'')
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''CMZorder''')
        self.e2=entry(self.frm,0.5,ry,rh,rw2,self.config['nei']['cm_zorder'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Linewidth''')
        self.e3=entry(self.frm,0.5,ry,rh,rw2,self.config['nei']['linewidth'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Linecolor''')
        self.e4=entry(self.frm,0.5,ry,rh,rw2,self.config['nei']['linecolor'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Zorder''')
        self.e5=entry(self.frm,0.5,ry,rh,rw2,self.config['nei']['zorder'])


        


        ################################################################
        #Save close apply buttons
        ################################################################
        self.b_save=button(self.frm,.01+sh*0.1,.925,rh,rw3*.95,'''Save''',self.saveConfig)
        self.b_cancel=button(self.frm,.01+rw3*.95+sh*.25,.925,rh,rw3*.95,'''Close''',self.top.destroy)
        self.b_submit=button(self.frm,.01+rw3*2*.95+sh*.4,.925,rh,rw3*.95,'''Apply''',self.setConfig)


    def setConfig(self):
        replot=False
        replotc=False
        
        e1=self.e1.get() 
        if e1 != '' and self.config['nei']['colormap']!=e1:
            try:
                mpl.cm.get_cmap(e1)            
                self.config['nei']['colormap']=e1
                replotc=True
            except ValueError:
                print('Invalid Colormap')
        elif self.config['nei']['colormap']!=self.CMMenuVar.get():
            self.config['nei']['colormap']=self.CMMenuVar.get()
            replotc=True
            
        e2=self.e2.get() 
        if self.config['nei']['cm_zorder']!=e2:
            self.config['nei']['cm_zorder']=e2
            replot=True            
        e3=self.e3.get() 
        if self.config['nei']['linewidth']!=e3:
            self.config['nei']['linewidth']=e3
            replot=True
        e4=self.e4.get() 
        if self.config['nei']['linecolor']!=e4:
            self.config['nei']['linecolor']=e4
            replot=True
        e5=self.e5.get() 
        if self.config['nei']['zorder']!=e5:
            self.config['nei']['zorder']=e5
            replot=True
        
        if replotc:
            pygrid_support._plot_neifilecolor()
        if replot:
            pygrid_support.TODO 
    
    def saveConfig(self):
        '''Set and save the config file'''  
        
        self.setConfig()        
        saveConfigFile(self.config)     
        
class NodOptionBox(object):

    root = None

    def __init__(self, config):
        """
        Create the NeiOptionBox
        """        
        self.config=config
        
        tki = tkinter
        self.top = tki.Toplevel(NeiOptionBox.root)
        self.top.geometry("400x500+650+250")
        self.top.title("Nod Plot Options")
        self.top.configure(highlightcolor="black")

        self.frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        self.frm.pack(fill='both', expand=True)

        rh = 0.055
        rw = 0.85
        rw2 = 0.4 
        rw3 = 0.33       
        sh = 0.06
        ry = 0.01
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Markersize''')
        self.e1=entry(self.frm,0.5,ry,rh,rw2,self.config['nod']['markersize'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Facecolor''')
        self.e2=entry(self.frm,0.5,ry,rh,rw2,self.config['nod']['facecolor'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Edgecolor''')
        self.e3=entry(self.frm,0.5,ry,rh,rw2,self.config['nod']['edgecolor'])
               
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Zorder''')
        self.e4=entry(self.frm,0.5,ry,rh,rw2,self.config['nod']['zorder'])


        ################################################################
        #Save close apply buttons
        ################################################################
        self.b_save=button(self.frm,.01+sh*0.1,.925,rh,rw3*.95,'''Save''',self.saveConfig)
        self.b_cancel=button(self.frm,.01+rw3*.95+sh*.25,.925,rh,rw3*.95,'''Close''',self.top.destroy)
        self.b_submit=button(self.frm,.01+rw3*2*.95+sh*.4,.925,rh,rw3*.95,'''Apply''',self.setConfig)


    def setConfig(self):
        replot=False  
              
        e1=self.e1.get() 
        if self.config['nod']['markersize']!=e1:
            self.config['nod']['markersize']=e1
            replot=True
        e2=self.e2.get() 
        if self.config['nod']['facecolor']!=e2:
            self.config['nod']['facecolor']=e2
            replot=True
        e3=self.e3.get() 
        if self.config['nod']['edgecolor']!=e3:
            self.config['nod']['edgecolor']=e3
            replot=True
        e4=self.e4.get() 
        if self.config['nod']['zorder']!=e4:
            self.config['nod']['zorder']=e4
            replot=True
        
        if replot:
            pygrid_support._plot_nodfile()  
    
    def saveConfig(self):
        '''Set and save the config file'''  
        
        self.setConfig()        
        saveConfigFile(self.config)   
        
        
class llzOptionBox(object):

    root = None

    def __init__(self, config):
        """
        Create the NeiOptionBox
        """        
        self.config=config
        
        tki = tkinter
        self.top = tki.Toplevel(NeiOptionBox.root)
        self.top.geometry("400x500+650+250")
        self.top.title("llz Plot Options")
        self.top.configure(highlightcolor="black")

        self.frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        self.frm.pack(fill='both', expand=True)

        rh = 0.055
        rw = 0.85
        rw2 = 0.4 
        rw3 = 0.33       
        sh = 0.06
        ry = 0.01
                
        label(self.frm,0.650,ry,rh,rw3,'''Override''')

        ry += sh
        label(self.frm,0.0,ry,rh,rw3,'''Colormap''')

        self.CMMenuVar = tki.StringVar(self.root)
        self.CMChoices={'viridis','jet','seismic'}
        self.CMMenuVar.set(self.config['llz']['colormap'])
        self.CMMenu = tki.OptionMenu(self.frm,self.CMMenuVar,*self.CMChoices)
        self.CMMenu.place(relx=0.2850, rely=ry, relheight=rh, relwidth=rw3)
        
        self.e0=entry(self.frm,0.65,ry,rh,rw3,'')
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Markersize''')
        self.e1=entry(self.frm,0.5,ry,rh,rw2,self.config['llz']['markersize'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Edgecolor''')
        self.e3=entry(self.frm,0.5,ry,rh,rw2,self.config['llz']['edgecolor'])
               
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Zorder''')
        self.e4=entry(self.frm,0.5,ry,rh,rw2,self.config['llz']['zorder'])


        ################################################################
        #Save close apply buttons
        ################################################################
        self.b_save=button(self.frm,.01+sh*0.1,.925,rh,rw3*.95,'''Save''',self.saveConfig)
        self.b_cancel=button(self.frm,.01+rw3*.95+sh*.25,.925,rh,rw3*.95,'''Close''',self.top.destroy)
        self.b_submit=button(self.frm,.01+rw3*2*.95+sh*.4,.925,rh,rw3*.95,'''Apply''',self.setConfig)


    def setConfig(self):
        replot=False
        
        e0=self.e0.get() 
        if e0 != '' and self.config['llz']['colormap']!=e0:
            try:
                mpl.cm.get_cmap(e1)            
                self.config['llz']['colormap']=e0
                replot=True
            except ValueError:
                print('Invalid Colormap')
        elif self.config['llz']['colormap']!=self.CMMenuVar.get():
            self.config['llz']['colormap']=self.CMMenuVar.get()
            replot=True
        
        e1=self.e1.get() 
        if self.config['llz']['markersize']!=e1:
            self.config['llz']['markersize']=e1
            replot=True
        e3=self.e3.get() 
        if self.config['llz']['edgecolor']!=e3:
            self.config['llz']['edgecolor']=e3
            replot=True
        e4=self.e4.get() 
        if self.config['llz']['zorder']!=e4:
            self.config['llz']['zorder']=e4
            replot=True
        
        if replot:
            pygrid_support._plot_llzfile()  
    
    def saveConfig(self):
        '''Set and save the config file'''  
        
        self.setConfig()        
        saveConfigFile(self.config)   


class fvcomOptionBox(object):

    root = None

    def __init__(self, config):
        """
        Create the fvcomOptionBox
        """        
        self.config=config
        
        tki = tkinter
        self.top = tki.Toplevel(NeiOptionBox.root)
        self.top.geometry("400x500+650+250")
        self.top.title("FVCOM Plot Options")
        self.top.configure(highlightcolor="black")

        self.frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        self.frm.pack(fill='both', expand=True)

        rh = 0.055
        rw = 0.85
        rw2 = 0.4 
        rw3 = 0.33       
        sh = 0.06
        ry = 0.01
        
        label(self.frm,0.650,ry,rh,rw3,'''Override''')

        ry += sh
        label(self.frm,0.0,ry,rh,rw3,'''Colormap''')

        self.CMMenuVar = tki.StringVar(self.root)
        self.CMChoices={'viridis','jet','seismic'}
        self.CMMenuVar.set(self.config['fvcom']['colormap'])
        self.CMMenu = tki.OptionMenu(self.frm,self.CMMenuVar,*self.CMChoices)
        self.CMMenu.place(relx=0.2850, rely=ry, relheight=rh, relwidth=rw3)
        
        self.e1=entry(self.frm,0.65,ry,rh,rw3,'')
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Zorder''')
        self.e2=entry(self.frm,0.5,ry,rh,rw2,self.config['fvcom']['zorder'])
        
        ry += sh
        label(self.frm,0.0,ry,rh,rw2,'''Shift lon (-360)''')

        self.SMenuVar = tki.StringVar(self.root)
        self.SChoices={'True','False'}
        self.SMenuVar.set(self.config['fvcom']['shiftlonTF'])
        self.SMenu = tki.OptionMenu(self.frm,self.SMenuVar,*self.SChoices)
        self.SMenu.place(relx=0.50, rely=ry, relheight=rh, relwidth=rw2)
        # ry += sh
        # label(self.frm,0.0,ry,rh,rw2,'''Linewidth''')
        # self.e3=entry(self.frm,0.5,ry,rh,rw2,self.config['fvcom']['linewidth'])
        
        # ry += sh
        # label(self.frm,0.0,ry,rh,rw2,'''Linecolor''')
        # self.e4=entry(self.frm,0.5,ry,rh,rw2,self.config['fvcom']['linecolor'])
        
        # ry += sh
        # label(self.frm,0.0,ry,rh,rw2,'''Zorder''')
        # self.e5=entry(self.frm,0.5,ry,rh,rw2,self.config['fvcom']['zorder'])


        


        ################################################################
        #Save close apply buttons
        ################################################################
        self.b_save=button(self.frm,.01+sh*0.1,.925,rh,rw3*.95,'''Save''',self.saveConfig)
        self.b_cancel=button(self.frm,.01+rw3*.95+sh*.25,.925,rh,rw3*.95,'''Close''',self.top.destroy)
        self.b_submit=button(self.frm,.01+rw3*2*.95+sh*.4,.925,rh,rw3*.95,'''Apply''',self.setConfig)


    def setConfig(self):
        replot=False
        
        e1=self.e1.get() 
        if e1 != '' and self.config['fvcom']['colormap']!=e1:
            try:
                mpl.cm.get_cmap(e1)            
                self.config['fvcom']['colormap']=e1
                replot=True
            except ValueError:
                print('Invalid Colormap')
        elif self.config['fvcom']['colormap']!=self.CMMenuVar.get():
            self.config['fvcom']['colormap']=self.CMMenuVar.get()
            replot=True
                       
        e2=self.e2.get() 
        if self.config['fvcom']['zorder']!=e2:
            self.config['fvcom']['zorder']=e2
            replot=True    
                    
        e3=self.SMenuVar.get() 
        if self.config['fvcom']['shiftlonTF']!=e3:
            self.config['fvcom']['shiftlonTF']=e3
            replot=True
        # e4=self.e4.get() 
        # if self.config['fvcom']['linecolor']!=e4:
            # self.config['fvcom']['linecolor']=e4
            # replot=True
        # e5=self.e5.get() 
        # if self.config['fvcom']['zorder']!=e5:
            # self.config['fvcom']['zorder']=e5
            # replot=True
        
        if replot:
            pygrid_support._plot_fvcomfile()  

    
    def saveConfig(self):
        '''Set and save the config file'''  
        
        self.setConfig()        
        saveConfigFile(self.config)     
            

class markerOptionBox(object):

    root = None

    def __init__(self, config):
        """
        Create the MarkerOptionBox
        """        
        self.config=config
        
        tki = tkinter
        self.top = tki.Toplevel(markerOptionBox.root)
        self.top.geometry("400x500+650+250")
        self.top.title("Marker Plot Options")
        self.top.configure(highlightcolor="black")

        self.frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        self.frm.pack(fill='both', expand=True)

        rh = 0.055
        rw = 0.85
        rw2 = 0.4 
        rw3 = 0.33       
        sh = 0.06
        ry = 0.01
        

        label(self.frm,0.0,ry,rh,rw2,'''Zorder''')
        self.e1=entry(self.frm,0.5,ry,rh,rw2,self.config['marker']['zorder'])
        
        label(self.frm,0.075,ry+sh*1,rh,rw,'''Marker Options:''')
        label(self.frm,0.0,ry+sh*2,rh,rw2,'''Markersize''')
        self.e2=entry(self.frm,0.5,ry+sh*2,rh,rw2,self.config['marker']['markersize']) 
        label(self.frm,0.0,ry+sh*3,rh,rw2,'''Facecolor''')
        self.e3=entry(self.frm,0.5,ry+sh*3,rh,rw2,self.config['marker']['facecolor'])  
        label(self.frm,0.0,ry+sh*4,rh,rw2,'''Edgecolor''')
        self.e4=entry(self.frm,0.5,ry+sh*4,rh,rw2,self.config['marker']['edgecolor'])
        
        label(self.frm,0.075,ry+sh*5,rh,rw,'''Box Options:''')
        label(self.frm,0.0,ry+sh*6,rh,rw2,'''Text Offset''')
        self.e5=entry(self.frm,0.5,ry+sh*6,rh,rw2,self.config['marker']['offset']) 
        label(self.frm,0.0,ry+sh*7,rh,rw2,'''BoxStyle''')
        self.e6=entry(self.frm,0.5,ry+sh*7,rh,rw2,self.config['marker']['boxstyle'])  
        label(self.frm,0.0,ry+sh*8,rh,rw2,'''Facecolor''')
        self.e7=entry(self.frm,0.5,ry+sh*8,rh,rw2,self.config['marker']['fc'])
        label(self.frm,0.0,ry+sh*9,rh,rw2,'''Edgecolor''')
        self.e8=entry(self.frm,0.5,ry+sh*9,rh,rw2,self.config['marker']['ec'])
        label(self.frm,0.0,ry+sh*10,rh,rw2,'''Linewidth''')
        self.e9=entry(self.frm,0.5,ry+sh*10,rh,rw2,self.config['marker']['lw'])
        label(self.frm,0.0,ry+sh*11,rh,rw2,'''Alpha''')
        self.e10=entry(self.frm,0.5,ry+sh*11,rh,rw2,self.config['marker']['alpha'])
        label(self.frm,0.0,ry+sh*12,rh,rw2,'''Fontsize''')
        self.e11=entry(self.frm,0.5,ry+sh*12,rh,rw2,self.config['marker']['fontsize'])
        label(self.frm,0.0,ry+sh*13,rh,rw2,'''Fontcolor''')
        self.e12=entry(self.frm,0.5,ry+sh*13,rh,rw2,self.config['marker']['fontcolor'])
               

        


        ################################################################
        #Save close apply buttons
        ################################################################
        self.b_save=button(self.frm,.01+sh*0.1,.925,rh,rw3*.95,'''Save''',self.saveConfig)
        self.b_cancel=button(self.frm,.01+rw3*.95+sh*.25,.925,rh,rw3*.95,'''Close''',self.top.destroy)
        self.b_submit=button(self.frm,.01+rw3*2*.95+sh*.4,.925,rh,rw3*.95,'''Apply''',self.setConfig)


    def setConfig(self):
        replot=False  
              
        e1=self.e1.get() 
        if self.config['marker']['zorder']!=e1:
            self.config['marker']['zorder']=e1
            replot=True
        e2=self.e2.get() 
        if self.config['marker']['markersize']!=e2:
            self.config['marker']['markersize']=e2
            replot=True
        e3=self.e3.get() 
        if self.config['marker']['facecolor']!=e3:
            self.config['marker']['facecolor']=e3
            replot=True
        e4=self.e4.get() 
        if self.config['marker']['edgecolor']!=e4:
            self.config['marker']['edgecolor']=e4
            replot=True
        e5=self.e5.get() 
        if self.config['marker']['offset']!=e5:
            self.config['marker']['offset']=e5
            replot=True
        e6=self.e6.get() 
        if self.config['marker']['boxstyle']!=e6:
            self.config['marker']['boxstyle']=e6
            replot=True
        e7=self.e7.get() 
        if self.config['marker']['fc']!=e7:
            self.config['marker']['fc']=e7
            replot=True
        e8=self.e8.get() 
        if self.config['marker']['ec']!=e8:
            self.config['marker']['ec']=e8
            replot=True
        e9=self.e9.get() 
        if self.config['marker']['lw']!=e9:
            self.config['marker']['lw']=e9
            replot=True
        e10=self.e10.get() 
        if self.config['marker']['alpha']!=e10:
            self.config['marker']['alpha']=e10
            replot=True
        e11=self.e11.get() 
        if self.config['marker']['fontsize']!=e11:
            self.config['marker']['fontsize']=e11
            replot=True
        e12=self.e12.get() 
        if self.config['marker']['fontcolor']!=e12:
            self.config['marker']['fontcolor']=e12
            replot=True
        
        if replot:
            pygrid_support._plot_markerfile()  
    
    def saveConfig(self):
        '''Set and save the config file'''  
        
        self.setConfig()        
        saveConfigFile(self.config)   
        



def defaultConfig():
    '''Default options'''
    config = OrderedDict()
    
    
    config['gen']=OrderedDict([('axis', 'NEGE'),
                               ('dlonmin', -180),
                               ('dlonmax', 180),
                               ('dlatmin', -90),
                               ('dlatmax', 90),
                               ('clonmin', -180),
                               ('clonmax', 180),
                               ('clatmin', -90),
                               ('clatmax', 90)])
    
    config['coast']=OrderedDict([('fill', True),
                                 ('facecolor', '0.75'),
                                 ('edgecolor', 'k'),
                                 ('linewidth', 1),
                                 ('linestyle', 'solid'),
                                 ('zorder', 10)])
    
    config['seg']=OrderedDict([('markersize', 40),
                               ('markercolor', 'm'),
                               ('linecolor', 'b'),
                               ('linewidth', 1),
                               ('linedotsize', 6),
                               ('zorder', 10)])

    config['nei']=OrderedDict([('colormap', 'viridis'),
                               ('cm_zorder', 10),
                               ('linewidth', .25),
                               ('linecolor', 'k'),
                               ('zorder', 10)])
                               
    config['nod']=OrderedDict([('markersize', 36.0),
                               ('facecolor', 'g'),
                               ('edgecolor', 'None'),
                               ('zorder', 10)])
                               
    config['llz']=OrderedDict([('colormap', 'viridis'),
                               ('markersize', 36.0),
                               ('edgecolor', 'None'),
                               ('zorder', 10)])
     
    config['fvcom']=OrderedDict([('colormap', 'viridis'),
                                 ('zorder', 10),
                                 ('shiftlonTF', False)])
                                 
    config['marker']=OrderedDict([('markersize', 36.0),
                                  ('facecolor', 'b'),
                                  ('edgecolor', 'None'),
                                  ('zorder', 10),
                                  ('offset',10),
                                  ('boxstyle', 'round'),
                                  ('fc', 'w'),
                                  ('ec', '0.5'),
                                  ('lw',1),
                                  ('alpha', 0.9),
                                  ('fontsize', 10),
                                  ('fontcolor', 'k')])
                                  
    
    return config
    
                
def loadConfig(config):
    '''This is a ... less then stellar parser and should be replaced.'''            
    
    try:
        # Open the file and read it
        with open('.config', "r") as f:
            dkey=''
            for line in f:
                line=line.replace('\n','')
                if line.startswith('['):
                    dkey=line[1:-1]
                    continue
                if len(line)>0:
                    sline=line.split(' ')
                    #print(dkey)
                    #print(sline)
                    config[dkey][sline[0]]=sline[1]
    except:
        print('Error: Could not load .config file')


def saveConfigFile(config):
    '''Save the config file to .config''' 
        
    # Open the file and write to it
    with open('.config', "w") as f:
        
        for key1 in config.keys():
            f.write('[{}]\n'.format(key1))
            for key2 in config[key1].keys():
                f.write('{} {}\n'.format(key2,config[key1][key2]))
            f.write('\n')




def label(frm,x,y,h,w,t):
    l = tkinter.Label(frm)
    l.place(relx=x, rely=y, relheight=h, relwidth=w)
    l.configure(activebackground="#f9f9f9")
    l.configure(text=t)     
    return l
    
def entry(frm,x,y,h,w,t):
    e = tkinter.Entry(frm)
    e.place(relx=x, rely=y, relheight=h, relwidth=w)
    e.configure(background="white")
    e.configure(font="TkFixedFont")
    e.configure(selectbackground="#c4c4c4")
    e.insert(0,t)
    return e
    
def button(frm,x,y,h,w,t,c):
    b = tkinter.Button(frm)
    b.place(relx=x, rely=y, relheight=h, relwidth=w)
    b.configure(activebackground="#d9d9d9")
    b.configure(text=t)
    b.configure(command=c)
    return b

def rbutton(frm,x,y,h,w,t,v,m):
    cb = tkinter.Radiobutton(frm)
    cb.place(relx=x, rely=y, relheight=h, relwidth=w)
    cb.configure(activebackground="#d9d9d9",justify=tkinter.LEFT)
    cb.configure(text=t,variable=v,value=m)
    return cb
