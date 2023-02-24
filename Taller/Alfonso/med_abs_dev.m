%Medn_Abs_devs
function mad = med_abs_dev(vector_medidas)
    median_v = median(vector_medidas);
    vector_medidas = abs(vector_medidas-median_v);
    mad = median(vector_medidas);
end