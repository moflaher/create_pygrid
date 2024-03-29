#load modules
from __future__ import division,print_function

#Numerical modules
import numpy as np

#I/O modules
import glob
from scipy.io import netcdf
import scipy.io as sio
from matplotlib.collections import LineCollection as LC
from matplotlib.collections import PolyCollection as PC
import matplotlib.pyplot as plt
import matplotlib.tri as mplt
import matplotlib.dates as dates
import collections
import copy
import netCDF4 as n4


########################################################################
#
# Code for loading files
#
########################################################################

def loadnc(datadir, singlename=[], fvcom=True, suppress=False):
    """
    Loads a .nc  data file

    :Parameters:
        **datadir** -- The path to the ncfile.
        **filename** -- The nc filename.
        
        **fvcom** -- True/False - is the ncfile an fvcom file. 
    """
    if singlename==[]:
        singlename = glob.glob('*.nc')[0]

    # Initialize a dictionary for the data.
    data = {}
    #does the datadir end in / if not append it
    if (len(datadir)>0) and (not datadir.endswith('/')):
        datadir = datadir + '/'
    # Store the filepath and data dir in case it is needed in the future
    data['datadir'] = datadir
    data['filepath'] = datadir + singlename
    
    try:
        # Load data with scipy netcdf
        ncid = netcdf.netcdf_file(data['filepath'], 'r', mmap=True)

        for key in ncid.variables.keys():
            data[key] = ncid.variables[key].data   
        
        data['dims'] = {}
        for key in ncid.dimensions.keys():
            data['dims'][key] = ncid.dimensions[key]
    except TypeError:
        if not suppress:
            print('File is netcdf4 type')
        ncid = n4.Dataset(data['filepath'])
        data = ncid.variables      
            

    if fvcom:
        if 'nv' in data:
            data['nv'] = data['nv'].astype(int).T-1
        if 'nbe' in data:
            data['nbe'] = data['nbe'].astype(int).T-1
        data = ncdatasort(data)  
        
    return data


def ncdatasort(data,trifinder=False,uvhset=True):
    """
    From the nc data provided, common variables are produced.

    :Parameters: **data** -- a data dictionary of data from a .nc file

    :Returns: **data** -- Python data dictionary updated to include uvnode and uvnodell
    """
    lond=False
    latd=False
    try:
        #load lon/lat from files and use it
        if glob.glob(data['datadir'] + "../input/*_lon.dat"):        
            data['lon'] = np.loadtxt(glob.glob(data['datadir'] + "../input/*_lon.dat")[0])
            lond=True
        if glob.glob(data['datadir'] + "../input/*_long.dat"):        
            data['lon'] = np.loadtxt(glob.glob(data['datadir'] + "../input/*_long.dat")[0])
            lond=True
        if glob.glob(data['datadir'] + "../input/*_lat.dat"):
            data['lat'] = np.loadtxt(glob.glob(data['datadir'] + "../input/*_lat.dat")[0])
            latd=True
    except:
        pass

    lonx=False
    if 'lon' not in data:
        print("No lon found. Lon set to x")
        data['lon'] = data['x']
        lonx=True
    latx=False
    if 'lat' not in data:
        print("No lat found. Lat set to y")
        data['lat'] = data['y']
        latx=True

    
    if ('lonc' not in data) or lond or lonx:    
        data['lonc'] = data['lon'][data['nv']].mean(axis=1)
    if ('latc' not in data) or latd or latx:   
        data['latc'] = data['lat'][data['nv']].mean(axis=1)

    data['nodell'] = np.vstack([data['lon'],data['lat']]).T
    data['uvnodell'] = np.vstack([data['lonc'],data['latc']]).T


    data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
        
    data['nodexy'] = np.vstack([data['x'],data['y']]).T
    data['uvnodexy'] = data['nodexy'][data['nv'],:].mean(axis=1)
    data['xc'] = data['uvnodexy'][:,0]
    data['yc'] = data['uvnodexy'][:,1]
    
    try:
        if 'nele' in data['dims']:    
            data['nele'] = data['dims']['nele']
        if 'node' in data['dims']:
            data['node'] = data['dims']['node']
    except KeyError:
        pass

    if 'Times' in data:
        data['Time']=np.empty((len(data['Times']),),dtype='|S26')
        for i in range(len(data['Times'])):
                data['Time'][i]=''.join(data['Times'][i,].astype(str))
        data['time']=dates.datestr2num(data['Time'])    
        
    if 'trigrid' not in data:
        if (('nv' in data) and('lon' in data) and ('lat' in data)):
            data['trigrid'] = mplt.Triangulation(data['lon'], data['lat'],data['nv'])      
    if 'trigridxy' not in data:
        if (('nv' in data) and('x' in data) and ('y' in data)):
            data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])  

    if uvhset:
        data['uvh']=data['h'][data['nv']].mean(axis=1)

    if trifinder:
        data['trigrid_finder'] = data['trigrid'].get_trifinder()
        data['trigridxy_finder'] = data['trigridxy'].get_trifinder()

    return data


