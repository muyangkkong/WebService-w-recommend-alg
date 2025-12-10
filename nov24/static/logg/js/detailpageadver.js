
function button_event(){
  if (confirm("신청하시겠습니까?") == true){    //확인
      document.form.submit();
  }else{   //취소
      return;
  }
}
