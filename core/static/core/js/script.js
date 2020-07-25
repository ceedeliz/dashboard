//estaticas  djksaskdajkskls


var dataTable = [];

    var ano_actual ={};
    var total_x = [];
    var col_noFormat = [];
    var total_noFormat = [];
    var sumTotal_noFormat = [];
function fillTable(resp){
    //alert(resp.total_anos);
    for (i = 0; i < resp.detalles.length; i++) {
        dataTable.push({
            ID_: i+1,
            Concepto: resp.detalles[i],
            Descripcion: resp.cb_categoria[i],
            Total: 0,
            Total_porc: 'Total_porc',
            Elasticidad: 'Elasticidad',
            Quiebre: 'Punto de quiebre',
        });
            for (y = 0; y < resp.facum.length;y++){
                if((i+y*resp.filas_totales) < resp.fna_d_R.length){
                   dataTable[i]["Ano"+(y+1)] = resp.fna_d_R[i+y*resp.filas_totales] ;
                }
            } 
                       
        total_x=0;
        if(!resp.ano_cerrado){
            if(resp.ano_incompleto[i]){
                dataTable[i]["Ano"+resp.facum.length] = resp.fna_d_R[resp.fna_d_R.length-i];
            }else{
                dataTable[i]["Ano"+resp.facum.length] = 0;
            }
        }

        for (y = 0; y < resp.facum.length;y++){
            if((i+y*resp.filas_totales) < resp.fna_d_R.length){
               dataTable[i]["Total"] =dataTable[i]["Total"] + parseFloat(dataTable[i]["Ano"+(y+1)]);          
            }
        }
        

    if(resp.cb_impacto[i] == "Positivo"){
         dataTable[i]["Total_porc"] = formatNumber(parseFloat(dataTable[i]["Total"])/ parseFloat(resp.beneficios)*100) + "%";
    }else{
         dataTable[i]["Total_porc"] = formatNumber(parseFloat(dataTable[i]["Total"])/ parseFloat(resp.costos)*100) + "%";
    }
        dataTable[i]["Elasticidad"] = parseFloat(dataTable[i])

    }
        dataTable.push({
            ID_: parseInt(resp.filas_totales)+1,
            Concepto: "Total",
            Descripcion: ' ',
            Detalle: ' ',   
            Total: " ",
            Total_porc: ' ',
            Elasticidad: ' ',
            Quiebre: 'Total7',
        });

        var sum_row =[];
        var sum_all = -1;
    
for (y = 0; y < resp.facum.length;y++){
    var sum_col = 0;
    for(x = 0; x < resp.filas_totales; x++){
                sum_all = sum_all + 1;
                sum_col = sum_col + parseFloat(resp.fna_d_R[sum_all]);
        }

    sum_row.push(formatNumber(sum_col));
    col_noFormat.push(sum_col);
}
    console.log("años");
    console.log(col_noFormat);

for (y = 0; y < resp.facum.length;y++){
       dataTable[i]["Ano"+(y+1)] = sum_row[y];
}
        var sum_total= 0;

for (i = 0; i < resp.detalles.length; i++) {
    sum_total = sum_total + parseFloat(dataTable[i]["Total"]); 
}
dataTable[parseInt(resp.filas_totales)]["Total"] = formatNumber(sum_total);
for (i = 0; i < resp.detalles.length; i++) {
    dataTable[i]["Elasticidad"] = Math.abs(formatNumber(dataTable[i]["Total"]/sum_total));
    elasticidad.push(Math.abs(formatNumber(dataTable[i]["Total"]/sum_total)));
}
for (i = 0; i < resp.detalles.length; i++) {
    dataTable[i]["Quiebre"] = (formatNumber(1/dataTable[i]["Elasticidad"]) * 100);
    if(dataTable[i]["Quiebre"] % 1 == 0){
        dataTable[i]["Quiebre"] = (dataTable[i]["Quiebre"]).toFixed(1);
    }
    if((dataTable[i]["Quiebre"]).toString().match(/^-?\d+(?:\.\d{0,1})?/)){
        dataTable[i]["Quiebre"] = (dataTable[i]["Quiebre"]).toString().match(/^-?\d+(?:\.\d{0,1})?/)[0];

    }
    dataTable[i]["Quiebre"] = (dataTable[i]["Quiebre"]) + "%";
    punto_de_quiebre.push(dataTable[i]["Quiebre"]);
    
}
for (i = 0; i < resp.detalles.length; i++) {
    dataTable[i]["Total"] = formatNumber(dataTable[i]["Total"]);
    total_noFormat.push(dataTable[i]["Total"]);
}


var TestData = {
    data: dataTable,
    columns: columns
}
var columns = {
    'ID_': 'ID_',
    'Concepto': 'Concepto',
    'Descripcion': 'Descripción',
    'Total': 'Total',
    'Total_porc': 'Total_porc',
    'Elasticidad': 'Elasticidad',
    'Quiebre': 'Punto de quiebre'
};

for(i = 1; i <= resp.total_anos; i++){
         columns["Ano"+[i]]= "Año "+[i];
         //console.log(columns);
}
var TestData = {
    data: dataTable,
    columns: columns
};
var table = $('#root').tableSortable({
    data: TestData.data,
    columns: TestData.columns,
    dateParsing: true,
    processHtml: function(row, key) {
        if (key === 'avatar_url') {
            return '<a href="' + row[key] + '" target="_blank">View Avatar</a>'
        }
        if (key === 'url') {
            return '<a href="' + row[key] + '" target="_blank">Github Link</a>'
        }
        if (key === 'site_admin' && row[key]) {
            return '<span class="btn btn-warning btn-sm">Admin</span>'
        }
        return row[key]
    },
    columnsHtml: function(value, key) {
        return value;
    },
    pagination: 100,
    showPaginationLabel: true,
    prevText: 'Prev',
    nextText: 'Next',
    searchField: $('#search'),
    responsive: [
        {
            maxWidth: 992,
            minWidth: 769,
            columns: TestData.col,
            pagination: true,
            paginationLength: 3
        },
        {
            maxWidth: 768,
            minWidth: 0,
            columns: TestData.colXS,
            pagination: true,
            paginationLength: 2
        }
    ]
});
}
  $("#save_flow").click(function(){
      flowTable = dataTable;
      download_flow(flowTable,col_noFormat);
  });

