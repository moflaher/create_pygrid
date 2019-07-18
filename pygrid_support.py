#! /usr/bin/env python
#
# Support module generated by PAGE version 4.8.6
# In conjunction with Tcl version 8.6
#    Jan 17, 2017 02:39:52 AM


import sys
import utilities as ut
import numpy as np
from tkFileDialog import askopenfilename, asksaveasfilename
import copy
import collections
import matplotlib.patches as mpatches
import matplotlib.path as path
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1


def TODO():
    print('pygrid_support.TODO')
    sys.stdout.flush()    
    
 
########################################################################
#
#   selection code
#
########################################################################      
def clear_selection():
    
    if not hasattr(w,'haveArea'):
        w.haveArea=False
    if w.haveArea:
        w.areaFIG.remove()
        w.figure.canvas.draw()
        w.haveArea=False
        
    if hasattr(w,'path'):    
        del(w.path)
    if hasattr(w,'contains'):    
        del(w.contains)
    if hasattr(w,'cid'):
        w.figure.canvas.mpl_disconnect(w.cid)
    if hasattr(w,'areaVec'):
        del(w.areaVec)
        
        
def select_area():   
    
    def onclick_handler1(event):
        draw=False
        if event.button==1:
            w.areaVec=np.vstack([w.areaVec,np.array([event.xdata,event.ydata])])
            w.areaPts+=1
            draw=True
        elif event.button==3:
            if w.areaPts>0:
                w.areaVec=w.areaVec[:w.areaPts,:]
                w.areaPts-=1
                draw=True
        elif event.button==2:
            w.figure.canvas.mpl_disconnect(w.cid)
            w.path=path.Path(w.areaVec[1:,:])      
            w.contains=w.path.contains_points 
        else:
            print('Unknown button')
        
        if draw:   
            if w.haveArea:
                w.areaFIG.remove()         
            w.areaFIG=mpatches.Polygon(w.areaVec[1:,:],facecolor='y',edgecolor='k',alpha=.35)
            w.ax.add_patch(w.areaFIG)
            w.figure.canvas.draw()
            w.haveArea=True
            
        return
              
    
    clear_selection()
        
    w.areaVec=np.array([0,0])
    w.areaPts=0
    
    w.cid = w.Canvas1.mpl_connect('button_press_event',onclick_handler1)  
    
    return 

########################################################################
#
#   node code
#
######################################################################## 
def spray_area():
    if w.Entry1.get()=='':
        return
    else:
        space=int(w.Entry1.get())
    if not hasattr(w,'areaVec'):
        return
    if not hasattr(w,'contains'):
        return
    gfactor=.25
    
    x,y,proj=ut.lcc(w.areaVec[1:,0],w.areaVec[1:,1])
    
    xh=np.arange(x.min(),x.max()+space,space)
    yh=np.arange(y.min(),y.max()+space,space)
    XH,YH=np.meshgrid(xh,yh)
    XH=XH.flatten()
    YH=YH.flatten()
    XH=XH+(np.random.rand(len(XH))-.5)*space*gfactor
    YH=YH+(np.random.rand(len(YH))-.5)*space*gfactor
    
    lon,lat=proj(XH,YH,inverse=True)    
    idx_vec=w.contains(np.array([lon,lat]).T)    
    lon,lat=lon[idx_vec],lat[idx_vec]
    
    if hasattr(w,'nodfile'):
        idx_vec=w.contains(w.nodfile)
        w.nodfile=w.nodfile[~idx_vec,:]
        w.nodfile=np.vstack([w.nodfile,np.vstack([lon,lat]).T])
    else:
        w.nodfile=np.vstack([lon,lat]).T
        w.CBVar['nod'].set(1)
        w.TF['nod']=True
        
    
    
    _plot_nodfile()
        

def remove_area():
    if not hasattr(w,'areaVec'):
        return
    if not hasattr(w,'contains'):
        return      
    if not hasattr(w,'nodfile'):
        return
        
    idx_vec=w.contains(w.nodfile)
    w.nodfile=w.nodfile[~idx_vec,:]
        
    _plot_nodfile()
    

def remove_area_llz():
    if not hasattr(w,'areaVec'):
        return
    if not hasattr(w,'contains'):
        return      
    if not hasattr(w,'llzfile'):
        return
        
    idx_vec=w.contains(w.llzfile[:,:2])
    w.llzfile=w.llzfile[~idx_vec,:]
        
    _plot_llzfile()
 
