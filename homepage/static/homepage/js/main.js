const yearElement = document.getElementById("current-year");

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

// Переход на страницу заявки по клику на строку таблицы
document.querySelectorAll(".clickable-row").forEach((row) => {
    row.addEventListener("click", (event) => {
        if (event.target.closest("a")) {
            return;
        }
        window.location.href = row.dataset.href;
    });
});
