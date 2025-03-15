document.addEventListener('DOMContentLoaded', () => {

  const heroImages = [
    'background_images/hero1.png',
    'background_images/hero2.png',
    'background_images/hero3.png',
    'background_images/hero4.png'
  ];

  const randomIndex = Math.floor(Math.random() * heroImages.length);
  const randomImage = heroImages[randomIndex];

  const heroImageEl = document.getElementById('heroImage');
  if (heroImageEl) {
    heroImageEl.src = randomImage;
  }
});