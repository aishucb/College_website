document.addEventListener("DOMContentLoaded", function () {
  var swiper = new Swiper(".slide-container", {
    slidesPerView: 1, // Show one card at a time on mobile
    spaceBetween: 20,
    loop: true,
    centeredSlides: true, // Center the current card
    autoplay: {
      delay: 1500, // Auto play with a 1.5-second delay
    },
    speed: 800, // Smooth transition speed
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
      dynamicBullets: true,
    },
    breakpoints: {
      520: {
        slidesPerView: 2, // Show two cards at a time on tablets
      },
      768: {
        slidesPerView: 3, // Show three cards at a time on small desktops
      },
      1000: {
        slidesPerView: 4, // Show four cards at a time on larger screens
      },
    },
  });
});
