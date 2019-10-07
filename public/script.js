getItems();
function getItems(){
  $.get("/items", function(data){
    if(!data){
      console.log("No data reveived");
    }
    console.log("Received data:");
    for(var i=0; i < data.length; i++){
      console.log(data[i].name);
    }
    showItems(data);
  });
}

function showItems(items){
  var itemsSection = document.getElementById("suggestions");
  for (var i in items){
    var section = document.createElement("section");
    // var heading = document.createElement("h3");
    // heading.innerHTML = items[i].name;
    var item = document.createElement("p");
    item.innerHTML = items[i].name + ": " + items[i].item;
    // section.appendChild(heading);
    section.appendChild(item);
    itemsSection.appendChild(section);
  }
}
