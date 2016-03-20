import os
import collections
import utilities

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

Coord = collections.namedtuple('Coord','i_height, i_width')

class MapGrid:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.terrain = []

    def append(self, row: list):
        self.terrain.append(row)

    def __str__(self):
        str_out = '\n'
        for i in range(self.height):
            str_out +=' '.join(str(x) for x in self.terrain[i])+'\n'
        return str_out

class Terrain(MapGrid):
    NORTH = Coord(-1,0)
    WEST = Coord(0,-1)
    EAST = Coord(0,1)
    SOUTH = Coord(1,0)
    COMPASS = (NORTH, WEST, EAST, SOUTH)

    def get_sinks(self):
        sink_dict = {}
        for i_height in range(self.height):
            for i_width in range(self.width):
                location = Coord(i_height,i_width)
                if self.is_sink(location):
                    sink_dict[location]= len(sink_dict)
        return sink_dict

    def pour(self,location: Coord,sink_dict):
        visited_locations = []
        while True:
            if location in sink_dict:
                for visited_coord in visited_locations:
                    sink_dict[visited_coord]=sink_dict[location]
                return sink_dict[location]
            visited_locations.append(location)
            current_altitude = self.get_altitude(location)
            altitude_min = current_altitude
            for point in self.COMPASS:
                altitude_to_point = self.altitude_of_direction(location,point)
                if altitude_to_point is not None and altitude_to_point<altitude_min:
                    altitude_min = altitude_to_point
                    current_point = point
            location = Coord(location.i_height + current_point.i_height, location.i_width+ current_point.i_width)



    def get_altitude(self, location: Coord):
         return self.terrain[location.i_height][location.i_width]

    def altitude_of_direction(self,location: Coord, direction: Coord = NORTH):
        i_height = location.i_height + direction.i_height
        i_width = location.i_width + direction.i_width
        if i_height < 0 or i_height >= self.height:
            return None
        if i_width < 0 or i_width >= self.width:
            return None
        return self.get_altitude(Coord(i_height,i_width))

    def is_sink(self,location: Coord):
        for point in self.COMPASS:
            altitude = self.altitude_of_direction(location,point)
            if altitude is not None and altitude < self.get_altitude(location):
                return False
        return True

class SinkMap(MapGrid):

    def __init__(self, height, width):
        super().__init__(height, width)
        self.counts = collections.defaultdict(int)
        self.index_map = {}
    def append(self, row: list):
        self.terrain.append(row)
        for i in row:
            if i not in self.index_map:
                self.index_map[i]=chr(len(self.index_map)+ord('a'))

    def __str__(self):
        str_out = '\n'
        for i in range(self.height):
            str_out +=' '.join(str(self.index_map[x]) for x in self.terrain[i])+'\n'
        return str_out

class WaterSheds:
    def __init__(self, height, width,file_pointer: open):
        self.height = height
        self.width = width
        self.terrain = Terrain(height, width)
        self.read_terrain(file_pointer, self.terrain)

    def read_terrain(self, file_pointer: open, terrain : Terrain):
        for i_height in range(self.height):

            terrain.append(utilities.return_int_list(file_pointer.readline()))


    def get_result(self):
        sink_dict = self.terrain.get_sinks()
        sink_map = self.terrain_run_water(sink_dict)
        return str(sink_map)

    def terrain_run_water(self,sink_dict: dict):
        sink_map = SinkMap(self.height,self.width)
        for i_height in range(self.height):
            sink_list = []
            for i_width in range(self.width):
                sink_list.append(self.terrain.pour(Coord(i_height, i_width),sink_dict))
            sink_map.append(sink_list)
        return sink_map




def write_output_file(large=False):
    text = "large" if large else 'small'
    file_name = os.path.join(__location__, 'B-%s-practice.' % text)
    file_read, file_write = utilities.get_file(file_name)
    number_of_cases = int(file_read.readline())
    for i in range(0, number_of_cases):
        height, width = utilities.return_int_list(file_read.readline())
        water_sheds = WaterSheds(height, width, file_read)
        out_str = 'Case #%s:%s' % (i + 1, water_sheds.get_result())
        file_write.write(out_str)
        print(out_str)
    file_read.close()
    file_write.close()


write_output_file(True)
