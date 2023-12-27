function animateLoading(theTag) {
    theTag.innerHTML = `<span class="spinner-border spinner-border-sm"></span>`
}


function displayImage(imageInputEl) {
    const file = imageInputEl.files[0];
    const reader = new FileReader();
    reader.onloadend = function() {
        document.getElementById("previewImg").src = reader.result;
    };
    reader.readAsDataURL(file);
}