########################################################################
#
#   depth code
#
########################################################################
def set_depth():
    if w.Entry3.get()=='':
        return
    else:
        depth=float(w.Entry3.get())
    if not hasattr(w,'areaVec'):
        return
    if not hasattr(w,'contains'):
        return
    
    
    if hasattr(w,'neifile'):
        idx_vec=w.contains(w.neifile['nodell'])
        w.neifile['h'][idx_vec]=depth
    
        _plot_neifilecolor()


def avg_depth():
    if w.Entry4.get()=='':
        return
    else:
        depth=float(w.Entry4.get())
    if not hasattr(w,'areaVec'):
        return
    if not hasattr(w,'contains'):
        return
    
    
    if hasattr(w,'neifile'):
        idx_vec=w.contains(w.neifile['nodell'])
        w.neifile['h'][idx_vec]=np.divide(depth+ w.neifile['h'][idx_vec],2.0)
    
        _plot_neifilecolor()

    
def calc_stats():
    if not hasattr(w,'areaVec'):
        return
    if not hasattr(w,'contains'):
        return    
    
    if hasattr(w,'neifile'):
        idx_vec=w.contains(w.neifile['nodell'])
        h=w.neifile['h'][idx_vec]
        #print(dir( w.Labelsmin))
        w.Labelsmin['text']="{:.2f}".format(h.min())
        w.Labelsmax['text']="{:.2f}".format(h.max())
        w.Labelsmean['text']="{:.2f}".format(h.mean())
        

def smooth():
    """
    Smooth bathymetry. Ignore values based on dhh or depth.
    """
    
    
    if not hasattr(w,'areaVec'):
        return
    if not hasattr(w,'contains'):
        return
    if not hasattr(w,'neifile'):
        return
    
    hmin=-999999
    hmax=999999
    dhhmin=-999999
    dhhmax=999999
    
    if w.Entryhmin.get()!='':
        hmin=float(w.Entryhmin.get())
    if w.Entryhmax.get()!='':
        hmax=float(w.Entryhmax.get())
    if w.Entrydhhmin.get()!='':
        dhhmin=float(w.Entrydhhmin.get())
    if w.Entrydhhmax.get()!='':
        dhhmax=float(w.Entrydhhmax.get())
       
    hidx=w.contains(w.neifile['nodell'])  
    nidxdhh=np.arange(0,len(w.neifile['nodell']),dtype=int)[hidx]
    hhidx=np.arange(0,len(w.neifile['nodell']),dtype=int)[hidx]
     
    h=copy.deepcopy(w.neifile['h'])
        
    if dhhmin!=-999999 or dhhmax!=999999:
        w.neifile=ut.get_dhh(w.neifile)
        
        eidx=w.contains(w.neifile['uvnodell'])
        tidx=np.arange(0,len(w.neifile['uvnodell']),dtype=int)[eidx]
        dhhidx=np.argwhere((w.neifile['dhh'][eidx]>=dhhmin) & (w.neifile['dhh'][eidx]<=dhhmax))
        nidxdhh=np.unique(w.neifile['nv'][tidx[dhhidx],:])

        
    if hmin!=-999999 or hmax!=999999:
        hsidx=np.argwhere((w.neifile['h'][hidx]>=hmin) & (w.neifile['h'][hidx]<=hmax))
        hhidx=hhidx[hsidx]

    TFidx=np.in1d(nidxdhh,hhidx)
    nidx=nidxdhh[TFidx]  
    

    for idx in nidx:
        n=w.neifile['neighbours'][idx,]
        n=n[n!=0]
        
        h[idx]=w.neifile['h'][n-1].mean()
        
    w.neifile['h']=h
    
    
    if dhhmin!=-999999 or dhhmax!=999999:
        w.neifile=ut.get_dhh(w.neifile)
        
    if w.TF['neic']:
        _plot_neifilecolor()


########################################################################
#
#   segment code
#
########################################################################    
def clear_tmp_seg():
    
    if not hasattr(w,'haveAreaSEG'):
        w.haveAreaSEG=False
    if w.haveAreaSEG:
        w.areaFIGSEG.remove()
        w.figure.canvas.draw()
        w.haveAreaSEG=False
        
    if hasattr(w,'cid_seg'):
        w.figure.canvas.mpl_disconnect(w.cid_seg)
    if hasattr(w,'tempSeg'):
        del(w.tempSeg)



