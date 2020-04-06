  function gogo(name) {
      d3.csv(name + ".csv", function (data) { initialize(data); });
      function initialize(data) {

        var myOptions = {
          center: new google.maps.LatLng(37.5647673, 126.7086641),
          zoom: 12.75,
          mapTypeId: google.maps.MapTypeId.ROADMAP

        };
        var map = new google.maps.Map(document.getElementById("default"),
          myOptions);

        setMarkers(map, data);

      }

      function setMarkers(map, locations) {

        var marker, i

        for (i = 0; i < locations.length; i++) {

          var titl = locations[i]['제목']
          var lat = locations[i]['lat']
          var long = locations[i]['lng']
          var inst = locations[i]['모집기관']
          var addr = locations[i]['formatted_address']
          var dates = locations[i]['봉사기간']

          latlngset = new google.maps.LatLng(lat, long);

          var marker = new google.maps.Marker({
            map: map, title: titl, position: latlngset, icon: {
              url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
            }
          });
          map.setCenter(marker.getPosition())


          var content = "<h2>제목: " + titl + '</h2><br>' + "모집기관: " + inst + "<br>봉사기간: " + dates

          var infowindow = new google.maps.InfoWindow()

          google.maps.event.addListener(marker, 'click', (function (marker, content, infowindow) {
            return function () {
              infowindow.setContent(content);
              infowindow.open(map, marker);
            };
          })(marker, content, infowindow));

        }
      }
    }