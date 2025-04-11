//// Saving the filter selected option to localstorage to reuse after reload
//document.getElementById('country-filter').on('change', function() {
//    localStorage.setItem('country-filter-select', this.textContent)
//})


// finding out the country code of the user's current location for auto-filling the country phone code of cafe phone number
function auto_select() {
    $.getJSON('http://ip-api.com/json/', function(data) {
        var n = JSON.stringify(data, null, 2);
        var country = JSON.parse(n).country;
        var country_code = JSON.parse(n).countryCode;
//        var dial_code = JSON.parse(n).country_calling_code;
        var call_num_list = document.getElementById('phone-codes-dropdown');
        var country_list = document.getElementById('country-dropdown');
        var country_filter_list = document.getElementById('country-filter');

        if (country_filter_list == null) {
            var j;
            for (j = 0; j < call_num_list.length; j++) {
                let u = call_num_list.options[j]
                if (u.getAttribute('id') == country) {
                    u.innerText = u.getAttribute('data-display');
                    u.setAttribute('selected', true);
                };
            };
            var k;
            for (k = 0; k < country_list.length; k++) {
                let u = country_list.options[k]
                if (u.getAttribute('data-display') == country_code) {
                    u.setAttribute('selected', true);
                };
            };
        } else {
            var i;
            document.getElementById('country-filter').addEventListener('change', function() {
                for (i = 0; i < country_filter_list.length; i++) {
                    let u = country_filter_list.options[i]
                    if (u.getAttribute('data-display') == country) {
                        u.setAttribute('selected', true);
                    };
                };
            })
        }
    });
}

if (sessionStorage.getItem('access')) auto_select();


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
