// Fonction permetant de mettre en place un sleep time
const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

// Capteurs
function gaz(){
  $.ajax({url: "/capteur/gaz", success: function(result){
    $("#gaz").html(result)
  }})
}

function tempAndHum(){
  $.ajax({url: "/capteur/tempAndHum", success: function(result){
    res = result.split(",")
    $("#temp").html(res[0])
    $("#hum").html(res[1])
  }})
}

function reload(){
  gaz()
  tempAndHum()
}

// Acquisition des différents capteurs automatiquement
reload()
intervalID = setInterval(reload, 5000)

// Commandes
