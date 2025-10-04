(function(){
  // CSRF helper
  // getCookie function is defined at the bottom of the file, so we use that implementation.
  const CSRFTOKEN = getCookie('csrftoken');

  // Toasts
  const wrap = document.getElementById('toastWrap');
  function toast(msg){
    if(!wrap) return;
    const t = document.createElement('div');
    t.className = 'toast-item';
    t.innerHTML = `<div class="toast-body">${msg}</div>`;
    wrap.appendChild(t);
    setTimeout(()=>t.classList.add('show'), 10);
    setTimeout(()=>{ t.classList.remove('show'); setTimeout(()=>t.remove(), 250); }, 2500);
  }

  // Mini-cart toggle
  const miniBtn = document.getElementById('miniCartBtn');
  const mini = document.getElementById('miniCart');
  if(miniBtn && mini){
    miniBtn.addEventListener('mouseenter', () => mini.classList.add('open'));
    miniBtn.addEventListener('mouseleave', () => setTimeout(()=>mini.classList.remove('open'), 200));
    mini.addEventListener('mouseenter', ()=>mini.classList.add('open'));
    mini.addEventListener('mouseleave', ()=>mini.classList.remove('open'));
    // position near button
    const pos = () => {
      const r = miniBtn.getBoundingClientRect();
      mini.style.top = (r.bottom + window.scrollY + 6) + 'px';
      mini.style.right = (document.body.clientWidth - (r.right + window.scrollX)) + 'px';
    };
    window.addEventListener('resize', pos); window.addEventListener('scroll', pos); pos();
  }

  // Quick add-to-cart buttons (product list)
  document.querySelectorAll('[data-add-to-cart]').forEach(btn=>{
    btn.addEventListener('click', async (e)=>{
      e.preventDefault();
      const url = btn.dataset.url;
      const name = btn.dataset.name || 'Item';
      try{
        await fetch(url, {
          method: 'POST',
          headers: {
            'X-CSRFToken': CSRFTOKEN,
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: 'quantity=1'
        });
        toast(`✅ Added <b>${name}</b> to cart`);
        // Optimistically bump badge
        const badge = document.querySelector('#miniCartBtn .badge');
        if(badge){ badge.textContent = (parseInt(badge.textContent||'0',10)+1).toString(); }
      }catch(err){ toast('⚠️ Could not add to cart'); }
    });
  });

  // Intercept add-to-cart form on product detail
  const addForm = document.querySelector('[data-add-to-cart-form]');
  if(addForm){
    addForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const formData = new FormData(addForm);
      try{
        const res = await fetch(addForm.action, { method:'POST', body: formData, headers:{'X-CSRFToken': CSRFTOKEN}});
        toast(`✅ Added <b>${addForm.dataset.name||'Item'}</b> to cart`);
        const badge = document.querySelector('#miniCartBtn .badge');
        if(badge){ badge.textContent = (parseInt(badge.textContent||'0',10)+1).toString(); }
      }catch(err){ toast('⚠️ Could not add to cart'); }
    });
  }

  // Cart quantity +/- via AJAX
  document.querySelectorAll('.cart-table form').forEach(f=>{
    f.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const btn = e.submitter;
      const row = f.closest('.cart-row');
      const qtyInput = row.querySelector('.qty-input');
      const priceEl = row.querySelector('[data-price]');
      const price = parseFloat(priceEl?.dataset.price||'0');
      const prevQty = parseInt(qtyInput.value, 10);
      const action = btn?.value;
      try{
        await fetch(f.action, { method:'POST', headers:{'X-CSRFToken': CSRFTOKEN}, body: new URLSearchParams({action}) });
        const nextQty = Math.max( action==='decrease' ? prevQty-1 : prevQty+1, 1);
        qtyInput.value = nextQty;
        // Update row total (if there is a cell with total text-success)
        const totalCell = row.querySelector('.text-success');
        if(totalCell){ totalCell.textContent = '$' + (price * nextQty).toFixed(2); }
        // Recalc cart total
        let sum = 0;
        document.querySelectorAll('.cart-row').forEach(r=>{
          const p = parseFloat(r.querySelector('[data-price]')?.dataset.price||'0');
          const q = parseInt(r.querySelector('.qty-input')?.value||'1',10);
          sum += p*q;
        });
        const cartTotal = document.getElementById('cartTotal');
        if(cartTotal){ cartTotal.textContent = '$' + sum.toFixed(2); }
      }catch(err){ window.location.reload(); }
    });
  });

  // Checkout Wizard (front-end only)
  const wizard = document.querySelector('[data-wizard]');
  if(wizard){
    const steps = Array.from(document.querySelectorAll('.checkout-steps .step'));
    const prev = document.querySelector('[data-prev]');
    const next = document.querySelector('[data-next]');
    const submit = document.querySelector('[data-submit]');
    let idx = 0;

    function apply(){
      steps.forEach((s,i)=> s.classList.toggle('active', i<=idx));
      // simple: show/hide groups based on idx
      const groups = [
        ['#full_name', '#phone', '#address', '#city'],
        ['#cod', '#card'],
        [] // review step (nothing extra)
      ];
      // enable all fields
      wizard.querySelectorAll('input,textarea,select').forEach(el=> el.closest('.mb-3,.form-check')?.classList.remove('d-none'));
      // hide others if before their step
      if(idx===0){
        wizard.querySelectorAll('#cod,#card').forEach(el=> el.closest('.form-check')?.classList.add('d-none'));
        submit.hidden = true;
      } else if(idx===1){
        wizard.querySelectorAll('#full_name,#phone,#address,#city').forEach(el=> el.closest('.mb-3')?.classList.add('d-none'));
        submit.hidden = true;
      } else {
        wizard.querySelectorAll('#full_name,#phone,#address,#city').forEach(el=> el.closest('.mb-3')?.classList.add('d-none'));
        wizard.querySelectorAll('#cod,#card').forEach(el=> el.closest('.form-check')?.classList.add('d-none'));
        submit.hidden = false;
      }
      prev.disabled = idx===0;
      next.hidden = idx===2;
    }
    prev?.addEventListener('click', ()=>{ idx = Math.max(0, idx-1); apply(); });
    next?.addEventListener('click', ()=>{ idx = Math.min(2, idx+1); apply(); });
    apply();
  }
})();
// Enhanced Preloader
window.addEventListener('load', function() {
  const preloader = document.getElementById('preloader');
  setTimeout(() => {
    preloader.style.opacity = '0';
    setTimeout(() => {
      preloader.style.display = 'none';
    }, 300);
  }, 500);
});

