/** based on code by Shiv Kumar 
    http://www.matlus.com/html5-file-upload-with-progress/
*/
var bytesUploaded = 0;
var bytesTotal = 0;
var previousBytesLoaded = 0;
var intervalTimer = 0;

function fileSelected() {
  var file = $('#img')[0].files[0];
  $('#fileName').html('Name: ' + file.name);

  var fileSize = 0;
  var sizeError = false;
  if (file.size > 1024 * 1024) {
    fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
  }
  else {
    fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';
  }
  if (file.size > 2 * 1024 * 1024) {
    sizeError = true;
    $('#fileSize').addClass('error');
    fileSize += ' | Max: 2MB';
  }
  else {
    $('#fileSize').removeClass('error');
  }
  $('#fileSize').html('Size: ' + fileSize);

  var typeError = false;
  var fileType = file.type;
  if(fileType != 'image/jpeg' && fileType != 'image/png' && fileType != 'image/bmp') {
    typeError = true;
    $('#fileType').addClass('error');
    fileType += ' | Only: jpeg, png, bmp';
  }
  else {
    $('#fileType').removeClass('error');
  }
  $('#fileType').html('Type: ' + fileType);
  if(sizeError || typeError) {
    $('#uploadButton').hide();
  }
  else {
    $('#uploadButton').show();
  }
  $('#step2').show();
}

function uploadFile() {
  previousBytesLoaded = 0;
  $('#step3').show();
  $('#uploadResponse').hide();
  $('#progressNumber').html('');
  var progressBar = $('#progressBar');
  progressBar.show();
  progressBar.css('width', '0px');        
  
  var fd = new FormData();
  fd.append("img", $('#img')[0].files[0]);
  
  var xhr = new XMLHttpRequest();        
  xhr.upload.addEventListener("progress", uploadProgress, false);
  xhr.addEventListener("load", uploadComplete, false);
  xhr.addEventListener("error", uploadFailed, false);
  xhr.addEventListener("abort", uploadCanceled, false);
  xhr.open("POST", "py/upload");
  xhr.send(fd);

  intervalTimer = setInterval(updateTransferSpeed, 1000);
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
  $('#transferSpeedInfo').html(speed);
  $('#timeRemainingInfo').html('| ' + secondsToString(secondsRemaining));        
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
    var percentComplete = Math.round(evt.loaded * 1000 / evt.total) / 10;
    var bytesTransfered = '';
    if (bytesUploaded > 1024*1024)
      bytesTransfered = (Math.round(bytesUploaded * 100/(1024*1024))/100).toString() + 'MB';
    else if (bytesUploaded > 1024)
      bytesTransfered = (Math.round(bytesUploaded * 100/1024)/100).toString() + 'KB';
    else
      bytesTransfered = (Math.round(bytesUploaded * 100)/100).toString() + 'Bytes';

    $('#progressNumber').html(percentComplete.toString() + '%');
    $('#progressBar').css('width', percentComplete.toString() + '%');
    $('#transferBytesInfo').html(bytesTransfered);
  }
  else {
    $('#progressBar').html('unable to compute progress');
  }  
}

function uploadComplete(evt) {
  clearInterval(intervalTimer);
  if(evt.target.responseText !== 'OK') {
    setErrorText(evt.target.responseText);
  }
  else {
    window.location = "form.html";
  }
}  

function uploadFailed(evt) {
  clearInterval(intervalTimer);
  setErrorText("An error occurred while uploading the file.");
}  

function uploadCanceled(evt) {
  clearInterval(intervalTimer);
  setErrorText("The upload has been canceled by the user or the browser dropped the connection.");
}

function setErrorText(text) {
  var div = $('#uploadResponse');  
  div.html(text + '<br /><a href="/">try again</a>');
  div.show();
}

