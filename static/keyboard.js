document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('input');
    const backspaceKey = document.getElementById('backspace-key');
    const enterKey = document.getElementById('enter-key');
    const form = document.querySelector('.quiz-form');

    // Handle all keys (including space)
    document.querySelectorAll('.key').forEach(key => {
        if (!key.classList.contains('special-key')) {
            key.addEventListener('click', () => {
                input.value += key.dataset.key;
                input.focus();
            });
        }
    });

    // Handle Backspace
    backspaceKey.addEventListener('click', () => {
        input.value = input.value.slice(0, -1);
        input.focus();
    });

    // Handle Enter
    enterKey.addEventListener('click', () => {
        form.submit();
    });
});
