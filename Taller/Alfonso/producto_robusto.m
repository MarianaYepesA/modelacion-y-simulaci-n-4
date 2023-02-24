%Function to define the robust product of any given matrices. We define the
%dot product between columns as n*median(x1y1 x2y2 ... xnyn)

function Mr = producto_robusto(A, B)
    index_filas = size(A,1);
    index_mults = size(A,2);
    index_colum = size(B,2);
    Mr = [];
    for row = 1:index_filas
        vector_medianas = [];
        for col = 1:index_colum
            vector_elements = [];
            for element = 1:index_mults
                vector_elements = [vector_elements, A(row,element)*B(element,col)];
            end
            vector_medianas = [vector_medianas, median(vector_elements)];
        end
        Mr = [Mr;vector_medianas];
    end
    Mr = index_mults*Mr;
end

