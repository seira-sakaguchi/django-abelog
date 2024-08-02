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

// カードタイプのカルーセル2
const mySwiper3 = new Swiper('.card02 .swiper', {
  slidesPerView: 1,
  spaceBetween: 24,
  grabCursor: true,
  pagination: {
    el: '.card02 .swiper-pagination',
    clickable: true,
  },
  navigation: {
    nextEl: '.card02 .swiper-button-next',
    prevEl: '.card02 .swiper-button-prev',
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



//お気に入り機能(ハートマーク)の非同期処理(店舗詳細ページ)
document.addEventListener('DOMContentLoaded', ()=> { 
  document.getElementById('fav-form').addEventListener('submit', (event)=> {
      event.preventDefault(); //これがないとフォームが送信されてしまい、変なJSONデータのページに遷移してしまう。
      const form = event.target;
      const formData = new FormData(form);

      fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
              'X-CSRFToken': formData.get('csrfmiddlewaretoken')
          }
      })
      .then(response => response.json())
      .then(data => {
          if (data.status === 'added') {
              document.getElementById('fav-btn').innerHTML = '<span id="fav"><i class="fa-solid fa-heart-circle-plus"></i></span>';
          } else {
              document.getElementById('fav-btn').innerHTML = 'お気に入りに追加<span id="non-fav"><i class="fa-regular fa-heart"></i></span>';
          }
          document.getElementById('like-count').innerText = `${data.count}件のいいねがあります。`;
      });
  });
});

//お気に入りリストの解除ボタン
document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('.list-form'); //formはひとつだが、その中に複数のお気に入りボタンがあるため、書くボタンがどの店舗に対するアクションかを識別する必要がある。
  forms.forEach(form => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const url = form.action;
      const csrftoken = form.querySelector('[name=csrfmiddlewaretoken]').value;

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken,
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: new FormData(form)
      })
      .then(response => {
        if (!response.ok) { //レスポンスが正常でない場合はエラーを投げる。
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log(data); // レスポンスの内容をコンソールに出力
        const btn = form.querySelector('.list-btn');
        if (data.status === 'added') {
          btn.textContent = 'お気に入りを解除';
          btn.classList.add('btn-design')
        } else {
          btn.innerHTML = 'お気に入り追加 <span><i class="fa-solid fa-heart"></i></span>';
          btn.classList.remove('btn-design');
          btn.classList.add('btn-add');
        }
      })
      .catch(error => console.error('Error:', error));
    });
  });
});