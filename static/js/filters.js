var wifi = document.getElementById('wifi');
var price = document.getElementById('price');
var outlets = document.getElementById('outlets');
var toilets = document.getElementById('toilets');
var calls = document.getElementById('calls');
//const seats = document.getElementById('seats');
//const clear = document.getElementById('clear');

function filter() {
    const cafes = document.getElementsByClassName("cafe-card");
    var check_list = [];
    var check_complete = [];

    if (wifi.getAttribute("style")) {
        check_list.push("#lower-body .row #properties #has_wifi");
    };
    if (outlets.getAttribute("style")) {
        check_list.push("#lower-body .row #properties #has_outlets");
    };
    if (toilets.getAttribute("style")) {
        check_list.push("#lower-body .row #properties #has_toilets");
    };
    if (calls.getAttribute("style")) {
        check_list.push(".card-body .grid-container #has_calls");
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
//        for (let cafe of cafes) {
//            const parent = cafe.querySelectorAll("#lower-body .row #properties #has_wifi");
//            if (parent.length == 0) {
//                cafe.removeAttribute("hidden");
//            };
//        };
    } else {
        icon.setAttributeNS(null,"fill", "var(--contrast-hover)");
        text.style.color = "var(--contrast-hover)";
        wifi.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
        filter();
//        for (let cafe of cafes) {
//            const parent = cafe.querySelectorAll("#lower-body .row #properties #has_wifi");
//            if (parent.length == 0) {
//                cafe.setAttributeNS(null,"hidden", true);
//            };
//        }
    };
};
//////////////////////////////////////////////
///////////////// FOR OUTLETS ////////////////
function clicked_outlets() {
    const icon = document.querySelector("#outlets span .filter-svg g");
    const text = document.querySelector("#outlets .filter-text");
    if (outlets.getAttribute("style")) {
        icon.setAttributeNS(null,"fill", "#757575");
        text.style.color = "#757575";
        outlets.removeAttribute("style");
        filter();
    } else {
        icon.setAttributeNS(null,"fill", "var(--contrast-hover)");
        text.style.color = "var(--contrast-hover)";
        outlets.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
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
    var old_span_id;
    var new_span_id;
    const text = document.querySelector("#price .filter-text");

    if (document.querySelector("#price #price-lowtohigh").hidden &&
        document.querySelector("#price #price-hightolow").hidden) {
        old_span_id = "price-neutral";
        new_span_id = "price-lowtohigh";
    };
    if (document.querySelector("#price #price-neutral").hidden &&
        document.querySelector("#price #price-hightolow").hidden) {
        old_span_id = "price-lowtohigh";
        new_span_id = "price-hightolow";
    };
    if (document.querySelector("#price #price-neutral").hidden &&
        document.querySelector("#price #price-lowtohigh").hidden) {
        old_span_id = "price-hightolow";
        new_span_id = "price-neutral";
    };

    if (old_span_id == "price-neutral" && new_span_id == "price-lowtohigh") {
        document.querySelector("#price #" + old_span_id).setAttributeNS(null,"hidden", true);
        document.querySelector("#price #" + new_span_id).removeAttribute("hidden");
        text.style.color = "var(--contrast-hover)";
        price.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
    };
    if (old_span_id == "price-lowtohigh" && new_span_id == "price-hightolow") {
        document.querySelector("#price #" + old_span_id).setAttributeNS(null,"hidden", true);
        document.querySelector("#price #" + new_span_id).removeAttribute("hidden");
        text.style.color = "var(--contrast-hover)";
        price.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
    };
    if (old_span_id == "price-hightolow" && new_span_id == "price-neutral") {
        document.querySelector("#price #" + old_span_id).setAttributeNS(null,"hidden", true);
        document.querySelector("#price #" + new_span_id).removeAttribute("hidden");
        const icon = document.querySelector("#price #" + new_span_id + " .filter-svg g");
        icon.setAttributeNS(null,"fill", "#757575");
        text.style.color = "#757575";
        price.removeAttribute("style");
    };
//
//    if (price.getAttribute("style")) {
//
//
//    } else {
//        icon.setAttributeNS(null,"fill", "var(--contrast-hover)");
//        text.style.color = "var(--contrast-hover)";
//        price.setAttributeNS(null, "style", "background-color: var(--contrast); color: var(--contrast-hover);");
//    };
};


wifi.addEventListener('click', clicked_wifi);
price.addEventListener('click', clicked_price);
outlets.addEventListener('click', clicked_outlets);
toilets.addEventListener('click', clicked_toilets);
calls.addEventListener('click', clicked_calls);

