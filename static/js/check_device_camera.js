var scroll_y = 0, scroll_x = 0;
  window.addEventListener("scroll", function(event) {  
    if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)){
      scroll_y = 0; 
      scroll_x = 0; 
    }else{
      scroll_y = this.scrollY; 
      scroll_x = this.scrollX; 
    }   
  });

var final_width = 640;
var final_height = 480;
var camera_width = 640;
var camera_height = 480;
if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)){  
  camera_width = 320;
  camera_height = 240;
}else{
  camera_width = 640;
  camera_height = 480;
}
