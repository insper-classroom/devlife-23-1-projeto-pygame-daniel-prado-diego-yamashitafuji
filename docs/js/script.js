function menubar(id) {
    const section = document.getElementById(id);
    window.scrollTo({
        top: section.offsetTop,
        behavior: 'smooth'
    });
}