def select_seg():

    def set_seg():
        dist=100000000000000000000000
        for seg in w.segfile:
            tdist=(w.segfile[seg][:,0]-w.segpt[0])**2 +(w.segfile[seg][:,1]-w.segpt[1])**2
            tmin=tdist[np.argmin(tdist)]
            if tmin<dist:
                dist=tmin
                bestseg=seg
        w.Entry2.delete(0,END)
        w.Entry2.insert(0,bestseg)
    
    def pick_seg(event):
        remove=False

        if event.button==1:
            w.segpt=np.array([event.xdata,event.ydata])
        elif event.button==2:
            w.figure.canvas.mpl_disconnect(w.cid_seg)
            remove=True
        else:
            print('Unknown button')
            
        
        if hasattr(w,'segptFIG'):
            w.segptFIG.remove()       
            
        w.segptFIG=w.ax.scatter(w.segpt[0],w.segpt[1],c=w.config['seg']['markercolor'],s=float(w.config['seg']['markersize']))
        w.figure.canvas.draw()
        
        if remove:
            w.segptFIG.remove()
            w.figure.canvas.draw()
            del(w.segptFIG)
            remove=False
            set_seg()
            
        return
    
    if not hasattr(w,'segfile'):
        return
    if hasattr(w,'cid_seg'):
        w.figure.canvas.mpl_disconnect(w.cid_seg)
    
    w.cid_seg = w.Canvas1.mpl_connect('button_press_event',pick_seg)
    
    
def create_seg():   
    
    def onclick_handler2(event):
        draw=False
        if event.button==1:
            w.tempSeg=np.vstack([w.tempSeg,np.array([event.xdata,event.ydata])])
            w.SegPts+=1
            draw=True
        elif event.button==3:
            if w.SegPts>0:
                w.tempSeg=w.tempSeg[:w.SegPts,:]
                w.SegPts-=1
                draw=True
        elif event.button==2:
            w.figure.canvas.mpl_disconnect(w.cid_seg)
            if not hasattr(w,'segfile'):
                w.segfile=collections.OrderedDict()
                w.segfile['1']=np.vstack([w.tempSeg[1:,:],w.tempSeg[1,:]])
                w.TF['seg']=True
                w.CBVar['seg'].set(1)
            else:
                itm=np.array([int(seg) for seg in w.segfile.keys()])
                maxitm=itm.max()
                w.segfile[str(maxitm+1)]=np.vstack([w.tempSeg[1:,:],w.tempSeg[1,:]])
                
            clear_tmp_seg()    
            _plot_segfile()                
                
        else:
            print('Unknown button')
        
        if draw:   
            if w.haveAreaSEG:
                w.areaFIGSEG.remove()         
            w.areaFIGSEG=mpatches.Polygon(w.tempSeg[1:,:],facecolor='b',edgecolor='k',alpha=.35)
            w.ax.add_patch(w.areaFIGSEG)
            w.figure.canvas.draw()
            w.haveAreaSEG=True
            
        return
              
    
    clear_tmp_seg()
        
    w.tempSeg=np.array([0,0])
    w.SegPts=0
    
    w.cid_seg = w.Canvas1.mpl_connect('button_press_event',onclick_handler2)  
    
    return 
    
    
def delete_seg():
    if w.Entry2.get()=='':
        return
    if hasattr(w,'segfile'):
        if w.Entry2.get() in w.segfile:
            del w.segfile[w.Entry2.get()]
        if len(w.segfile.keys())==0:
            del w.segfile  
            w.TF['seg']=False
            w.CBVar['seg'].set(0)  
            
    _plot_segfile()
    
        

########################################################################
#
#   misc functions
#
########################################################################
def remove_nodeseg_in():
    
    if w.Entry2.get()=='':
        return
    if not hasattr(w,'nodfile'):
        return  
    tpath=path.Path(w.segfile[w.Entry2.get()])      
    idx_vec=tpath.contains_points(w.nodfile)
    w.nodfile=w.nodfile[~idx_vec,:]

    _plot_nodfile()
    
def remove_nodeseg_out():
    
    if w.Entry2.get()=='':
        return
    if not hasattr(w,'nodfile'):
        return  
    tpath=path.Path(w.segfile[w.Entry2.get()])      
    idx_vec=tpath.contains_points(w.nodfile)
    w.nodfile=w.nodfile[idx_vec,:]

    _plot_nodfile()
    
