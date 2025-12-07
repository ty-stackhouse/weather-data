let nonZeroData = []; // Global variable to store filtered data

function renderTable(data) {
    const tableBody = document.getElementById('table-body');
    tableBody.innerHTML = '';

    data.forEach(row => {
        const rowElement = document.createElement('tr');
        rowElement.innerHTML = `
            <td>${row.date}</td>
            <td>${row.precip_in}</td>
        `;
        tableBody.appendChild(rowElement);
    });
}

function sortTable(column) {
    const order = (currentSort.column === column && currentSort.order === 'desc') ? 'asc' : 'desc';
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

// Initialize currentSort
let currentSort = { column: 'date', order: 'desc' };
