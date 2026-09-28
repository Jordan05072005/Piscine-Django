# import antigravity
import sys
from linecache import clearcache

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_geohash(latitude: float, longitude: float, precision: int):
    interval_latitude, interval_longitude = [-90, 90], [-180, 180]
    bits, geohash = "", ""
    base32 = "0123456789bcdefghjkmnpqrstuvwxyz"
    if precision <= 0 :
        return print("La précision doit être positive")
    for i in range(precision * 5):
        mid_long = (interval_longitude[1] + interval_longitude[0]) / 2
        mid_lat = (interval_latitude[1] + interval_latitude[0]) / 2
        if longitude <= mid_long:
            bits += "0"
            interval_longitude[1] = mid_long
        else:
            bits += "1"
            interval_longitude[0] = mid_long
        if latitude <= mid_lat:
            bits += "0"
            interval_latitude[1] = mid_lat
        else:
            bits+="1"
            interval_latitude[0] = mid_lat
    for bit in range (0, precision * 5, 5):
        geohash += base32[int(bits[bit: bit + 5], 2)]
    return geohash

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Il manque des arguments")
    else:
        if not (is_float(sys.argv[1]) and is_float(sys.argv[2]) and sys.argv[3].isdigit()):
            print("Les arguments ne sont pas du bon type, float, float, int")
        else:
            print(get_geohash(float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])))

    # assert (get_geohash(48.8588443, 2.2943506, 7) == "u09tunq")
    # assert(get_geohash(45.7640, 4.8357, 7) == "u05kq51")
    # assert(get_geohash(44.7640, 4.8357, 7) != "u05kq51")
    # assert(get_geohash(42.6985, 2.8885, 7) == "spd4ctp")
    # for i in range (1, 13): # au dela de 12, c'est trop petit et donne toujours des valeurs identiques de 11111 + pas utile
    #     print(get_geohash(42.6985, 2.8885, i))

clearcache()





