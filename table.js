// Function to fetch and render the table
function renderTable() {
    const csvUrl = 'precipitation_data.csv';
    Papa.parse(csvUrl, {
        download: true,
        header: true,
        dynamicTyping: true,
        complete: function(results) {
            const data = results.data;
            const kojcData = data.filter(d => d.station_id === 'KOJC').sort((a, b) => new Date(b.date) - new Date(a.date));

            const tableBody = document.getElementById('table-body');
            tableBody.innerHTML = '';

            kojcData.forEach(row => {
                const rowElement = document.createElement('tr');
                rowElement.innerHTML = `
                    <td>${row.date}</td>
                    <td>${row.precip_in} in</td>
                `;
                tableBody.appendChild(rowElement);
            });
        }
    });
}

// Call the function when the window loads
window.onload = renderTable;
