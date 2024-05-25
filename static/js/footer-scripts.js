window.onscroll = function() {
  var title = this.document.getElementById("footer-main-text");
  var scrollTop = document.documentElement.scrollTop * 0.5;
  title.style.transform =
    "translateX(-" + scrollTop + "px)";
};
document.getElementById("footer-copyright").innerHTML = new Date().getFullYear();