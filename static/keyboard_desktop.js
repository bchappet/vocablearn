document.addEventListener('DOMContentLoaded', function () {
    const input = document.querySelector('.input-area');
    const keys = document.querySelectorAll('.key');
    let isShiftActive = false;

    keys.forEach(key => {
        key.addEventListener('click', () => {
            const keyText = key.textContent;

            switch (keyText) {
                case 'Shift':
                    isShiftActive = !isShiftActive;
                    break;
                case 'Space':
                    input.value += ' ';
                    break;
                case '←':
                    input.value = input.value.slice(0, -1);
                    break;
                case 'Enter':
                    input.value += '\n';
                    break;
                default:
                    input.value += isShiftActive ? keyText.toUpperCase() : keyText;
                    if (isShiftActive) isShiftActive = false;
            }
            input.focus();
        });
    });
});
