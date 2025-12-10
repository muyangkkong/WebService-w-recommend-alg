const button = document.getElementsByClassName("home-button")[0]

if(button){
  button.addEventListener("click", () => {
    // 버튼 클릭 시 hello.html로 이동
    window.location.href = "/"
  });
}
