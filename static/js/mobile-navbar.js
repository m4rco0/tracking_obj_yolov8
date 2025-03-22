function handleClick(navList) {
    console.log(this)
    navList.classList.toggle("active");
}
function animateLinks(navLinks) {
    navLinks.forEach((link, index) => {
        link.style.animation  ? link.style.animation = "": link.style.animation = `navLinkFade 0.5s ease forwards 0.3s`
    });
}
function addClickEvent(mobileMenu, navList, navLinks) {
    mobileMenu.addEventListener("click", () => handleClick(navList))
    animateLinks(navLinks)
}

let mobileMenu = document.querySelector('.mobile-menu')
let navList = document.querySelector('.nav-list')
let navLinks = document.querySelectorAll('.nav-list li')

addClickEvent(mobileMenu, navList, navLinks)