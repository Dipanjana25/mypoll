function myFunction() {
    var copyText = document.getElementById('haa').innerHTML;
    // copyText.select();
    // copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText);
    alert(" Your link is ready to be shared!");
  }
