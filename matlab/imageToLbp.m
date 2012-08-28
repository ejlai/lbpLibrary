function imgOut = imageToLbp(imgIn, type, radius, samples)
% Funkce vytvo�� lbp reprezentaci obr�zku p�edan�ho v parametru img a vrac�
% obr�zek v LBP reprezentaci
% Vol�n� : imgOut = imageToLbp(imgIn, type, radius, samples)
% Type : 1 - klasicke LBP,2 - uniform, 3 - 5 RotMin 8 - 32 bit

type = type + 15;
pdata = libpointer('doublePtr',imgIn);
t = calllib('lbp','imageToLbp',size(imgIn,1),size(imgIn,2),pdata, type, radius, samples);
imgOut = get(pdata,'Value');