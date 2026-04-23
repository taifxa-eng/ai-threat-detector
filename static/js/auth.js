document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.login-card');
    if (hero) {
        hero.style.opacity = '0';
        hero.style.transform = 'translateY(16px)';
        requestAnimationFrame(() => {
            hero.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            hero.style.opacity = '1';
            hero.style.transform = 'translateY(0)';
        });
    }
});
