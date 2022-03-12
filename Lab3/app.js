"use strict";

var myNodelist = document.getElementsByTagName("LI");
var i;
for (i = 0; i < myNodelist.length; i++) {
  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  myNodelist[i].appendChild(span);
}

// Click on a close button to hide the current list item
var close = document.getElementsByClassName("close");
var i;
for (i = 0; i < close.length; i++) {
  close[i].onclick = function() {
    var div = this.parentElement;
    div.remove();
  }
}

// Add a "checked" symbol when clicking on a list item
var list = document.querySelector('ul');
list.addEventListener('click', function(ev) {
  if (ev.target.tagName === 'LI') {
    ev.target.classList.toggle('checked');
  }
}, false);

// Create a new list item when clicking on the "Add" button
function newElement() {
  var li = document.createElement("li");
  var inputValue = document.getElementById("myInput").value;
  var t = document.createTextNode(inputValue);
  li.appendChild(t);
  if (inputValue === '') {
    alert("You must write something!");
  } else {
    document.getElementById("myUL").appendChild(li);
  }
  document.getElementById("myInput").value = "";

  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  li.appendChild(span);

  for (i = 0; i < close.length; i++) {
    close[i].onclick = function() {
      var div = this.parentElement;
      div.remove();
    }
  }
}

function filterItems() {
    var e = document.getElementById("filter");
    var ul = document.getElementById("myUL");
    var li = ul.getElementsByTagName('li')
    var lic = ul.getElementsByClassName("checked");
    var liun = ul.querySelectorAll("li:not(.checked)"); 

       switch(e.value){
            case "Non Checked" :  
                for (let i = 0; i < liun.length; i++) {
                    liun[i].style.display = "";
                }           
                for (let i = 0; i < lic.length; i++) {
                    lic[i].style.display = "none";
                }
                break;
            case "Checked" :
                for (let i = 0; i < lic.length; i++) {
                    lic[i].style.display = "";
                }             
                for (let i = 0; i < liun.length; i++) {
                    liun[i].style.display = "none";
                }
                break; 
            case "All" :             
                for (let i = 0; i < li.length; i++) {
                    li[i].style.display = "";
                }
                break;           
       }
}

