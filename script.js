function toggleMenu() {
    let nav = document.querySelector("nav ul");
    if (window.innerWidth <= 768) { 
        nav.classList.toggle("show");
    }
}
