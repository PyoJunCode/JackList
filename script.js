$(function() {
var toggle= false;
var width=340;
var height=228;
var i =0;
var r_count = 0;
var y_count =0;
var temp_count=0;
var check = false;
var r_arrImageUrl = [];
var r_arrItemName = [];
var r_arrItemPrice = [];
var r_arrItemReview=[];
var r_arrItemRer_count=[];
var r_arrPageUrl=[];

var y_arrImageUrl = [];
var y_arrItemName = [];
var y_arrItemPrice = [];
var y_arrItemReview=[];
var y_arrItemRer_count=[];
var y_arrPageUrl=[];

var r_fselectValue=0;
var r_sselectValue=0;
var r_tselectValue=0;

var y_fselectValue=0;
var y_sselectValue=0;

var genreId = new Array();
var genreId2 = new Array();
var y_genreId = new Array();


var r_mainCategoryArray = new Array();
var r_mainCategoryObject = new Object();
var r_secCategoryArray = new Array();
var r_thirdCategoryArray = new Array();

var y_mainCategoryArray = new Array();
var y_secCategoryArray = new Array();

var para = "?genreId=";
var baseUrl;
var gId;
var r_arrItemObject = new Object();

var r_topselector = $("span[name='r_topselector']");
var r_secselector = $("span[name='r_secselector']");
var r_thrselector = $("span[name='r_thrselector']");

var y_topselector = $("span[name='y_topselector']");
var y_secselector = $("span[name='y_secselector']");

var r_mainCategorySelectBox = $("select[name='r_mainCategory']");
var r_subCategorySelectBox = $("select[name='r_subCategory']");
var r_thirdCategorySelectBox = $("select[name='r_thirdCategory']");

var y_mainCategorySelectBox = $("select[name='y_mainCategory']");
var y_subCategorySelectBox = $("select[name='y_subCategory']");

//데이터 디폴트 페이지 정보 가져오기

item_ajax('http://127.0.0.1:5000/rakuten_selected_ranking',para,0,1);
// item_ajax('http://127.0.0.1:5000/yahoo_selected_ranking',para,1,3);
// item_ajax("http://127.0.0.1:5000/yahoo_cate",'','',4);

   //******************** 키워드 검색 및 카테고리 클릭 **************************
$(document).ready(function(){

  cat_init();
     $("#submit").click(function(){
       toggle = true;
       initialize('ry'); //기존 화면의 데이터 초기
      if(r_fselectValue==0){ //아무것도 선택 안한 경우
        var temp=[0];
        post('http://127.0.0.1:5000/rakuten_searched',para,$("#input").val(),temp,1);
      }
      else if(r_sselectValue!=0 && r_tselectValue!=0){ //소분류까지 선택한 경우
        var temp=[r_thirdCategoryArray[r_tselectValue-1].genreId];
        post('http://127.0.0.1:5000/rakuten_searched',para,$("#input").val(),temp,1);
      } //다 선택
      else{//대분류 혹은 중분류까지 선택한 경우
        post('http://127.0.0.1:5000/rakuten_searched',para,$("#input").val(),genreId2,1);
      }
      if(y_fselectValue==0){ //아무것도 선택 안한 경우
        var temp=[0];
        post('http://127.0.0.1:5000/yahoo_searched',para,$("#input").val(),temp,3);
      }
      else if(y_sselectValue==0){ //대분류만선택한 경우
          post('http://127.0.0.1:5000/yahoo_searched',para,$("#input").val(),y_genreId,3);
      } //다 선택
      else{//중분류까지 선택한 경우
        var temp=[y_secCategoryArray[y_sselectValue-1].genreId];
        post('http://127.0.0.1:5000/yahoo_searched',para,$("#input").val(),temp,3);
      }
     });
     $("#r_topselector").click(function(){
        f_Click();
     });
     $("#r_secselector").click(function(){
       s_Click();
     });
     $("#r_thrselector").click(function(){
       t_Click();
        });

       $("#y_topselector").click(function(){
          y_f_Click();
       });
       $("#y_secselector").click(function(){
         y_s_Click();
       });
  });

  //*************************** 카테고리 셀렉트박스로 접근하는 경!!!!!!!!!!!!!!!!!!!!!!!!!!1
    for(i=0;i<r_mainCategoryArray.length;i++){
        r_mainCategorySelectBox.append("<option value='"+r_mainCategoryArray[i].id+"'>"+r_mainCategoryArray[i].cateName+"</option>");
      }
    //*********** 라쿠텐 1depth카테고리 선택 후 2depth 생성 START ***********
    $(document).on("change","select[name='r_mainCategory']",function(){    //첫번째 카테고리 선택한 상황
        //***********선택한 첫번째 박스의 값을 가져와 일치하는 값을 두번째 셀렉트 박스에 넣는다.***********
        $("option:selected", this).each(function(){
          r_fselectValue = $(this).val(); //main category 에서 선택한 값
          f_Click();
        });
    });

    //*********** 야후 1depth카테고리 선택 후 2depth 생성 START ***********
    $(document).on("change","select[name='y_mainCategory']",function(){    //첫번째 카테고리 선택한 상황
        //***********선택한 첫번째 박스의 값을 가져와 일치하는 값을 두번째 셀렉트 박스에 넣는다.***********
        $("option:selected", this).each(function(){
          y_fselectValue = $(this).val(); //main category 에서 선택한 값
          y_f_Click();
        });
    });

    //*********** 라쿠텐 2depth카테고리 선택 후 3depth 생성 START ***********
    $(document).on("change","select[name='r_subCategory']",function(){    //두번째 셀렉트 박스 선택한 상황
      //****** 두,세번째 세부항목과 셀렉트박스 초기화 ***********
        $("option:selected", this).each(function(){//두번째 셀렉트 박스의 값을 고른 상황
          r_sselectValue = $(this).val(); //main category 에서 선택한 값
          s_Click();
        });
    });

    //*********** yahoo 2depth카테고리 선택 후 3depth 생성 START ***********
    $(document).on("change","select[name='y_subCategory']",function(){    //두번째 셀렉트 박스 선택한 상황
      //****** 두,세번째 세부항목과 셀렉트박스 초기화 ***********
        $("option:selected", this).each(function(){//두번째 셀렉트 박스의 값을 고른 상황
          y_sselectValue = $(this).val(); //main category 에서 선택한 값
          y_s_Click();
        });
    });

    //라쿠텐세번째 셀렉트 박스 선택한 상황
    $(document).on("change","select[name='r_thirdCategory']",function(){
        //세번째 셀렉트 박스를 삭제 시킨다.
        $("option:selected", this).each(function(){
          r_tselectValue = $(this).val(); //main category 에서 선택한 값
          t_Click();
        });
    });

    function y_making_one_div(){
        var img = document.createElement("IMG");
        var num = document.createElement("P");
        var a = document.createElement("a");
        var linkText = document.createTextNode(y_arrItemName[y_count]);
        var div = document.createElement("DIV");
         div.setAttribute("style"," text-align:center; display:inline-block; border: 1px solid black; margin-top:3px");
         a.setAttribute("style", "text-decoration: none; color:#0080FF");
         num.setAttribute("style", "font-size:18px; color:red;");
         img.setAttribute("src", y_arrImageUrl[y_count]);
         img.setAttribute("width", width);
         img.setAttribute("height", height);

         a.appendChild(img);
         a.href = y_arrPageUrl[y_count];
         a.appendChild(linkText);

          num.innerHTML=y_count+1+"위";

          div.appendChild(num);
          div.appendChild(a);
          div.innerHTML+=y_arrItemPrice[y_count];
        var yellow = Math.round(y_arrItemReview[y_count] * 2) / 2;
        var white = 5 - yellow;
        for ( ; yellow >= 1; yellow--)
        {
          var star = document.createElement("i");
          star.setAttribute("style", "color:#D7DF01; ");
          star.className = "fa fa-star text-yellow";
          div.appendChild(star);
        }
        if (yellow == .5) {
          var star = document.createElement("i");
          star.setAttribute("style", "color:#D7DF01;");
          star.className = "fa fa-star-half-o text-yellow";
          div.appendChild(star);
        }
        for ( ; white >= 1; white--)
        {
          var star = document.createElement("i");
          star.className = "fa fa-star-o ";
          star.setAttribute("style", "color:#D7DF01;");
          div.appendChild(star);
        }
        var review = document.createElement("SPAN");
        review.innerHTML = "("+y_arrItemRer_count[y_count]+")건";
        div.appendChild(review);
         document.getElementById("y_myList").appendChild(div);

        y_count++;
    }

function making_one_div(){
    var img = document.createElement("IMG");
    var num = document.createElement("P");
    var a = document.createElement("a");
    var linkText = document.createTextNode(r_arrItemName[r_count]);
    var div = document.createElement("DIV");
     div.setAttribute("style"," text-align:center; display:inline-block; border: 1px solid black; margin-top:3px");
     a.setAttribute("style", "text-decoration: none; color:#0080FF");
     num.setAttribute("style", "font-size:18px; color:red;");
     img.setAttribute("src", r_arrImageUrl[r_count]);
     img.setAttribute("width", width);
     img.setAttribute("height", height);

     a.appendChild(img);
     a.href = r_arrPageUrl[r_count];
     a.appendChild(linkText);

      num.innerHTML=r_count+1+"위";

      div.appendChild(num);
      div.appendChild(a);
      div.innerHTML+=r_arrItemPrice[r_count];
    var yellow = Math.round(r_arrItemReview[r_count] * 2) / 2;
    var white = 5 - yellow;
    for ( ; yellow >= 1; yellow--)
    {
      var star = document.createElement("i");
      star.setAttribute("style", "color:#D7DF01; ");
      star.className = "fa fa-star text-yellow";
      div.appendChild(star);
    }
    if (yellow == .5) {
      var star = document.createElement("i");
      star.setAttribute("style", "color:#D7DF01;");
      star.className = "fa fa-star-half-o text-yellow";
      div.appendChild(star);
    }
    for ( ; white >= 1; white--)
    {
      var star = document.createElement("i");
      star.className = "fa fa-star-o ";
      star.setAttribute("style", "color:#D7DF01;");
      div.appendChild(star);
    }
    var review = document.createElement("SPAN");
    review.innerHTML = "("+r_arrItemRer_count[r_count]+")건";
    div.appendChild(review);
     document.getElementById("r_myList").appendChild(div);

    r_count++;
}

function initialize(what){
  if(what.includes('r')){
  var child =document.getElementById("r_myList");
          $("#r_myList").empty();
          r_count=0;
          check =false;
          r_arrImageUrl = [];
          r_arrItemName = [];
          r_arrItemPrice = [];
          r_arrItemReview=[];
          r_arrItemRer_count=[];
  }
  if(what.includes('y')){
    var child =document.getElementById("y_myList");
    $("#y_myList").empty();
    y_count=0;
    check =false;
    y_arrImageUrl = [];
    y_arrItemName = [];
    y_arrItemPrice = [];
    y_arrItemReview=[];
    y_arrItemRer_count=[];
  }

}

function y_arrPush_print(result){
  for (i in result){
    y_arrImageUrl.push(result[i].mediumImageUrls);
    y_arrItemName.push(result[i].itemName);
    y_arrItemPrice.push("<p style=\"color:red;text-align:center;\">"+result[i].itemPrice+"円</p>");
    y_arrItemReview.push(result[i].reviewAverage);
    y_arrItemRer_count.push(result[i].reviewr_count);
    y_arrPageUrl.push(result[i].itemUrl);
  }
  for(i=0;i<5;i++){
  y_making_one_div();
  }
//window.onscroll =function(){y_scroll_Throw()};
}

function arrPush_print(result){
  for (i in result){
    r_arrImageUrl.push(result[i].mediumImageUrls);
    r_arrItemName.push(result[i].itemName);
    r_arrItemPrice.push("<p style=\"color:red;text-align:center;\">"+result[i].itemPrice+"円</p>");
    r_arrItemReview.push(result[i].reviewAverage);
    r_arrItemRer_count.push(result[i].reviewr_count);
    r_arrPageUrl.push(result[i].itemUrl);
  }
  for(i=0;i<5;i++){
  making_one_div();
  }
  window.onscroll =function(){
    scroll_Throw();
  };

}
function f_init(){
  //전체 세부 카테고리 항목를 지운다
  r_topselector.children().remove();
  r_secselector.children().remove();
  r_thrselector.children().remove();
  r_subCategorySelectBox.children().remove(); //두번째 셀렉트 박스를 초기화 시킨다.
  r_thirdCategorySelectBox.children().remove(); //세번째 셀렉트 박스를 초기화 시킨다.
}

function item_ajax(baseUrl,param,gId,number){
  $.ajax({
      type:"GET",
      dataType : 'JSON',
      url:baseUrl+param+gId,
      success: function(result) {
        switch (number) {
          case 1:arrPush_print(result);
            break;
          case 3:y_arrPush_print(result);
            break;
          case 4:y_cate_append(result);
            break;
        }
      },
        error : function(xtr,status,error){
          alert(xtr +":"+status+":"+error);
       }
    });
}
function y_cate_append(result){
  result.filter(function(element){
    if(element.depth==1){
      element.main_category_id = ++temp_count;
      y_mainCategoryArray.push(element);
      y_mainCategorySelectBox.append("<option value='"+temp_count+"'>"+element.cateName+"</option>");
    }
  });
}

var g_json;
function y_cate_ajax(){
  y_genreId = new Array();
  y_secCategoryArray = new Array();
  $.ajax({
      type:"GET",
      dataType : 'JSON',
      url:"http://127.0.0.1:5000/yahoo_cate",
      success: function(result) {
          result.filter(function(element){
            for(var j=0; j<y_mainCategoryArray[y_fselectValue-1].children.length;j++){
              if(element.id == y_mainCategoryArray[y_fselectValue-1].children[j]){
                g_json = new Object();
                g_json.children = element.genreId;
                g_json.genreId =y_mainCategoryArray[y_fselectValue-1].genreId;
                y_genreId.push(g_json);
                element.main_category_id = String(y_fselectValue);
                element.sub_category_id = String(j+1);
                y_secCategoryArray.push(element);
                y_subCategorySelectBox.append("<option value='"+element.sub_category_id+"'>"+element.cateName+"</option>");
                }
              }
          });
        }
    });

}

function cate_ajax(){
  genreId = new Array();
  genreId2 = new Array();
  r_secCategoryArray = new Array();
  $.ajax({
      type:"GET",
      dataType : 'JSON',
      url:"http://127.0.0.1:5000/rakuten_cate",
      success: function(result) {
          //첫번째 id의 children 값들 가져오기
          result.filter(function(element){
            for(var j=0; j<r_mainCategoryArray[r_fselectValue-1].children.length;j++){
              if(element.id == r_mainCategoryArray[r_fselectValue-1].children[j]){
                g_json = new Object();
                g_json.children = element.children;
                g_json.genreId = element.genreId;
                genreId.push(g_json);
                element.main_category_id = String(r_fselectValue);
                element.sub_category_id = String(j+1);
                r_secCategoryArray.push(element);
                r_subCategorySelectBox.append("<option value='"+element.sub_category_id+"'>"+element.cateName+"</option>");
                }
              }
              for(i=0;i<genreId.length;i++){
                for(var j=0;j<genreId[i].children.length;j++){
                  if(element.id==genreId[i].children[j]){
                    g_json = new Object();
                    g_json.children = element.genreId;
                    g_json.genreId = genreId[i];
                    genreId2.push(g_json);
                  }
                }
              }
          });
        }
    });

}
function cat_init(){
  r_mainCategoryObject.id = "1";
  r_mainCategoryObject.cateName = "スポーツ・ゴルフ";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["102"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "2";
  r_mainCategoryObject.cateName = "ファッション・インナー";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["1","22","37"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "3";
  r_mainCategoryObject.cateName = "ファッション小物";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["42","62","67","77"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "4";
  r_mainCategoryObject.cateName = "キッズ・ベビー・玩具";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["88","95"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "5";
  r_mainCategoryObject.cateName = "家電・TV・カメラ";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["136","146"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "6";
  r_mainCategoryObject.cateName = "PC・スマホ・通信";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["161","180","193"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "7";
  r_mainCategoryObject.cateName = "食品・スイーツ";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["199","218"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "8";
  r_mainCategoryObject.cateName = "ドリンク・お酒";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["235","257","274"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "9";
  r_mainCategoryObject.cateName = "本・電子書籍・音楽";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["338","367"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "10";
  r_mainCategoryObject.cateName = "ゲーム・ホビー・楽器";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["376","393"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "11";
  r_mainCategoryObject.cateName = "車・バイク";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["407","412"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "12";
  r_mainCategoryObject.cateName = "インテリア・寝具";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["279"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "13";
  r_mainCategoryObject.cateName = "日用雑貨・キッチン用品";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["306","323"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "14";
  r_mainCategoryObject.cateName = "ペット・花・DIY工具";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["454","469"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "15";
  r_mainCategoryObject.cateName = "コスメ・健康・医薬品";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["416","431","440"];
  r_mainCategoryArray.push(r_mainCategoryObject);

  r_mainCategoryObject = new Object();
  r_mainCategoryObject.id = "16";
  r_mainCategoryObject.cateName = "サービス・リフォーム";
  r_mainCategoryObject.depth = "1";
  r_mainCategoryObject.children = ["478","494"];
  r_mainCategoryArray.push(r_mainCategoryObject);
}
function t_Click(){
  r_thrselector.children().remove();
  for(var i=0;i<r_thirdCategoryArray.length;i++){
      if(r_fselectValue == r_thirdCategoryArray[i].main_category_id && r_sselectValue==r_thirdCategoryArray[i].sub_category_id && r_tselectValue == r_thirdCategoryArray[i].thr_category_id){
        r_thrselector.append("<a href='#'>"+r_thirdCategoryArray[i].cateName+"</a>");
        break;
      }
  }
  initialize('r');
//********************신경쓸 부분*************************
    if(toggle){
    var temp= [r_thirdCategoryArray[r_tselectValue-1].genreId];
    post('http://127.0.0.1:5000/rakuten_searched',para,$("#input").val(),temp,1);
    }
    else{
    item_ajax('http://127.0.0.1:5000/rakuten_selected_ranking',para,r_thirdCategoryArray[r_tselectValue-1].genreId,1);
    }
}
function s_Click(){
  r_secselector.children().remove();
  r_thrselector.children().remove();
   r_thirdCategorySelectBox.children().remove();
  for(var i=0;i<r_secCategoryArray.length;i++){ //두번째 세부항목을 넣어보자.
  if(r_fselectValue==r_secCategoryArray[i].main_category_id && r_sselectValue==r_secCategoryArray[i].sub_category_id){
    r_secselector.append("<a href='#'>"+r_secCategoryArray[i].cateName+"</a>"+"<span> > </span>");
    break;
    }
  }
  r_thirdCategorySelectBox.append("<option value=''>전체</option>"); //세번째 셀렉트 베이스 초기화
  //****** 세번째 셀렉트 박스 내용 만들기 ***********
  initialize('r');//기존 자료 자료들 지우기
//********************신경쓸 부분*************************
genreId = new Array();
genreId2 = new Array();
   $.ajax({
       type:"GET",
       dataType : 'JSON',
       url:"http://127.0.0.1:5000/rakuten_cate",
       success: function(result) {
           result.filter(function(element){
               for(var j=0;j<r_secCategoryArray[r_sselectValue-1].children.length;j++){
               if(element.id==r_secCategoryArray[r_sselectValue-1].children[j]){
                 g_json = new Object();
                 g_json.children = element.children;
                 g_json.genreId = element.genreId;
                 genreId.push(g_json);
                 element.main_category_id = String(r_fselectValue);
                 element.sub_category_id = String(r_sselectValue);
                 element.thr_category_id = String(j+1);
                 r_thirdCategoryArray.push(element);
                 r_thirdCategorySelectBox.append("<option value='"+element.thr_category_id+"'>"+element.cateName+"</option>");
              }
             }
             for(i=0;i<genreId.length;i++){
               for(var j=0;j<genreId[i].children.length;j++){
                 if(element.id==genreId[i].children[j]){
                   g_json = new Object();
                   g_json.children = element.genreId;
                   g_json.genreId = genreId[i];
                   genreId2.push(g_json);
                 }
               }
             }

           });
         }
     });
if(toggle){ //검색한 경우
       post('http://127.0.0.1:5000/rakuten_searched',para,$("#input").val(),genreId2,1);
}
else { //검색 안한 경우
  item_ajax('http://127.0.0.1:5000/rakuten_selected_ranking',para,r_secCategoryArray[r_sselectValue-1].genreId,1);
}
}
function y_s_Click(){
  y_secselector.children().remove();

  for(var i=0;i<y_secCategoryArray.length;i++){ //두번째 세부항목을 넣어보자.
  if(y_fselectValue==y_secCategoryArray[i].main_category_id && y_sselectValue==y_secCategoryArray[i].sub_category_id){
    y_secselector.append("<a href='#'>"+y_secCategoryArray[i].cateName+"</a>");
    break;
    }
  }
  //****** 세번째 셀렉트 박스 내용 만들기 ***********
  initialize('y');//기존 자료 자료들 지우기
//********************신경쓸 부분*************************

if(toggle){ //검색한 경우
       post('http://127.0.0.1:5000/yahoo_searched',para,$("#input").val(),y_genreId,3);
}
else { //검색 안한 경우
  item_ajax('http://127.0.0.1:5000/yahoo_selected_ranking',para,y_secCategoryArray[y_sselectValue-1].genreId,3);
}
}

function f_Click(){
  f_init();
  r_topselector.append("<a href='#'>"+r_mainCategoryArray[r_fselectValue-1].cateName+"</a>"+"<span> > </span>");   //main 세부항목 만들기
  r_subCategorySelectBox.append("<option value=''>전체</option>");//두 세번째 베이스값 만들기
  r_thirdCategorySelectBox.append("<option value=''>전체</option>");
  //****** 두번째 셀렉트 박스 내용 만들기 ***********
  cate_ajax();

  if(toggle){ //검색한 경우
     initialize('r');
    // a_ajax('http://127.0.0.1:5000/rakuten',para,$("#input").val());
  post('http://127.0.0.1:5000/rakuten_searched',para,$("#input").val(),genreId2,1);
  }
  else { //검색 안한 경우
    if(check == false){
    var div = document.createElement("DIV");
    div.setAttribute("style"," text-align:center; display:inline-block; border: 1px solid black; margin-top:3px");
    div.innerHTML="중카테고리를 선택하세요";
    document.getElementById("r_myList").prepend(div);
    check=true;
    }

  }
}
function y_f_Click(){
  y_topselector.children().remove();
  y_secselector.children().remove();
  y_subCategorySelectBox.children().remove(); //두번째 셀렉트 박스를 초기화 시킨다.
  y_topselector.append("<a href='#'>"+y_mainCategoryArray[y_fselectValue-1].cateName+"</a>"+"<span> > </span>");   //main 세부항목 만들기
  y_subCategorySelectBox.append("<option value=''>전체</option>");//두 세번째 베이스값 만들기
  //****** 두번째 셀렉트 박스 내용 만들기 ***********
  y_cate_ajax();
//  initialize();
  if(toggle){ //검색한 경우
     initialize('y');
    post('http://127.0.0.1:5000/yahoo_searched',para,$("#input").val(),y_genreId,3);
  }
  else { //검색 안한 경우
    item_ajax('http://127.0.0.1:5000/yahoo_selected_ranking',para,y_mainCategoryArray[y_fselectValue-1].genreId,3);
    console.log(y_mainCategoryArray[y_fselectValue-1].genreId);
  }
}

function scroll_Throw(){
  var scrolltop = $(window).scrollTop();
if(scrolltop == $(document).height() - $(window).height()){
  for(i=0;i<5;i++){
    if(r_count ==r_arrImageUrl.length) break;
     making_one_div();
     if(y_count !=y_arrImageUrl.length)
     y_making_one_div();
  }
 }
}

function y_scroll_Throw(){
  var scrolltop = $(window).scrollTop();
if(scrolltop == $(document).height() - $(window).height()){
  for(i=0;i<5;i++){
    if(y_count ==y_arrImageUrl.length) break;
     y_making_one_div();
  }
 }
}

function post(baseUrl,para,gId,genre,number){
  $.post(baseUrl+para+gId,
  {
    genreId:genre,
  },
  function(data){
    switch (number) {
      case 1:arrPush_print(data);
        break;
      case 3:y_arrPush_print(data);
        break;
    }
  });
}

// function y_post(baseUrl,para,gId,genre){
//   $.post(baseUrl+para+gId,
//   {
//     genreId:genre,
//   },
//   function(data){
//     y_arrPush_print(data);
//   });
// }

function start(){
  item_ajax('http://127.0.0.1:5000/rakuten_selected_ranking',para,0,1);
  item_ajax('http://127.0.0.1:5000/yahoo_selected_ranking',para,1,3);
  item_ajax("http://127.0.0.1:5000/yahoo_cate",'','',4);
  cat_init(); //대카테고리 정보 입력
  // $.ajax({
  //     async:false,
  //     type:"GET",
  //     dataType : 'JSON',
  //     url:"http://127.0.0.1:5000/yahoo_cate",
  //     success: function(result) {
  //         //첫번째 id의 children 값들 가져오기
  //         result.filter(function(element){
  //           if(element.depth==1){
  //             element.main_category_id = ++temp_count;
  //             y_mainCategoryArray.push(element);
  //             y_mainCategorySelectBox.append("<option value='"+temp_count+"'>"+element.cateName+"</option>");
  //           }
  //         });
  //       }
  //   });
}
});
