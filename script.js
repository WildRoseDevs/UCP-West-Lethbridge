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
            card.classList.remove("nay-animation");
            card.classList.add("yay-animation");

            setTimeout(() => {
                card.classList.add("fade-out");
            }, 1000);

            setTimeout(() => {
                card.classList.remove("yay-animation", "fade-out");
            }, 2000);
        });
    });

    nayButtons.forEach((button) => {
        button.addEventListener("click", function () {
            let card = this.closest(".card");
            card.classList.remove("yay-animation");
            card.classList.add("nay-animation");

            setTimeout(() => {
                card.classList.add("fade-out");
            }, 1000);

            setTimeout(() => {
                card.classList.remove("nay-animation", "fade-out");
            }, 2000);
        });
    });
});
