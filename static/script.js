document.addEventListener('DOMContentLoaded', () => {
  const hamburgerMenu = document.getElementById('hamburger-menu');
  const dropdownNav = document.getElementById('dropdown-nav');

  hamburgerMenu.addEventListener('click', () => {
      dropdownNav.classList.toggle('show');
  });

  // Sliding header images
  let currentSlide = 0;
  const slides = document.querySelectorAll('.slide');

  function showSlide(index) {
      slides.forEach((slide, i) => {
          slide.style.opacity = i === index ? '1' : '0';
      });
  }

  function nextSlide() {
      currentSlide = (currentSlide + 1) % slides.length;
      showSlide(currentSlide);
  }

  setInterval(nextSlide, 4000);

  // Chart.js dynamic charts
  const pieChartCtx = document.getElementById('pieChart').getContext('2d');
  const lineChartCtx = document.getElementById('lineChart').getContext('2d');
  const barChartCtx = document.getElementById('barChart').getContext('2d');

  new Chart(pieChartCtx, {
      type: 'pie',
      data: {
          labels: ['Food', 'Medicine', 'Clothes'],
          datasets: [{
              data: [30, 50, 20], // Example data, should be dynamic
              backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe']
          }]
      },
      options: {
          responsive: true
      }
  });

  new Chart(lineChartCtx, {
      type: 'line',
      data: {
          labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
          datasets: [{
              label: 'Donations Over Time',
              data: [65, 59, 80, 81, 56, 55, 40], // Example data, should be dynamic
              borderColor: '#36a2eb',
              fill: false
          }]
      },
      options: {
          responsive: true
      }
  });

  new Chart(barChartCtx, {
      type: 'bar',
      data: {
          labels: ['Food', 'Medicine', 'Clothes'],
          datasets: [{
              label: 'Items Donated',
              data: [12, 19, 3], // Example data, should be dynamic
              backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe']
          }]
      },
      options: {
          responsive: true
      }
  });
});
let map;
let marker;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
      center: { lat: -34.397, lng: 150.644 },
      zoom: 8
  });

  map.addListener('click', (event) => {
      placeMarker(event.latLng);
  });
}

function placeMarker(location) {
  if (marker) {
      marker.setPosition(location);
  } else {
      marker = new google.maps.Marker({
          position: location,
          map: map
      });
  }
  document.getElementById('current-location').value = ${location.lat()},${location.lng()};
}
//CODE FOR DISASTER TIPS 
// scripts.js for displaying disaster tips and video
function showDisasterTips() {
  const disasterType = document.getElementById('disaster-type').value;
  const tipsContainer = document.getElementById('disaster-tips');
  const videoContainer = document.getElementById('disaster-video');

  const disasterTips = {
      earthquake: {
          tips: `
              <ul>
                  <li>Drop, cover, and hold on.</li>
                  <li>Stay indoors until the shaking stops.</li>
                  <li>Stay away from windows and doors.</li>
              </ul>
          `,
          video: 'https://youtu.be/N4j8OEY6Dtc?si=7k5odV1sZknCuePt'
      },
      flood: {
          tips: `
              <ul>
                  <li>Move to higher ground immediately.</li>
                  <li>Avoid walking or driving through flood waters.</li>
                  <li>Stay informed through local news updates.</li>
              </ul>
          `,
          video: 'https://www.youtube.com/embed/wIopfCvLBAA'
      },
      fire: {
          tips: `
              <ul>
                  <li>Stop, drop, and roll if your clothes catch fire.</li>
                  <li>Stay low to the ground to avoid smoke.</li>
                  <li>Exit the building immediately and call 911.</li>
              </ul>
          `,
          video: 'https://www.youtube.com/embed/RjQOHfA-eNE'
      },
      hurricane: {
          tips: `
              <ul>
                  <li>Secure your home and outdoor objects.</li>
                  <li>Evacuate if instructed by authorities.</li>
                  <li>Stay indoors and away from windows.</li>
              </ul>
          `,
          video: 'https://www.youtube.com/embed/N8yts1qCw4Y'
      }
  };

  if (disasterType && disasterTips[disasterType]) {
      tipsContainer.innerHTML = disasterTips[disasterType].tips;
      videoContainer.innerHTML = <iframe src="${disasterTips[disasterType].video}" frameborder="0" allowfullscreen></iframe>;
  } else {
      tipsContainer.innerHTML = '';
      videoContainer.innerHTML = '';
  }
}
//the new code for dragges menue
document.addEventListener("DOMContentLoaded", function() { 
const carousel = document.querySelector(".carousel"); 
const arrowBtns = document.querySelectorAll(".wrapper i"); 
const wrapper = document.querySelector(".wrapper"); 

const firstCard = carousel.querySelector(".card"); 
const firstCardWidth = firstCard.offsetWidth; 

let isDragging = false, 
  startX, 
  startScrollLeft, 
  timeoutId; 

const dragStart = (e) => { 
  isDragging = true; 
  carousel.classList.add("dragging"); 
  startX = e.pageX; 
  startScrollLeft = carousel.scrollLeft; 
}; 

const dragging = (e) => { 
  if (!isDragging) return; 

  // Calculate the new scroll position 
  const newScrollLeft = startScrollLeft - (e.pageX - startX); 

  // Check if the new scroll position exceeds 
  // the carousel boundaries 
  if (newScrollLeft <= 0 || newScrollLeft >= 
    carousel.scrollWidth - carousel.offsetWidth) { 
    
    // If so, prevent further dragging 
    isDragging = false; 
    return; 
  } 

  // Otherwise, update the scroll position of the carousel 
  carousel.scrollLeft = newScrollLeft; 
}; 

const dragStop = () => { 
  isDragging = false; 
  carousel.classList.remove("dragging"); 
}; 

const autoPlay = () => { 

  // Return if window is smaller than 800 
  if (window.innerWidth < 800) return; 
  
  // Calculate the total width of all cards 
  const totalCardWidth = carousel.scrollWidth; 
  
  // Calculate the maximum scroll position 
  const maxScrollLeft = totalCardWidth - carousel.offsetWidth; 
  
  // If the carousel is at the end, stop autoplay 
  if (carousel.scrollLeft >= maxScrollLeft) return; 
  
  // Autoplay the carousel after every 2500ms 
  timeoutId = setTimeout(() => 
    carousel.scrollLeft += firstCardWidth, 2500); 
}; 

carousel.addEventListener("mousedown", dragStart); 
carousel.addEventListener("mousemove", dragging); 
document.addEventListener("mouseup", dragStop); 
wrapper.addEventListener("mouseenter", () => 
  clearTimeout(timeoutId)); 
wrapper.addEventListener("mouseleave", autoPlay); 

// Add event listeners for the arrow buttons to 
// scroll the carousel left and right 
arrowBtns.forEach(btn => { 
  btn.addEventListener("click", () => { 
    carousel.scrollLeft += btn.id === "left" ? 
      -firstCardWidth : firstCardWidth; 
  }); 
}); 
});