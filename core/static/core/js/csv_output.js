
 
function download_csv(resp,td1,td2,td3) {
console.log(resp.tir);
    
var data = [
   ['VPN social ( '+ td1*100 + '%)', resp.vpn_social_1, 'mdp', '(+/-' + resp.vpn_social_1_err + ')', 'Desv. Est', resp.vpn_social_1_std],
   ['VPN social ( '+ td2*100 + '%)', resp.vpn_social_2, 'mdp', '(+/-' + resp.vpn_social_2_err + ')', 'Desv. Est', resp.vpn_social_2_std],
   ['VPN social ( '+ td3*100 + '%)', resp.vpn_social_3, 'mdp', '(+/-' + resp.vpn_social_3_err + ')', 'Desv. Est', resp.vpn_social_3_std],
   ['VPN de externalidades', resp.vpn_externalidades, 'mdp','','',''],
   ['VPN privado', resp.vpn_privado,'%','','',''],
   ['Costos ', resp.costos, 'mdp', '(+/-' + resp.costos_err +')','',''],
   ['Beneficios ', resp.beneficios,'mdp','(+/- ' + resp.beneficios_err +')','',''],
   ['ICB ',resp.icb,'pesos/invertido','','',''],
   ['FAE  ( '+ td1*100 + '%)',resp.fae_1,'pesos/año','','',''],
   ['FAE  ( '+ td2*100 + '%)',resp.fae_2,'pesos/año','','',''],
   ['FAE  ( '+ td3*100 + '%)',resp.fae_3,'pesos/año','','',''],
   ['Plazo ',resp.plazo,'años','(+/-' + resp.plazo_err +')','',''],
   ['ICE ',resp.ice,'pesos /tC','(+/- '+ resp.ice_err +' )','',''],
   ['Cantidad ICE ', resp.cantidad_ice,'(+/- '+ resp.ice_err + '0)','','',''],
   ['VPN pesim ( '+ td1*100 + ' %) ',resp.vpn_pesimista,'mdp','p > y_pesim =' + resp.vpn_pesimista_R + '%','',''],
   ['VPN neut ( '+ td2*100 + '%) ',resp.vpn_base,'mdp','p > y_pesim = ' + resp.vpn_base_R + '%','',''],
   ['VPN opt ( '+ td3*100 + ' %) ',resp.vpn_optimista,'mdp','p > y_pesim = '+ resp.vpn_optimista_R + '%','',''],
   ['TIR ',resp.tir,'%','(' + resp.tir_2 +'|'+ resp.tir_3 + ')','',''],
   ['% de casos con VPN positivo',resp.casos_positivos,'%','','','']
];
 
    
     
    var csv = 'V1,V2,V3,V4,V5,V6\n';
    data.forEach(function(row) {
            csv += row.join(',');
            csv += "\n";
    });
 
    console.log(csv);
    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'resultados.csv';
    hiddenElement.click();
}
 

function download_flow(flowTable, col_sum) {
var data = [];
var years = "";
var line = "\n";
    
    
    for(var x = 0;  x < flowTable.length; x++){
        flowTable[x]["Total"] =  flowTable[x]["Total"].toString().replace(/[#,]/g,'');
        flowTable[x]["Total_porc"] =  flowTable[x]["Total_porc"].toString().replace(/[#,]/g,'');
        flowTable[x]["Descripcion"] =  flowTable[x]["Descripcion"].toString().replace(/[#,]/g,'');
        flowTable[x]["Concepto"] =  flowTable[x]["Concepto"].toString().replace(/[#,]/g,'');
        flowTable[x]["Elasticidad"] =  flowTable[x]["Elasticidad"].toString().replace(/[#,]/g,'');
        flowTable[x]["Quiebre"] =  flowTable[x]["Quiebre"].toString().replace(/[#,]/g,'');
    }

    for(var x = 0;  x < (Object.keys(flowTable[2]).length - 8); x++){
        if (col_sum[x] != null){
        flowTable[flowTable.length-1]["Ano"+(x+1)] = col_sum[x].toFixed(2);
        }
//        console.log(Object.keys(flowTable[3]).length - 9);
    }
    
    for(var x = 0;  x < flowTable.length; x++){
        data.push(Object.values(flowTable[x]))
    }

for(var x = 0;  x < (Object.keys(flowTable[0]).length - 8)
; x++){    
  var str2 = " Año " + [x+1] + ",";
  years = years.concat(str2);
}
    

    
    var csv = 'ID,CONCEPTO,DESCRIPCIÓN,TOTAL,TOTAL_PORC,ELASTICIDAD,PUNTO DE QUIEBRE,';
    csv = csv.concat(years);
    csv = csv.concat(line);
    data.forEach(function(row) {
            row.toString().replace(',','');
        
            csv += row.join(',');
            csv += "\n";
    });
 
    var hiddenElement = document.createElement('a');
    csv= csv.replace("Total, , ,","Total, ,");
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'flujo.csv';
    hiddenElement.click();
}
