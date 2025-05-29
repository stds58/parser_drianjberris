// === Глобальные переменные ===
let rawData = [];                // Все полученные элементы
let filteredData = [];           // Отфильтрованные/отсортированные данные
let currentSort = {              // Состояние сортировки
    column: null,
    direction: 1
};

// === Подключение к Server-Sent Events (SSE) ===
document.addEventListener("DOMContentLoaded", () => {
    updateSortIcons();
    applyFilters(); // Рендерим начальное состояние (может быть пустым)

    if (typeof EventSource !== "undefined") {
        const eventSource = new EventSource("/frontend/v2/search/stream-data");
        eventSource.onmessage = function(event) {
            try {
                const item = JSON.parse(event.data);
                rawData.push(item); // Добавляем новый товар
                applyFilters();     // Пересчитываем фильтры и рендерим
            } catch (e) {
                console.error("Ошибка парсинга события:", e);
            }
        };
        eventSource.onerror = function(err) {
            console.error("Ошибка SSE:", err);
        };
    } else {
        alert("Ваш браузер не поддерживает Server-Sent Events.");
    }
});

// === Фильтрация и сортировка ===
function applyFilters() {
    let result = [...rawData];

    // 1. Фильтр по текстовым полям
    document.querySelectorAll('.filter-input').forEach(input => {
        const column = input.getAttribute('data-column');
        const value = input.value.trim().toLowerCase();
        if (value) {
            result = result.filter(item =>
                String(item[column] || '').toLowerCase().includes(value)
            );
        }
    });

    // 2. Фильтр по диапазонам (цена, отзывы и т.д.)
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

// === Рендер таблицы ===
function renderTable(data) {
    const tbody = document.getElementById("tableBody");
    if (!tbody) return;

    tbody.innerHTML = ""; // Очищаем текущие строки

    if (!data || data.length === 0) {
        const row = document.createElement("tr");
        row.innerHTML = "<td colspan='6'>Нет данных для отображения</td>";
        tbody.appendChild(row);
        return;
    }

    data.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.name || ''}</td>
            <td>${item.brand || ''}</td>
            <td>${(item.price_u / 100).toFixed(2) || ''}</td>
            <td>${(item.sale_price_u / 100).toFixed(2) || ''}</td>
            <td>${item.feedbacks || ''}</td>
            <td>${item.rating || ''}</td>
        `;
        tbody.appendChild(row);
    });
}

// === Обработчики событий для сортировки ===
window.setSort = function(column) {
    if (currentSort.column === column) {
        currentSort.direction *= -1; // меняем направление
    } else {
        currentSort.column = column;
        currentSort.direction = 1;
    }
    updateSortIcons();
    applyFilters();
};

// === Обновление иконок сортировки ===
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