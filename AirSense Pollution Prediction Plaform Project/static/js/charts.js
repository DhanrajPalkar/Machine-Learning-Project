fetch("/graph-data")
.then(response => response.json())
.then(data => {

    //-----------------------------
    // AQI Trend (Line Chart)
    //-----------------------------

    new Chart(document.getElementById("aqiTrend"), {

        type: "line",

        data: {

            labels: Array.from({length: data.aqiTrend.length}, (_, i) => i + 1),

            datasets: [{

                label: "AQI",

                data: data.aqiTrend,

                borderColor: "#38bdf8",

                backgroundColor: "rgba(56,189,248,0.2)",

                fill: true,

                tension: 0.4

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    labels: {

                        color: "white"

                    }

                }

            },

            scales: {

                x: {

                    ticks: {

                        color: "white"

                    }

                },

                y: {

                    ticks: {

                        color: "white"

                    }

                }

            }

        }

    });


    //-----------------------------
    // Pollutant Levels
    //-----------------------------

    new Chart(document.getElementById("pollutionChart"), {

        type: "bar",

        data: {

            labels: data.pollutantLabels,

            datasets: [{

                label: "Average Value",

                data: data.pollutantValues,

                backgroundColor: [

                    "#3b82f6",

                    "#22c55e",

                    "#f59e0b",

                    "#ef4444",

                    "#8b5cf6",

                    "#06b6d4"

                ]

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    labels: {

                        color: "white"

                    }

                }

            },

            scales: {

                x: {

                    ticks: {

                        color: "white"

                    }

                },

                y: {

                    ticks: {

                        color: "white"

                    }

                }

            }

        }

    });


    //-----------------------------
    // AQI Category Pie Chart
    //-----------------------------

    new Chart(document.getElementById("pieChart"), {

        type: "pie",

        data: {

            labels: [

                "Good",

                "Moderate",

                "Unhealthy",

                "Very Unhealthy",

                "Hazardous"

            ],

            datasets: [{

                data: data.categoryValues,

                backgroundColor: [

                    "#22c55e",

                    "#facc15",

                    "#fb923c",

                    "#ef4444",

                    "#7e22ce"

                ]

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    labels: {

                        color: "white"

                    }

                }

            }

        }

    });


    //-----------------------------
    // Feature Importance
    //-----------------------------

    new Chart(document.getElementById("importanceChart"), {

        type: "bar",

        data: {

            labels: data.featureNames,

            datasets: [{

                label: "Importance",

                data: data.featureImportance,

                backgroundColor: "#38bdf8"

            }]

        },

        options: {

            indexAxis: "y",

            responsive: true,

            plugins: {

                legend: {

                    labels: {

                        color: "white"

                    }

                }

            },

            scales: {

                x: {

                    ticks: {

                        color: "white"

                    }

                },

                y: {

                    ticks: {

                        color: "white"

                    }

                }

            }

        }

    });

});

