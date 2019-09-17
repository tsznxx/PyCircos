#!/usr/bin/env python3
# coding: utf-8
# branch: dev
# version: 1.0.2
# license: AGPLv3
# author: Yunfei Wang (yfwang0405@gmail.com)
#         Baochen Yang (yangbaochen1217@gmail.com) 


import os
import sys
import pandas
import numpy
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch

class Utils(object):
    def naturalkeys(text):
        '''
        nlist = sorted(old_list,key=natural_keys) #sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        '''
        import re
        def atoi(text):
            return int(text) if text.isdigit() else text
        return [ atoi(c) for c in re.split('(\d+)', text) ]
    naturalkeys=staticmethod(naturalkeys)
    
    
class Circos(object):
    '''
    Python Circos.
    '''
    def __init__(self,data,length='length',figsize=(10,10),gap=0.5):
        '''
        Initiation from a list of beds.
        Parameters:
            data: pandas.DataFrame
                chomosome regions, with index as chromosome IDs, and size as chromosizes.
            size: string
                column name for chrom sizes
            figsize: tuple or list of floats
                width x height
            gap: float
                gap between each Bed.  
        '''
        self.regions = data        
        self.regions =self.regions.loc[sorted(self.regions.index,key=Utils.naturalkeys),:] # the gid order of the beds
        total_len = self.regions.length.sum()
        self.len_per_degree = total_len/(360.-gap*data.shape[0])
        self.len_per_theta  = total_len/(numpy.pi*2-numpy.deg2rad(gap)*data.shape[0])
        # chromosome start thetas
        cumlen = [0] + list(self.regions.length.cumsum())[:-1] # accumulative length
        self.regions['theta_start'] = [numpy.deg2rad(l/self.len_per_degree+gap*i) for i,l in enumerate(cumlen)]
        # polar axis
        self.fig = plt.figure(figsize=figsize)
        l = max(figsize)
        self.pax = self.fig.add_axes([0,0,1,1],polar=True)
        self.pax.axis('off')
        self.pax.set_ylim(0,l)
    def get_theta(self,gid,pos):
        '''
        get the theta of the position.
        Parameters:
            gid: string or list
                chrom labels
            pos: int or list
                chrom coordinates
        Note:
            gid and pos must be the same length if they are lists.
        '''        
        if isinstance(pos,int) or isinstance(pos,float):
            et = self.regions.loc[gid,'theta_start']+pos/self.len_per_theta
            return et
        # iterable
        ets = [self.regions.loc[g,'theta_start']+(p/self.len_per_theta) for g,p in list(zip(gid,pos))]
        return ets
    def draw_scaffold(self,rad,width,colors=[],fill=False,**kwargs):
        '''
        Draw scaffold.
        Parameters:
            rad: float
                radius.
            width: float
                width of the band. negative width means inner width. eg. rad=8,width=1 equal to rad=9,width=-1.
            colors: list of colors
                cycling colors. at least two colors.
            alpha: float
                alpha value.
        '''
        mtick = numpy.deg2rad(50000000/self.len_per_degree)
        n = len(colors)  
        if fill == False or n == 0:
            kwargs.update({'edgecolor':'k','linewidth':1,'linestyle':'-','fill':False})
        else:
            kwargs.update({'linewidth':0})              
        for i,gid in enumerate(self.regions.index):
            if n:
                kwargs['color'] = colors[i%n]
            et1, et2 = self.regions.theta_start[gid], self.get_theta([gid],[self.regions.length[gid]-1])            
            self.pax.bar([(et1+et2)/2],[width],width=et2-et1,bottom=rad,**kwargs)            
    def draw_ticks(self,rad,tick_length,tick_gap=50000000,unit=1000000,unit_label='M',inside=False,**kwargs):
        '''
        Draw ticks.
        Parameters:
            rad: float
                radius
            tick_length: float
                tick length
            tick_gap: float
                gap between ticks
            unit: float
                the ticklabels shown in unit.
            unit_label: string
                eg. 1000 to 'K', 1000000 to 'M'
            inside: bool
                draw ticks inside
            kwargs: dict
                parameters to vlines                
        '''
        ml = max([len("{0}{1}".format(int(self.regions.loc[gid,'length']/unit),unit_label)) for gid in self.regions.index ]) # max ticklabel length
        for i,gid in enumerate(self.regions.index):
            et1, et2 = self.regions.theta_start[gid], self.get_theta([gid],[self.regions.length[gid]-1])
            ets = numpy.arange(et1,et2,tick_gap/self.len_per_theta)
            if inside:
                self.pax.vlines(ets,[rad]*len(ets),[rad-tick_length]*len(ets))
            else:
                self.pax.vlines(ets,[rad]*len(ets),[rad+tick_length]*len(ets)) 
            for j,et in enumerate(ets): 
                lstr = "{0}{1}".format(j*tick_gap/unit,unit_label)
                if inside:
                    lstr = ' '*(ml-len(lstr)) + lstr
                    self.pax.annotate(lstr,xy=[et,rad-tick_length-ml*0.1], ha='center',va='center',rotation=numpy.rad2deg(et))
                else:
                    lstr += ' '*(ml-len(lstr))
                    self.pax.annotate(lstr,xy=[et,rad+tick_length+ml*0.1], ha='center',va='center',rotation=numpy.rad2deg(et))
    def draw_cytobands(self,rad,width,cbfile,**kwargs):
        '''
        Draw cytobands.
        Parameters:
            rad: float
                radius
            width: float
                width of the band
            cbfile: string
                UCSC cytoband file
            kwargs: dict
                parameters passed to pax.bar                
        '''
        cyto_colors = {"gneg":"#FFFFFF","gpos25":"#E5E5E5","gpos50":"#B3B3B3","gpos75":"#666666",
                       "gpos100":"#000000","gvar":"#FFFFFF","stalk":"#CD3333","acen":"#8B2323"}
        cb = pandas.read_table(cbfile,index_col=None,header=None,names=['chrom','start','end','band','color'])
        cb['color'] = [cyto_colors[c] for c in cb.color]
        cb['et1'] = self.get_theta(cb.chrom,cb.start)
        cb['et2'] = self.get_theta(cb.chrom,cb.end)
        cb['etm'] = cb.loc[:,['et1','et2']].mean(axis=1)
        cb['etw'] = cb['et2']-cb['et1']
        self.pax.bar(cb.etm,[width]*cb.shape[0],width=cb.etw,bottom=rad,color=cb.color,**kwargs)   
    def draw_scaffold_ids(self,rad,inside=False,**kwargs):
        '''
        Draw scaffold region IDs.
        Parameters:
            rad: float
                radius
            inside: bool
                draw chrom labels inside
            kwargs: dict
                to ax.annotate()
                    fontsize, rotation
        '''        
        kwargs.setdefault('ha','center')
        kwargs.setdefault('va','center')
        rotation = kwargs.get('rotation',0)
        ml = max([len(gid) for gid in self.regions.index])
        for gid in self.regions.index:
            deg = numpy.rad2deg(self.get_theta(gid,self.regions.length[gid]/2))
            kwargs['rotation'] = rotation + deg
            if 90 < kwargs['rotation'] < 270:
                kwargs['rotation'] += 180
            if inside: # add spaces to the right side
                lstr = ' '*(ml-len(gid)) + gid                  
            else:
                lstr = gid + ' '*(ml-len(gid))                  
            self.pax.annotate(gid,xy=[numpy.deg2rad(deg),rad],**kwargs)
    def fill_between(self,rad,data,gid='chrom',start='start',end='end',score='score',cutoff=0.1,scale=1.,**kwargs):
        '''
        Draw densities.
        Parameters:
            rad: float
                radius
            data: pandas.DataFrame
                chromosomal regions
            start, end: int
                chrom start or end
            score: float
                chrom interval scores
            cutoff: float
                abs(value) < cutoff are filled in grey
            scale: float
                scalling factor of original scores
            kwargs: dict
                parameters passed to ax.fill_between
        '''
        rads = [rad,rad]
        facecolor = kwargs.get('facecolor','red')
        for gid, start, end, score in zip(data[gid],data[start],data[end],data[score]):
            ets = self.get_theta([gid,gid],[start,end])
            kwargs['facecolor'] = facecolor if abs(score)>cutoff else 'grey'                
            score = scale*score + rad
            self.pax.fill_between(ets,rads,[score, score],**kwargs)
    def draw_link(self,rad,gids,starts,ends,color=None,alpha=1.):
        '''
        Draw links
        Parameters:
            rad: float
                radius
            gids: list
                list of two chroms
            starts, ends: list
                list of start/end coordinates
            color: string
                face color
            alpha: float
                alpha            
        '''
        ets = self.get_theta(gids,starts)
        ete = self.get_theta(gids,ends)
        points = [(ets[0],rad), # start1
                  ((ets[0]+ete[0])/2,rad), # through point
                  (ete[0],rad), # end 1
                  (0,0), # through point
                  (ets[1],rad), # start2
                  ((ets[1]+ete[1])/2,rad), # through point
                  (ete[1],rad), # end2 
                  (0,0), # through point
                  (ets[0],rad)]
        # parse patches
        codes = [Path.CURVE3]*len(points)
        codes[0] = Path.MOVETO
        path = Path(points, codes)
        patch = PathPatch(path, facecolor=color, lw=0.2,alpha=alpha)
        self.pax.add_patch(patch)

# ------------------------------------
# Main
# ------------------------------------

if __name__=="__main__":
    pass    
