let currentTab = 0;
showTab(currentTab);

function showTab(n) {
   let x = document.getElementsByClassName("wizard-step");
    x[n].style.display = "block";
    if (n==0) {
        document.getElementById("prevBtn").style.display = "none";
    } else {
        document.getElementById("prevBtn").style.display = "inline";}
    if (n == (x.length - 1)){
        document.getElementById("nextBtn").innerHTML = "Generate & Save Quote";
        calculateSummary();
    } else {
        document.getElementById("nextBtn").innerHTML = "Next";
    }
    updateIndicators(n);
    
    }
function updateIndicators(n){
    for (let i = 1; i <= 4; i++) {
        let indicator = document.getElementById(`indicator-${i}`);
        if (i - 1 === n) {
            indicator.classList.add("text-cyan-400", "font-bold");
        } else {
            indicator.classList.remove("text-cyan-400", "font-bold");
        }
    }
}