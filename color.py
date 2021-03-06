'''
Created on 11-Nov-2013

@author: savs95
'''
import math

class Color(object):
    '''
    classdocs
    '''


    def __init__(self, rgb):
        '''
        Precompute and keep the normalized values for r, g and b calculated from the raw rgb values given in the argument rgb.
        Raw rgb - (R, G, B) where all three are integers in the range 0-255
        Also have the total raw RGB in case you want to recover the raw rgb values
        The other attribute (apart from total, and normalized rgb values) you would need is intensity - total/3
        '''
        # Your code
        self.total=float(rgb[0]+rgb[1]+rgb[2])
        if(self.total==0):
            self.r=0
            self.g=0
            self.b=0
            self.intensity=0
        else:
            self.r=float(rgb[0])/float(self.total)
            self.g=float(rgb[1])/float(self.total)
            self.b=float(rgb[2])/float(self.total)
            self.intensity=float(self.total/3)
        

    def hue(self):
        '''
        Return the hue in radians - calculated as atan((sqrt(3)*(green-blue))/((red-green) + (red-blue)))
        The color values in the formula are the normalized color values
        You need to check if the denominator is zero and if it is return the appropriate value for the atan.
        '''
        # Your code
        if(((self.r-self.g)+(self.r-self.b))!=0):
            hue_radians=float(math.atan(((math.sqrt(3)*(self.g-self.b))/((self.r-self.g)+(self.r-self.b)))))
            return hue_radians      
        else:
            return float(math.pi/2)           


    def hue_degrees(self):
        '''
        Return the hue in degrees
        '''
        # Your code
        hue_radians=self.hue()
        hue_degree=math.degrees(hue_radians)
        #float(180*hue_radians/float(math.pi))
        return hue_degree

    def rgb_abs(self):
        '''
        Recover and return the raw RGB values as a triple of integers
        '''
        # Your code
        r_raw=self.r*self.total
        g_raw=self.g*self.total
        b_raw=self.b*self.total
        rgb_triple=(r_raw,g_raw,b_raw)
        return rgb_triple

    
