var camera_width = 640;
var camera_height = 480;
if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)){  
  camera_width = 320;
  camera_height = 240;
}else{
  camera_width = 640;
  camera_height = 480;
}
