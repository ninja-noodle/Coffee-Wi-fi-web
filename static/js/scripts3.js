let slider = document.getElementById("formRange")
let value = document.querySelector(".rangeValue");

slider.value = value.value;

function calcValue() {
    let valuePercentage = (slider.value / slider.max) * 100;
    let color = 'linear-gradient(to right, #1A1A1A ' + valuePercentage + '%, #c5c5c5 ' + valuePercentage + '%)'
    slider.style.background = color;
}
slider.addEventListener('input', function(){
    calcValue();
    value.value = this.value;
})
calcValue()

let countryFilter = document.getElementById("country-filter");
function countryChange(){
    document.getElementById("bottom-form").submit();
    countryFilter.options[countryFilter.selectedIndex].setAttribute('selected', true);
};
countryFilter.addEventListener('change', countryChange);
