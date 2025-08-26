function downloadPDF(pdfUrl, fileName = 'documento.pdf') {
    const link = document.createElement('a');
    link.href = pdfUrl;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Ejemplo de uso con un botón:
document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('btn-descargar-pdf');
    if (btn) {
        btn.addEventListener('click', function () {
            // Cambia la ruta por la de tu PDF
            downloadPDF('/static/files/GUIA DE REGULADO A LIBRE - SAFIRA ENERGÍA CHILE.pdf', 'GUIA-DE-REGULADO-A-LIBRE-SAFIRA-ENERGÍA-CHILE.pdf');
        });
    }
});