def extract_seg():
    
    w.segfile=collections.OrderedDict()
    
    bcode=w.neifile['bcode']  
    nbound=np.unique(bcode) 
        
    for j in range(1,len(nbound)):
        idx=ut.sort_boundary(w.neifile,boundary=j)-1
        w.segfile[str(j)]=np.vstack([w.neifile['lon'][idx],w.neifile['lat'][idx]]).T          

    _plot_segfile()
    w.TF['seg']=True
    w.CBVar['seg'].set(1)
    w.figure.canvas.draw()
    
    return    
    
def extract_nod():
    
    w.nodfile=np.vstack([w.neifile['lon'][w.neifile['bcode']==0],w.neifile['lat'][w.neifile['bcode']==0]]).T
    _plot_nodfile()
    w.TF['nod']=True
    w.CBVar['nod'].set(1)
    w.figure.canvas.draw()
    
    return
    
def extract_llz():
    
    w.llzfile=np.vstack([w.neifile['lon'][w.neifile['bcode']==0],w.neifile['lat'][w.neifile['bcode']==0],w.neifile['h'][w.neifile['bcode']==0]]).T
    _plot_llzfile()
    w.TF['llz']=True
    w.CBVar['llz'].set(1)
    w.figure.canvas.draw()
    
    return
    

def set_initdir(init_dir):
    w.init_dir = init_dir
    
    
def flatten(xs):
    """
    Flatten any list.
    Found at https://stackoverflow.com/a/10632307
    """
    result = []
    if isinstance(xs, (list, tuple)):
        for x in xs:
            result.extend(flatten(x))
    else:
        result.append(xs)
    return result
    
########################################################################
#
#   file type functions
#
########################################################################
def nodfile(filename = '', axis=False):
    """
    Load and plot an nodfile.
    **lots of different format for "nod" files this one is just ll**
    """

    if filename != '':
        w.nodfile=ut.load_llzfile(filename)
        _plot_nodfile()
        if axis:
            w.ax.axis([w.nodfile[:,0].min(),w.nodfile[:,0].max(),w.nodfile[:,1].min(),w.nodfile[:,1].max()])
        w.TF['nod']=True
        w.CBVar['nod'].set(1)
        w.figure.canvas.draw()
            
    return
    
 
def neifile(filename = '', axis=False):
    """
    Load and plot an neifile for command line.
    """
    if filename != '':
        w.neifile=ut.load_nei2fvcom(filename)
        if 'nei' in w.FIGS:
            w.FIGS['nei'].remove()
        w.FIGS['nei']=w.ax.triplot(w.neifile['trigrid'],color=w.config['nei']['linecolor'],lw=float(w.config['nei']['linewidth']),zorder=int(w.config['nei']['zorder']))
        if axis:
            w.ax.axis([w.neifile['lon'].min(),w.neifile['lon'].max(),w.neifile['lat'].min(),w.neifile['lat'].max()])
        w.TF['nei']=True
        w.TF['neic']=False
        w.CBVar['nei'].set(1)
        w.CBVar['neic'].set(0)
        for key in w.FIGS['neic'].keys():
            w.FIGS['neic'][key].remove()
        w.FIGS['neic']={}
        
        w.figure.canvas.draw()
            
    return
    
    
def segfile(filename='', axis=False):
    """
    Load and plot an segfile for command line.
    """

    if filename != '':
        w.segfile=ut.load_segfile(filename)
        _plot_segfile()
        if axis:
            x=np.array([val for seg in w.segfile for val in w.segfile[seg][:,0]])
            y=np.array([val for seg in w.segfile for val in w.segfile[seg][:,1]])
            w.ax.axis([x.min(),x.max(),y.min(),y.max()]) 
        w.TF['seg']=True
        w.CBVar['seg'].set(1)
        w.figure.canvas.draw()
            
    return

    
def llzfile(filename = '' , axis=False, flip=False):
    """
    Load and plot an llzfile.
    """

    if filename != '':
        w.llzfile=ut.load_llzfile(filename, flip)
        
        if w.llzfile.shape[1]==2:
            del w.llzfile
            nodfile(filename,True)
            return
        
        _plot_llzfile()

        w.cax.set_visible(True)
        if axis:
            w.ax.axis([w.llzfile[:,0].min(),w.llzfile[:,0].max(),w.llzfile[:,1].min(),w.llzfile[:,1].max()])        
        w.TF['llz']=True
        w.caxTF=True
        w.CBVar['llz'].set(1)
        w.figure.canvas.draw()
            
    return
    
    
