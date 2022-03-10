function getData() {
    //============================== RECOMMEND ===========================
    const recommend_data = {
        labels: recommend.items,
        datasets: [
        {
            label: "Recommend",
            data: recommend.count,
            backgroundColor: [
            "#0F52BA",
            "#4169E1",
            "#4682B4",
            "#87CEEB",
            "#B6D0E2",
        ],
        borderColor: [
            "#0F52BA",
            "#4169E1",
            "#4682B4",
            "#87CEEB",
            "#B6D0E2",
        ],
        borderWidth: 2,
        },
    ],
    };

    const recommend_config = {
        type: "pie",
        data: recommend_data,

        options: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {},
        },
    };

//============================== RATING ===========================

    const rating_data = {
        labels: rating.items,
        datasets: [
        {
            label: "Rating",
            data: rating.count,
            backgroundColor: [
                "#0F52BA",
                "#4169E1",
                "#4682B4",
                "#87CEEB",
                "#B6D0E2",
            ],
            borderColor: [
                "#0F52BA",
                "#4169E1",
                "#4682B4",
                "#87CEEB",
                "#B6D0E2",
            ],
        borderWidth: 2,
        },
    ],
    };

    const rating_config = {
        type: "line",
        data: rating_data,

        options: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {},
        },
    };

    //============================== CONFIRMED ===========================

    const confirmed_data = {
        labels: confirmed.items,
        datasets: [
        {
            label: "Confirmed",
            data: confirmed.count,
            backgroundColor: [
                "#0F52BA",
                "#4169E1",
                "#4682B4",
                "#87CEEB",
                "#B6D0E2",
            ],
            borderColor: [
                "#0F52BA",
                "#4169E1",
                "#4682B4",
                "#87CEEB",
                "#B6D0E2",
            ],
        borderWidth: 2,
        },
    ],
    };

    const confirmed_config = {
        type: "pie",
        data: confirmed_data,

        options: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {},
        },
    };


    //============================== UPSIDES ===========================

    const upsides_data = {
        labels: upsides.items,
        datasets: [
        {
            label: "Upsides",
            data: upsides.count,
            backgroundColor: [
                "#0F52BA",
                "#4169E1",
                "#4682B4",
                "#87CEEB",
                "#B6D0E2",
            ],
            borderColor: [
                "#0F52BA",
                "#4169E1",
                "#4682B4",
                "#87CEEB",
                "#B6D0E2",
            ],
        borderWidth: 2,
        },
    ],
    };
    
    const upsides_config = {
        type: "pie",
        data: upsides_data,

        options: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {},
        },
    };
    //============================== DOWNSIDES ===========================

    const downsides_data = {
        labels: downsides.items,
        datasets: [
        {
            label: "Downsides",
            data: downsides.count,
            backgroundColor: [
                "#0F52BA",
                "#4169E1",
                "#4682B4",
                "#87CEEB",
                "#B6D0E2",
            ],
            borderColor: [
                "#0F52BA",
                "#4169E1",
                "#4682B4",
                "#87CEEB",
                "#B6D0E2",
            ],
        borderWidth: 2,
        },
    ],
    };

    const downsides_config = {
        type: "pie",
        data: downsides_data,

        options: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {},
        },
    };
    

    return {
        recommend: recommend_config,
        rating: rating_config,
        confirmed : confirmed_config,
        upsides: upsides_config,
        downsides: downsides_config
    };
}



function loadData(data){
    recommend = data.recommend
    rating = data.rating
    confirmed = data.confirmed
    upsides = data.upsides
    downsides = data.downsides

    config = getData()

    const recommendChart = new Chart(document.getElementById("recommendChart").getContext("2d"),config.recommend);
    const ratingChart = new Chart(document.getElementById("ratingChart").getContext("2d"),config.rating);
    const confirmedChart = new Chart(document.getElementById("confirmedChart").getContext("2d"),config.confirmed);
    const upsidesChart = new Chart(document.getElementById("upsidesChart").getContext("2d"),config.upsides);
    const downsidesChart = new Chart(document.getElementById("downsidesChart").getContext("2d"),config.downsides);

}

console.log("Im Wornikg")


