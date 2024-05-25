window.onscroll = function() {
  var title = this.document.getElementById("footer-main-text");
  var scrollTop = document.documentElement.scrollTop * 1;
  title.style.transform =
    "translateX(-" + scrollTop + "px)";
};
