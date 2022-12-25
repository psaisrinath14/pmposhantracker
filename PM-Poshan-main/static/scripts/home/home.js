// hard coded passwords for login page
// change it to preferred DB 

document.getElementById("loginbtn").onclick = function() {
    console.log(document.getElementById("dashselect").value)

    if(document.getElementById("dashselect").value == 0 && document.getElementById("email").value == "school@gmail.com" && document.getElementById("password").value == "pass"){
        window.location.href = "school_dash"
    }

    //student has admission number and dob as password for simplicity 
    else if(document.getElementById("dashselect").value == 2 && document.getElementById("email").value == "srinath" && document.getElementById("password").value == "14082003"){
        window.location.href = "student_dash"
    }

    else{
        alert("\nInvalid Login Details")
    }
}

document.getElementById("forgotpwdbtn").onclick = function() {
    alert("\nPlease contact officer@pmposhan.com \nfor account related queries!")
}