////////////////COUNTRY FILTER AUTO-SELECT////////////////////////
var countryFilter = document.getElementById('country-filter');
var storedValue = sessionStorage.getItem('selectedCountry');

function auto_select_inMain() {
    var i;
    var country = sessionStorage.getItem('country');
    for (i = 0; i < countryFilter.length; i++) {
        let u = countryFilter.options[i]
        if (u.getAttribute('data-display') == country) {
            u.setAttribute('selected', true);
        };
    };
};

if (sessionStorage.getItem('access_inMain')) auto_select_inMain();

////////////////COUNTRY FILTER CHOOSING THE SELECTED COUNTRY (SELECTION)////////////////////////
if (storedValue) {
  countryFilter.value = storedValue;
}

//////////////////COUNTRY FILTER CHOOSING THE SELECTED COUNTRY (ADDING VARIABLE AND RELOAD)//////////////////////
function countryChange(){
    sessionStorage.setItem('selectedCountry', this.value);
    document.getElementById('country-filter-form').submit();
};
countryFilter.addEventListener('change', countryChange);

/////TO SHOW COUNTRY NAME IN CAFE CARD IF "SHOW ALL" IS SELECTED IN COUNTRY FILER////
countryTags = document.getElementsByClassName('cafe-country');
breakers = document.getElementsByClassName('breaker')
if (countryFilter.options[countryFilter.selectedIndex].innerHTML == "All cafes") {
  for (let tag of countryTags) {
    tag.removeAttribute("hidden");
  };
  for (let br of breakers) {
    br.removeAttribute("hidden");
  };
} else {
  for (let tag of countryTags) {
    tag.setAttributeNS(null, "hidden", true);
  };
  for (let br of breakers) {
    br.setAttributeNS(null, "hidden", true);
  };
};


//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

///////////////////////THE ACTUAL FILTERS///////////////////////
var wifi = document.getElementById('wifi');
var price = document.getElementById('price');
var plugs = document.getElementById('plugs');
var toilets = document.getElementById('toilets');
var calls = document.getElementById('calls');
var seats = document.getElementById('seats');

function filter() {
    const cafes = document.getElementsByClassName("cafe-card");
    var check_list = [];
    var check_complete = [];

    if (wifi.getAttribute("style")) {
        check_list.push(".lower .properties .has_wifi");
    };
    if (plugs.getAttribute("style")) {
        check_list.push(".lower .properties .has_plugs");
    };
    if (toilets.getAttribute("style")) {
        check_list.push(".lower .properties .has_toilets");
    };
    if (calls.getAttribute("style")) {
        check_list.push(".lower .properties .has_calls");
    };

    for (let cafe of cafes) {
        for (let check_path of check_list) {
            if (cafe.querySelectorAll(check_path).length != 0) {
                check_complete.push(check_path);
            };
        };
        if (check_list.length == check_complete.length) {
            cafe.removeAttribute("hidden");
        } else {
            cafe.setAttributeNS(null,"hidden", true);
        };
        check_complete = [];
    };
};

function rearrange() {
    const cafes = document.getElementsByClassName("cafe-card");
    const price_list = [];
    for (let cafe of cafes) {
        price_list.push(cafe.querySelector("#lower .row #price #price-text").innerHTML)
    };
    console.log(price_list)

}


