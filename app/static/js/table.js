
let rawData = [];                // Все полученные элементы
let filteredData = [];           // Отфильтрованные/отсортированные данные
let currentSort = {              // Состояние сортировки
        column: null,
        direction: 1
    };
const loadedItemIds = new Set();
const pendingItems = [];         // Очередь новых товаров для рендеринга
const BATCH_SIZE = 50;           // Размер порции
const BATCH_INTERVAL = 0;        // Задержка между порциями (0 = мгновенно, но не блокирует UI)
let isRendering = false;
let allDataLoadedAlertShown = false; // Флаг для однократного алерта


function addRowToBatchQueue(item) {
        pendingItems.push(item);
    }

function startBatchRender() {
        if (isRendering) return;
        requestAnimationFrame(renderNextBatch);
    }

function renderNextBatch() {
    isRendering = true;
    const tbody = document.getElementById('tableBody');
    if (!tbody || pendingItems.length === 0) {
        isRendering = false;
        if (!allDataLoadedAlertShown && !document.querySelector('.loading-message')) {
            allDataLoadedAlertShown = true;
        }
        return;
    }

    const chunk = pendingItems.splice(0, BATCH_SIZE);
    const fragment = document.createDocumentFragment();

    chunk.forEach(item => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.name || ''}</td>
            <td>${item.brand || ''}</td>
            <td>${(item.price_u / 100).toFixed(2) || ''}</td>
            <td>${(item.sale_price_u / 100).toFixed(2) || ''}</td>
            <td>${item.feedbacks || ''}</td>
            <td>${item.rating ? item.rating.toFixed(1) : ''}</td>
        `;
        fragment.appendChild(tr);
    });

    tbody.appendChild(fragment); // Одна операция DOM-вставки

    setTimeout(() => {
        isRendering = false;
        requestAnimationFrame(renderNextBatch); // продолжаем рендерить остаток
    }, BATCH_INTERVAL);
}

function setSort(column) {
        if (currentSort.column === column) {
            currentSort.direction *= -1;
        } else {
            currentSort = { column, direction: 1 };
        }
        updateSortIcons();
        applyFilters();
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
    updateTableWithFilteredData();
}


function updateTableWithFilteredData() {
    const tbody = document.getElementById('tableBody');
    if (!tbody) return;

    // Удаляем все текущие строки
    tbody.querySelectorAll('tr').forEach(row => row.remove());

    if (!filteredData.length) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="6">Нет данных после фильтрации</td>';
        tbody.appendChild(row);
        return;
    }

    // Добавляем в очередь только отфильтрованные данные
    filteredData.forEach(addRowToBatchQueue);
    startBatchRender(); // начинаем пакетную отрисовку
}


// === Подключение к Server-Sent Events (SSE) ===
document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.getElementById('tableBody');
    if (tbody) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align:center; color:#888;" class="loading-message">Загрузка данных...</td>
            </tr>
        `;
    }

    if (typeof EventSource !== "undefined") {
        const eventSource = new EventSource("/frontend/v2/search/stream-data");
        let renderTimeout = null;

        eventSource.onmessage = function(event) {
            try {
                const item = JSON.parse(event.data);
                if (item.id && loadedItemIds.has(item.id)) return;

                rawData.push(item);
                loadedItemIds.add(item.id);

                if (passesFilters(item)) {
                    addRowToBatchQueue(item);

                    // Запланируем рендеринг через короткий промежуток времени
                    if (!renderTimeout) {
                        renderTimeout = setTimeout(() => {
                            startBatchRender();
                            renderTimeout = null;
                        }, 0); // можно увеличить до 50–100 мс, чтобы ещё больше снизить нагрузку
                    }
                }
            } catch (e) {
                console.error("Ошибка парсинга события:", e);
           }
        };

        eventSource.onerror = function(err) {
            console.error(err);
            const loading = document.querySelector('.loading-message');
            if (loading) loading.remove();

            // === ПОКАЗЫВАЕМ ДАННЫЕ, ЕСЛИ ЕСТЬ ===
            if (rawData.length > 0) {
                applyFilters();
                updateTableWithFilteredData();
            } else {
                const tbody = document.getElementById('tableBody');
                if (tbody) {
                    tbody.innerHTML = `
                        <tr>
                            <td colspan="6" style="color:red;">Ошибка подключения к серверу</td>
                        </tr>
                    `;
                }
            }
        };

        eventSource.onopen = function () {
            const loading = document.querySelector('.loading-message');
            if (loading) loading.remove();
        };

    } else {
        alert("Ваш браузер не поддерживает Server-Sent Events.");
    }

});


// === Вспомогательная функция: проходит ли товар текущие фильтры? ===
function passesFilters(item) {
    const textFiltersPassed = Array.from(document.querySelectorAll('.filter-input')).every(input => {
        const column = input.getAttribute('data-column');
        const value = input.value.trim().toLowerCase();
        if (!value) return true;

        return String(item[column] || '').toLowerCase().includes(value);
    });

    if (!textFiltersPassed) return false;

    const rangeInputs = document.querySelectorAll('.range-input');
    const ranges = {};
    rangeInputs.forEach(input => {
        const column = input.getAttribute('data-column');
        if (!ranges[column]) ranges[column] = [];
        const val = input.value.trim();
        ranges[column].push(val ? parseFloat(val) : null);
    });

    for (const [column, [min, max]] of Object.entries(ranges)) {
        if ((min !== null && !isNaN(min)) || (max !== null && !isNaN(max))) {
            let numVal = ['price_u', 'sale_price_u'].includes(column)
                ? item[column] / 100
                : item[column];

            if ((min !== null && !isNaN(min) && numVal < min) ||
                (max !== null && !isNaN(max) && numVal > max)) {
                return false;
            }
        }
    }

    return true;
}
