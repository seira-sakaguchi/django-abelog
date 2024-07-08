//スマホの時のみハンバーガーメニューを表示
document.addEventListener('DOMContentLoaded', () => {
  const ham = document.querySelector('#js-hamburger');
  const nav = document.querySelector('#js-nav');

  ham.addEventListener('click', () => {
    ham.classList.toggle('active'); // ハンバーガーメニューにactiveクラスを付け外し
    nav.classList.toggle('active'); // ナビゲーションメニューにactiveクラスを付け外し
  });
});


//メインビジュアルスライド
const mySwiper = new Swiper('.mv01 .swiper', {
  effect: 'fade',
  fadeEffect: {
    crossFade: true,
  },
  loop: true,
  loopAdditionalSlides: 1,
  speed: 2000,
  autoplay: {
    delay: 7000,
    disableOnInteraction: false,
    waitForTransition: false,
  },
  followFinger: false,
  pagination: {
    el: '.mv01 .swiper-pagination',
    clickable: true,
  },
});

//カードタイプのカルーセル
const mySwiper2 = new Swiper('.card01 .swiper', {
  slidesPerView: 1,
  spaceBetween: 24,
  grabCursor: true,
  pagination: {
    el: '.card01 .swiper-pagination',
    clickable: true,
  },
  navigation: {
    nextEl: '.card01 .swiper-button-next',
    prevEl: '.card01 .swiper-button-prev',
  },
  breakpoints: {
    600: {
      slidesPerView: 2,
    },
    1025: {
      slidesPerView: 4,
      spaceBetween: 32,
    }
  },
});