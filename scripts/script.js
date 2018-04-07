function init() {

    var inputFile = document.querySelector('#file_upload');

    inputFile.addEventListener('change', function (e) {
        var label = inputFile.nextElementSibling;
        var labelValue = label.innerHTML;
        console.log('TESt');
        var fileName = labelValue;
        if (this.files && this.files.length > 1) {
            fileName = this.files.length + " files selected"
        } else {
            fileName = e.target.value.split('\\').pop();
        }

        label.style.backgroundColor = '#456a86';
        label.style.color = '#fff';
        label.innerHTML = fileName;
    });

    var inputText = document.querySelector('#text_input');

    inputText.addEventListener('input', function (e) {
        if (inputText.value !== '') {
            inputText.style.backgroundColor = '#456a86';
            inputText.style.color = '#fff';
        } else {
            inputText.removeAttribute('style');
        }
    });
}

window.onscroll = function () {
    scrollFunction()
};

// display/ hide scroll up button
function scrollFunction() {
    if (document.body.scrollTop > 25 || document.documentElement.scrollTop > 25) {
        document.getElementById('top_button').style.display = "block";
    } else {
        document.getElementById('top_button').style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
function goToTopFunction() {
    var i = window.scrollY;
    var int = setInterval(function () {
        window.scrollTo(0, i);
        i -= 10;
        if (i <= 0) clearInterval(int);
    }, 3);
}