def fvcomfile(filename = '', axis=False):
    """
    Load and plot an fvcomfile.
    """

    if filename != '':
        r=filename.rfind('/')+1
        w.fvcom=ut.loadnc(filename[:r],filename[r:])
        #print(w.fvcom.keys())
        
        check=np.array(['ua','va','u','v','ww','uvh','wet_cells_prev_int','zeta','wet_cells_prev_ext','h_center','omega','wet_nodes','tauc','h','partition','wet_nodes_prev_int','wet_cells'])
        w.fvcom['pable_txt']=np.array([])
        w.fvcom['pable']=np.array([])
        for key in w.fvcom.keys():
            if key in check:     
                w.fvcom['pable_txt']=np.append(w.fvcom['pable_txt'],key + " - {}".format(np.shape(w.fvcom[key])))           
                w.fvcom['pable']=np.append(w.fvcom['pable'],key)
        # for key in w.fvcom.keys():
            # if w.fvcom['dims']['nele'] in np.shape(w.fvcom[key]):
                # w.fvcom['pable']=np.append(w.fvcom['pable'],key + " - {}".format(np.shape(w.fvcom[key])))
            # if w.fvcom['dims']['node'] in np.shape(w.fvcom[key]):
                # w.fvcom['pable']=np.append(w.fvcom['pable'],key + " - {}".format(np.shape(w.fvcom[key])))  
        
        for i in w.fvcom['pable_txt']:
            w.listbox.insert(END, i)
        
        w.timemin.configure(text='0')
        w.timemax.configure(text=str(len(w.fvcom['time'])))
        
        w.lvlmin.configure(text='0')
        w.lvlmax.configure(text=str(w.fvcom['dims']['siglev']))
                
        _plot_fvcomfile()

        w.cax.set_visible(True)
        if axis:
            w.ax.axis([w.fvcom['lon'].min(),w.fvcom['lon'].max(),w.fvcom['lat'].min(),w.fvcom['lat'].max()])        
        w.TF['fvcom']=True
        w.caxTF=True
        w.CBVar['fvcom'].set(1)
        w.figure.canvas.draw()
            
    return
 
########################################################################
#
#   draw plots
#
########################################################################
def _plot_nodfile():
  
    if 'nod' in w.FIGS:
        w.FIGS['nod'].remove()        
       
    w.FIGS['nod']=w.ax.scatter(w.nodfile[:,0], w.nodfile[:,1],s=float(w.config['nod']['markersize']),c=w.config['nod']['facecolor'],edgecolor=w.config['nod']['edgecolor'],zorder=int(w.config['nod']['zorder']))
    w.figure.canvas.draw()

    return
 
def _plot_segfile():
  
    try:
        if 'seg' in w.FIGS:
            w.FIGS['seg'][0].remove()
            w.FIGS['seg'][1][0].remove()
    except:
        pass

    if hasattr(w,'segfile'):
        ptarray=np.hstack([[w.segfile[seg][:,0],w.segfile[seg][:,1]] for seg in w.segfile]).T
        tmparray=[list(zip(w.segfile[seg][:,0],w.segfile[seg][:,1])) for seg in w.segfile]
        w.linecollection=LC(tmparray,color=w.config['seg']['linecolor'],linewidth=float(w.config['seg']['linewidth']),zorder=int(w.config['seg']['zorder']))
        w.FIGS['seg']=[w.linecollection,
                      w.ax.plot(ptarray[:,0],ptarray[:,1],w.config['seg']['linecolor']+'.',markersize=float(w.config['seg']['linedotsize']),zorder=int(w.config['seg']['zorder']))]
        w.ax.add_collection(w.linecollection)
    
    w.figure.canvas.draw()

    return
    
