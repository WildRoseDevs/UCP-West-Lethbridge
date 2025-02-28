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
            if (!card.classList.contains("yay-animation")) {
                card.classList.remove("nay-animation");
                card.classList.add("yay-animation");
            }
        });
    });

    nayButtons.forEach((button) => {
        button.addEventListener("click", function () {
            let card = this.closest(".card");
            if (!card.classList.contains("nay-animation")) {
                card.classList.remove("yay-animation");
                card.classList.add("nay-animation");
            }
        });
    });
});
