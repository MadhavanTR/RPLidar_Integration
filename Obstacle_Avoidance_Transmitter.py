import math
import serial
ser = serial.Serial('/dev/ttyACM0', 9600)
xref=0
yref=0
def obsavoid(d,a,xd,yd):
    global xref,yref
    betai = []
    xcoordinate = []
    ycoordinate = []
    alpha = math.degrees(math.atan((yd-yref)/(xd-xref)))
    print("alpha is",alpha)
    max = 0   
    dist = 0
    dist1 = 0
    botmax=0
    m = 0       
    gamma = 0    
    jc = 0
    i=0
    flag=0
    dist2 = math.sqrt(math.pow((xd-xref),2)+math.pow((yd-yref),2))
    count=0
    for j in range(0,len(d)):
        xcoordinate.append((d[count])*(math.cos((math.radians(a[count])))))
        ycoordinate.append((d[count])*(math.sin((math.radians(a[count])))))
        count = count+1
    #print(xcoordinate, ycoordinate)
    for j in range (0,len(xcoordinate)-1):
        dist = math.sqrt(math.pow((xcoordinate[j]-xcoordinate[j+1]),2)+math.pow((ycoordinate[j]-ycoordinate[j+1]),2))
        if max<dist:
            max = dist
            jc = j
    print("max=",max)
    print("jc=",jc)    
    m = (ycoordinate[jc+1] - ycoordinate[jc])/(xcoordinate[jc+1]-xcoordinate[jc])
    print("slope is",m)
    dist1 = abs((m*xcoordinate[jc])-ycoordinate[jc])/(math.sqrt(1+math.pow(m,2)))
    gamma = math.degrees(math.acos(dist1/(math.sqrt(math.pow(xcoordinate[jc],2)+math.pow(ycoordinate[jc],2)))))
    print("gamma is",gamma)
    count=0
    for j in range(0,len(d)):
        '''direct, without obstacle'''
        if alpha-gamma<a[j]<alpha+gamma:   
            for i in range(j, j+1):
                if dist2<d[j]:
                    xref = xd
                    yref = yd
                    flag=1    
                else:
                    flag=0
        '''turning by beta, target behind obstacle'''
        if alpha-gamma<a[j]<alpha+gamma and max > 100:  
            for k in range(-90,90):
                betai.append(alpha+k)
            for k in range(0,len(betai)):
                betai[k] = abs(betai[k]-alpha)
            beta = min(betai)
            xref = 500*math.sin(math.radians(alpha+beta))      
            yref = 500*math.cos(math.radians(alpha+beta))
            flag=1
        elif max > 100:
            xref = xd
            yref = yd
            flag=1
            
            #print("b") 
        else:
            flag=0
    if flag==1:
        xref=round(xref,2)
        yref=round(yref,2)
        xrefstr=str(xref)
        yrefstr=str(yref)
        ser.write(xrefstr.encode())
        ser.write(yrefstr.encode())
        print("xref=",xrefstr,"yref=",yrefstr)
        
##        bus = smbus.SMBus(1)
##        bus.write_i2c_block_data(0x15,0,[xd, yd])
        
        '''Devide by 10'''
    else:
        print("Cannot move")
    return xref,yref 

def liscan(xd, yd):
    i=0
    len1=0
    count=0
    d=[]
    a=[]
    lenmax=0
    try:
        d.append([])
        a.append([])
        print('Recording measurments... Press Crl+C to stop.')
        for measurment in lidar.iter_measurments():
            line = (str(measurment))
            '''a[4] = line'''
            angle = line.split(' ')[2][0:(len(line.split(' ')[2])-1)]
            dist = line.split(' ')[3][0:(len(line.split(' ')[3])-1)]
            qual = line.split(' ')[1][0:(len(line.split(' ')[1])-1)]
            qualint = int(float(qual))
            distfl = float(dist)
            anglefl = float(angle)
            if qualint != 0:
                for count in range(count, count+1):
                    d[i].append(distfl)
                    a[i].append(anglefl)
                if count != 0 and a[i][count]<a[i][count-1]:
                    i=i+1
                    d.append([])
                    a.append([])
                    count=-1
                count=count+1
            if i == 6:
                break;
        i=1;
        '''for i in range(1, 6):
            count=0
            print ("\nReading in", i ,"th block", "of length ", len(a[i]), "\n")
            for j in range(1, (len(d[i])+1)):
                print(d[i][count], a[i][count])
                count=count+1'''
        for i in range(1, 6):
            if(len(a[i]) > lenmax):
                    lenmax=len(a[i])
                    len1=i
        #print("d[i]=",d[len1],"\na[i]=",a[len1])
        
        obsavoid(d[len1],a[len1],xd,yd);
    except KeyboardInterrupt:
        print('Stopping.')
    return 
     
from rplidar import RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)
print("Enter the destination x coordinate")
xd = float(input())
print("Enter destination y coordinate")
yd = float(input())
print("xd = ",xd,"yd = ",yd)
while xref!=xd and yref!=yd:
    try:        
        liscan(xd, yd);       
    except:
        PORT_NAME = '/dev/ttyUSB0'
        lidar = RPLidar(PORT_NAME)
        continue
lidar.stop()
lidar.disconnect()





