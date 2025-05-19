var checkbox = document.getElementById("anonymous");
    checkbox.addEventListener('change', function(e) {
        const contributor_name = document.getElementById("contributor-name");
        const contributor_email = document.getElementById("contributor-email");
         if (checkbox.checked) {
            contributor_name.value = '';
            contributor_name.placeholder = 'No input required'
            contributor_name.disabled = true;
            /////////////////////////////////
            contributor_email.value = '';
            contributor_email.placeholder = 'No input required'
            contributor_email.disabled = true;
         } else {
            contributor_name.disabled = false;
            contributor_name.placeholder = 'Your name'
            /////////////////////////////////
            contributor_email.disabled = false;
            contributor_email.placeholder = 'Your email'
        }
    });

var full_address = document.getElementById("full-address");
full_address.addEventListener('change', function(e) {
    let address_input = document.getElementById("address");
     if (full_address.checked) {
        address_input.type = 'text';
        address_input.value = '';
        address_input.placeholder = 'Cafe Address';
     } else {
        address_input.type = 'url';
        address_input.value = '';
        address_input.placeholder = 'Google Maps Link';
    }
});

var title = document.getElementById('title');
var inputSlider = document.getElementById('input');
var dot = document.getElementById('dot');
var sliderRange = document.getElementById('slider-range');

function setValue() {
    let value = this.value;
    let min = parseInt(this.min);
    let max = parseInt(this.max);
    let percent = (value / max) * 100;
    sliderRange.style.right = (100 - percent) + '%';
    dot.style.left = percent + '%';
    if (value == 51) {
        title.value = '>50 :O' ;
    } else {
        title.value = '~' + value ;
    };
};
inputSlider.addEventListener('input', setValue);

/////////////////////////////////////////////////////////////////
var uploadClick_area = document.getElementById("primary-image-area");
const img = document.querySelector(".image-content");
const fake = document.querySelector(".no-image-content");
const file_input = document.querySelector('input[type=file]');
const reader = new FileReader();
uploadClick_area.addEventListener('click', function() {
    file_input.click();
});
file_input.addEventListener('change', function () {
    if (this.files[0]) {
        fake.setAttributeNS(null, 'hidden', true);
        img.removeAttribute('hidden');
        const file = this.files[0];
        reader.onload = (event) => {
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
//        upload.classList.add('hide');
        reset.classList.remove('hide');
    }
    else{
        upload.classList.remove('hide');
        reset.classList.add('hide');
    }
});

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

/////////////////////////////////////////////////////////////////
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
if (sessionStorage.getItem('access_inForm')) auto_select_inForm()