def load_coastline(filename):
    """
    Plots the coastline on an ax.

    :Parameters:
        axin - a plt axes to plot on.
    :Optional:
        filename - which coastline file to use. Use nc coastline format from xscan. (default mid_nwatl6b.nc)
        color - the color on the coastline (default black).
        lw - the width of the coastline's lines (default 1).
        ls - the style of the coastline's lines (default 1).
        fill - True/False to fill in the coastline (default False)
        fcolor - the color used to fill the coastline (default 0.75, dark gray)
        ticksout - Face the axis ticksout  (R style - default False) 
    """
   
    sl=loadnc('',filename,False)

    idx=np.where(sl['count']!=0)[0]
    sl['count']=sl['count'][idx]
    sl['start']=sl['start'][idx]

    tmparray=[list(zip(sl['lon'][sl['start'][i]:(sl['start'][i]+sl['count'][i])],sl['lat'][sl['start'][i]:(sl['start'][i]+sl['count'][i])])) for i in range(0,len(sl['start']))]

    return np.array(tmparray)
    
    
def load_neifile(neifilename=None):
    """
    Loads a .nei file and returns the data as a dictionary. 
    """
    
    if neifilename==None:
        print('loadnei requires a filename to load.')
        return
    try:
        fp=open(neifilename,'r')
    except IOError:
        print('Can not find ' + neifilename)
        return

    nnodes=int(fp.readline())
    maxnei=int(fp.readline())
    llminmax=np.array([float(x) for x in fp.readline().split()])
    t_data=np.loadtxt(neifilename,skiprows=3,dtype='float64')
    fp.close()

    neifile={}

    neifile['nnodes']=nnodes
    neifile['maxnei']=maxnei
    neifile['llminmax']=llminmax

    neifile['nodenumber']=t_data[:,0].astype(int)
    neifile['nodell']=t_data[:,1:3]
    neifile['bcode']=t_data[:,3].astype(int)
    neifile['h']=t_data[:,4]
    neifile['neighbours']=t_data[:,5:].astype(int)
    neifile['lon']=t_data[:,1]
    neifile['lat']=t_data[:,2]
    
    return neifile
    
    
def load_nei2fvcom(filename):
    """
    Loads a .nei file and returns the data as a dictionary that mimics the structure of fvcom output as closely as possible. 
    """
    
    # Load the neifile
    data=load_neifile(filename)
    
    # Use lcc projection get x,y data
    data['x'],data['y'],data['proj']=lcc(data['lon'],data['lat'])
    
    # Get nv for grid
    data=get_nv(data)
    
    # ncdatasort to make typically structures
    data=ncdatasort_old(data)     
        
    return data


def load_segfile(filename=None):
    """
    Loads an seg file the data as a dictionary. 
    """

    data={}
    
    if filename==None:
        print('load_segfile requires a filename to load.')
        return
    try:
        fp=open(filename,'r')
    except IOError:
        print('load_segfile: invalid filename.')
        return data

    data=collections.OrderedDict()

    for line in fp:
        llist=line.split()
        if len(llist)==2:
            cnt=0
            currentseg=llist[0]
            data[currentseg]=np.empty((int(llist[1]),2))
        else:
            data[currentseg][cnt,:]=llist[1:3]
            cnt+=1

    fp.close()

    return data


def load_llzfile(filename=None, flip=False):
    """
    Loads an llz file the data as an array. 
    """

    data={}
    
    if filename==None:
        print('load_llzfile requires a filename to load.')
        return
    try:
        fp=open(filename,'r')
    except IOError:
        print('load_llzfile: invalid filename.')
        return data

    data=np.loadtxt(filename)
    if flip:
        data[:,[0, 1]] = data[:,[1, 0]]
        
    fp.close()

    return data
    