////////////////// FOR WIFI //////////////////
function clicked_wifi() {
    const icon = document.querySelector("#wifi span .filter-svg g");
    const text = document.querySelector("#wifi .filter-text");
//    const cafes = document.getElementsByClassName("cafe-card");
    if (wifi.getAttribute("style")) {
        icon.setAttributeNS(null,"fill", "#757575");
        text.style.color = "#757575";
        wifi.removeAttribute("style");
        filter();
    } else {
        icon.setAttributeNS(null,"fill", "var(--contrast-hover)");
        text.style.color = "var(--contrast-hover)";
        wifi.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
        filter();
    };
};
//////////////////////////////////////////////
///////////////// FOR PLUGS //////////////////
function clicked_plugs() {
    const icon = document.querySelector("#plugs span .filter-svg g");
    const text = document.querySelector("#plugs .filter-text");
    if (plugs.getAttribute("style")) {
        icon.setAttributeNS(null,"fill", "#757575");
        text.style.color = "#757575";
        plugs.removeAttribute("style");
        filter();
    } else {
        icon.setAttributeNS(null,"fill", "var(--contrast-hover)");
        text.style.color = "var(--contrast-hover)";
        plugs.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
        filter();
    };
};
//////////////////////////////////////////////
///////////////// FOR TOILETS ////////////////
function clicked_toilets() {
    const icon = document.querySelector("#toilets span .filter-svg g");
    const text = document.querySelector("#toilets .filter-text");
    if (toilets.getAttribute("style")) {
        icon.setAttributeNS(null,"fill", "#757575");
        text.style.color = "#757575";
        toilets.removeAttribute("style");
        filter();
    } else {
        icon.setAttributeNS(null,"fill", "var(--contrast-hover)");
        text.style.color = "var(--contrast-hover)";
        toilets.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
        filter();
    };
};
//////////////////////////////////////////////
////////////////// FOR CALLS /////////////////
function clicked_calls() {
    const icon = document.querySelector("#calls span .filter-svg g");
    const text = document.querySelector("#calls .filter-text");
    if (calls.getAttribute("style")) {
        icon.setAttributeNS(null,"fill", "#757575");
        text.style.color = "#757575";
        calls.removeAttribute("style");
        filter();
    } else {
        icon.setAttributeNS(null,"fill", "var(--contrast-hover)");
        text.style.color = "var(--contrast-hover)";
        calls.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
        filter();
    };
};
//////////////////////////////////////////////
////////////////// FOR PRICE /////////////////
function clicked_price() {
    const price_neutral = document.querySelector("#price #price-neutral");
    const price_lowtohigh = document.querySelector("#price #price-lowtohigh");
    const price_hightolow = document.querySelector("#price #price-hightolow");
    const text = document.querySelector("#price .filter-text");
    const icon = document.querySelector("#price #price-neutral .filter-svg g");

    if (price_lowtohigh.hidden && price_hightolow.hidden) {
        price_neutral.setAttributeNS(null,"hidden", true);
        price_lowtohigh.removeAttribute("hidden");
        text.style.color = "var(--contrast-hover)";
        price.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
        rearrange();
    } else if (price_neutral.hidden && price_hightolow.hidden) {
        price_lowtohigh.setAttributeNS(null,"hidden", true);
        price_hightolow.removeAttribute("hidden");
        text.style.color = "var(--contrast-hover)";
        price.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
    } else {
        if (price_neutral.hidden && price_lowtohigh.hidden) {
            price_hightolow.setAttributeNS(null,"hidden", true);
            price_neutral.removeAttribute("hidden");
            icon.setAttributeNS(null,"fill", "#757575");
            text.style.color = "#757575";
            price.removeAttribute("style");
        };
    };
};
//////////////////////////////////////////////
////////////////// FOR SEATS /////////////////
function clicked_seats() {
    const seats_neutral = document.querySelector("#seats #seats-neutral");
    const seats_lowtohigh = document.querySelector("#seats #seats-lowtohigh");
    const seats_hightolow = document.querySelector("#seats #seats-hightolow");
    const text = document.querySelector("#seats .filter-text");
    const icon = document.querySelector("#seats #seats-neutral .filter-svg g");

    if (seats_lowtohigh.hidden && seats_hightolow.hidden) {
        seats_neutral.setAttributeNS(null,"hidden", true);
        seats_lowtohigh.removeAttribute("hidden");
        text.style.color = "var(--contrast-hover)";
        seats.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
    } else if (seats_neutral.hidden && seats_hightolow.hidden) {
        seats_lowtohigh.setAttributeNS(null,"hidden", true);
        seats_hightolow.removeAttribute("hidden");
        text.style.color = "var(--contrast-hover)";
        seats.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
    } else {
        if (seats_neutral.hidden && seats_lowtohigh.hidden) {
            seats_hightolow.setAttributeNS(null,"hidden", true);
            seats_neutral.removeAttribute("hidden");
            icon.setAttributeNS(null,"fill", "#757575");
            text.style.color = "#757575";
            seats.removeAttribute("style");
        };
    };
};


wifi.addEventListener('click', clicked_wifi);
price.addEventListener('click', clicked_price);
plugs.addEventListener('click', clicked_plugs);
toilets.addEventListener('click', clicked_toilets);
calls.addEventListener('click', clicked_calls);
seats.addEventListener('click', clicked_seats);
/////////////////////////////////////////////////////////////////////