def _plot_llzfile():
  
    state = True
    if 'llz' in w.FIGS:
        w.FIGS['llz'].remove()
        state = w.TF['llz']
    if not hasattr(w,'cb'):
        w.cb={}

    cmin, cmax = getcb(w.llzfile[:,2])    
    w.FIGS['llz']=w.ax.scatter(w.llzfile[:,0], w.llzfile[:,1],s=float(w.config['llz']['markersize']),cmap=w.config['llz']['colormap'], c=w.llzfile[:,2],edgecolor=w.config['llz']['edgecolor'],zorder=int(w.config['llz']['zorder']),vmin=cmin,vmax=cmax,visible=state)
    w.cb['llz']=w.figure.colorbar(w.FIGS['llz'],cax=w.cax)
    
    w.figure.canvas.draw()

    return

    
def _plot_neifilecolor():
    
    if 'neic' not in w.FIGS:
        w.FIGS['neic']={}
    if not hasattr(w,'cb'):
        w.cb={}

    w.neiplot = w.NeiMenuVar.get()    

    state = True    
    if w.neiplot in w.FIGS['neic']:
        w.FIGS['neic'][w.neiplot].remove()
        state = w.TF['neic']
  
    if w.neiplot == 'Depth':
        dname='h'
        cmin, cmax = getcb(w.neifile['h']) 
    if w.neiplot == 'dhh':
        dname='dhh'
        if w.neiplot not in w.neifile:
            w.neifile=ut.get_dhh(w.neifile)
        cmin, cmax = getcb(w.neifile['dhh'])
    if w.neiplot == 'Sidelength':
        dname='sl'
        if w.neiplot not in w.neifile:
            w.neifile=ut.get_sidelength(w.neifile)
        cmin, cmax = getcb(w.neifile['sl']) 
          
    w.FIGS['neic'][w.neiplot]=w.ax.tripcolor(w.neifile['trigrid'], w.neifile[dname],vmin=cmin,vmax=cmax,visible=state,cmap=w.config['nei']['colormap'],zorder=int(w.config['nei']['cm_zorder']))
    w.cb[w.neiplot]=w.figure.colorbar(w.FIGS['neic'][w.neiplot],cax=w.cax)

    w.figure.canvas.draw()

    return
    
def _plot_fvcomfile():
    
    if 'fvcom' not in w.FIGS:
        w.FIGS['fvcom']={}
    if not hasattr(w,'cb'):
        w.cb={}
        
        
    state = True  
    try:
        if w.fvcomplot in w.FIGS['fvcom']:
            w.FIGS['fvcom'][w.fvcomplot].remove()
            state = w.TF['fvcom']
    except:
        w.fvcomplot=''
  

    if w.overmenu.get()!='':
        if w.overmenu.get() in w.fvcom['pable']:
            w.fvcomplot=w.overmenu.get()
    else:
        w.fvcomplot = w.FVCOMMenuVar.get()   
    
    if w.etime!='':
        w.timeTF=True
        w.time=int(w.etime.get())
    else:
        w.timeTF=False
    if w.elvl!='':
        w.lvlTF=True
        w.lvl=int(w.elvl.get())
    else:
        w.lvlTF=False        

    #print(w.fvcomplot)

    if w.fvcomplot == 'dhh':
        dname='dhh'
        if w.fvcomplot not in w.fvcom:
            w.fvcom=ut.get_dhh(w.fvcom)
    elif w.fvcomplot == 'sidelength':
        dname='sl'
        if w.fvcomplot not in w.fvcom:
            w.fvcom=ut.get_sidelength(w.fvcom)
    elif (w.fvcomplot == 'speed_da' and w.timeTF):
        dname='speed_da'
        w.fvcom['speed_da']=np.sqrt(w.fvcom['ua'][w.time,:]**2+w.fvcom['va'][w.time,:]**2)        
    elif (w.fvcomplot == 'speed' and w.timeTF and w.lvlTF):
        dname='speed'
        w.fvcom['speed']=np.sqrt(w.fvcom['u'][w.time,w.lvl,:]**2+w.fvcom['v'][w.time,w.lvl,:]**2)        
    else:
        dname='field'
        shp=np.shape(w.fvcom[w.fvcomplot])
        tTF=(len(w.fvcom['time']) in shp)
        lTF=(w.fvcom['dims']['siglev'] in shp) or (w.fvcom['dims']['siglay'] in shp)
        if (tTF==False and lTF==False):
            w.fvcom['field']=w.fvcom[w.fvcomplot]
        elif (tTF==True and lTF==False):
            w.fvcom['field']=w.fvcom[w.fvcomplot][w.time,:]
        else:
            w.fvcom['field']=w.fvcom[w.fvcomplot][w.time,w.lvl,:]
        
    cmin, cmax = getcb(w.fvcom[dname])          
    w.FIGS['fvcom'][w.fvcomplot]=w.ax.tripcolor(w.fvcom['trigrid'], w.fvcom[dname],vmin=cmin,vmax=cmax,visible=state,cmap=w.config['nei']['colormap'],zorder=int(w.config['nei']['cm_zorder']))
    w.cb[w.fvcomplot]=w.figure.colorbar(w.FIGS['fvcom'][w.fvcomplot],cax=w.cax)

    w.figure.canvas.draw()

    return


