
$(document).ready(
	function()
	{
		oMain.init();
	}
);

window.oMain = {
  init : function(){
    setTimeout(function(){
     oLazyLoad.init();
    },2000);
    window.onscroll = function(ev) {
      oLazyLoad.init();
    };
  }
};

// Lazy loading Images
window.oLazyLoad = {
  img : {},
  loadingImg : null,
  init : function() {
    var aImg = this.get();
    this.lazyLoad(aImg);
  },
  get : function()
  {
    return document.getElementsByClassName('lazy');
  },
  lazyLoad : function(aArg){
    for(var i = 0 ; i < aArg.length ; i++ ){
      var src = aArg[i].getAttribute('data-src');
      if(this.elementInViewPort(aArg[i])){
        aArg[i].setAttribute('src', aArg[i].getAttribute('data-src'));
      }
    }
  },
  elementInViewPort : function(el) {
    var rect = el.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right  <=  (window.innerWidth || document.documentElement.clientWidth)
    );
  }
};
