window.onload = function () {

    // Definitions
    var canvas = document.getElementById("light-canvas");
    var context = canvas.getContext("2d");
    var boundings = canvas.getBoundingClientRect();
  
    // Specifications
    var mouseX = 0;
    var mouseY = 0;
    context.fillStyle = '#cc0000'
    var isDrawing = false;
    var storedCoordinates = new Array(100);


    function paintBarNew(x_axis_value) {
      var x_axis = Math.round(x_axis_value) < 0 ? 0 : Math.round(x_axis_value);
      var percentAxis = Math.round((x_axis / canvas.width) * 100) / 100;

      var barWidth = 20;
      context.fillRect(x_axis - (barWidth/2), 0, barWidth, canvas.height);
      console.log(percentAxis);
      storedCoordinates[Math.round(percentAxis * 100)] = context.fillStyle;
    }

    function paintBar(x_axis_value) {
      var x_axis = Math.round(x_axis_value);
      var barWidth = 10;
      var halfbarWidth = Math.round(barWidth/2);
      let lower = x_axis - halfbarWidth < 0 ? 0 : x_axis - halfbarWidth;
      let upper = x_axis + halfbarWidth;
      var update_range = range(lower, upper);
      for (i = 0; i < update_range.length; i++) {
        storedCoordinates[update_range[i]] = context.fillStyle;
      }
      context.fillRect(x_axis - (barWidth/2), 0, barWidth, canvas.height);
    }

    // Handle Colors
    document.querySelectorAll('.colour-button').forEach(item => {
      item.addEventListener('click', function(event) {
        context.fillStyle = event.target.value || 'red';
      });
    });  
  
    // Mouse Down Event
    canvas.addEventListener('mousedown', function(event) {
      setMouseCoordinates(event);
      isDrawing = true;
  
      // Start Drawing
      context.beginPath();
      context.moveTo(mouseX, mouseY);

    });

  
    // Mouse Move Event
    canvas.addEventListener('mousemove', function(event) {
      setMouseCoordinates(event);
  
      if(isDrawing){
        // paintBar(mouseX);
        paintBarNew(mouseX);
      }
    });
  
    // Mouse Up Event
    canvas.addEventListener('mouseup', function(event) {
      setMouseCoordinates(event);
      isDrawing = false;
      sendToServer();
    });

    // Sends the stored drawing coordinates to the server
    function sendToServer() {
      console.log(JSON.stringify(storedCoordinates))
      $.post("/update/",
        {
          diff: JSON.stringify(storedCoordinates),
        },
        function(){
        });
        storedCoordinates = new Array(100);
    }
  
    // Handle Mouse Coordinates
    function setMouseCoordinates(event) {
      // mouseX = event.clientX - boundings.left;
      // mouseY = event.clientY - boundings.top;
      var rect = canvas.getBoundingClientRect();
      mouseX = (event.clientX - rect.left) / (rect.right - rect.left) * canvas.width;
      mouseY = (event.clientY - rect.top) / (rect.bottom - rect.top) * canvas.height;
    }
  
    // Handle Clear Button
    var clearButton = document.getElementById('clear');
  
    clearButton.addEventListener('click', function() {
      context.clearRect(0, 0, canvas.width, canvas.height);
      $.get("/clear/");
    });

  
    document.getElementById('btn-flash').addEventListener('click', function() {
      $.get("/feature/?feature=flash");
    });
    document.getElementById('btn-pinwheel').addEventListener('click', function() {
      $.get("/feature/?feature=pinwheel");
    });
    document.getElementById('btn-chase').addEventListener('click', function() {
      $.get("/feature/?feature=chase");
    });
    document.getElementById('btn-twinkle').addEventListener('click', function() {
      $.get("/feature/?feature=twinkle");
    });



    // Touch screens
    // Set up touch events for mobile, etc
    canvas.addEventListener("touchstart", function (e) {
      console.log('touch start')
      mousePos = getTouchPos(canvas, e);
    var touch = e.touches[0];
    var mouseEvent = new MouseEvent("mousedown", {
    clientX: touch.clientX,
    clientY: touch.clientY
    });
    canvas.dispatchEvent(mouseEvent);
    }, false);
    canvas.addEventListener("touchend", function (e) {
    var mouseEvent = new MouseEvent("mouseup", {});
    canvas.dispatchEvent(mouseEvent);
    }, false);
    canvas.addEventListener("touchmove", function (e) {
    var touch = e.touches[0];
    var mouseEvent = new MouseEvent("mousemove", {
    clientX: touch.clientX,
    clientY: touch.clientY
    });
    canvas.dispatchEvent(mouseEvent);
    }, false);

    // Get the position of a touch relative to the canvas
    function getTouchPos(canvasDom, touchEvent) {
    var rect = canvasDom.getBoundingClientRect();
    return {
    x: touchEvent.touches[0].clientX - rect.left,
    y: touchEvent.touches[0].clientY - rect.top
    };
    }

    document.body.addEventListener("touchstart", function (e) {
      if (e.target == canvas) {
        e.preventDefault();
      }
    }, { passive: false });
    document.body.addEventListener("touchend", function (e) {
      if (e.target == canvas) {
        e.preventDefault();
      }
    }, { passive: false });
    document.body.addEventListener("touchmove", function (e) {
      if (e.target == canvas) {
        e.preventDefault();
      }
    }, { passive: false });
    
  
  };
  

