


from math import radians, cos, sin, asin, sqrt

#Replicating haversine distance formula in python 

def dist(lat1, long1, lat2, long2):
    """
    Implements haversine formula for computing distance between two points
    on a sphere. 
    """
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula 
    dlon = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

def find_nearest(points_of_interest,lat, long):
    distances = points_of_interest.apply(
        lambda row: dist(lat, long, row['lat'], row['lon']), 
        axis=1)
    return distances.min()



def min_dist(colname,points_of_interest, listings):
    listings[colname] = listings.apply(
    lambda row: find_nearest(points_of_interest,row['lat'], row['lon']), 
    axis=1)
    return(listings)


