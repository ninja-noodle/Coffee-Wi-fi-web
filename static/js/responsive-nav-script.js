var contributeText = document.getElementById("contribute-text");
var contributeLogo = document.getElementById("contribute-logo");
//var search = document.getElementById("navSearch");
var countryFilter = document.getElementById("country-filter-form");
////var filterList = [];
//filterList.push(document.getElementById("wifi"));
//filterList.push(document.getElementById("price"));
//filterList.push(document.getElementById("plugs"));
//filterList.push(document.getElementById("toilets"));
//filterList.push(document.getElementById("calls"));
//filterList.push(document.getElementById("seats"));
//var back = document.getElementById("back");
//var filters = document.getElementById("filters");

function heightAdjust() {
    var navContainer = document.getElementById("navbar");
    var contentWrapper = document.getElementById("contentWrapper");
    var navHeight = document.getElementsByClassName("is-fixed");

    contentWrapper.setAttribute("style", "padding-top: " + navContainer.offsetHeight + "px;")
//    for (n of navHeight) {
//        n.setAttribute("style", "top: -" + navContainer.offsetHeight + "px;")
//    };

    let scrollPos = 0;
    const headerHeight = navContainer.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && navContainer.classList.contains('is-fixed')) {
                navContainer.classList.add('is-visible');
                navContainer.classList.add('main-nav-container-shadow');
            } else {
                navContainer.classList.remove('is-visible', 'is-fixed', 'main-nav-container-shadow');
                navContainer.removeAttribute("style");
            }
        } else {
            // Scrolling Down
            navContainer.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !navContainer.classList.contains('is-fixed')) {
                navContainer.classList.add('is-fixed');
                navContainer.setAttribute("style", "top: -" + navContainer.offsetHeight + "px;");
            }
        }
        scrollPos = currentTop;
    });
};

window.addEventListener('DOMContentLoaded', heightAdjust);

var filtersForm = document.getElementById("filtersForm");
var topNav = document.getElementById("top");
function responsive() {
    if (window.innerWidth < 1240) {
        contributeText.setAttributeNS(null, "hidden", true);
        contributeLogo.removeAttribute("hidden");
    } else {
        contributeText.removeAttribute("hidden");
        contributeLogo.setAttributeNS(null, "hidden", true);
    };

    if (window.innerWidth < 1120) {
        topNav.insertAdjacentElement("afterend", filtersForm);
        countryFilter.removeAttribute("style");
        filtersForm.setAttribute("style", "margin-top: 5px;border-radius: 10px;background: #CDB797;");
    } else {
        countryFilter.insertAdjacentElement("afterend", filtersForm);
        countryFilter.setAttribute("style", "border-right: 2px solid var(--border-color);");
        filtersForm.removeAttribute("style");
    };
    heightAdjust();
}

responsive();
window.onresize = responsive;