// Enhanced Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Product Image Lazy Loading
const lazyImages = document.querySelectorAll('img[loading="lazy"]');
const imageObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      if (img.dataset.src) {
        img.src = img.dataset.src;
      }
      img.classList.remove('lazy');
      imageObserver.unobserve(img);
    }
  });
});

lazyImages.forEach(img => imageObserver.observe(img));

// Add to Cart Animation
function animateAddToCart(button, productName) {
  const originalText = button.innerHTML;
  button.innerHTML = '<div class="loading-spinner"></div>';
  button.disabled = true;
  
  setTimeout(() => {
    button.innerHTML = '<i class="fas fa-check"></i> Added!';
    setTimeout(() => {
      button.innerHTML = originalText;
      button.disabled = false;
    }, 2000);
  }, 1000);
  
  // Update cart count with animation
  const cartCount = document.querySelector('#miniCartBtn .badge');
  if (cartCount) {
    const currentCount = parseInt(cartCount.textContent) || 0;
    cartCount.textContent = currentCount + 1;
    cartCount.style.transform = 'scale(1.2)';
    setTimeout(() => {
      cartCount.style.transform = 'scale(1)';
    }, 300);
  }
}

// Initialize all interactive elements
document.addEventListener('DOMContentLoaded', function() {
  // Add to cart buttons
  document.querySelectorAll('[data-add-to-cart]').forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const productName = this.getAttribute('data-name');
      animateAddToCart(this, productName);
      fetch(this.getAttribute('data-url'), {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'quantity=1'
      }).then(response => {
        if (response.ok) {
          toast(`✅ Added <b>${productName}</b> to cart`);
          return response.json();
        }
        throw new Error('Failed to add item to cart');
      }).then(data => {
        // Success handling if needed
      }).catch(error => {
        toast('⚠️ Failed to add item to cart');
      });
    });
  });

  // Wishlist button handlers
  document.querySelectorAll('.btn-wishlist').forEach(button => {
    button.addEventListener('click', function() {
      const message = this.classList.contains('active') ? 
        'Added to wishlist' : 'Removed from wishlist';
      this.classList.toggle('active');
      this.innerHTML = this.classList.contains('active') ? 
        '<i class="fas fa-heart"></i>' : 
        '<i class="far fa-heart"></i>';
      toast(message);
    });
  });
});