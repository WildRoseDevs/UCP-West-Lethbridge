function toggleMenu() {
    const mobileNav = document.querySelector('.mobile-nav');
    mobileNav.classList.toggle('show');
}

document.addEventListener("DOMContentLoaded", function () {
    const yayButtons = document.querySelectorAll(".btn.yay");
    const nayButtons = document.querySelectorAll(".btn.nay");

    yayButtons.forEach((button) => {
        button.addEventListener("click", function () {
            let card = this.closest(".card");
            card.classList.add("yay-animation");

            setTimeout(() => {
                card.classList.remove("yay-animation");
            }, 1000); // Reset after animation
        });
    });

    nayButtons.forEach((button) => {
        button.addEventListener("click", function () {
            let card = this.closest(".card");
            card.classList.add("nay-animation");

            setTimeout(() => {
                card.classList.remove("nay-animation");
            }, 1000); // Reset after animation
        });
    });
});
