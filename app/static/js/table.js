
let filteredData = [...rawData];
let currentSort = { column: null, direction: 1 };

function renderTable(data) {
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '';

        data.forEach(row => {
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td>${row.name}</td>
                <td>${row.brand}</td>
                <td>${(row.price_u / 100).toFixed(2)}</td>
                <td>${(row.sale_price_u / 100).toFixed(2)}</td>
                <td>${row.feedbacks}</td>
                <td>${row.rating}</td>
            `;

            tbody.appendChild(tr);
        });
    }

function setSort(column) {
        if (currentSort.column === column) {
            currentSort.direction *= -1;
        } else {
            currentSort = { column, direction: 1 };
        }
        updateSortIcons();
        applyFilters(); // Применяем сортировку сразу
    }

function updateSortIcons() {
        const icons = ['name', 'brand', 'price_u', 'sale_price_u', 'feedbacks', 'rating'];
        icons.forEach(col => {
            const icon = document.getElementById(`${col}-sort-icon`);
            icon.innerHTML = '';
        });

        if (currentSort.column) {
            const icon = document.getElementById(`${currentSort.column}-sort-icon`);
            if (currentSort.direction === 1) {
                icon.innerHTML = '↑';
            } else {
                icon.innerHTML = '↓';
            }
        }
    }

function applyFilters() {
    let result = [...rawData];

    // 1. Фильтр по текстовым полям
    document.querySelectorAll('.filter-input').forEach(input => {
        const column = input.getAttribute('data-column');
        const value = input.value.trim().toLowerCase();

        if (value) {
            result = result.filter(item =>
                String(item[column]).toLowerCase().includes(value)
            );
        }
    });

    // 2. Фильтр по диапазонам (цена, отзывы, рейтинг)
    const rangeInputs = document.querySelectorAll('.range-input');
    const ranges = {};

    rangeInputs.forEach(input => {
        const column = input.getAttribute('data-column');
        if (!ranges[column]) ranges[column] = [];

        const val = input.value.trim();
        ranges[column].push(val ? parseFloat(val) : null);
    });

    Object.entries(ranges).forEach(([column, [min, max]]) => {
        if ((min !== null && !isNaN(min)) || (max !== null && !isNaN(max))) {
            result = result.filter(item => {
                let numVal;

                // Если поле — цена или скидка, делим на 100
                if (['price_u', 'sale_price_u'].includes(column)) {
                    numVal = item[column] / 100;
                } else {
                    numVal = item[column];
                }

                return (
                    (min === null || isNaN(min) || numVal >= min) &&
                    (max === null || isNaN(max) || numVal <= max)
                );
            });
        }
    });

    // 3. Сортировка (если задана)
    if (currentSort.column) {
        result.sort((a, b) => {
            const valA = a[currentSort.column];
            const valB = b[currentSort.column];

            if (typeof valA === 'string' && typeof valB === 'string') {
                return valA.localeCompare(valB) * currentSort.direction;
            }

            return (valA > valB ? 1 : -1) * currentSort.direction;
        });
    }

    filteredData = result;
    renderTable(filteredData);
    }

// Инициализация
    window.onload = () => {
        renderTable(rawData);
    };
