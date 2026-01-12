
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".tab-button");
  const contents = document.querySelectorAll(".tab-content");

  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const target = button.dataset.tab;

      buttons.forEach(b => b.classList.remove("active"));
      contents.forEach(c => c.classList.remove("active"));

      button.classList.add("active");
      document.getElementById(target).classList.add("active");
    });
  });
});


document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".entry-abstract").forEach(el => {
    el.addEventListener("click", () => {
      el.classList.toggle("expanded");

      // Re-typeset MathJax when expanding
      if (window.MathJax) {
        MathJax.typesetPromise([el]);
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".entry-authors").forEach(el => {
    el.addEventListener("click", () => {
      el.classList.toggle("expanded");

      // Re-typeset MathJax when expanding
      if (window.MathJax) {
        MathJax.typesetPromise([el]);
      }
    });
  });
});
