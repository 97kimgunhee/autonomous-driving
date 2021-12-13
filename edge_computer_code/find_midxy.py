import cv2


def midxy(x1,y1,x2,y2):
    k=(x2-x1)/2
    new_x=x1+k
    q=(y2-y1)/2
    new_y=y1+q
    new_x=int(new_x)
    new_y=int(new_y)

    return new_x,new_y
