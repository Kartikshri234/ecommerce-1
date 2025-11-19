
document.addEventListener('DOMContentLoaded', function() {
    const priceMin = document.getElementById('price-min');
    const priceMax = document.getElementById('price-max');
    const minValue = document.getElementById('price-min-value');
    const maxValue = document.getElementById('price-max-value');

    function updateValues() {
        minValue.textContent = priceMin.value;
        maxValue.textContent = priceMax.value;
    }

    priceMin.addEventListener('input', updateValues);
    priceMax.addEventListener('input', updateValues);
});
