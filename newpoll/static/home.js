function copyJoke() {
    var copyText = document.getElementById("button.link").innerHTML;
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value)
    alert("Copied Text: " + "\n" + copyText.value);
}