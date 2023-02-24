rep_res = [145 157 183 151 143 147 153 163 130 148];
med_abs_dev(rep_res)

A = randi([1 50],17,17);
B = randi([1 80],17,17);

org_norm_AB = norm(A*B,"fro"); %norma original producto
org_norm_rAB = norm(producto_robusto(A,B),"fro"); %norma original robusta
%disp(A)
%disp(B)

frob_rob = [];
frob_reg = [];
ind_r = [size(A,1) size(B, 1)];
ind_c = [size(A,2) size(B, 2)];


for i = 0:500
    cornrB = B(ind_r(2),ind_c(2)) + i; %Cambiar valor de la esquina en +1
    B(ind_r(2),ind_c(2)) = cornrB;
    rAB = producto_robusto(A,B);
    %disp(A*B)
    %disp(rAB)
    norm_AB = norm(A*B,"fro"); %norma producto nrml;
    norm_rAB = norm(rAB,"fro"); %norma producto robusto;
    frob_reg = [frob_reg, norm_AB]; %arreglo normas regulares
    frob_rob = [frob_rob, norm_rAB]; %arreglo normas robustas
    B(ind_r(2),ind_c(2)) = cornrB - i; %recuperar esquina orig
end   
absiz = 0:500;
rltv_norm = (1/org_norm_AB)*(abs(frob_reg-org_norm_AB)); %Err relativo normal
rltv_norm_r = (1/org_norm_rAB)*(abs(frob_rob-org_norm_rAB)); %Err rltv robusto

plot(absiz,rltv_norm,LineStyle="-.")
hold on
plot(rltv_norm_r)
hold off

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Comparar MADS y DESVEST
iters = 10;
S_to_cmpr = rand(iters,1); %Data set para comparar robustez
std_S = []; %Arreglo de desv-ests
MAD_S = []; %Arreglo de MADS
org_std = std(S_to_cmpr);
org_MAD = med_abs_dev(S_to_cmpr);
for i = 0:iters
    n = size(S_to_cmpr); 

    S_to_cmpr(n) = S_to_cmpr(n) + i; 
    %Contaminación con dato outlier en el final
    std_S = [std_S, std(S_to_cmpr)];
    MAD_S = [MAD_S, med_abs_dev(S_to_cmpr)];
    S_to_cmpr(n) = S_to_cmpr(n) - i; 
end

absiz2 = 0:iters;
rltv_std = (1/org_std)*(abs(std_S-org_std)); %Err relativo std
rltv_MAD = (1/org_MAD)*(abs(MAD_S-org_MAD)); %Err rltv Mad

plot(absiz2,rltv_std,LineStyle="-.")
hold on
plot(rltv_MAD)
hold off
