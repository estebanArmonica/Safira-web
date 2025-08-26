document.addEventListener('DOMContentLoaded', function () {
    // Cargamos el PDF de manera tradicional
    const pdfjsScript = document.createElement('script');
    pdfjsScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.min.js';

    // cuando lea y abra el archivo PDF se genera una función
    pdfjsScript.onload = function () {
        // Configuramos el worker path
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';

        // configuramos el event listener después de cargar el PDF
        document.getElementById('id_archivo').addEventListener('change', handlePDFUpload);
    };

    document.head.appendChild(pdfjsScript);

    // generamos la función para el handler (errores)
    function handlePDFUpload(event) {
        const file = event.target.files[0] // creamos un evento de una constante para buscar por lista de matriz
        if (!file) return;

        const reader = new FileReader(); // creamos la instancia para los files reader

        // abrimos el reader 
        reader.onload = function (e) {
            const typeArray = new Uint8Array(e.target.result); // CORRECCIÓN: usar e.target.result

            // CORRECCIÓN: Usar pdfjsLib en lugar de pdfjsScript
            pdfjsLib.getDocument(typeArray).promise.then(function (pdf) {
                console.log('PDF cargado correctamente. Páginas: ', pdf.numPages);
                return extractTextFromPDF(pdf);
            }).then(function (data) {
                console.log('Datos extraídos: ', JSON.stringify(data, null, 2)); // transformamos los datos extraidos en formato Json

                // Autocompletar campos del formulario
                if (data.nombre_empresa) {
                    document.getElementById('nombreEmpresa').value = data.nombre_empresa;
                }
                if (data.rut_empresa) {
                    document.getElementById('rutEmpresa').value = data.rut_empresa;
                }
                if (data.direccion_suministro) {
                    document.getElementById('direcciones').value = data.direccion_suministro;
                }
                if (data.numero_cliente) {
                    // Si tienes un campo para el número de cliente
                    const clienteField = document.getElementById('numero_cliente');
                    if (clienteField) clienteField.value = data.numero_cliente;
                }
                if (data.consumo_mensual) {
                    const consumoInput = document.getElementById('consumoMensual');
                    if (consumoInput) consumoInput.value = data.consumo_mensual;
                }
                if (data.demanda_maxima) {
                    const demandaMaximaInput = document.getElementById('demandaMaxima');
                    if(demandaMaximaInput) demandaMaximaInput.value = data.demanda_maxima;
                }
                if (data.demanda_maxima_hp) {
                    const demandaMaximaHpInput = document.getElementById('demandaMaximaHp');
                    if(demandaMaximaHpInput) demandaMaximaHpInput.value = data.demanda_maxima_hp;
                }
                if (data.tarifa_contratada) {
                    document.getElementById('tarifaContratada').value = data.tarifa_contratada
                }
                if (data.subestacion) {
                    document.getElementById('subestacion').value = data.subestacion
                }
            }).catch(function (error) {
                console.error('Error al procesar PDF: ', error);
                alert('Error al procesar el PDF. Por favor verifica que el archivo no esté dañado');
            });
        };

        // Leemos el ArrayList de los datos rescatados del PDF en formato Json
        reader.readAsArrayBuffer(file);
    }

    async function extractTextFromPDF(pdf) {
        let fullText = ''; // constante -> varia 

        // realizamos una busqueda por el for del numero de paginas a través de un contador
        for (let i = 1; i <= pdf.numPages; i++) {
            try {
                const page = await pdf.getPage(i);
                const textContent = await page.getTextContent();
                const pageText = textContent.items.map(item => item.str).join(' ');
                fullText += pageText + '\n';

                console.log(`Texto página ${i}: `, pageText.substring(0, 100) + '...'); // Muestra solo el inicio
            } catch (error) {
                console.error(`Error en página ${i}: `, error);
            }
        }

        // retornamos el proceso del pdf 
        return processPdfText(fullText);
    }

    function processPdfText(text) {
        console.log(`Texto completo para análisis: ${text.substring(0, 500) + '...'}`); // nuevamente mostramos solo el inicio

        const result = {}; // creamos una constante de un array vacio

        /**
         * Realizamos por partes la extracion de los datos del PDF
         * 1. Extraemos el nombre de la empresa 
         * 2. Extraemos la direccion del suministro
         * 3. Extraemos el numero del cliente 
         * 4. Extraemos el tipo de documento (Factura Electronica o Boleta Electronica)
         * 5. Extraemos el Rut de la empresa
         * 6. Extraemos los consumos mensuales, demanda maxima y por hora
        */

        /**
         * 1. Nombre de la empresa, dependiendo del archivo su forma cambia 
         * tanto en facturas como boletas se tiene de forma diferente
         * Facturas como: (Señor(es)), Boleta como: (Sr.(a) )
        */
        const empresaRegex = /Sr\.?\s?\(?a\)?[:\s-]*(.+?)(?:\n|Dirección|$)/i;
        const empresaMatch = text.match(empresaRegex);
        let empresaSeniorMatch = null;

        // en caso de ser (Sr. (a) )
        if (empresaMatch && empresaMatch[1]) {
            result.nombre_empresa = empresaMatch[1]
                .replace(/^[:\s-]+/, '')
                .replace(/\s+/g, ' ')
                .trim();
            console.log('Nombre empresa encontrado:', result.nombre_empresa);
        }

        // en caso de ser Señor(es): pero buscando el nombre por mayusculas
        if (!empresaSeniorMatch) {
            const empresaMayusculas = text.match(/([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s&]{10,50}(?:S\.A\.|LTDA|SPA|EIRL|SA))/);
            if (empresaMayusculas) {
                result.nombre_empresa = empresaMayusculas[1].trim();
                console.log(`Nombre encontrado por mayusculas: ${result.nombre_empresa}`);
            }
        }


        /**
         * 2. Direccion de suministro del cliente
         * este por defecto en ambos documentos esta escrito de la misma forma
         * Dirección suministro
        */
        // Buscar "Dirección suministro" y capturar la dirección

        const index = text.toLowerCase().indexOf('dirección suministro');
        if (index !== -1) {
            // Muestra los 80 caracteres siguientes para ver el formato real
            console.log('Fragmento encontrado:', text.substring(index, index + 80));
        } else {
            console.log('fragmento no encontrado')
        }

        // Busca el RUT y luego la dirección
        const direccionRegex = /\d{2}\.\d{3}\.\d{3}-\d\s+([A-ZÁÉÍÓÚÑ0-9\s\.,\-°º#]+?)(?=\s+Administración|Electricidad|Cargo|$)/i;
        const direccionRegex1 = /Direcci[óo]n\s+suministro\s*[:\-]?\s*([^\n]+?)(?=\s*Ruta:|\n|$)/i;

        const direccionMatch = text.match(direccionRegex); // para facturas 
        const direccionMatch1 = text.match(direccionRegex1); // para boletas 

        if (direccionMatch && direccionMatch[1]) {
            result.direccion_suministro = direccionMatch[1].trim();
            console.log(`Dirección suministro: ${result.direccion_suministro}`);
        } else if (direccionMatch1 && direccionMatch1[1]) {
            result.direccion_suministro = direccionMatch1[1].trim();
            console.log(`Dirección suministro: ${result.direccion_suministro}`);
        } else {
            console.log("No se encontró dirección suministro");
        }

        /**
         * 3. Numero del cliente
         * este tambien tiene un apartado por defecto en ambos documentos
         * n° -0  -
         * número de cliente, PAC
        */
        const clienteRegex1 = /^(\d{7,8}-\d)/; // Al inicio del documento (7 u 8 dígitos)
        const clienteRegex2 = /N[º°]?[\s-]*Cliente[\s:]*(\d{7,8}-\d)/i; // Con "N° Cliente"
        const clienteRegex3 = /N[úu]mero[\s-]*de[\s-]*cliente[\s:]*(\d{7,8}-\d)/i; // Con "Número de cliente"
        const clienteRegex4 = /PAC (\d{7,8})/; // En el código PAC (7 u 8 dígitos)
        const clienteRegex5 = /(\d{7,8}-\d)(?=\s|$)/; // Cualquier número de cliente en el texto

        const clienteMatch1 = text.match(clienteRegex1);
        const clienteMatch2 = text.match(clienteRegex2);
        const clienteMatch3 = text.match(clienteRegex3);
        const clienteMatch4 = text.match(clienteRegex4);
        const clienteMatch5 = text.match(clienteRegex5);

        if (clienteMatch1) {
            result.numero_cliente = clienteMatch1[1];
        } else if (clienteMatch2) {
            result.numero_cliente = clienteMatch2[1];
        } else if (clienteMatch3) {
            result.numero_cliente = clienteMatch3[1];
        } else if (clienteMatch4) {
            result.numero_cliente = clienteMatch4[1] + '-0'; // Formato XXXX-0
        } else if (clienteMatch5) {
            result.numero_cliente = clienteMatch5[1];
        }

        // si todo sale bien en los primeros if-elseif, se muestra el numero del cliente por completo
        if (result.numero_cliente) {
            console.log(`Número cliente encontrado: ${result.numero_cliente}`);
        } else {
            console.log("No se encontró número de cliente");
        }

        /**
         * 4. Tipo de documento
         * este tambien tiene un apartado por defecto en ambos documentos
         * para hacer la busqueda más rapido solo escribiremos los nombres de ambos documentos 
         * BOLETA ELECTRÓNICA y FACTURA ELECTRÓNICA
        */

        if (text.includes('BOLETA ELECTRÓNICA')) {
            result.tipo_documento = 'BOLETA ELECTRÓNICA';
        } else if (text.includes('FACTURA ELECTRÓNICA')) {
            result.tipo_documento = 'FACTURA ELECTRÓNICA';
        } else if (text.includes('FACTURA ELECTRONICA')) {
            result.tipo_documento = 'FACTURA ELECTRONICA';
        }

        console.log(`Tipo documento: ${result.tipo_documento}`);

        /**
         * 5. RUT de la empresa
         * este tambien tiene un apartado por defecto en ambos documentos
        */
        const rutRegex = /R\.?U\.?T\.?[\s:]*([\d\.\-]{8,})/i;
        const rutMatch = text.match(rutRegex);
        if (rutMatch && rutMatch[1]) {
            result.rut_empresa = rutMatch[1].replace(/[^\d\-kK]/g, '');
            console.log(`RUT empresa encontrado: ${result.rut_empresa}`);
        }

        /**
         * 6. Consumos mensuales, demanda maxima y maxima por hora punta
        */

        // ...existing code...

        // Para Factura
        const consumoFactura = text.match(/Electricidad Consumida\s*\(([\d.,]+)kW[h]?\)/i);
        const demandaMaxFactura = text.match(/Dem\.?\s*Max\.?\s*\(([\d.,]+)kW\)/i);
        const demandaPuntaFactura = text.match(/Dem\.?\s*Horas\s*punta\s*\(([\d.,]+)kW\)/i);

        // Para Boleta
        const consumoBoletaAlt = text.match(/Consumo\s*total\s*del\s*mes\s*[:=]?\s*([\d.,]+)\s*kWh?/i);

        const demandaMaxBoletaAlt = text.match(/Demanda\s*Sum[ií]nistrada\s*[:=]?\s*([\d.,]+)\s*kW/i)
            || text.match(/Demanda\s*Suminsitrada[^0-9]*([\d.,]+)\s*kW/i);

        const demandaPuntaBoletaAlt = text.match(/Demanda\s*Horas\s*Punta\s*[:=]?\s*([\d.,]+)\s*kW/i);

        // Asignación priorizando Factura, luego Boleta
        result.consumo_mensual = consumoFactura?.[1]?.replace(/[,\.]/g, '') ||
            consumoBoletaAlt?.[1]?.replace(/[,\.]/g, '') || null;
        result.demanda_maxima = demandaMaxFactura?.[1]?.replace(/[,\.]/g, '') ||
            demandaMaxBoletaAlt?.[1]?.replace(/[,\.]/g, '') || null;
        result.demanda_maxima_hp = demandaPuntaFactura?.[1]?.replace(/[,\.]/g, '') ||
            demandaPuntaBoletaAlt?.[1]?.replace(/[,\.]/g, '') || null;

        if (result.consumo_mensual) {
            document.getElementById('consumoMensual').value = result.consumo_mensual;
        }
        if (result.demanda_maxima) {
            document.getElementById('demandaMaxima').value = result.demanda_maxima;
        }
        if (result.demanda_maxima_hp) {
            document.getElementById('demandaMaximaHp').value = result.demanda_maxima_hp;
        }


        console.log(`Consumo mensual: ${result.consumo_mensual}`);
        console.log(`Demanda máxima: ${result.demanda_maxima}`);
        console.log(`Demanda hora punta: ${result.demanda_maxima_hp}`);

        /**
         * 7. Subestacion a la que pertenece
        */
        // Extraer tipo de tarifa contratada
        const tarifaRegex = /Tipo de tarifa contratada\s*:\s*([A-Z0-9\-]+)/i;
        const tarifaMatch = text.match(tarifaRegex);
        if (tarifaMatch && tarifaMatch[1]) {
            result.tarifa_contratada = tarifaMatch[1].trim();
            console.log(`Tarifa contratada: ${result.tarifa_contratada}`);
        }

        // Extraer subestación
        const subestacionRegex = /Subestaci[óo]n\s*:\s*([A-ZÁÉÍÓÚÑ0-9\s\-]+)/i;
        const subestacionMatch = text.match(subestacionRegex);

        if (subestacionMatch && subestacionMatch[1]) {
            result.subestacion = subestacionMatch[1].replace(/Fecha límite para cambio de tarifa.*/i, '').trim();
            console.log(`Subestación: ${result.subestacion}`);
        }

        // retornamos el resultado
        return result;

    }
});