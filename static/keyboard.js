document.addEventListener('DOMContentLoaded', function () {
    const isMobile = window.matchMedia("(max-width: 768px)").matches;
    
    if (isMobile) {
        initMobileKeyboard();
    } else {
        initDesktopKeyboard();
    }
});

function initDesktopKeyboard() {
    const input = document.querySelector('.input-area');
    const hiddenInput = document.getElementById('hidden-answer');
    const keys = document.querySelectorAll('.key');
    let isShiftActive = false;

    keys.forEach(key => {
        key.addEventListener('click', () => handleKeyPress(key.textContent, input));
    });

    function handleKeyPress(keyText, input) {
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
                const form = document.querySelector('form');
                if (form) {
                    hiddenInput.value = input.value;  // Sync before submit
                    form.submit();
                }
                break;
            default:
                input.value += isShiftActive ? keyText.toUpperCase() : keyText;
                if (isShiftActive) isShiftActive = false;
        }
        hiddenInput.value = input.value;  // Keep hidden input in sync
        input.focus();
    }
}

function initMobileKeyboard() {
    let inputText = '';
    const inputDisplay = document.getElementById('input-text');
    const hiddenInput = document.getElementById('hidden-answer');

    document.addEventListener('touchstart', function (e) {
        if (e.target.tagName !== 'BUTTON') {
            e.preventDefault();
        }
    }, { passive: false });

    document.querySelectorAll('.key, .space-key').forEach(key => {
        key.addEventListener('click', function () {
            handleKeyPress(this.textContent);
        });
    });

    function handleKeyPress(keyContent) {
        switch (keyContent) {
            case '←':
                inputText = inputText.slice(0, -1);
                break;
            case 'Enter':
                const form = document.querySelector('form');
                if (form) {
                    hiddenInput.value = inputText;
                    form.submit();
                }
                return;
            case ' ':
                inputText += ' ';
                break;
            default:
                inputText += keyContent;
        }
        inputDisplay.textContent = inputText;
        hiddenInput.value = inputText; // Update hidden input as user types
    }

    document.querySelector('.keyboard').addEventListener('touchmove', function (e) {
        e.preventDefault();
    }, { passive: false });

    window.getInputValue = function () {
        return inputText;
    };
}