########################################################################
#
#   plot toggles
#
########################################################################
def toggle_coastline():
    """
    Toggle coastline
    """
    
    toggle_plot('coast')   
    
    return
    
def toggle_segfile():
    """
    Toggle segfile
    """
    
    toggle_plot('seg')  
    
    return
    
def toggle_neifile():
    """
    Toggle neifile
    """
    
    toggle_plot('nei')
    
    return

def toggle_nodfile():
    """
    Toggle nodfile
    """

    toggle_plot('nod')   
    
    return
    
def toggle_llzfile():
    """
    Toggle llzfile
    """
        
    toggle_plot('llz',True)   
    
    return
        
def toggle_neifilecolor():
    """
    Toggle neifile depth
    """
    
    try:
        if w.TF['neic']:
            w.FIGS['neic'][w.neiplot].set_visible(False)
            w.TF['neic']=False
            w.cax.set_visible(False)
            w.caxTF=False
        else:
            if w.neiplot not in w.FIGS['neic']:
                _plot_neifilecolor()   
            w.FIGS['neic'][w.neiplot].set_visible(True)
            w.TF['neic']=True
            w.cax.set_visible(True)
            w.caxTF=True
            
        w.figure.canvas.draw()
    except AttributeError:
        w.CBVar['neic'].set(0)    
    
    return  
    
def toggle_fvcom():
    """
    Toggle fvcomfile
    """

    try:
        if w.TF['fvcom']:
            w.FIGS['fvcom'][w.fvcomplot].set_visible(False)
            w.TF['fvcom']=False
            w.cax.set_visible(False)
            w.caxTF=False
        else:
            if w.fvcomplot not in w.FIGS['fvcom']:
                _plot_fvcomfile()   
            w.FIGS['fvcom'][w.fvcomplot].set_visible(True)
            w.TF['fvcom']=True
            w.cax.set_visible(True)
            w.caxTF=True
            
        w.figure.canvas.draw()
    except AttributeError:
        w.CBVar['fvcom'].set(0)   
    
    return
 
def toggle_plot(name,color=False):
    """
    Toggle the checkbox plots
    """
    try:
        swap=flatten(w.FIGS[name])
        if w.TF[name]:
            for p in swap:
                p.set_visible(False)
            w.TF[name]=False
            if color:
                w.cax.set_visible(False)
                w.caxTF=False
        else:
            for p in swap:
                p.set_visible(True)
            w.TF[name]=True
            if color:
                w.cax.set_visible(True)
                w.caxTF=True
            
        w.figure.canvas.draw()
    except AttributeError:
        w.CBVar[name].set(0)     
    
    
def getcb(datain):
    """
    Get colorbar min max from interface. Use those values default min and max of datain
    """
    
    if w.Entry41.get() == "":
        cmax = datain.max()
    else:
        cmax = float(w.Entry41.get())
        
    if w.Entry42.get() == "":
        cmin = datain.min()
    else:
        cmin = float(w.Entry42.get())
       
    return cmin, cmax
        

def redraw_llz():
    
    if 'llz' in w.FIGS:
        _plot_llzfile()
        
    return    

def redraw_nei():

    if 'neic' in w.FIGS:
        _plot_neifilecolor()     
    
    return
    
def change_neimenu(*args):
    
    #if the color plots are off or there is not neifile do nothing when plot is changed
    if not w.TF['neic']:
        return    
    if not hasattr(w,'neifile'):
        return
    
    if hasattr(w,'neiplot'):
        if w.neiplot in w.FIGS['neic']:
            w.FIGS['neic'][w.neiplot].set_visible(False)
        
        w.neiplot = w.NeiMenuVar.get()    
        if w.neiplot in w.FIGS['neic']:
            w.FIGS['neic'][w.neiplot].set_visible(True)
            w.figure.canvas.draw()
        else:
            _plot_neifilecolor()

        
        
    
    
    
    
    
    
    
    
