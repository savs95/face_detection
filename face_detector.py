'''
Created on 10-Nov-2013

@author: savs95
'''
from color import Color
from pyimage import PyImage
from graph import Graph

class FaceDetector(object):
    '''
    classdocs
    '''

    def __init__(self, filename, block_size = 5, min_component_size = 10, majority = 0.5):
        '''
        Constructor - keeps input image filename, image read from the file as a PyImage object, block size (in pixels),
        threshold to decide how many skin color pixels are required to declare a block as a skin-block
        and min number of blocks required for a component. The majority argument says what fraction of
        the block pixels must be skin/hair colored for the block to be a skin/hair block - the default value is
        0.5 (half).
        '''
        # Your code
        self.filename=filename
        self.block_size=block_size
        self.majority=majority
        self.min_component_size=min_component_size
        self.pyimage_obj = PyImage(filename)
        
        

    def skin_green_limits(self, red):
        '''
        Return the limits of normalized green given the normalized red component as a tuple (min, max)
        '''
        return ((-0.776*red*red + 0.5601*red + 0.18), (-1.376*red*red + 1.0743*red + 0.2))


    def is_skin(self, pixel_color):
        '''
        Given the pixel color (as a Color object) return True if it represents the skin color
        Color is skin if hue in degrees is (> 240 or less than or equal to 20) and 
        green is in the green limits and it is not white
        '''
        # Your code
        pix_color=pixel_color.hue_degrees()
        green=pixel_color.g
        limit=self.skin_green_limits(pixel_color.r)
        if(pix_color!=255):
            if(pix_color>240 or pix_color<=20):
                if (green>=limit[0] and green<=limit[1]):
                    return True
        return False            


    def is_hair(self, pixel_color):
        '''
        Return True if the pixel color represents hair - it is if intensity < 80 and ((B-G)<15 or (B-R)<15 or
        hue is between 20 and 40)
        '''
        # Your code
        rgb=pixel_color.rgb_abs()
        if(pixel_color.intensity<80):
            if((rgb[2]-rgb[1])<15 or (rgb[2]-rgb[0])<15 or pixel_color.hue() in range(20,40)):
                return True
        return False    
            

    def is_skin_hair_block(self, block, block_type):
        '''
        Return true if the block (given by the argument 'block' which is the coordinate-tuple for the top-left corner)
        is a skin/hair-block - it is if a majority (as per the threshold attribute) of the pixels in the block are
        skin/hair colored. 'block_type' says whether we are testing for a skin block ('s') or a hair block ('h).
        '''
        # Your code
        pyimage_object=PyImage(self.filename)
        k=pyimage_object.size()
        pixel_x=block[0]
        pixel_y=block[1]
        lst_skin=[]
        lst_hair=[]
        temp_x=0
        while(pixel_x<k[0]):
            temp_y=0
            while(pixel_y<k[1] and temp_y<self.block_size):
                rgb_a=pyimage_object.get_rgba(pixel_x,pixel_y)
                pixel_color=Color(rgb_a)
                if(self.is_skin(pixel_color)):
                    lst_skin.append((pixel_x,pixel_y))
                elif(self.is_hair(pixel_color)):
                    lst_hair.append((pixel_x,pixel_y))  
                pixel_y+=1
                temp_y+=1
            pixel_x+=1
            temp_x+=1
            if(len(lst_skin)>self.majority*self.block_size and  block_type=='s'):
                return True
            elif(len(lst_hair)>self.majority*self.block_size and  block_type=='h'):
                return True
            else:
                return False
                
    def add_neighbour_blocks(self, block, graph):
        '''
        Given a block (given by the argument 'block' which is the coordinate-tuple for the top-left corner)
        and a graph (could be a hair or a skin graph), add edges from the current block to its neighbours
        on the image that are already nodes of the graph
        Check blocks to the left, top-left and top of the current block and if any of these blocks is in the
        graph (means the neighbour is also of the same type - skin or hair) add an edge from the current block
        to the neighbour.
        '''
        # Your code
        pyimage_object=PyImage(self.filename)
        k=pyimage_object.size()
        if(self.is_skin_hair_block(block, 's')):
            if((block[0]-self.block_size)<k[0] and (block[0]-self.block_size)>=0 and self.is_skin_hair_block((block[0]-self.block_size,block[1]), 's')):
                graph.add_edge(block, (block[0]-self.block_size,block[1]))
            if((block[1]-self.block_size)<k[1] and (block[1]-self.block_size)>=0 and self.is_skin_hair_block((block[0],block[1]-self.block_size), 's')):
                graph.add_edge(block, (block[0],block[1]-self.block_size))   
            if((block[1]-self.block_size)<k[1] and (block[0]-self.block_size)<k[0] and (block[1]-self.block_size)>=0 and (block[0]-self.block_size)>=0 and self.is_skin_hair_block((block[0],block[1]-self.block_size), 's')):
                graph.add_edge(block, (block[0]-self.block_size,block[1]-self.block_size))
            if((block[1]-self.block_size)<k[1] and (block[0]+self.block_size)<k[0] and (block[1]-self.block_size)>=0 and (block[0]+self.block_size)>=0 and self.is_skin_hair_block((block[0],block[1]-self.block_size), 's')):
                graph.add_edge(block, (block[0]+self.block_size,block[1]-self.block_size))        
        if(self.is_skin_hair_block(block, 'h')):
            if((block[0]-self.block_size)<k[0] and (block[0]-self.block_size)>=0 and self.is_skin_hair_block((block[0]-self.block_size,block[1]), 'h')):
                graph.add_edge(block, (block[0]-self.block_size,block[1]))
            if((block[1]-self.block_size)<k[1] and (block[1]-self.block_size)>=0 and self.is_skin_hair_block((block[0],block[1]-self.block_size), 'h')):
                graph.add_edge(block, (block[0],block[1]-self.block_size))   
            if((block[1]-self.block_size)<k[1] and (block[0]-self.block_size)<k[0] and (block[1]-self.block_size)>=0 and (block[0]-self.block_size)>=0 and self.is_skin_hair_block((block[0],block[1]-self.block_size), 'h')):
                graph.add_edge(block, (block[0]-self.block_size,block[1]-self.block_size))
            if((block[1]-self.block_size)<k[1] and (block[0]+self.block_size)<k[0] and (block[1]-self.block_size)>=0 and (block[0]+self.block_size)>=0 and self.is_skin_hair_block((block[0],block[1]-self.block_size), 'h')):
                graph.add_edge(block, (block[0]+self.block_size,block[1]-self.block_size))        
         
               
    def make_block_graph(self):
        '''
        Return the skin and hair graphs - nodes are the skin/hair blocks respectively
        Initialize skin and hair graphs. For every block if it is a  skin(hair) block
        add edges to its neighbour skin(hair) blocks in the corresponding graph
        For this to work the blocks have to be traversed in the top->bottom, left->right order
        '''
        # Your code
        graph_object_skin=Graph(None)
        graph_object_hair=Graph(None)
        pyimage_object=PyImage(self.filename)
        k=pyimage_object.size()
        i=0
        while(i<k[0]):
            # 3
            j=0
            while(j<k[1]):
                #  4
                if(self.is_skin_hair_block((i,j),'s')):
                    graph_object_skin.add_node((i,j))
                    self.add_neighbour_blocks((i,j),graph_object_skin)
                j+=self.block_size
            i+=self.block_size
        i=0
        while(i<k[0]):
            #  5
            j=0
            while(j<k[1]):
                # 6
                if(self.is_skin_hair_block((i,j),'h')):
                    graph_object_hair.add_node((i,j))
                    self.add_neighbour_blocks((i,j),graph_object_hair)
                j+=self.block_size
            i+=self.block_size
        
        return graph_object_skin, graph_object_hair


    def find_bounding_box(self, component):
        '''
        Return the bounding box - a box is a pair of tuples - ((minx, miny), (maxx, maxy)) for the component
        Argument 'component' - is just the list of blocks in that component where each block is represented by the
        coordinates of its top-left pixel.
        '''
        # Your code
        temp_y=[]
        temp_x=[]
        size_component=len(component)
        i=0
        while(i<size_component):
            # 7
            temp_y+=[component[i][1]]
            i+=1
        i=0    
        while(i<size_component):
            # 7
            temp_x+=[component[i][0]]
            i+=1    
        return ((min(temp_x),min(temp_y)),(max(temp_x),max(temp_y))) 
       
    
    def skin_hair_match(self, skin_box, hair_box):
        '''
        Return True if the skin-box and hair-box given are matching according to one of the pre-defined patterns
        '''
        # Your code
        skin_coord=self.find_bounding_box(skin_box)
        hair_coord=self.find_bounding_box(hair_box)
        min_x_skin=skin_coord[0][0]
        min_y_skin=skin_coord[0][1]
        max_x_skin=skin_coord[1][0]
        max_y_skin=skin_coord[1][1]
        min_x_hair=hair_coord[0][0]
        min_y_hair=hair_coord[0][1]
        max_x_hair=hair_coord[1][0]
        max_y_hair=hair_coord[1][1]
        if min_x_skin>min_x_hair and max_x_skin<max_x_hair and min_y_skin>min_y_hair and max_y_skin<max_y_hair :
            return True #2
        elif min_x_skin>min_x_hair and max_x_skin<max_x_hair and min_y_skin>min_y_hair and max_y_skin>max_y_hair :
            return True #3
        elif min_x_skin>min_x_hair and max_x_skin<max_x_hair and min_y_skin>min_y_hair and max_y_skin==max_y_hair :
            return True #4
        elif min_x_skin<min_x_hair and max_x_skin<max_x_hair and min_y_skin>min_y_hair and max_y_skin>max_y_hair :
            return True #5
        elif min_x_skin>min_x_hair and max_x_skin>max_x_hair and min_y_skin>min_y_hair and max_y_skin>max_y_hair :
            return True #6
        elif min_x_skin==min_x_hair and max_x_skin<max_x_hair and min_y_skin>min_y_hair and max_y_skin>max_y_hair :
            return True #7
        elif min_x_skin>min_x_hair and max_x_skin==max_x_hair and min_y_skin>min_y_hair and max_y_skin>max_y_hair :
            return True #8
        elif min_x_skin>min_x_hair and max_x_skin<max_x_hair and min_y_skin<min_y_hair and max_y_skin>max_y_hair :
            return True #9
        elif min_x_skin>min_x_hair and max_x_skin>max_x_hair and min_y_skin<min_y_hair and max_y_skin>max_y_hair :
            return True #10
        elif min_x_skin<min_x_hair and max_x_skin<max_x_hair and min_y_skin<min_y_hair and max_y_skin>max_y_hair :
            return True #11
        elif min_x_skin==min_x_hair and max_x_skin<max_x_hair and min_y_skin>min_y_hair and max_y_skin==max_y_hair :
            return True #12
        elif min_x_skin>min_x_hair and max_x_skin--max_x_hair and min_y_skin>min_y_hair and max_y_skin==max_y_hair :
            return True #13
        elif min_x_skin<min_x_hair and max_x_skin>max_x_hair and min_y_skin==max_y_hair:
            return True #14
        elif min_x_skin<min_x_hair and max_x_skin==max_x_hair and min_y_skin==max_y_hair:
            return True #15
        elif min_x_skin==min_x_hair and max_x_skin>max_x_hair and min_y_skin==max_y_hair:
            return True #16
        elif min_x_skin==min_x_hair and max_x_skin==max_x_hair and min_y_skin==max_y_hair:
            return True #1
        else:
            return False
        
    def detect_faces(self):
        '''
        Main method - to detect faces in the image that this class was initialized with
        Return list of face boxes - a box is a pair of tuples - ((minx, miny), (maxx, maxy))
        Algo: (i) Make block graph (ii) get the connected components of the graph (iii) filter the connected components
        (iv) find bounding box for each component (v) Look for matches between face and hair bounding boxes
        Return the list of face boxes that have matching hair boxes
        '''
        # Your code
        #1
        skin_object, hair_object=self.make_block_graph()
        skin_list=skin_object.get_connected_components()
        hair_list=hair_object.get_connected_components()
        final_list=[]
        skin_list_final=[]
        hair_list_final=[]
        for block in skin_list:
            if(len(block)>self.min_component_size):
                bounding_tuple=self.find_bounding_box(block)
                skin_list_final.append(bounding_tuple)
        for block in hair_list:
            if(len(block)>self.min_component_size):
                bounding_tuple=self.find_bounding_box(block)
                hair_list_final.append(bounding_tuple)        
        for s in skin_list_final:
            for h in hair_list_final:
                if(self.skin_hair_match(s,h)==True):
                    if s not in final_list:
                        final_list.append(s)
        #print final_list
        return final_list            
                
        
    
    
    def mark_box(self, box, color):
        '''
        Mark the box (same as in the above methods) with a given color (given as a raw triple)
        This is just a one-pixel wide line showing the box.
        '''
        # Your code
        min_x=box[0][0]
        min_y=box[0][1]
        max_x=box[1][0]
        max_y=box[1][1]
        i=min_x
        while(i<max_x):
            # 8
            self.pyimage_obj.set(i,min_y,(254,0,0))
            self.pyimage_obj.set(i,max_y,(254,0,0))
            i+=1
        i=min_y
        while(i<max_y):
            # 9
            self.pyimage_obj.set(min_x,i,(254,0,0))
            self.pyimage_obj.set(max_x,i,color)
            i+=1


    def mark_faces(self, marked_file):
        '''
        Detect faces and mark each face detected -- mark the bounding box of each face in red
        and save the marked image in a new file
        '''
        # Your code
        face_list=self.detect_faces()
        for i in face_list:
            self.mark_box(i, (254,0,0))
        self.pyimage_obj.save(marked_file)

if __name__ == '__main__':
    detect_face_in = FaceDetector('faces-01.jpeg')
    detect_face_in.mark_faces('yo.jpeg')
    '''detect_face_in = FaceDetector('faces-02.jpeg')
    detect_face_in.mark_faces('marked2.jpeg')
    detect_face_in = FaceDetector('faces-03.jpeg')
    detect_face_in.mark_faces('marked3.jpeg')
    detect_face_in = FaceDetector('faces-04.jpeg')
    detect_face_in.mark_faces('marked4.jpeg')
    detect_face_in = FaceDetector('faces-05.jpeg')
    detect_face_in.mark_faces('marked5.jpeg')'''
