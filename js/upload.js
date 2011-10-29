/** based on code by Shiv Kumar 
    http://www.matlus.com/html5-file-upload-with-progress/
*/
var bytesUploaded = 0;
var bytesTotal = 0;
var previousBytesLoaded = 0;
var intervalTimer = 0;

function fileSelected() {
  var file = document.getElementById('img').files[0];
  var fileSize = 0;
  if (file.size > 1024 * 1024)
    fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
  else
    fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';
  document.getElementById('step2').style.display = 'block';
  document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
  document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
  document.getElementById('fileType').innerHTML = 'Type: ' + file.type;
}

function uploadFile() {
  previousBytesLoaded = 0;
  document.getElementById('step3').style.display = 'block';
  document.getElementById('uploadResponse').style.display = 'none';
  document.getElementById('progressNumber').innerHTML = '';
  var progressBar = document.getElementById('progressBar');
  progressBar.style.display = 'block';
  progressBar.style.width = '0px';        
  
  var fd = new FormData();
  fd.append("img", document.getElementById('img').files[0]);
  
  var xhr = new XMLHttpRequest();        
  xhr.upload.addEventListener("progress", uploadProgress, false);
  xhr.addEventListener("load", uploadComplete, false);
  xhr.addEventListener("error", uploadFailed, false);
  xhr.addEventListener("abort", uploadCanceled, false);
  xhr.open("POST", "py/upload");
  xhr.send(fd);

  intervalTimer = setInterval(updateTransferSpeed, 500);
}

function updateTransferSpeed() {
  var currentBytes = bytesUploaded;
  var bytesDiff = currentBytes - previousBytesLoaded;
  if (bytesDiff == 0) return;
  previousBytesLoaded = currentBytes;
  bytesDiff = bytesDiff * 2;
  var bytesRemaining = bytesTotal - previousBytesLoaded;
  var secondsRemaining = bytesRemaining / bytesDiff;

  var speed = "";
  if (bytesDiff > 1024 * 1024)
    speed = (Math.round(bytesDiff * 100/(1024*1024))/100).toString() + 'MBps';
  else if (bytesDiff > 1024)
    speed =  (Math.round(bytesDiff * 100/1024)/100).toString() + 'KBps';
  else
    speed = bytesDiff.toString() + 'Bps';
  document.getElementById('transferSpeedInfo').innerHTML = speed;
  document.getElementById('timeRemainingInfo').innerHTML = '| ' + secondsToString(secondsRemaining);        
}

function secondsToString(seconds) {        
  var h = Math.floor(seconds / 3600);
  var m = Math.floor(seconds % 3600 / 60);
  var s = Math.floor(seconds % 3600 % 60);
  return ((h > 0 ? h + ":" : "") + (m > 0 ? (h > 0 && m < 10 ? "0" : "") + m + ":" : "0:") + (s < 10 ? "0" : "") + s);
}

function uploadProgress(evt) {
  if (evt.lengthComputable) {
    bytesUploaded = evt.loaded;
    bytesTotal = evt.total;
    var percentComplete = Math.round(evt.loaded * 100 / evt.total);
    var bytesTransfered = '';
    if (bytesUploaded > 1024*1024)
      bytesTransfered = (Math.round(bytesUploaded * 100/(1024*1024))/100).toString() + 'MB';
    else if (bytesUploaded > 1024)
      bytesTransfered = (Math.round(bytesUploaded * 100/1024)/100).toString() + 'KB';
    else
      bytesTransfered = (Math.round(bytesUploaded * 100)/100).toString() + 'Bytes';

    document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
    document.getElementById('progressBar').style.width = (percentComplete * 3.55).toString() + 'px';
    document.getElementById('transferBytesInfo').innerHTML = bytesTransfered;
  }
  else {
    document.getElementById('progressBar').innerHTML = 'unable to compute progress';
  }  
}

function uploadComplete(evt) {
  clearInterval(intervalTimer);
  window.location = "form.html";
}  

function uploadFailed(evt) {
  clearInterval(intervalTimer);
  document.getElementById('uploadResponse');
  uploadResponse.innerHTML = "An error occurred while uploading the file.";
  uploadResponse.style.display = 'block';
}  

function uploadCanceled(evt) {
  clearInterval(intervalTimer);
  document.getElementById('uploadResponse');
  uploadResponse.innerHTML = "The upload has been canceled by the user or the browser dropped the connection.";
  uploadResponse.style.display = 'block';
}  

