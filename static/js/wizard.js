let currentTab = 0;
showTab(currentTab);

function showTab(n) {
   let x = document.getElementsByClassName("wizard-step");
    x[n].style.display = "block";
    if (n==0) {
        document.getElementById("prevBtn").style.display = "none":
    } else {
        document.getElementById("prevBtn").style.display = "inline";
    }
}