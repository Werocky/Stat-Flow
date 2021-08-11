function update() {
    var source = 'http://localhost/html/cam.jpg',
        timestamp = (new Date()).getTime(),
        newUrl = source + '?_=' + timestamp;
    document.getElementById("img").src = newUrl;
    document.getElementById("img1").src =  newUrl;
    setTimeout(update, 1000);
}