document.getElementById("predictButton").addEventListener("click", function () {

    const data = {

        "PM2.5": document.getElementById("pm25").value,

        "PM10": document.getElementById("pm10").value,

        "NO": document.getElementById("no").value,

        "SO": document.getElementById("so").value,

        "CO": document.getElementById("co").value,

        "O": document.getElementById("o").value,

        "Temp_C": document.getElementById("temp").value,

        "Humidity_%": document.getElementById("humidity").value

    };

    // Check for empty inputs
    for (const key in data) {

        if (data[key] === "") {

            alert("Please fill all fields.");

            return;

        }

    }

    document.getElementById("loading").style.display = "block";

    fetch("/predict", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(data)

    })

    .then(response => response.json())

    .then(result => {

    document.getElementById("prediction").innerHTML =
        "Predicted AQI : " + result.prediction;

    document.getElementById("category").innerHTML =
        result.category;

    document.getElementById("advice").innerHTML =
        result.advice;

    document.getElementById("loading").style.display = "none";

    const category = document.getElementById("category");

    switch(result.category){

        case "Good":
            category.style.color="#22c55e";
            break;

        case "Moderate":
            category.style.color="#facc15";
            break;

        case "Unhealthy for Sensitive Groups":
            category.style.color="#fb923c";
            break;

        case "Unhealthy":
            category.style.color="#ef4444";
            break;

        case "Very Unhealthy":
            category.style.color="#8b5cf6";
            break;

        default:
            category.style.color="#dc2626";
    }
    })

    .catch(error => {

        console.log(error);

        document.getElementById("loading").style.display = "none";

        alert("Prediction Failed.");

    });

});