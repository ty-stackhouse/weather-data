function renderTable() {
    const csvUrl = 'precipitation_data.csv';
    Papa.parse(csvUrl, {
        download: true,
        header: true,
        dynamicTyping: true,
        complete: function(results) {
            const data = results.data;
            
            // Remove empty rows if any
            const cleanData = data.filter(row => row.date && row.station_id);

            // Filter out rows with zero precipitation
            const nonZeroData = cleanData.filter(row => parseFloat(row.precip_in) !== 0);

            const tableBody = document.getElementById('table-body');
            tableBody.innerHTML = '';

            nonZeroData.forEach(row => {
                const rowElement = document.createElement('tr');
                rowElement.innerHTML = `
                    <td>${row.date}</td>
                    <td>${row.precip_in}</td>
                `;
                tableBody.appendChild(rowElement);
            });
        }
    });
}

// Call the function when the window loads
window.onload = renderTable;
