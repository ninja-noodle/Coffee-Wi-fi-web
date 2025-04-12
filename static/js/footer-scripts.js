window.onscroll = function() {
  if (window.scrollY + window.innerHeight >= document.documentElement.offsetHeight - 100) {
  var title = this.document.getElementById("footer-main-text");
  var scrollTop = document.documentElement.scrollTop * 0.7;
  title.style.transform ="translateX(-" + scrollTop + "px)";
 };
 }
document.getElementById("footer-copyright").innerHTML = new Date().getFullYear();
