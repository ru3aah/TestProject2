document.addEventListener('DOMContentLoaded', () => {

  const heroImages = [
    'background_images/1.png',
    'background_images/2.png',
    'background_images/3.png',
    'background_images/4.png',
    'background_images/5.png'
  ];

  const randomIndex = Math.floor(Math.random() * heroImages.length);
  const randomImage = heroImages[randomIndex];

  const heroImageEl = document.getElementById('heroImage');
  if (heroImageEl) {
    heroImageEl.src = randomImage;
  }
});