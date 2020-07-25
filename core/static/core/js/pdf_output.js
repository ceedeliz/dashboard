function custom_img(){
    var res = "";
var template1 = [];

    var xhr = new XMLHttpRequest(); 
    var img_custom = $('#input_img').val();
    xhr.open("GET", img_custom, true); 
    xhr.responseType = "blob";
    xhr.onload = function (e) {
            var reader = new FileReader();
            reader.onload = function(event) {
               res_img = event.target.result;
                template1.push(res_img);
            }
            var file = this.response;
            reader.readAsDataURL(file)
    };
    xhr.onerror = function(e){
        alert("Tipo de imagen no soportado");
    }
    xhr.send();
    
}

    

function generate_pdf(resp){ 
    
    
   var doc = new jsPDF('p','mm','letter');
//   doc.addImage(template1[0], 'JPEG',0,0,215.9,279.4);
   var proyecto = $('#input_Proyecto').val();
   var unidad_analisis = $('#input_unidad').val();
   var potencial = $('#input_potencial').val();
   var autor = $('#input_autor').val();
   var medida = $('#input_Medida').val();
   var descripcion = $('#input_descripcion').val();
   var interpretacion = $('#input_interpretacion').val();
   var recomendaciones = $('#input_recomendaciones').val();
   var td1 = (parseFloat($("#ex1").val())*100).toString()+ "%";
   var td2 = (parseFloat($("#ex2").val())*100).toString()+ "%";
   var td3 = (parseFloat($("#ex3").val())*100).toString()+ "%";
    var cell_prop            = resp.cb_prop;
    var cell_tipo           = resp.cb_tipo;
    var cell_frecuencias    = resp.cb_frecuencias;
    var cell_impacto         = resp.cb_impacto;
    var cell_unidad_medida  = resp.cb_unidad_medida;
    var cell_detalle        = resp.cb_detalle;
    var cell_p              = resp.cb_p;
    var cell_p_pes          = resp.cb_p_pes;
    var cell_p_opt          = resp.cb_p_opt;
    var cell_categoria      = resp.cb_categoria;
    var cell_modelo         = resp.cb_modelo;
    var cell_cantidad       = resp.cb_cantidad;
    var cell_cantidad_pes   = resp.cb_cantidad_pes;
    var cell_cantidad_opt   = resp.cb_cantidad_opt;
    var cell_fecha_inicio   = resp.cb_fecha_inicio;
    var cell_fecha_final    = resp.cb_fecha_final;
    var cell_externalidad   = resp.cb_externalidad;
    var cell_coef1 = resp.cb_coef1;
    var cell_coef2 = resp.cb_coef2;
    var cell_coef3 = resp.cb_coef3;
    
    var rows1= [
    ];
    var rows2 =[
    ];

    for(var i = 0; i < cell_detalle.length; i++){
             rows1.push(new Array());
//             console.log(rows1);
             rows1[i].push(i+1);
             rows1[i].push(cell_tipo[i]);
             rows1[i].push(cell_impacto[i]);
             rows1[i].push(cell_categoria[i]);
             rows1[i].push(cell_detalle[i]);    
             rows1[i].push(cell_prop[i]);
             rows1[i].push(cell_frecuencias[i]);
             rows1[i].push(cell_unidad_medida[i]);
             rows1[i].push(cell_cantidad[i]);
             rows1[i].push(cell_externalidad[i]);

             rows2.push(new Array());
             rows2[i].push(cell_cantidad_pes[i]);
             rows2[i].push(cell_cantidad_opt[i]);
             rows2[i].push(cell_p[i]);
             rows2[i].push(cell_p_pes[i]);
             rows2[i].push(cell_p_opt[i]);
             rows2[i].push(cell_fecha_inicio[i]);
             rows2[i].push(cell_fecha_final[i]);
             rows2[i].push(cell_modelo[i]);
             rows2[i].push(cell_coef1[i]);
             rows2[i].push(cell_coef2[i]);
             rows2[i].push(cell_coef3[i]);
    }
 //   var department = $('#department').val();
 //   var title = $('#title').val();
    //doc.splitTextToSize(company, 180);
    doc.setFontSize(18);
    doc.setDrawColor(color_value["r"],color_value["g"],color_value["b"]);
    doc.setLineWidth(1);
    doc.line(0, 20, 270, 20);
    doc.line(0, 260, 270, 260);

    doc.setTextColor(color_value["r"],color_value["g"],color_value["b"]);
    doc.addImage(res_img, 'JPG',9,3,40,12);
    //800 235 - 400 117 - 200 59 

    doc.text(30,30,"Ficha de resultados del análisis costo beneficio social");
    doc.setFontSize(14);
    doc.text(10,52,"Nombre de la medida:");
    doc.text(10,72,"Nombre del proyecto:");
    doc.text(10,  92, "Elaboró: ");
    doc.text(10, 156, "Descripción de la medida: ");

    doc.setTextColor(36, 37, 41);
    doc.text(65, 52, doc.splitTextToSize(medida, 120));
    doc.text(65, 72, doc.splitTextToSize(proyecto, 120));
    doc.text(10, 166, doc.splitTextToSize(descripcion, 190));

//  doc.setTextColor(color_value["r"],color_value["g"],color_value["b"]);
    
//    doc.text(27, 84, doc.splitTextToSize(eje, 160));
//    doc.text(100, 84, doc.splitTextToSize(categoria, 160));
//    doc.text(166, 84, doc.splitTextToSize(pasta, 160));
//    doc.text(46, 112, doc.splitTextToSize(medida, 120));
    doc.text(10, 96+30, "Unidad de análisis: ");
    doc.text(10, 102+30, "Universo potencial: ");
    doc.text(10, 108+30, "Horizonte de evaluación: ");
    doc.text(111, 96+30, "Tasa de descuento mínima: ");
    doc.text(111, 102+30, "Tasa de descuento media: ");
    doc.text(111, 108+30, "Tasa de descuento máxima: ");
    doc.text(30, 92, autor);

    
    doc.setTextColor(color_value["r"],color_value["g"],color_value["b"]);
    doc.text(66, 96+30, unidad_analisis);
    doc.text(66, 102+30, potencial);
    doc.text(66, 108+30, (resp.cb_mes_final/12).toString().substr(0,8));
    doc.text(174, 96+30, td1);
    doc.text(174, 102+30, td2);
    doc.text(174, 108+30, td3);


    doc.addPage(); 
//  doc.addImage(template1[1], 'JPEG',0,0,215.9,279.4);
    doc.setTextColor(color_value["r"],color_value["g"],color_value["b"]);
    doc.setFontSize(18);
    doc.text(70.8,30, "Resultados de rentabilidad");

    doc.setFontSize(10);
    doc.setDrawColor(color_value["r"],color_value["g"],color_value["b"]);
    doc.setLineWidth(1);
    doc.line(0, 20, 270, 20);
    doc.line(0, 260, 270, 260);

    
    doc.setDrawColor(color_value["r"],color_value["g"],color_value["b"]);
    doc.setLineWidth(1);
    doc.line(0, 20, 270, 20);
    doc.line(0, 260, 270, 260);
    
    doc.setTextColor(color_value["r"],color_value["g"],color_value["b"]);
    doc.text(23, 60, "Parámetro");
    doc.text(82, 60, "Valor");
    doc.text(128, 60, "Unidad");
    doc.text(168, 57, "Error.");
    doc.text(168, 60, "estándar");
    doc.text(190, 57, "Desv.");
    doc.text(190, 60, "estándar");

    doc.setTextColor(36, 37, 41);
    
    doc.text(16, 71, "Valor Presente");
    doc.text(16, 75, "Neto Social (VPNS) " +td2);
    doc.text(70, 75, formatNumber(resp.vpn_social_1).substring(0,17));
    doc.text(128, 75, "Pesos");
    doc.text(165, 75, formatNumber(resp.vpn_social_1_err).substring(0,9));
    doc.text(187, 75, formatNumber(resp.vpn_social_1_std).substring(0,9));
    
    doc.text(16, 84, "Valor Presente");
    doc.text(16, 88, "Neto Social (VPNS) " +td1);
    doc.text(70, 88, formatNumber(resp.vpn_social_2).substring(0,17));
    doc.text(128, 88, "Pesos");
    doc.text(165, 88, formatNumber(resp.vpn_social_2_err).substring(0,9));
    doc.text(187, 88, formatNumber(resp.vpn_social_2_std).substring(0,9));
    
    doc.text(16, 96, "Valor Presente");
    doc.text(16, 100, "Neto Social (VPNS) " +td3);
    doc.text(70, 100, formatNumber(resp.vpn_social_3).substring(0,17));
    doc.text(128, 100, "Pesos");
    doc.text(165, 100, formatNumber(resp.vpn_social_3_err).substring(0,9));
    doc.text(187, 100, formatNumber(resp.vpn_social_3_std).substring(0,9));

    doc.text(16, 109, "Valor Presente Neto ");
    doc.text(16, 113, "de Externalidades " + td2);
    doc.text(128, 113, "Pesos ");
    doc.text(70, 113, formatNumber(resp.VPN_soc).substring(0,9));
    doc.text(165, 113, formatNumber(resp.VPN_soc_err).toString().substring(0,9));
    doc.text(187, 113, formatNumber(resp.VPN_soc_sig).toString().substring(0,9));

    doc.text(128, 125, "Pesos");    
    doc.text(16, 121, "Valor Presente ");
    doc.text(16, 125, "Neto privado " + td2);

    doc.text(70, 125, formatNumber(resp.vpn_privado).substring(0,9));
    doc.text(165, 125, formatNumber(resp.VPN_priv_err).toString().substring(0,9));
    doc.text(187, 125, formatNumber(resp.VPN_priv_sig).toString().substring(0,9));

    doc.text(16, 134, "Costos Totales "+ td2);			
    doc.text(70, 134, formatNumber(resp.costos).substring(0,9));
    doc.text(128, 134, "Pesos");
    doc.text(165, 134, formatNumber(resp.costos_err).substring(0,9));
    doc.text(187, 134, formatNumber(resp.costos_sd).substring(0,9));

    
    doc.text(16, 144, "Beneficios Totales "+ td2);				
    doc.text(70, 144, formatNumber(resp.beneficios).substring(0,9));	
    doc.text(128, 144, "Pesos");
    doc.text(165, 144, formatNumber(resp.beneficios_err).substring(0,9));
    doc.text(187, 144, formatNumber(resp.beneficios_sd).substring(0,9));

    doc.text(16, 155, "Índice Costo Beneficio"	);
    doc.text(70, 155, formatNumber(resp.icb).substring(0,9)	);
    doc.text(128, 155, "Pesos/Peso invertido");
    doc.text(165, 155, formatNumber(resp.icb_err).substring(0,9));
    doc.text(187, 155, formatNumber(resp.icb_sd).substring(0,9));
    
    doc.text(16, 165, "Tasa Interna de Retorno"	);
    doc.text(70, 165, formatNumber(resp.tir_2*100));
    doc.text(165, 165, "(" + formatNumber(resp.tir*100).substr(0,9));
    doc.text(180, 165, " , ");
    doc.text(187, 165, formatNumber(resp.tir_3*100).substr(0,9) + ")");
    doc.text(128, 165, "%");

    
   doc.text(16, 180, "Flujo Anual Equiv (FAE) " + td1);
   doc.text(70, 180, formatNumber(resp.fae_1).substring(0,9));
   doc.text(128, 180, "Pesos/Año");
   doc.text(165, 180, formatNumber(resp.fae1_err).toString().substring(0,9));
   doc.text(187, 180, formatNumber(resp.fae1_sd).toString().substring(0,9));
    
    
   doc.text(16, 193, "Flujo Anual Equiv (FAE) " + td2);	
   doc.text(70, 193, formatNumber(resp.fae_2).substring(0,9));	
   doc.text(128, 193, "Pesos/Año");
   doc.text(165, 193, formatNumber(resp.fae2_err).toString().substring(0,9));
   doc.text(187, 193, formatNumber(resp.fae3_sd).toString().substring(0,9));

    
    
   doc.text(16, 204, "Flujo Anual Equiv (FAE) " + td3);
   doc.text(70, 204, formatNumber(resp.fae_3).substring(0,9));
   doc.text(128, 204, "Pesos/Año");
   doc.text(165, 204, formatNumber(resp.fae3_err).toString().substring(0,9));
   doc.text(187, 204, formatNumber(resp.fae3_sd).toString().substring(0,9));

   doc.text(16, 215, "Plazo de recuperación" );
   doc.text(70, 215, (resp.plazo));
   doc.text(128, 215, "Años");
   doc.text(165, 215, resp.plazo_err.toString());
   doc.text(187, 215, resp.plazo_sd.toString());
        
   doc.text(16, 222, "Cantidad generada"	);	
   doc.text(16, 226, "con el proyecto"	);	
   doc.text(70, 226, formatNumber(resp.ice).substring(0,9)	);	
   doc.text(165, 226, formatNumber(resp.ice_err).substring(0,9));	
   doc.text(187, 226, formatNumber(resp.ice_sd).substring(0,9));	
   doc.text(128, 226,resp.unidad_medida);

    doc.text(16, 237, "Índice Costo Efectividad");
   doc.text(70, 237, formatNumber(resp.cantidad_ice).substring(0,9));
   doc.text(128, 237, "Pesos/" + resp.unidad_medida);
   doc.text(165, 237,formatNumber( resp.cantidad_ice_err).substring(0,9));
   doc.text(187, 237, formatNumber(resp.cantidad_ice_sd).substring(0,9));


    //doc.addPage ( 'letter', 'p');
    
    //doc.addImage(template1[3], 'JPEG',0,0,215.9,279.4);
    doc.addPage();
    doc.setDrawColor(color_value["r"],color_value["g"],color_value["b"]);
    doc.setLineWidth(1);
    doc.line(0, 20, 270, 20);
    doc.line(0, 260, 270, 260);


  //  doc.addImage(template1[2], 'JPEG',0,0,215.9,279.4);
    doc.setTextColor(color_value["r"],color_value["g"],color_value["b"]);
    doc.setFontSize(18); 
    doc.text(10, 40, "Tipo de proyecto: ");
    doc.text(10,60, "Interpretación:");
    doc.text(10,130, "Recomendaciones:");

    doc.setTextColor(36, 37, 41);
    doc.text(63, 40, app_string);
    doc.setFontSize(10);  

    doc.text(10, 66, doc.splitTextToSize(interpretacion, 190));
    doc.text(10, 136, doc.splitTextToSize(recomendaciones,190));
    

    doc.addPage();
    doc.setDrawColor(color_value["r"],color_value["g"],color_value["b"]);
    doc.setLineWidth(1);
    doc.line(0, 20, 270, 20);
    doc.line(0, 260, 270, 260);

    doc.addImage(pdf_graph1, 'JPEG',6,23.7,120,66);
    doc.addImage(pdf_graph2, 'JPEG',6,100.31,120,66);
    doc.addImage(pdf_graph3, 'JPEG',6,182.8,120,66);
    doc.addImage(pdf_graph4, 'JPEG',100,23.7,120,66);
    doc.addImage(pdf_graph5, 'JPEG',100,100.31,120,66);
    doc.text(130,  200, "Probabilidad de éxito:");
    doc.text(170, 200, resp.casos_positivos + "%");
    

    var n_page = parseInt(resp.filas_totales/16);
    var n_page_re = resp.filas_totales%16;
    var main_id = 0;
    for(var p = 0; p <= n_page; p++){
            doc.addPage();
            //doc.addImage(template1[4], 'JPEG',0,0,215.9,279.4);
            doc.setTextColor(color_value["r"],color_value["g"],color_value["b"]);
            doc.setFontSize(18);
            doc.setDrawColor(color_value["r"],color_value["g"],color_value["b"]);
            doc.setLineWidth(1);
            doc.line(0, 20, 270, 20);
            doc.line(0, 260, 270, 260);
            doc.text(78,30, "Precios y cantidades:");

            doc.setFontSize(10);    
            doc.text(10,55, "ID");
            doc.text(34,55, "Conceptos considerados");
            doc.text(120,55, "Elasticidad");
            doc.text(160,55, "Quiebre");

            doc.setTextColor(36, 37, 41);
            doc.setFontSize(10);    

            var space_mid = 65;
        if(p != n_page){
            for(var i = 0; i <= 15; i++) {
                main_id = main_id + 1;
                doc.text(12, space_mid,  (main_id).toString());   
                doc.text(36, space_mid,  (resp.cb_detalle[main_id-1]).substr(0,40));  
                doc.text(122, space_mid, (elasticidad[main_id-1]).toString());   
                doc.text(162, space_mid, (punto_de_quiebre[main_id-1]).toString());   
                space_mid = space_mid + 12.70;
            }    
        }else{
            for(var i = 0; i < n_page_re; i++) {
                main_id = main_id + 1;
                doc.text(12, space_mid,  (main_id-1).toString());   
                doc.text(36, space_mid,  (resp.cb_detalle[main_id-1]).substr(0,40));
                console.log("elasticidad pdf");
                console.log(elasticidad[main_id-1]);

                doc.text(122, space_mid, (elasticidad[main_id-1]).toString());   
                doc.text(162, space_mid, (punto_de_quiebre[main_id-1]).toString());   
                space_mid = space_mid + 12.70;
            }                            
        }
    }


    //doc.addImage(pdf_graph4, 'JPEG',20,120,180,100);
    doc.addPage ( 'letter', 'l');
    doc.autoTable({
        head: [['ID', 'Tipo', 'Impacto', 'Categoría', 'Detalles', 'prop', 'Frecuencia','Unidad de medida', 'Cantidad','Externalidad']],
        body: rows1,
        didParseCell: function (table) {

          if (table.section === 'head') {
            table.cell.styles.fillColor = '#A9A9A9';
          }
       }
//        styles: { fillColor: "#ec3d43" },
    });
    doc.addPage ( 'letter', 'l');
    doc.autoTable({
        head: [['Cant_pesimista','Cant_optimista','p','p_pes','p_opt','Fecha_inicio','Fecha_final','Modelo','coef1','coef2','coef3']],
        body: rows2,
        didParseCell: function (table) {

          if (table.section === 'head') {
            table.cell.styles.fillColor = '#A9A9A9';
          }
       }
//        styles: { fillColor: "#ec3d43" },
    });

    
    var n_page = parseInt(resp.filas_totales/9);
    console.log("n_page");
    console.log(n_page);
    var n_page_re = resp.filas_totales%9;
    var main_id = 0;
    for(var p = 0; p <= n_page; p++){
            doc.addPage('letter', 'l');
            //doc.addImage(template1[4], 'JPEG',0,0,215.9,279.4);
            doc.setTextColor(color_value["r"],color_value["g"],color_value["b"]);
            doc.setFontSize(18);
            doc.setDrawColor(color_value["r"],color_value["g"],color_value["b"]);
            doc.setLineWidth(1);
            doc.line(0, 20, 270, 20);
            doc.line(0, 260, 270, 260);

            doc.setFontSize(10);    
            doc.text(10,35, "ID");
            doc.text(44,35, "Conceptos considerados");
            doc.text(160,35, "Fuentes de información");

            doc.setTextColor(36, 37, 41);
            doc.setFontSize(10);    

            var space_mid = 50;
        
        if(p != n_page){
            for(var i = 0; i <= 8; i++) {
                main_id = main_id + 1;
                doc.text(12, space_mid,  (main_id).toString());   
                doc.text(36, space_mid,  (resp.cb_detalle[main_id - 1]).substr(0,50));   
                doc.text(125, space_mid, doc.splitTextToSize(resp.cb_fuentes[main_id - 1],135));   
                space_mid = space_mid + 20;        
        } 
            
        }else{
            for(var i = 0; i < n_page_re; i++) {
                main_id = main_id + 1;
                doc.text(12, space_mid,  (main_id).toString());   
                doc.text(36, space_mid,  (resp.cb_detalle[main_id - 1]).substr(0,50));   
                doc.text(125, space_mid,  doc.splitTextToSize(resp.cb_fuentes[main_id - 1],135));   
                space_mid = space_mid + 20;        
            }                            
        }
    }

    

    doc.save('reporte.pdf');
}