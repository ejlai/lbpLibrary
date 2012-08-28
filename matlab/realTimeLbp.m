function histogram = realTimeLbp(img)
% Funkce vytvo�� lbp reprezentaci obr�zku p�edan�ho v parametru img a vrac�
% histogram tohoto obr�zku
% Vol�n� : histogram = imageToLbpR(img)

pdata = libpointer('int32Ptr',img);
res = int32(1:256);
pdata2 = libpointer('int32Ptr',res);
t = calllib('reallbp','RealTimeLbp',size(img,1),size(img,2),pdata, pdata2);
histogram = get(pdata2,'Value');