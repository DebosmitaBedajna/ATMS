document.addEventListener("DOMContentLoaded", function () {
    // const signInButton = document.getElementById('sgnbttn');
    // const originalBackgroundColor = getComputedStyle(signInButton).backgroundColor;

    // signInButton.addEventListener('click', function () {
    //     signInButton.style.backgroundColor = 'transparent';
    //     setTimeout(function () {
    //         signInButton.style.backgroundColor = originalBackgroundColor;
    //     }, 500); // 500 milliseconds (0.5 seconds)
    // });

    const totalDiv = document.querySelector('.total');
    setTimeout(function() {
        totalDiv.style.display = 'none';
    }, 3000);
});
