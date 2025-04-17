var countryFilter = document.getElementById('country-filter');
var storedValue = sessionStorage.getItem('selectedCountry');

function auto_select_inForm() {
    var country = sessionStorage.getItem('country');
    var country_code = sessionStorage.getItem('country_code');
    var currency = sessionStorage.getItem('currency');
    var city = sessionStorage.getItem('city');
    if (countryFilter == null) {
    //     ^^^ checks if the country filter exists on the page
        var call_num_list = document.getElementById('phone-codes-dropdown');
        var country_list = document.getElementById('country-dropdown');

        var j;
        for (j = 0; j < call_num_list.length; j++) {
            let u = call_num_list.options[j]
            if (u.getAttribute('id') == country) {
                u.innerText = u.getAttribute('data-display');
                u.setAttribute('selected', true);
            };
        };
        document.getElementById('located-city').value = city;
        document.getElementById('currency').value = currency;
        var k;
        for (k = 0; k < country_list.length; k++) {
            let u = country_list.options[k]
            if (u.getAttribute('data-display') == country_code) {
                u.setAttribute('selected', true);
            };
        };
    };
};

function auto_select_inMain() {
    var i;
    var country = sessionStorage.getItem('country');
    for (i = 0; i < countryFilter.length; i++) {
        let u = countryFilter.options[i]
        if (u.getAttribute('data-display') == country) {
            u.setAttribute('selected', true);
        };
    };
    sessionStorage.removeItem("access_inMain");
};

if (sessionStorage.getItem('access_inForm')) auto_select_inForm();
if (sessionStorage.getItem('access_inMain')) auto_select_inMain();

if (storedValue) {
  countryFilter.value = storedValue;
}
function countryChange(){
    sessionStorage.setItem('selectedCountry', this.value);
    document.getElementById('bottom-form').submit();
};
countryFilter.addEventListener('change', countryChange);

/////////////////////////////////////////////////////////////////

function showDisplayValue(e) {
  var options = e.target.options,
      option = e.target.selectedOptions[0],
      i;

  // reset options
  for (i = 0; i < options.length; ++i) {
    options[i].innerText = options[i].value;
  }

  // change the selected option's text to its `data-display` attribute value
  option.innerText = option.getAttribute('data-display');
}

document.getElementById('phone-codes-dropdown').addEventListener('change', showDisplayValue, false);
