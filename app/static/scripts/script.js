document.addEventListener('DOMContentLoaded', function () {
    const btnAlright = document.querySelector('.btn-inc-alright');
    const btnControl = document.querySelector('.btn-inc-control');
    const btnAlert = document.querySelector('.btn-inc-alert');
    const detailControl = document.querySelector('.st-inc-control');
    const detailAlert = document.querySelector('.st-inc-alert');

    let activeButton = null;
    let activeDetail = null;

    function hideAllDetails() {
        detailControl.classList.add('d-none');
        detailAlert.classList.add('d-none');
        activeButton = null;
        activeDetail = null;
    }

    function setArrowPosition(button, detailBlock) {
        const btnRect = button.getBoundingClientRect();
        const detailRect = detailBlock.getBoundingClientRect();
        const arrowLeft = btnRect.left - detailRect.left + btnRect.width / 2;
        detailBlock.style.setProperty('--arrow-left', arrowLeft + 'px');
    }

    function updateArrowPosition() {
        if (activeButton && activeDetail && !activeDetail.classList.contains('d-none')) {
            setArrowPosition(activeButton, activeDetail);
        }
    }

    btnAlright.addEventListener('click', function () {
        hideAllDetails();
    });

    btnControl.addEventListener('click', function () {
        hideAllDetails();
        detailControl.classList.remove('d-none');
        activeButton = this;
        activeDetail = detailControl;
        setTimeout(() => setArrowPosition(this, detailControl), 10);
    });

    btnAlert.addEventListener('click', function () {
        hideAllDetails();
        detailAlert.classList.remove('d-none');
        activeButton = this;
        activeDetail = detailAlert;
        setTimeout(() => setArrowPosition(this, detailAlert), 10);
    });

    // Обработчик изменения размера окна
    window.addEventListener('resize', updateArrowPosition);

});