document.addEventListener("DOMContentLoaded", function () {
  new Swiper(".examples-swiper", {
    slidesPerView: 4,
    spaceBetween: 16,
    loop: true,
    autoplay: { delay: 3000, disableOnInteraction: false },
    pagination: { el: ".examples-pagination", clickable: true },
    breakpoints: {
      320:  { slidesPerView: 1, spaceBetween: 12 },
      768:  { slidesPerView: 2, spaceBetween: 14 },
      1024: { slidesPerView: 4, spaceBetween: 16 },
    },
  });
});
