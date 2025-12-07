let nonZeroData = []; // Global variable to store filtered data
let currentSort = { column: 'date', order: 'desc' }; // Initialize with default sort

function renderTable(data) {
    if (!data || !data.length) {
        console.log('No data to render');
        return;
    }
    
    // Apply default sort if no sort is specified
    if (!currentSort) {
        data.sort((a, b) => new Date(b.date) - new Date(a.date));
    }
    
    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = '';

    // Update today's precipitation status
    const todayPrecip = data[0].precip_in;
    const status = todayPrecip.toFixed(3) > 0 ? 'rain detected' : 'no rain';
    document.getElementById('today-precip-status').textContent = status;

    data.forEach(row => {
        const rowElement = document.createElement('tr');
        rowElement.innerHTML = `
            <td>${row.date}</td>
            <td>${row.precip_in.toFixed(3)}</td>
        `;
        tableBody.appendChild(rowElement);
    });
}

function sortTable(column) {
    if (!nonZeroData || !nonZeroData.length) {
        console.log('No data to sort');
        return;
    }
    
    if (!column || typeof column !== 'string') {
        console.log('Invalid column to sort by');
        return;
    }

    const order = (currentSort.column === column && currentSort.order === 'desc') 
        ? 'asc' 
        : 'desc';
    currentSort = { column, order };

    // Update sort indicators
    document.querySelectorAll('#precip-table th span').forEach(span => span.textContent = '');
    const indicator = order === 'desc' ? '▼' : '▲';
    document.getElementById(`${column}-sort-indicator`).textContent = indicator;

    const sortedData = [...nonZeroData].sort((a, b) => {
        if (column === 'date') {
            return order === 'desc' ? new Date(b.date) - new Date(a.date) : new Date(a.date) - new Date(b.date);
        } else if (column === 'precip_in') {
            return order === 'desc' ? b.precip_in - a.precip_in : a.precip_in - b.precip_in;
        }
        return 0;
    });

    renderTable(sortedData);
}

