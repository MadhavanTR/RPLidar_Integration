fileID = fopen('G:\New Project\Experiment\a.txt');
C = textscan(fileID,'%f32 %f32');
fclose(fileID);
x = cell2mat(C);
a = x(:,1);
d = x(:,2);
xref =0;
yref =0;
xd =100;
yd =100;
max = 0;
alpha = radtodeg(atan(yd-yref)/(xd-xref));
fprintf('alpha is %i',alpha);
dist2 = sqrt((xd-xref).^2+(yd-yref).^2);
fprintf('distance between initial point and destination is %i',dist2)
while xref~=xd
 
    for i=1:length(d)
      x(i)=d(i)*cos(radtodeg(a(i)));
      y(i)=d(i)*sin(radtodeg(a(i)));
    end
    for j=1:length(d)-1
        dist = sqrt(((x(j)-x(j+1)).^2)+((y(j)-y(j+1)).^2));
    if (max<dist)
        max = dist;
        jc = j;
    end       
    end
    fprintf('max is %f',max);
    fprintf('jc is %i',jc);
    m = (y(jc+1)-y(jc))/(x(jc+1)-x(jc));
    fprintf('slope is %f',m);
    dist1 = abs((m*x(jc)-y(jc))/sqrt(1+m.^2));
    gamma = radtodeg(acos(dist1/sqrt((x(jc).^2)+(y(jc).^2))));
    fprintf('gamma is %i',gamma);
    for b = 1:length(d)
    if alpha-gamma < a(i) <alpha+gamma && dist2<d(i)
        fprintf('xd = %i yd = %i',xd,yd);
    elseif alpha-gamma < a(i) <alpha+gamma && max>400
        for k = -90:90
            for k1 = 0:900
                betai(k1) = alpha+k;
                fprint('betai values %i',betai);
            end
            
        end
        beta = betai(0)-alpha;
        for h = 1:length(betai)
            if beta>(betai(h)-alpha)
                beta = betai(h)-alpha;
            end
        end
        xd = 500*cos(alpha+beta);
        yd = 500*sin(alpha+beta);
        fprintf('xd = %i yd = %i', xd,yd);
    else 
        fprintf('xd = %i yd = %i',xd,yd);
         
    end 
    end
end