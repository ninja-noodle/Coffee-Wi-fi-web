var checkbox = document.getElementById("anonymous");
    checkbox.addEventListener('change', function(e) {
         if (checkbox.checked) {
            document.getElementById("contributor-name").value = '';
            document.getElementById("contributor-name").disabled = true;
            document.getElementById("contributor-email").value = '';
            document.getElementById("contributor-email").disabled = true;
         } else {
            document.getElementById("contributor-name").disabled = false;
            document.getElementById("contributor-email").disabled = false;
        }
    });
var full_address = document.getElementById("full-address");
    full_address.addEventListener('change', function(e) {
        let address_input = document.getElementById("address");
         if (full_address.checked) {
            address_input.type = 'text';
            address_input.placeholder = 'Cafe Address';
         } else {
            address_input.type = 'url';
            address_input.placeholder = 'Google Maps Link';
        }
    });

    var titleMin = document.getElementById('title-min');
    var titleMax = document.getElementById('title-max');

    var inputLeft = document.getElementById('input-left');
    var inputRight = document.getElementById('input-right');

    var dotLeft = document.getElementById('dot-left');
    var dotRight = document.getElementById('dot-right');

    var sliderRange = document.getElementById('slider-range');

    function setLeftValue()
    {
        let value = this.value;
        let min = parseInt(this.min);
        let max = parseInt(this.max);

        value = Math.min(parseInt(value),
                parseInt(inputRight.value) - 1);
        let percent = ((value - min) / (max - min)) * 100;
        sliderRange.style.left = percent + '%';
        dotLeft.style.left = percent + '%';
        titleMin.value = value + ' <';

    }
    function setRightValue()
    {
        let value = this.value;
        let min = parseInt(this.min);
        let max = parseInt(this.max);

        value = Math.max(parseInt(value),
                parseInt(inputLeft.value) + 1);
        let percent = ((value - min) / (max - min)) * 100;
        sliderRange.style.right = (100 - percent) + '%';
        dotRight.style.right = (100 - percent) + '%';
        titleMax.value = '< ' + value;
    }
    inputLeft.addEventListener('input', setLeftValue);
    inputRight.addEventListener('input', setRightValue);


    const img = document.querySelector(".image-content");
    img.classList.add("hide");
    const fake = document.querySelector(".no-image-content");
    const upload = document.querySelector(".upload-button");
    const reset = document.querySelector(".reset-button");
    reset.classList.add("hide");
    const input = document.querySelector('input[type=file]');
    const reader = new FileReader();
    input.addEventListener('change', function () {
        if (this.files[0]) {
            fake.classList.add('hide');
            img.classList.remove('hide');
            const file = this.files[0];
            reader.onload = (event) => {
                img.src = event.target.result;
            };
            reader.readAsDataURL(file);
            upload.classList.add('hide');
            reset.classList.remove('hide');
        }
        else{
            upload.classList.remove('hide');
            reset.classList.add('hide');
        }
    })

    reset.addEventListener('click', function () {
        img.classList.add("hide");
        img.src = '';
        this.classList.add('hide');
        upload.classList.remove('hide');
        fake.classList.remove('hide');

    });