def load_markerfile(filename=None):
    """
    Loads an label file (lon lat label). 
    """

    data={}
    
    if filename==None:
        print('load_markerfile requires a filename to load.')
        return
    try:
        fp=open(filename,'r')
    except IOError:
        print('load_markerfile: invalid filename.')
        return data
        
    lon=np.array([])
    lat=np.array([])
    label=np.array([])

    for line in fp:
        sline=line.split(' ')
        lon=np.append(lon,float(sline[0]))
        lat=np.append(lat,float(sline[1]))
        label=np.append(label,' '.join(sline[2:]).replace('\n',''))
    
    fp.close()

    data['lon']=lon
    data['lat']=lat
    data['label']=label

    return data
    
    
########################################################################
#
# Code for saving files
#
########################################################################
    
def save_nodfile(data,filename=None):
    """
    Saves a nodfile array as a file.

 
    """
    
    if filename==None:
        print('save_nodfile requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('Can''t make ' + filename)
        return


    for i in range(len(data)):
        fp.write('%f %f\n' % (data[i,0],data[i,1]) )
    
    fp.close()



def save_segfile(segfile,outfile=None):
    """
    Saves a seg file. 
    """


    if outfile==None:
        print('save_segfile requires a filename to save.')
        return
    try:
        fp=open(outfile,'w')
    except IOError:
        print('save_segfile: invalid filename.')
        return

    for seg in segfile:
        fp.write('%s %d\n' % (seg,len(segfile[seg]) ) )
        for i in range(len(segfile[seg])):
            fp.write('%d %f %f\n' % (i+1,segfile[seg][i,0],segfile[seg][i,1] ) )
    fp.close()

    return 


def save_llzfile(data,filename=None):
    """
    Saves a llz array as a file. Takes an Nx3 array 
    """
    
    if filename==None:
        print('save_llz requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('Can''t make ' + filename)
        return

    for i in range(len(data)):
        fp.write('%f %f %f\n' % (data[i,0],data[i,1],data[i,2] ) )

    fp.close()
    
        
def save_neifile(neifile=None,neifilename=None):
    """
    save a .nei file

 
    """
    
    if neifilename==None:
        print('savenei requires a filename to save.')
        return
    try:
        fp=open(neifilename,'w')
    except IOError:
        print('Can''t make ' + neifilename)
        return

    if neifile==None:
        print('No neifile dict given.')
        return

    fp.write('%d\n' % neifile['nnodes'])
    fp.write('%d\n' % neifile['maxnei'])
    fp.write('%f %f %f %f\n' % (neifile['llminmax'][0],neifile['llminmax'][1],neifile['llminmax'][2],neifile['llminmax'][3]))   
   

    for i in range(0,neifile['nnodes']):
        fp.write('%d %f %f %d %f %s\n' % (neifile['nodenumber'][i], neifile['nodell'][i,0], neifile['nodell'][i,1], neifile['bcode'][i] ,neifile['h'][i],np.array_str(neifile['neighbours'][i,].astype(int))[1:-1] ) )

    
    fp.close()


def save_nod2polyfile(segfile,filename=None,bnum=[]):
    """
    Save a nod2poly file from a nod2poly dict. 
    """
    
    if filename==None:
        print('save_nodfile requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('save_nod2polyfile: invalid filename.')
        return data

    dictlen=0
    for key in segfile.keys():
        dictlen+=len(segfile[key])


    fp.write('%d\n' % dictlen )
    if bnum==[]:
        fp.write('%d\n' % len(segfile.keys()) )
    else:
        fp.write('%d\n' % bnum )

    for key in segfile.keys():
        fp.write('%d\n'% len(segfile[key]))
        for i in range(len(segfile[key])):
            fp.write('%f %f %f\n'% (segfile[key][i,0],segfile[key][i,1],0.0))

    fp.close()

   
    return 


def save_markerfile(data,filename=None):
    """
    Saves a markerfile.
    """
    
    if filename==None:
        print('save_markerfile requires a filename to save.')
        return
    try:
        fp=open(filename,'w')
    except IOError:
        print('Can''t make ' + filename)
        return

    for lon,lat,label in zip(data['lon'],data['lat'],data['label']):
        fp.write('{:6f} {:6f} {}\n'.format(lon,lat,label))

    fp.close()



########################################################################
#
#  Misc functions
#
########################################################################        
    
def get_nv(neifile):

    try:
        import pyximport; pyximport.install(language_level=3,setup_args={"include_dirs":numpy.get_include()})
        print('here1')
        import get_nv as gnv
        print('here2')
        neifile['nv']=gnv.get_nvc(neifile['neighbours'],neifile['nnodes'],neifile['maxnei'])
        neifile['trigrid'] = mplt.Triangulation(neifile['lon'], neifile['lat'],neifile['nv'])  
    except:
        print('There was an issue with during using cython falling back to python.')
    
        nv=np.empty((len(neifile['neighbours'])*2,3))    
        
        neighbours=copy.deepcopy(neifile['neighbours'])

        kk=0
        for i in range(neifile['nnodes']-2):
            nei_cnt=1
            for ii in range(neifile['maxnei']-1):
                if neighbours[i,ii+1]==0:
                    break
                nei_cnt=ii+1    
                if neighbours[i,ii]<=(i+1):
                    continue
                if neighbours[i,ii+1]<=(i+1):
                    continue   
                for j in range(neifile['maxnei']):
                    if neighbours[neighbours[i,ii]-1,j]!=neighbours[i,ii+1]:
                        continue
                    nv[kk,:]=[i+1,neighbours[i,ii],neighbours[i,ii+1]]
                    kk=kk+1
                    break

            if (nei_cnt>1):
                for j in range(neifile['maxnei']):
                    if neighbours[i,0]<=(i+1):
                        break
                    if neighbours[i,nei_cnt]<=(i+1):
                        break
                    if neighbours[neighbours[i,0]-1,j] ==0:
                        break    
                    if neighbours[neighbours[i,0]-1,j] !=neighbours[i,nei_cnt]:
                        continue
                    nv[kk,:]=[i+1,neighbours[i,nei_cnt],neighbours[i,0] ]
                    kk=kk+1
                    break
                     
        nv=np.delete(nv,np.s_[kk:],axis=0)
        neifile['nv']=(nv-1).astype(int)  
        neifile['trigrid'] = mplt.Triangulation(neifile['lon'], neifile['lat'],neifile['nv'])   
        
                
    return neifile
    
    
def ncdatasort_old(data,trifinder=False,uvhset=True):
    """
    From the nc data provided, common variables are produced.

    :Parameters: **data** -- a data dictionary of data from a .nc file

    :Returns: **data** -- Python data dictionary updated to include uvnode and uvnodell
    """

    nodexy = np.zeros((len(data['x']),2))
    nodexy[:,0]

    x = data['x']
    y = data['y']
    nv = data['nv']
    lon = data['lon']
    lat = data['lat']

    #make uvnodes by averaging the values of ua/va over the nodes of
    #an element
    nodexy = np.empty((len(lon),2))
    nodexy[:,0] = x
    nodexy[:,1] = y
    uvnode = np.empty((len(nv[:,0]),2))
    uvnode[:,0] = (x[nv[:,0]] + x[nv[:,1]] + x[nv[:,2]]) / 3.0
    uvnode[:,1] = (y[nv[:,0]] + y[nv[:,1]] + y[nv[:,2]]) / 3.0

    nodell = np.empty((len(lon),2))
    nodell[:,0] = lon
    nodell[:,1] = lat
    uvnodell = np.empty((len(nv[:,0]),2))
    uvnodell[:,0] = (lon[nv[:,0]] + lon[nv[:,1]] + lon[nv[:,2]]) / 3.0
    uvnodell[:,1] = (lat[nv[:,0]] + lat[nv[:,1]] + lat[nv[:,2]]) / 3.0
   
    if (uvhset==True):
        uvh= np.empty((len(nv[:,0]),1))   
        uvh[:,0] = (data['h'][nv[:,0]] + data['h'][nv[:,1]] + data['h'][nv[:,2]]) / 3.0
        data['uvh']=uvh

    data['uvnode'] = uvnode
    data['uvnodell'] = uvnodell
    data['nodell'] = nodell
    data['nodexy'] = nodexy

    if ('time' in data):
        data['time']=data['time']+678576

    if ('trigrid' in data)==False:
        if (('nv' in data) and('lon' in data) and ('lat' in data)):
            data['trigrid'] = mplt.Triangulation(data['lon'], data['lat'],data['nv'])  
    
    if ('trigridxy' in data)==False:
        if (('nv' in data) and('x' in data) and ('y' in data)):
            data['trigridxy'] = mplt.Triangulation(data['x'], data['y'],data['nv'])  

    if trifinder==True:
        data['trigrid_finder']=data['trigrid'].get_trifinder()
        data['trigridxy_finder']=data['trigridxy'].get_trifinder()

    return data
    
    
def lcc(lon,lat):
    """
    Given a lon lat converts to x,y and return them and the projection     
    """
    try:
        import pyproj as pyp
    except ImportError:
        print("pyproj is not installed, please install pyproj.")
        return
    
    
    #define the lcc projection
    xmax=np.nanmax(lon)
    xmin=np.nanmin(lon)
    ymax=np.nanmax(lat)
    ymin=np.nanmin(lat)
    xavg = ( xmax + xmin ) * 0.5;
    yavg = ( ymax + ymin ) * 0.5;
    ylower = ( ymax - ymin ) * 0.25 + ymin;
    yupper = ( ymax - ymin ) * 0.75 + ymin;
    
    projstr='lcc +lon_0='+str(xavg)+' +lat_0='+str(yavg)+' +lat_1='+str(ylower)+' +lat_2='+str(yupper)
    proj=pyp.Proj(proj=projstr)
    
    x,y=proj(lon,lat)     
    
    return x,y,proj
    

def get_sidelength(data):
    """
        Takes an FVCOM dictionary and returns it with the average element sidelength added.
    """
    sl=np.zeros([len(data['nv']),])
    sidemin=np.zeros([len(data['nv']),])+100000000
    sidemax=np.zeros([len(data['nv']),])
    
    for i in range(0,len(data['nv'])):
        slmin=0
        for j in range(3):
            slmin=np.sqrt((data['nodexy'][data['nv'][i,j-1],0]-data['nodexy'][data['nv'][i,j],0])**2+(data['nodexy'][data['nv'][i,j-1],1]-data['nodexy'][data['nv'][i,j],1])**2)+slmin
            sidemin[i]=np.min([np.sqrt((data['nodexy'][data['nv'][i,j-1],0]-data['nodexy'][data['nv'][i,j],0])**2+(data['nodexy'][data['nv'][i,j-1],1]-data['nodexy'][data['nv'][i,j],1])**2),sidemin[i]])
            sidemax[i]=np.max([np.sqrt((data['nodexy'][data['nv'][i,j-1],0]-data['nodexy'][data['nv'][i,j],0])**2+(data['nodexy'][data['nv'][i,j-1],1]-data['nodexy'][data['nv'][i,j],1])**2),sidemax[i]])
        sl[i]=slmin/3
        
    data['sl']=sl
    data['slmin']=sidemin
    data['slmax']=sidemax
    
    return data
 
    
def get_dhh(data):
    dh=np.zeros([len(data['nv']),])
    for i in range(0,len(data['nv'])):
        one=data['h'][data['nv'][i,0]]
        two=data['h'][data['nv'][i,1]]
        three=data['h'][data['nv'][i,2]]
        hmin=np.min([one,two,three])
        
        #control points close to zero to avoid division by small numbers
        if ((hmin>=0) and (hmin < 1)):
            hmin=1
        if ((hmin<0) and (hmin > -1)):
            hmin=-1
        
        first=np.fabs(np.fabs(one-two)/hmin)
        second=np.fabs(np.fabs(two-three)/hmin)
        thrid=np.fabs(np.fabs(three-one)/hmin)
	
        dh[i]=np.max([first,second,thrid]);
            
    data['dhh']=dh
    return data
    
    
def sort_boundary(neifile,boundary=1):

    nn=copy.deepcopy(neifile['nodenumber'][neifile['bcode']==boundary]).astype(int)
    nnei=copy.deepcopy(neifile['neighbours'][neifile['bcode']==boundary]).astype(int)
    
    #find the neighbour of the first node
    idx=np.argwhere(nnei==nn[0])[0][0]
    
    #have to use temp values with copy as the standard swap doesn't work when things are swapped again and again.
    #there must be a more python way to hand that....
    tmpval=nn[1].copy()
    nn[1]=nn[idx]
    nn[idx]=tmpval    
    tmpval=nnei[1,:].copy()
    nnei[1,:]=nnei[idx,:]
    nnei[idx,:]=tmpval
   
    for i in range(1,len(nn)-1):
        for j in range(neifile['maxnei']):
            nei=nnei[i,j]
            if nei==0: continue
            idx=np.argwhere(nn[(i+1):]==nei)

            if len(idx)==1:
                tmpval=nn[(i+1)].copy()
                nn[(i+1)]=nn[(idx+i+1)]
                nn[(idx+i+1)]=tmpval                
                tmpval=nnei[(i+1),:].copy()
                nnei[(i+1),:]=nnei[(idx+i+1),:]
                nnei[(idx+i+1),:]=tmpval
                break
                
                
    nn=np.hstack([nn,nn[0]])
    
    return nn