########################################################################
#
#   save files
#
########################################################################
def save_nodfile():
    
    filename=''
    filename=asksaveasfilename(initialdir=w.init_dir)
    if filename != '':
        ut.save_nodfile(w.nodfile,filename)
 
def save_llzfile():
    
    filename=''
    filename=asksaveasfilename(initialdir=w.init_dir)
    if filename != '':
        ut.save_llzfile(w.llzfile,filename)
        
def save_segfile():
    
    filename=''
    filename=asksaveasfilename(initialdir=w.init_dir)
    if filename != '':
        ut.save_segfile(w.segfile,filename)
        
def save_nod2polyfile():
    lastseg=int(list(w.segfile.keys())[-1])
    w.nod2polyfile=copy.deepcopy(w.segfile)
    w.nod2polyfile[str(lastseg+1)]=w.nodfile

    filename=''
    filename=asksaveasfilename(initialdir=w.init_dir)
    if filename != '':
        ut.save_nod2polyfile(w.nod2polyfile,filename,len(w.nod2polyfile.keys())-1)
        
def save_neifile():
    
    filename=''
    filename=asksaveasfilename(initialdir=w.init_dir)
    if filename != '':
        ut.save_neifile(w.neifile,filename)


########################################################################
#
#   load files
#
########################################################################
def load_nodfile():
    """
    Load and plot an nodfile.
    **lots of different format for "nod" files this one is just ll**
    """
    filename=''
    filename=askopenfilename(initialdir=w.init_dir)

    nodfile(filename)
            
    return
    
def load_coastline():
    """
    Load and plot a coastline.
    """
    filename=()
    filename=askopenfilename(initialdir=w.init_dir)
    if filename != ():
        w.coastline=ut.load_coastline(filename=filename)
        w.TF['coast']=True
        w.CBVar['coast'].set(1)
        
        #Reduce number of segments - helps but not enough
        #axis=[-68.5,-64,44,46.5]
        #yep=[]
        
        #def isin(axis,line):
            #return ((line[:,0]>=axis[0]) & (line[:,0]<=axis[1]) & (line[:,1]>=axis[2]) & (line[:,1]<=axis[3])).sum()
            
            
        #for i,line in enumerate(w.coastline):
            #if isin(axis,np.array(line)):
                #yep+=[i]
               
        if w.config['coast']['fill']:
            w.FIGS['coast']=PC(w.coastline,facecolor = w.config['coast']['facecolor'],edgecolor=w.config['coast']['edgecolor'],linewidths=float(w.config['coast']['linewidth']),zorder=int(w.config['coast']['zorder'])) 
        else:
            w.FIGS['coast']=LC(w.coastline,color=w.config['coast']['edgecolor'],linewidths=float(w.config['coast']['linewidth']),zorder=int(w.config['coast']['zorder'])) 
        w.ax.add_collection(w.FIGS['coast'])
        w.figure.canvas.draw()
            
    return

def load_neifile():
    """
    Load and plot an neifile.
    """
    filename=''
    filename=askopenfilename(initialdir=w.init_dir)
    
    neifile(filename)
            
    return
    
def load_segfile():
    """
    Load and plot an segfile.
    """
    filename=''
    filename=askopenfilename(initialdir=w.init_dir)
    
    segfile(filename)
            
    return
    
def load_llzfile():
    """
    Load and plot an llzfile.
    """
    filename=''
    filename=askopenfilename(initialdir=w.init_dir)
    
    llzfile(filename)
            
    return
    
def load_fvcomfile():
    """
    Load and plot an fvcomfile.
    """
    filename=''
    filename=askopenfilename(initialdir=w.init_dir)
    
    fvcomfile(filename)
            
    return


########################################################################
#
#   end code
#
########################################################################

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
    
    #init a bunch of stuff
    #w.types=['coastline','segfile','neifile','nodfile','llzfile','neifilecolor']
    #w.plots=['Depth','Sidelength','dhh']
    w.FIGS={}
    w.TF={}
    w.FIGS['neic']={}
    for tf in w.types:
        w.TF[tf]=False
    w.neiplot='Depth'
    
    

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import pygrid
    pygrid.vp_start_gui()








