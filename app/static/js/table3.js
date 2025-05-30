
    // === Глобальные переменные ===
    let rawData = [];                // Все полученные элементы
    let filteredData = [];           // Отфильтрованные/отсортированные данные
    let currentSort = {              // Состояние сортировки
        column: null,
        direction: 1
    };

    // === Функции для работы с таблицей ===

    function renderTable(data) {
        const tbody = document.getElementById('tableBody');
        if (!tbody) return;

        tbody.innerHTML = ''; // Очищаем текущие строки
        if (!data || data.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="6">Нет данных для отображения</td>';
            tbody.appendChild(row);
            return;
        }

        data.forEach(row => {
            const tr = document.createElement('tr');
            alert(row.name);
            tr.innerHTML = `
                <td>${row.name || ''}</td>
                <td>${row.brand || ''}</td>
                <td>${(row.price_u / 100).toFixed(2) || ''}</td>
                <td>${(row.sale_price_u / 100).toFixed(2) || ''}</td>
                <td>${row.feedbacks || ''}</td>
                <td>${row.rating ? row.rating.toFixed(1) : ''}</td>
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
        applyFilters(); // Применяем сортировку
    }

    function updateSortIcons() {
        const icons = ['name', 'brand', 'price_u', 'sale_price_u', 'feedbacks', 'rating'];
        icons.forEach(col => {
            const icon = document.getElementById(`${col}-sort-icon`);
            if (icon) icon.textContent = '';
        });

        if (currentSort.column) {
            const icon = document.getElementById(`${currentSort.column}-sort-icon`);
            if (icon) {
                icon.textContent = currentSort.direction === 1 ? '↑' : '↓';
            }
        }
    }

    function applyFilters() {
        let result = [...rawData];

        // 1. Текстовые фильтры
        document.querySelectorAll('.filter-input').forEach(input => {
            const column = input.getAttribute('data-column');
            const value = input.value.trim().toLowerCase();

            if (value) {
                result = result.filter(item =>
                    String(item[column] || '').toLowerCase().includes(value)
                );
            }
        });

        // 2. Диапазонные фильтры
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
                    let numVal = ['price_u', 'sale_price_u'].includes(column)
                        ? item[column] / 100
                        : item[column];

                    return (
                        (min === null || isNaN(min) || numVal >= min) &&
                        (max === null || isNaN(max) || numVal <= max)
                    );
                });
            }
        });

        // 3. Сортировка
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

    // === Подключение к Server-Sent Events (SSE) ===
    document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.getElementById('tableBody');
    if (tbody) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align:center; color:#888;">Загрузка данных...</td>
            </tr>
        `;
    }

    if (typeof EventSource !== "undefined") {
        const eventSource = new EventSource("/frontend/v2/search/stream-data");

        eventSource.onmessage = function(event) {
            try {
                const item = JSON.parse(event.data);
                rawData.push(item);
                //alert(item);
                renderTable(rawData);
            } catch (e) {
                console.error("Ошибка парсинга события:", e);
            }
        };

        eventSource.onerror = function(err) {
            console.error("Ошибка SSE:", err);
            const tbody = document.getElementById('tableBody');
            if (tbody) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" style="color:red;">Ошибка подключения к серверу</td>
                    </tr>
                `;
            }
        };
    } else {
        alert("Ваш браузер не поддерживает Server-Sent Events.");
    }
});
