function toggleMenu() {
    const mobileNav = document.querySelector('.mobile-nav');
    mobileNav.classList.toggle('show');
}

document.addEventListener("DOMContentLoaded", function () {
    const yayButtons = document.querySelectorAll(".btn.yay");
    const nayButtons = document.querySelectorAll(".btn.nay");

    function animateCard(card, animationClass) {
        card.classList.add(animationClass);

        setTimeout(() => {
            card.classList.add("hold-color");
        }, 600); // Holds the color after the wave finishes

        setTimeout(() => {
            card.classList.add("fade-out");
        }, 1400); // Start fading out

        setTimeout(() => {
            card.classList.remove(animationClass, "hold-color", "fade-out");
        }, 2000); // Fully reset after animation
    }

    yayButtons.forEach((button) => {
        button.addEventListener("click", function () {
            let card = this.closest(".card");
            animateCard(card, "yay-animation");
        });
    });

    nayButtons.forEach((button) => {
        button.addEventListener("click", function () {
            let card = this.closest(".card");
            animateCard(card, "nay-animation");
        });
    });
});
