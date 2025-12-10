// 버튼 요소 가져오기
const button = document.getElementById('log-button'); // 첫 번째 요소 선택

// 버튼이 존재할 경우 이벤트 리스너 추가
if(button){
  button.addEventListener("click", () => {
    // 버튼 클릭 시 hello.html로 이동
    window.location.href = "/login/"
  });
}